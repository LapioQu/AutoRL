"""Validation utilities for requirement audits and controlled comparison suites."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from math import comb, sqrt
from pathlib import Path
from statistics import fmean, stdev
from typing import Any, Iterable, Sequence

import yaml

from autorl.application.configs import load_config_from_mapping
from autorl.application.experiments import ExperimentOrchestrator
from autorl.domain import Config
from autorl.infrastructure import SQLiteRepository


@dataclass(frozen=True, slots=True)
class ValidationRun:
    """One executed run inside the validation suite."""

    scenario_name: str
    seed: int
    mode_label: str
    mean_reward: float
    experiment_id: str
    artifacts_path: str
    report_path: str


@dataclass(frozen=True, slots=True)
class ValidationSummary:
    """Aggregate comparison summary for one scenario."""

    scenario_name: str
    seeds: tuple[int, ...]
    adaptive_mean: float
    adaptive_std: float
    adaptive_ci95: float
    best_fixed_label: str
    best_fixed_mean: float
    best_fixed_std: float
    best_fixed_ci95: float
    delta_mean: float
    delta_std: float
    delta_ci95: float
    effect_size_d: float | None
    paired_sign_test_p_value: float | None


@dataclass(frozen=True, slots=True)
class ValidationSuiteResult:
    """Full validation suite output."""

    runs: tuple[ValidationRun, ...]
    summaries: tuple[ValidationSummary, ...]
    summary_json_path: str
    report_md_path: str


class PhaseValidationRunner:
    """Run controlled validation suites for phases 0-7."""

    def __init__(self, *, root: str | Path = "artifacts/validation_suite_0_7") -> None:
        self._root = Path(root)
        self._root.mkdir(parents=True, exist_ok=True)
        self._orchestrator = ExperimentOrchestrator()

    def run_nonstationary_suite(self, *, seeds: Sequence[int] = (41, 42, 43, 44, 45)) -> ValidationSuiteResult:
        runs: list[ValidationRun] = []
        summaries: list[ValidationSummary] = []
        scenarios = [
            self._build_abrupt_config,
            self._build_gradual_config,
        ]

        for builder in scenarios:
            scenario_runs = self._run_scenario_suite(builder=builder, seeds=seeds)
            runs.extend(scenario_runs)
            summaries.append(self._summarize_scenario(scenario_runs, seeds=seeds))

        summary_payload = {
            "suite": "phase_0_7_nonstationary_validation",
            "seeds": list(seeds),
            "runs": [asdict(run) for run in runs],
            "summaries": [
                {
                    "scenario_name": summary.scenario_name,
                    "seeds": list(summary.seeds),
                    "adaptive_mean": summary.adaptive_mean,
                    "adaptive_std": summary.adaptive_std,
                    "adaptive_ci95": summary.adaptive_ci95,
                    "best_fixed_label": summary.best_fixed_label,
                    "best_fixed_mean": summary.best_fixed_mean,
                    "best_fixed_std": summary.best_fixed_std,
                    "best_fixed_ci95": summary.best_fixed_ci95,
                    "delta_mean": summary.delta_mean,
                    "delta_std": summary.delta_std,
                    "delta_ci95": summary.delta_ci95,
                    "effect_size_d": summary.effect_size_d,
                    "paired_sign_test_p_value": summary.paired_sign_test_p_value,
                }
                for summary in summaries
            ],
        }
        summary_json_path = self._root / "summary.json"
        summary_json_path.write_text(json.dumps(summary_payload, ensure_ascii=True, indent=2, sort_keys=True), encoding="utf-8")

        report_md_path = self._root / "summary.md"
        report_md_path.write_text(self._build_markdown_report(summaries, runs, seeds=seeds), encoding="utf-8")
        return ValidationSuiteResult(
            runs=tuple(runs),
            summaries=tuple(summaries),
            summary_json_path=str(summary_json_path),
            report_md_path=str(report_md_path),
        )

    def _run_scenario_suite(
        self,
        *,
        builder: Any,
        seeds: Sequence[int],
    ) -> list[ValidationRun]:
        scenario_runs: list[ValidationRun] = []
        for seed in seeds:
            adaptive_config = builder(seed=seed, mode_label="adaptive")
            adaptive_result = self._orchestrator.run(adaptive_config)
            scenario_runs.append(self._run_record(adaptive_config, adaptive_result.experiment_id, adaptive_result.report_path, "adaptive"))

            for baseline_name in ("fixed_low", "fixed_mid", "fixed_high", "adaptive_meta_final"):
                baseline_config = builder(seed=seed, mode_label=baseline_name)
                baseline_result = self._orchestrator.run(baseline_config)
                scenario_runs.append(
                    self._run_record(
                        baseline_config,
                        baseline_result.experiment_id,
                        baseline_result.report_path,
                        baseline_name,
                    )
                )
        return scenario_runs

    def _run_record(self, config: Config, experiment_id: str, report_path: str, mode_label: str) -> ValidationRun:
        repository = SQLiteRepository(Path(config.artifacts_root) / "autorl.db")
        rows = repository.list_episode_metrics(experiment_id)
        mean_reward = fmean(row["reward"] for row in rows) if rows else 0.0
        experiment_row = repository.get_experiment(experiment_id)
        if experiment_row is None:
            raise FileNotFoundError(f"missing experiment row for validation run: {experiment_id}")
        return ValidationRun(
            scenario_name=config.scenario.name.value,
            seed=config.seed,
            mode_label=mode_label,
            mean_reward=mean_reward,
            experiment_id=experiment_id,
            artifacts_path=experiment_row["artifacts_path"],
            report_path=report_path,
        )

    def _summarize_scenario(self, runs: Iterable[ValidationRun], *, seeds: Sequence[int]) -> ValidationSummary:
        scenario_runs = list(runs)
        scenario_name = scenario_runs[0].scenario_name
        adaptive_runs = [run for run in scenario_runs if run.mode_label == "adaptive"]
        baseline_labels = sorted({run.mode_label for run in scenario_runs if run.mode_label != "adaptive"})
        best_fixed_label = max(
            baseline_labels,
            key=lambda label: fmean(run.mean_reward for run in scenario_runs if run.mode_label == label),
        )
        best_fixed_runs = [run for run in scenario_runs if run.mode_label == best_fixed_label]
        deltas = [adaptive.mean_reward - baseline.mean_reward for adaptive, baseline in zip(adaptive_runs, best_fixed_runs, strict=True)]
        delta_std = stdev(deltas) if len(deltas) > 1 else 0.0
        effect_size = None if delta_std == 0.0 else (fmean(deltas) / delta_std)
        sign_test_p_value = self._paired_sign_test_p_value(deltas)
        return ValidationSummary(
            scenario_name=scenario_name,
            seeds=tuple(seeds),
            adaptive_mean=fmean(run.mean_reward for run in adaptive_runs),
            adaptive_std=stdev(run.mean_reward for run in adaptive_runs) if len(adaptive_runs) > 1 else 0.0,
            adaptive_ci95=self._ci95(run.mean_reward for run in adaptive_runs),
            best_fixed_label=best_fixed_label,
            best_fixed_mean=fmean(run.mean_reward for run in best_fixed_runs),
            best_fixed_std=stdev(run.mean_reward for run in best_fixed_runs) if len(best_fixed_runs) > 1 else 0.0,
            best_fixed_ci95=self._ci95(run.mean_reward for run in best_fixed_runs),
            delta_mean=fmean(deltas),
            delta_std=delta_std,
            delta_ci95=self._ci95(deltas),
            effect_size_d=effect_size,
            paired_sign_test_p_value=sign_test_p_value,
        )

    def _build_abrupt_config(self, *, seed: int, mode_label: str) -> Config:
        payload = {
            "schema_version": "1.0",
            "experiment_name": f"phase0-7-abrupt-{mode_label}",
            "seed": seed,
            "mode": "adaptive" if mode_label == "adaptive" else "baseline",
            "scenario": {
                "name": "abrupt_drift",
                "episodes": 80,
                "steps_per_episode": 20,
                "drift_episode": 40,
                "description": "Phase 0-7 validation abrupt drift scenario.",
            },
            "strategies": self._portfolio_for_mode(mode_label),
            "meta_controller": {
                "window_size": 8,
                "min_samples": 5,
                "delta": 0.01,
                "lambda": 0.3,
                "switch_cost": 0.01,
                "utility_weights": {
                    "reward_mean": 1.0,
                    "reward_variance": 0.15,
                    "compute_cost": 0.08,
                    "switch_cost": 0.20,
                },
            },
            "artifacts_root": str(self._root / "abrupt_drift" / f"seed_{seed}" / mode_label),
            "tags": ["phase_validation", "abrupt_drift"],
        }
        return load_config_from_mapping(payload)

    def _build_gradual_config(self, *, seed: int, mode_label: str) -> Config:
        payload = {
            "schema_version": "1.0",
            "experiment_name": f"phase0-7-gradual-{mode_label}",
            "seed": seed,
            "mode": "adaptive" if mode_label == "adaptive" else "baseline",
            "scenario": {
                "name": "gradual_drift",
                "episodes": 90,
                "steps_per_episode": 20,
                "drift_start_episode": 25,
                "drift_end_episode": 65,
                "description": "Phase 0-7 validation gradual drift scenario.",
            },
            "strategies": self._portfolio_for_mode(mode_label),
            "meta_controller": {
                "window_size": 8,
                "min_samples": 5,
                "delta": 0.01,
                "lambda": 0.3,
                "switch_cost": 0.01,
                "utility_weights": {
                    "reward_mean": 1.0,
                    "reward_variance": 0.15,
                    "compute_cost": 0.08,
                    "switch_cost": 0.20,
                },
            },
            "artifacts_root": str(self._root / "gradual_drift" / f"seed_{seed}" / mode_label),
            "tags": ["phase_validation", "gradual_drift"],
        }
        return load_config_from_mapping(payload)

    def _portfolio_for_mode(self, mode_label: str) -> list[dict[str, Any]]:
        portfolio = [
            {"name": "fixed_low", "parameters": {"fixed_action_index": 0}, "compute_cost": 0.03},
            {"name": "fixed_mid", "parameters": {"fixed_action_index": 1}, "compute_cost": 0.05},
            {"name": "fixed_high", "parameters": {"fixed_action_index": 3}, "compute_cost": 0.07},
            {
                "name": "adaptive_meta_final",
                "parameters": {
                    "reward_weight": 0.20,
                    "success_weight": 0.20,
                    "fit_weight": 0.45,
                    "recency_weight": 0.20,
                    "cost_weight": 0.08,
                },
                "compute_cost": 0.12,
            },
        ]
        if mode_label == "adaptive":
            return portfolio
        return [entry for entry in portfolio if entry["name"] == mode_label] + [entry for entry in portfolio if entry["name"] != mode_label]

    def _ci95(self, values: Iterable[float]) -> float:
        values_list = list(values)
        if len(values_list) <= 1:
            return 0.0
        return 1.96 * stdev(values_list) / sqrt(len(values_list))

    def _paired_sign_test_p_value(self, deltas: Sequence[float]) -> float | None:
        non_zero = [delta for delta in deltas if abs(delta) > 1e-12]
        n = len(non_zero)
        if n == 0:
            return None
        positive = sum(1 for delta in non_zero if delta > 0.0)
        tail = min(positive, n - positive)
        probability = sum(comb(n, index) for index in range(tail + 1)) / (2**n)
        return min(1.0, 2.0 * probability)

    def _build_markdown_report(
        self,
        summaries: Sequence[ValidationSummary],
        runs: Sequence[ValidationRun],
        *,
        seeds: Sequence[int],
    ) -> str:
        lines = [
            "# Phase 0-7 Validation Suite",
            "",
            "Validation suite executed on the controlled non-stationary environment to check whether the adaptive system",
            "matches or exceeds the best fixed strategy under abrupt and gradual drift.",
            "",
            f"- n: {len(seeds)}",
            f"- seeds: {', '.join(str(seed) for seed in seeds)}",
            "- interpretation note: this is a controlled system-validation suite, not the final benchmark replay/H1/H2 study.",
            "",
            "## Scenario Summaries",
            "",
            "| Scenario | Adaptive Mean | Adaptive Std | Adaptive CI95 | Best Fixed | Best Fixed Mean | Best Fixed Std | Best Fixed CI95 | Delta Mean | Delta Std | Delta CI95 | Effect Size d | p-value |",
            "| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for summary in summaries:
            effect_size = "-" if summary.effect_size_d is None else f"{summary.effect_size_d:.6f}"
            p_value = "-" if summary.paired_sign_test_p_value is None else f"{summary.paired_sign_test_p_value:.6f}"
            lines.append(
                "| "
                + " | ".join(
                    [
                        summary.scenario_name,
                        f"{summary.adaptive_mean:.6f}",
                        f"{summary.adaptive_std:.6f}",
                        f"{summary.adaptive_ci95:.6f}",
                        summary.best_fixed_label,
                        f"{summary.best_fixed_mean:.6f}",
                        f"{summary.best_fixed_std:.6f}",
                        f"{summary.best_fixed_ci95:.6f}",
                        f"{summary.delta_mean:.6f}",
                        f"{summary.delta_std:.6f}",
                        f"{summary.delta_ci95:.6f}",
                        effect_size,
                        p_value,
                    ]
                )
                + " |"
            )

        lines.extend(
            [
                "",
                "## Run Artifacts",
                "",
                "| Scenario | Seed | Mode | Mean Reward | Experiment ID | Report Path |",
                "| --- | ---: | --- | ---: | --- | --- |",
            ]
        )
        for run in runs:
            lines.append(
                "| "
                + " | ".join(
                    [
                        run.scenario_name,
                        str(run.seed),
                        run.mode_label,
                        f"{run.mean_reward:.6f}",
                        run.experiment_id,
                        run.report_path,
                    ]
                )
                + " |"
            )
        return "\n".join(lines) + "\n"
