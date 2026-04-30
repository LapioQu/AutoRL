"""Experiment orchestration and CLI-facing application services for phase 6."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any, Callable
from uuid import uuid4
import zipfile
import yaml

from autorl.application.configs import load_config, load_config_from_mapping
from autorl.application.reporting import ExperimentReportBuilder
from autorl.domain import (
    AdaptiveLearningEnv,
    Config,
    Decision,
    Evaluator,
    EpisodeMetric,
    Experiment,
    ExperimentStatus,
    LearningStrategy,
    MetaController,
    MetricsCollector,
    RunMode,
    WindowMetric,
    build_runtime_strategy,
    ensure_experiment_status_transition,
)
from autorl.domain.errors import ConfigValidationError
from autorl.infrastructure import ExperimentArtifactStore, SQLiteRepository


class ExperimentStopRequested(RuntimeError):
    """Raised when an experiment receives a cooperative stop request."""


@dataclass(frozen=True, slots=True)
class StrategySimulation:
    """Precomputed per-strategy rollout used by the orchestrator."""

    strategy: LearningStrategy
    episode_metrics: tuple[EpisodeMetric, ...]
    window_metrics: tuple[WindowMetric, ...]


@dataclass(frozen=True, slots=True)
class ExperimentRunResult:
    """High-level result of one orchestrated experiment run."""

    experiment_id: str
    status: str
    artifacts_path: str
    metrics_path: str
    window_metrics_path: str
    decisions_path: str
    report_path: str
    html_report_path: str
    reward_curve_path: str
    strategy_timeline_path: str
    utility_lcb_path: str
    episode_count: int
    decision_count: int
    switch_count: int
    final_strategy: str
    config_hash: str


@dataclass(frozen=True, slots=True)
class CreatedExperiment:
    """Persisted experiment draft created before execution starts."""

    experiment_id: str
    status: str
    artifacts_path: str
    config_hash: str
    source_experiment_id: str | None = None


class ExperimentOrchestrator:
    """Run experiments end-to-end and expose CLI-friendly read operations."""

    def __init__(self, *, default_artifacts_root: str | Path = "artifacts") -> None:
        self._default_artifacts_root = Path(default_artifacts_root)
        self._evaluator = Evaluator()
        self._meta_controller = MetaController(self._evaluator)

    def run_from_config_path(self, config_path: str | Path) -> ExperimentRunResult:
        config = load_config(config_path)
        return self.run(config, source_config_path=config_path)

    def run(
        self,
        config: Config,
        *,
        source_config_path: str | Path | None = None,
        source_experiment_id: str | None = None,
    ) -> ExperimentRunResult:
        created = self.create_experiment(
            config,
            source_config_path=source_config_path,
            source_experiment_id=source_experiment_id,
        )
        return self.start_experiment(created.experiment_id, artifacts_root=config.artifacts_root)

    def create_experiment(
        self,
        config: Config,
        *,
        source_config_path: str | Path | None = None,
        experiment_id: str | None = None,
        source_experiment_id: str | None = None,
    ) -> CreatedExperiment:
        artifacts_root = Path(config.artifacts_root)
        repository = self._repository_for_root(artifacts_root)
        store = ExperimentArtifactStore(artifacts_root, repository)
        experiment = Experiment(
            experiment_id=experiment_id or self._new_experiment_id(config),
            config=config,
            seed=config.seed,
            config_hash=config.config_hash,
            status=ExperimentStatus.CREATED.value,
            source_experiment_id=source_experiment_id,
        )
        experiment_dir = store.create_experiment_bundle(experiment, source_config_path=source_config_path)
        return CreatedExperiment(
            experiment_id=experiment.experiment_id,
            status=ExperimentStatus.CREATED.value,
            artifacts_path=str(experiment_dir),
            config_hash=config.config_hash,
            source_experiment_id=source_experiment_id,
        )

    def start_experiment(
        self,
        experiment_id: str,
        *,
        artifacts_root: str | Path | None = None,
        stop_requested: Callable[[], bool] | None = None,
    ) -> ExperimentRunResult:
        repository = self._repository_for_root(artifacts_root or self._default_artifacts_root)
        experiment_row = repository.get_experiment(experiment_id)
        if experiment_row is None:
            raise FileNotFoundError(f"experiment not found: {experiment_id}")

        config_row = repository.get_config(experiment_row["config_hash"])
        if config_row is None:
            raise FileNotFoundError(f"config payload not found for experiment: {experiment_id}")

        config = load_config_from_mapping(json.loads(config_row["payload_json"]))
        root = Path(artifacts_root or config.artifacts_root)
        store = ExperimentArtifactStore(root, repository)
        report_builder = ExperimentReportBuilder(repository, store)
        experiment = Experiment(
            experiment_id=experiment_row["experiment_id"],
            config=config,
            seed=int(experiment_row["seed"]),
            config_hash=experiment_row["config_hash"],
            status=str(experiment_row["status"]),
            created_at=datetime.fromisoformat(str(experiment_row["created_at"])),
        )
        experiment_dir = Path(str(experiment_row["artifacts_path"]))
        repository.update_experiment_status(experiment.experiment_id, ExperimentStatus.RUNNING.value)
        store.append_event(
            experiment.experiment_id,
            level="INFO",
            message="Experiment run started.",
            details={
                "scenario": config.scenario.name.value,
                "episodes": config.scenario.episodes,
                "steps_per_episode": config.scenario.steps_per_episode,
                "mode": config.mode.value,
            },
        )

        try:
            simulations = self._simulate_strategies(config, stop_requested=stop_requested)
            managed_metrics, managed_decisions = self._compose_managed_run(config, simulations, stop_requested=stop_requested)
            managed_window_metrics = self._build_managed_windows(config, managed_metrics)

            metrics_path = store.write_episode_metrics(experiment.experiment_id, list(managed_metrics))
            window_metrics_path = store.write_window_metrics(experiment.experiment_id, managed_window_metrics)
            decisions_path = store.write_decisions(experiment.experiment_id, managed_decisions)
            generated_report = report_builder.generate_for_run(
                experiment=experiment,
                episode_metrics=managed_metrics,
                window_metrics=managed_window_metrics,
                decisions=managed_decisions,
            )

            repository.update_experiment_status(experiment.experiment_id, ExperimentStatus.COMPLETED.value)
            final_strategy = managed_metrics[-1].active_strategy if managed_metrics else ""
            switch_count = sum(1 for decision in managed_decisions if decision.switched)
            store.append_event(
                experiment.experiment_id,
                level="INFO",
                message="Experiment run completed.",
                details={
                    "episode_count": len(managed_metrics),
                    "window_count": len(managed_window_metrics),
                    "decision_count": len(managed_decisions),
                    "switch_count": switch_count,
                    "final_strategy": final_strategy,
                    "report_path": generated_report.report_path,
                    "html_report_path": generated_report.html_report_path,
                },
            )
        except ExperimentStopRequested as exc:
            running_status = repository.get_experiment(experiment.experiment_id)
            current_status = ExperimentStatus.RUNNING.value if running_status is None else str(running_status["status"])
            repository.update_experiment_status(
                experiment.experiment_id,
                ensure_experiment_status_transition(current_status, ExperimentStatus.STOPPING.value).value,
            )
            repository.update_experiment_status(experiment.experiment_id, ExperimentStatus.STOPPED.value)
            store.append_event(
                experiment.experiment_id,
                level="WARNING",
                message="Experiment run stopped by request.",
                details={"reason": str(exc)},
            )
            return ExperimentRunResult(
                experiment_id=experiment.experiment_id,
                status="stopped",
                artifacts_path=str(experiment_dir),
                metrics_path=str(Path(experiment_dir) / "metrics.csv"),
                window_metrics_path=str(Path(experiment_dir) / "window_metrics.csv"),
                decisions_path=str(Path(experiment_dir) / "decisions.csv"),
                report_path=str(Path(experiment_dir) / "report.md"),
                html_report_path=str(Path(experiment_dir) / "report.html"),
                reward_curve_path=str(Path(experiment_dir) / "reward_curve.png"),
                strategy_timeline_path=str(Path(experiment_dir) / "strategy_timeline.png"),
                utility_lcb_path=str(Path(experiment_dir) / "utility_lcb.png"),
                episode_count=0,
                decision_count=0,
                switch_count=0,
                final_strategy="",
                config_hash=config.config_hash,
            )
        except Exception as exc:
            repository.update_experiment_status(experiment.experiment_id, ExperimentStatus.FAILED.value)
            store.append_event(
                experiment.experiment_id,
                level="ERROR",
                message="Experiment run failed.",
                details={"error": str(exc)},
            )
            raise

        return ExperimentRunResult(
            experiment_id=experiment.experiment_id,
            status="completed",
            artifacts_path=str(experiment_dir),
            metrics_path=str(metrics_path),
            window_metrics_path=str(window_metrics_path),
            decisions_path=str(decisions_path),
            report_path=generated_report.report_path,
            html_report_path=generated_report.html_report_path,
            reward_curve_path=generated_report.reward_curve_path,
            strategy_timeline_path=generated_report.strategy_timeline_path,
            utility_lcb_path=generated_report.utility_lcb_path,
            episode_count=len(managed_metrics),
            decision_count=len(managed_decisions),
            switch_count=switch_count,
            final_strategy=final_strategy,
            config_hash=config.config_hash,
        )

    def list_experiments(self, *, artifacts_root: str | Path | None = None) -> list[dict[str, Any]]:
        repository = self._repository_for_root(artifacts_root or self._default_artifacts_root)
        return repository.list_experiments()

    def report_experiment(self, experiment_id: str, *, artifacts_root: str | Path | None = None) -> str:
        repository = self._repository_for_root(artifacts_root or self._default_artifacts_root)
        experiment = repository.get_experiment(experiment_id)
        if experiment is None:
            raise FileNotFoundError(f"experiment not found: {experiment_id}")
        report_path = Path(experiment["artifacts_path"]) / "report.md"
        if not report_path.exists():
            store = ExperimentArtifactStore(artifacts_root or self._default_artifacts_root, repository)
            ExperimentReportBuilder(repository, store).generate_for_experiment(experiment_id)
        return report_path.read_text(encoding="utf-8")

    def rerun_experiment(self, experiment_id: str, *, artifacts_root: str | Path | None = None) -> ExperimentRunResult:
        repository = self._repository_for_root(artifacts_root or self._default_artifacts_root)
        experiment_row = repository.get_experiment(experiment_id)
        if experiment_row is None:
            raise FileNotFoundError(f"experiment not found: {experiment_id}")

        config_row = repository.get_config(experiment_row["config_hash"])
        if config_row is None:
            raise FileNotFoundError(f"config payload not found for experiment: {experiment_id}")

        config_payload = json.loads(config_row["payload_json"])
        config = load_config_from_mapping(config_payload)
        source_config_path = Path(experiment_row["artifacts_path"]) / "config.yaml"
        return self.run(config, source_config_path=source_config_path, source_experiment_id=experiment_id)

    def run_suite_from_config_path(
        self,
        config_path: str | Path,
        *,
        seeds: list[int] | tuple[int, ...],
        artifacts_root: str | Path | None = None,
    ) -> dict[str, Any]:
        config_path = Path(config_path)
        suite_manifest = self._load_suite_manifest(config_path)
        if suite_manifest is None:
            config = load_config(config_path)
            root = Path(artifacts_root or config.artifacts_root)
            payload = self._run_single_suite_entry(
                config_path=config_path,
                root=root,
                entry_label=Path(config_path).stem,
                seeds=list(seeds),
            )
            payload["suite_name"] = Path(config_path).stem
        else:
            root = Path(artifacts_root or suite_manifest.get("artifacts_root") or (config_path.parent / "suite_artifacts"))
            root.mkdir(parents=True, exist_ok=True)
            entries_payload: list[dict[str, Any]] = []
            all_runs: list[dict[str, Any]] = []
            for entry in suite_manifest["runs"]:
                entry_config_path = (config_path.parent / str(entry["config"])).resolve() if not Path(str(entry["config"])).is_absolute() else Path(str(entry["config"])).resolve()
                entry_seeds = list(entry.get("seeds", seeds))
                entry_label = str(entry.get("label", entry_config_path.stem))
                entry_root = root / entry_label
                entry_payload = self._run_single_suite_entry(
                    config_path=entry_config_path,
                    root=entry_root,
                    entry_label=entry_label,
                    seeds=entry_seeds,
                )
                entries_payload.append(entry_payload)
                all_runs.extend(entry_payload["runs"])
            payload = {
                "suite_name": str(suite_manifest.get("suite_name", config_path.stem)),
                "config_path": str(config_path.resolve()),
                "n": len(all_runs),
                "seeds": sorted({row["seed"] for row in all_runs}),
                "entries": entries_payload,
                "runs": all_runs,
                "reward_mean": sum(row["reward_mean"] for row in all_runs) / max(1, len(all_runs)),
                "reward_std": self._sample_std([row["reward_mean"] for row in all_runs]),
                "reward_ci95": self._ci95([row["reward_mean"] for row in all_runs]),
            }
        summary_json_path = root / "suite_summary.json"
        summary_md_path = root / "suite_summary.md"
        summary_json_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        summary_md_path.write_text(self._build_suite_markdown(payload), encoding="utf-8")
        return {
            "suite_name": payload["suite_name"],
            "summary_json_path": str(summary_json_path),
            "summary_md_path": str(summary_md_path),
            "reward_mean": payload["reward_mean"],
            "reward_std": payload["reward_std"],
            "reward_ci95": payload["reward_ci95"],
            "run_count": len(payload["runs"]),
        }

    def get_experiment(self, experiment_id: str, *, artifacts_root: str | Path | None = None) -> dict[str, Any]:
        repository = self._repository_for_root(artifacts_root or self._default_artifacts_root)
        experiment_row = repository.get_experiment(experiment_id)
        if experiment_row is None:
            raise FileNotFoundError(f"experiment not found: {experiment_id}")
        config_row = repository.get_config(experiment_row["config_hash"])
        config_payload = None if config_row is None else json.loads(config_row["payload_json"])
        artifacts = repository.list_artifacts(experiment_id)
        events = repository.list_events(experiment_id)
        return {
            "experiment": experiment_row,
            "config": config_payload,
            "artifacts": artifacts,
            "events": events,
        }

    def get_experiment_status(self, experiment_id: str, *, artifacts_root: str | Path | None = None) -> dict[str, Any]:
        repository = self._repository_for_root(artifacts_root or self._default_artifacts_root)
        experiment_row = repository.get_experiment(experiment_id)
        if experiment_row is None:
            raise FileNotFoundError(f"experiment not found: {experiment_id}")
        episode_metrics = repository.list_episode_metrics(experiment_id)
        decisions = repository.list_decisions(experiment_id)
        active_strategy = episode_metrics[-1]["active_strategy"] if episode_metrics else None
        current_episode = episode_metrics[-1]["episode_index"] if episode_metrics else None
        return {
            "experiment_id": experiment_id,
            "status": experiment_row["status"],
            "source_experiment_id": experiment_row.get("source_experiment_id"),
            "active_strategy": active_strategy,
            "current_episode": current_episode,
            "episode_count": len(episode_metrics),
            "decision_count": len(decisions),
            "switch_count": sum(1 for decision in decisions if decision["switched"]),
        }

    def get_metrics(self, experiment_id: str, *, artifacts_root: str | Path | None = None) -> dict[str, list[dict[str, Any]]]:
        repository = self._repository_for_root(artifacts_root or self._default_artifacts_root)
        if repository.get_experiment(experiment_id) is None:
            raise FileNotFoundError(f"experiment not found: {experiment_id}")
        return {
            "episode_metrics": repository.list_episode_metrics(experiment_id),
            "window_metrics": repository.list_window_metrics(experiment_id),
        }

    def get_decisions(self, experiment_id: str, *, artifacts_root: str | Path | None = None) -> list[dict[str, Any]]:
        repository = self._repository_for_root(artifacts_root or self._default_artifacts_root)
        if repository.get_experiment(experiment_id) is None:
            raise FileNotFoundError(f"experiment not found: {experiment_id}")
        return repository.list_decisions(experiment_id)

    def compare_experiments(
        self,
        experiment_ids: list[str] | tuple[str, ...],
        *,
        artifacts_root: str | Path | None = None,
    ) -> list[dict[str, Any]]:
        repository = self._repository_for_root(artifacts_root or self._default_artifacts_root)
        comparison_rows: list[dict[str, Any]] = []
        for experiment_id in experiment_ids:
            experiment_row = repository.get_experiment(experiment_id)
            if experiment_row is None:
                continue
            metrics = repository.list_episode_metrics(experiment_id)
            decisions = repository.list_decisions(experiment_id)
            reward_mean = sum(metric["reward"] for metric in metrics) / len(metrics) if metrics else None
            comparison_rows.append(
                {
                    "experiment_id": experiment_id,
                    "experiment_name": experiment_row["experiment_name"],
                    "scenario_name": experiment_row["scenario_name"],
                    "status": experiment_row["status"],
                    "config_hash": experiment_row["config_hash"],
                    "source_experiment_id": experiment_row.get("source_experiment_id"),
                    "episode_count": len(metrics),
                    "decision_count": len(decisions),
                    "switch_count": sum(1 for decision in decisions if decision["switched"]),
                    "final_strategy": metrics[-1]["active_strategy"] if metrics else None,
                    "reward_mean": reward_mean,
                }
            )
        return comparison_rows

    def export_experiment(
        self,
        experiment_id: str,
        *,
        artifacts_root: str | Path | None = None,
        output_format: str = "zip",
    ) -> str:
        repository = self._repository_for_root(artifacts_root or self._default_artifacts_root)
        experiment = repository.get_experiment(experiment_id)
        if experiment is None:
            raise FileNotFoundError(f"experiment not found: {experiment_id}")
        experiment_root = Path(experiment["artifacts_path"])
        store = ExperimentArtifactStore(artifacts_root or self._default_artifacts_root, repository)
        generated = ExperimentReportBuilder(repository, store).generate_for_experiment(experiment_id)
        export_root = experiment_root / "exports"
        export_root.mkdir(parents=True, exist_ok=True)
        normalized = output_format.strip().lower()
        if normalized == "json":
            output_path = export_root / "experiment_export.json"
            payload = self.get_experiment(experiment_id, artifacts_root=artifacts_root)
            payload["metrics"] = self.get_metrics(experiment_id, artifacts_root=artifacts_root)
            payload["decisions"] = self.get_decisions(experiment_id, artifacts_root=artifacts_root)
            payload["generated_report_paths"] = {
                "markdown": generated.report_path,
                "html": generated.html_report_path,
            }
            output_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
            return str(output_path)
        if normalized == "html":
            return generated.html_report_path
        if normalized == "markdown":
            return generated.report_path
        if normalized == "zip":
            output_path = export_root / f"{experiment_id}.zip"
            with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for path in experiment_root.rglob("*"):
                    if path == output_path or not path.is_file():
                        continue
                    archive.write(path, path.relative_to(experiment_root))
            return str(output_path)
        raise ValueError(f"unsupported export format: {output_format!r}")

    def _compose_managed_run(
        self,
        config: Config,
        simulations: dict[str, StrategySimulation],
        *,
        stop_requested: Callable[[], bool] | None = None,
    ) -> tuple[tuple[EpisodeMetric, ...], list[Decision]]:
        strategy_order = [strategy.name for strategy in config.strategies if strategy.enabled]
        if not strategy_order:
            raise ConfigValidationError("run requires at least one enabled strategy")

        if any(len(simulation.episode_metrics) != config.scenario.episodes for simulation in simulations.values()):
            raise ConfigValidationError("strategy simulations must match configured episode count")

        current_strategy = strategy_order[0]
        collector = MetricsCollector()
        decisions: list[Decision] = []

        for episode_index in range(config.scenario.episodes):
            self._raise_if_stop_requested(stop_requested)
            if config.mode is RunMode.ADAPTIVE and len(strategy_order) > 1 and episode_index >= config.meta_controller.window_size - 1:
                current_windows = self._windows_until_episode(simulations[current_strategy].window_metrics, episode_index)
                candidate_strategy = self._select_candidate_strategy(
                    current_strategy=current_strategy,
                    strategy_order=strategy_order,
                    simulations=simulations,
                    episode_index=episode_index,
                    config=config,
                )
                candidate_windows = None
                if candidate_strategy is not None:
                    candidate_windows = self._windows_until_episode(simulations[candidate_strategy].window_metrics, episode_index)
                meta_decision = self._meta_controller.decide(
                    evaluation_index=len(decisions),
                    current_strategy=current_strategy,
                    candidate_strategy=candidate_strategy,
                    current_metrics=current_windows,
                    candidate_metrics=candidate_windows,
                    meta_config=config.meta_controller,
                )
                decisions.append(meta_decision.decision)
                if meta_decision.decision.switched and meta_decision.decision.candidate_strategy is not None:
                    current_strategy = meta_decision.decision.candidate_strategy

            episode_metric = simulations[current_strategy].episode_metrics[episode_index]
            collector.record_episode(
                episode_index=episode_metric.episode_index,
                reward=episode_metric.reward,
                success=episode_metric.success,
                active_strategy=current_strategy,
                steps=episode_metric.steps,
                compute_cost=episode_metric.compute_cost,
                learning_progress=episode_metric.learning_progress,
                fallback_triggered=episode_metric.fallback_triggered,
            )

        return collector.episodes, decisions

    def _simulate_strategies(
        self,
        config: Config,
        *,
        stop_requested: Callable[[], bool] | None = None,
    ) -> dict[str, StrategySimulation]:
        strategies = tuple(strategy for strategy in config.strategies if strategy.enabled)
        simulations: dict[str, StrategySimulation] = {}
        for index, strategy in enumerate(strategies):
            self._raise_if_stop_requested(stop_requested)
            env = AdaptiveLearningEnv(config)
            observation, _ = env.reset(seed=config.seed)
            runtime_strategy = build_runtime_strategy(
                strategy.name,
                strategies,
                seed=config.seed + index,
                parameters=strategy.parameters,
            )
            collector = MetricsCollector()
            terminated = False

            while not terminated:
                self._raise_if_stop_requested(stop_requested)
                current_episode = observation.episode_index
                reward_sum = 0.0
                success_count = 0
                learning_progress_sum = 0.0
                step_count = 0
                fallback_triggered = False

                while not terminated and observation.episode_index == current_episode:
                    self._raise_if_stop_requested(stop_requested)
                    step_observation = observation
                    strategy_decision = runtime_strategy.select_action(step_observation)
                    observation, reward, terminated, _, info = env.step(strategy_decision.action_index)
                    runtime_strategy.update(
                        step_observation,
                        action_index=strategy_decision.action_index,
                        reward=reward,
                        success=bool(info["success"]),
                        info=info,
                    )
                    reward_sum += float(reward)
                    success_count += int(bool(info["success"]))
                    learning_progress_sum += float(info["learning_progress"])
                    fallback_triggered = fallback_triggered or bool(info["fallback_triggered"])
                    step_count += 1

                collector.record_episode(
                    episode_index=current_episode,
                    reward=reward_sum / max(1, step_count),
                    success=(success_count / max(1, step_count)) >= 0.5,
                    active_strategy=strategy.name,
                    steps=step_count,
                    compute_cost=strategy.compute_cost,
                    learning_progress=learning_progress_sum / max(1, step_count),
                    fallback_triggered=fallback_triggered,
                )

            simulations[strategy.name] = StrategySimulation(
                strategy=strategy,
                episode_metrics=collector.episodes,
                window_metrics=tuple(
                    collector.window_metrics(
                        config.meta_controller.window_size,
                        switch_cost=config.meta_controller.switch_cost,
                        rolling=True,
                    )
                ),
            )
        return simulations

    def _build_managed_windows(self, config: Config, metrics: tuple[EpisodeMetric, ...]) -> list[WindowMetric]:
        collector = MetricsCollector()
        for episode_metric in metrics:
            collector.record_episode(
                episode_index=episode_metric.episode_index,
                reward=episode_metric.reward,
                success=episode_metric.success,
                active_strategy=episode_metric.active_strategy,
                steps=episode_metric.steps,
                compute_cost=episode_metric.compute_cost,
                learning_progress=episode_metric.learning_progress,
                fallback_triggered=episode_metric.fallback_triggered,
            )
        return collector.window_metrics(
            config.meta_controller.window_size,
            switch_cost=config.meta_controller.switch_cost,
            rolling=True,
        )

    def _select_candidate_strategy(
        self,
        *,
        current_strategy: str,
        strategy_order: list[str],
        simulations: dict[str, StrategySimulation],
        episode_index: int,
        config: Config,
    ) -> str | None:
        candidates = [strategy_name for strategy_name in strategy_order if strategy_name != current_strategy]
        if not candidates:
            return None

        best_strategy: str | None = None
        best_lcb: float | None = None
        fallback_strategy = candidates[0]
        for strategy_name in candidates:
            windows = self._windows_until_episode(simulations[strategy_name].window_metrics, episode_index)
            if len(windows) < config.meta_controller.min_samples:
                continue
            evaluation = self._evaluator.evaluate_strategy(
                strategy_name,
                windows[-config.meta_controller.min_samples :],
                meta_config=config.meta_controller,
                decision_switch_cost=config.meta_controller.switch_cost,
            )
            if best_lcb is None or evaluation.lcb > best_lcb:
                best_lcb = evaluation.lcb
                best_strategy = strategy_name
        return fallback_strategy if best_strategy is None else best_strategy

    def _windows_until_episode(self, windows: tuple[WindowMetric, ...], episode_index: int) -> list[WindowMetric]:
        return [window for window in windows if window.end_episode <= episode_index]

    def _new_experiment_id(self, config: Config) -> str:
        timestamp = datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S")
        slug = self._slugify(config.experiment_name)
        return f"{slug}-{timestamp}-{uuid4().hex[:8]}"

    def _repository_for_root(self, artifacts_root: str | Path) -> SQLiteRepository:
        root = Path(artifacts_root)
        return SQLiteRepository(root / "autorl.db")

    def _slugify(self, value: str) -> str:
        normalized = "".join(char.lower() if char.isalnum() else "-" for char in value.strip())
        compact = "-".join(part for part in normalized.split("-") if part)
        return compact or "experiment"

    def _raise_if_stop_requested(self, stop_requested: Callable[[], bool] | None) -> None:
        if stop_requested is not None and stop_requested():
            raise ExperimentStopRequested("cooperative stop requested")

    def _build_suite_markdown(self, payload: dict[str, Any]) -> str:
        lines = [
            "# Experiment Suite Summary",
            "",
            f"- suite_name: `{payload['suite_name']}`",
            f"- n: `{payload['n']}`",
            f"- seeds: `{', '.join(str(seed) for seed in payload['seeds'])}`",
            f"- reward_mean: `{payload['reward_mean']:.6f}`",
            f"- reward_std: `{payload['reward_std']:.6f}`",
            f"- reward_ci95: `{payload['reward_ci95']:.6f}`",
            "",
        ]
        if payload.get("entries"):
            lines.extend(
                [
                    "## Entries",
                    "",
                    "| Entry | n | Reward Mean | Reward Std | Reward CI95 |",
                    "| --- | ---: | ---: | ---: | ---: |",
                ]
            )
            for entry in payload["entries"]:
                lines.append(
                    f"| {entry['entry_label']} | {entry['n']} | {entry['reward_mean']:.6f} | {entry['reward_std']:.6f} | {entry['reward_ci95']:.6f} |"
                )
            lines.extend(["", "## Runs", ""])
        lines.extend([
            "| Seed | Experiment ID | Status | Reward Mean | Switches | Final Strategy |",
            "| ---: | --- | --- | ---: | ---: | --- |",
        ])
        for row in payload["runs"]:
            lines.append(
                f"| {row['seed']} | {row['experiment_id']} | {row['status']} | {row['reward_mean']:.6f} | {row['switch_count']} | {row['final_strategy']} |"
            )
        return "\n".join(lines) + "\n"

    def _run_single_suite_entry(
        self,
        *,
        config_path: Path,
        root: Path,
        entry_label: str,
        seeds: list[int],
    ) -> dict[str, Any]:
        config = load_config(config_path)
        root.mkdir(parents=True, exist_ok=True)
        rows: list[dict[str, Any]] = []
        reward_values: list[float] = []
        for seed in seeds:
            payload = config.to_dict()
            payload["seed"] = seed
            payload["experiment_name"] = f"{entry_label}-seed-{seed}"
            payload["artifacts_root"] = str(root / f"seed_{seed}")
            seeded_config = load_config_from_mapping(payload)
            result = self.run(seeded_config, source_config_path=config_path)
            metrics = self.get_metrics(result.experiment_id, artifacts_root=seeded_config.artifacts_root)["episode_metrics"]
            reward_mean = sum(row["reward"] for row in metrics) / max(1, len(metrics))
            reward_values.append(reward_mean)
            rows.append(
                {
                    "entry_label": entry_label,
                    "seed": seed,
                    "experiment_id": result.experiment_id,
                    "status": result.status,
                    "artifacts_path": result.artifacts_path,
                    "reward_mean": reward_mean,
                    "switch_count": result.switch_count,
                    "final_strategy": result.final_strategy,
                }
            )
        return {
            "entry_label": entry_label,
            "config_path": str(config_path.resolve()),
            "n": len(seeds),
            "seeds": list(seeds),
            "reward_mean": sum(reward_values) / max(1, len(reward_values)),
            "reward_std": self._sample_std(reward_values),
            "reward_ci95": self._ci95(reward_values),
            "runs": rows,
        }

    def _sample_std(self, values: list[float]) -> float:
        if len(values) <= 1:
            return 0.0
        mean = sum(values) / len(values)
        return (sum((value - mean) ** 2 for value in values) / (len(values) - 1)) ** 0.5

    def _ci95(self, values: list[float]) -> float:
        if len(values) <= 1:
            return 0.0
        return 1.96 * self._sample_std(values) / (len(values) ** 0.5)

    def _load_suite_manifest(self, config_path: Path) -> dict[str, Any] | None:
        text = config_path.read_text(encoding="utf-8")
        payload = json.loads(text) if config_path.suffix.lower() == ".json" else yaml.safe_load(text)
        if isinstance(payload, dict) and isinstance(payload.get("runs"), list):
            return payload
        return None
