"""API-facing application services for phase 8."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import Event, Lock, Thread
from typing import Any

from autorl.application.configs import load_config_from_mapping
from autorl.application.experiments import CreatedExperiment, ExperimentOrchestrator, ExperimentRunResult
from autorl.domain.models import ScenarioName
from autorl.infrastructure import SQLiteRepository


@dataclass(slots=True)
class BackgroundRunState:
    """One in-memory background execution slot."""

    experiment_id: str
    artifacts_root: str
    stop_event: Event
    thread: Thread
    last_result: ExperimentRunResult | None = None
    error_message: str | None = None


class ExperimentApiService:
    """Thin application facade shared by FastAPI handlers."""

    def __init__(self, *, default_artifacts_root: str | Path = "artifacts") -> None:
        self._default_artifacts_root = Path(default_artifacts_root)
        self._orchestrator = ExperimentOrchestrator(default_artifacts_root=self._default_artifacts_root)
        self._runs: dict[str, BackgroundRunState] = {}
        self._lock = Lock()

    def health(self) -> dict[str, object]:
        return {"status": "ok", "service": "autorl-api"}

    def list_scenarios(self) -> list[dict[str, str]]:
        descriptions = {
            ScenarioName.STATIONARY: "Stable reward regime without drift.",
            ScenarioName.ABRUPT_DRIFT: "One abrupt regime change at a configured episode.",
            ScenarioName.GRADUAL_DRIFT: "Gradual change between configured drift bounds.",
            ScenarioName.NOISY_REWARD: "Stationary regime with higher reward noise.",
            ScenarioName.FALLBACK: "Scenario that can trigger fallback after failures.",
            ScenarioName.REPRODUCIBILITY: "Stable reproducibility control scenario.",
        }
        return [
            {"name": scenario.value, "description": descriptions[scenario]}
            for scenario in ScenarioName
        ]

    def list_strategies(self) -> list[dict[str, str]]:
        return [
            {"name": "fixed", "description": "Always select the configured fixed action."},
            {"name": "random", "description": "Uniform random comparator baseline."},
            {"name": "greedy_reward", "description": "Choose the action with the best observed mean reward."},
            {"name": "drift_aware", "description": "Bias toward actions that fit the detected regime."},
            {"name": "lcb_conservative", "description": "Select by lower confidence bound with conservative uncertainty handling."},
            {"name": "tempered_reward", "description": "Softmax over reward estimates with a temperature parameter."},
            {"name": "adaptive_meta", "description": "Weighted meta-policy over reward, success, fit, recency, and cost."},
            {"name": "negative_control", "description": "Intentional weak comparator used as a negative control."},
        ]

    def create_experiment(self, config_payload: dict[str, Any]) -> CreatedExperiment:
        config = load_config_from_mapping(config_payload)
        return self._orchestrator.create_experiment(config)

    def start_experiment(self, experiment_id: str, *, artifacts_root: str | Path | None = None) -> dict[str, Any]:
        root = str(Path(artifacts_root or self._default_artifacts_root))
        with self._lock:
            existing = self._runs.get(experiment_id)
            if existing is not None and existing.thread.is_alive():
                return {"experiment_id": experiment_id, "status": "running", "artifacts_root": root}

            stop_event = Event()
            thread = Thread(
                target=self._run_background,
                args=(experiment_id, root, stop_event),
                daemon=True,
                name=f"autorl-api-{experiment_id}",
            )
            state = BackgroundRunState(
                experiment_id=experiment_id,
                artifacts_root=root,
                stop_event=stop_event,
                thread=thread,
            )
            self._runs[experiment_id] = state
            thread.start()
        return {"experiment_id": experiment_id, "status": "running", "artifacts_root": root}

    def stop_experiment(self, experiment_id: str, *, artifacts_root: str | Path | None = None) -> dict[str, Any]:
        root = Path(artifacts_root or self._default_artifacts_root)
        with self._lock:
            state = self._runs.get(experiment_id)
            if state is not None:
                state.stop_event.set()
        repository = SQLiteRepository(root / "autorl.db")
        experiment_row = repository.get_experiment(experiment_id)
        if experiment_row is None:
            raise FileNotFoundError(f"experiment not found: {experiment_id}")
        if experiment_row["status"] == "running":
            repository.update_experiment_status(experiment_id, "stopping")
        return {
            "experiment_id": experiment_id,
            "status": repository.get_experiment(experiment_id)["status"],
        }

    def list_experiments(self, *, artifacts_root: str | Path | None = None) -> list[dict[str, Any]]:
        return self._orchestrator.list_experiments(artifacts_root=artifacts_root or self._default_artifacts_root)

    def get_experiment(self, experiment_id: str, *, artifacts_root: str | Path | None = None) -> dict[str, Any]:
        return self._orchestrator.get_experiment(experiment_id, artifacts_root=artifacts_root or self._default_artifacts_root)

    def get_status(self, experiment_id: str, *, artifacts_root: str | Path | None = None) -> dict[str, Any]:
        status = self._orchestrator.get_experiment_status(experiment_id, artifacts_root=artifacts_root or self._default_artifacts_root)
        with self._lock:
            state = self._runs.get(experiment_id)
            if state is not None:
                status["stop_requested"] = state.stop_event.is_set()
                status["background_running"] = state.thread.is_alive()
                status["error_message"] = state.error_message
            else:
                status["stop_requested"] = False
                status["background_running"] = False
                status["error_message"] = None
        return status

    def get_metrics(self, experiment_id: str, *, artifacts_root: str | Path | None = None) -> dict[str, list[dict[str, Any]]]:
        return self._orchestrator.get_metrics(experiment_id, artifacts_root=artifacts_root or self._default_artifacts_root)

    def get_decisions(self, experiment_id: str, *, artifacts_root: str | Path | None = None) -> list[dict[str, Any]]:
        return self._orchestrator.get_decisions(experiment_id, artifacts_root=artifacts_root or self._default_artifacts_root)

    def get_report(self, experiment_id: str, *, artifacts_root: str | Path | None = None) -> dict[str, str]:
        report = self._orchestrator.report_experiment(experiment_id, artifacts_root=artifacts_root or self._default_artifacts_root)
        return {"experiment_id": experiment_id, "report_markdown": report}

    def rerun_experiment(self, experiment_id: str, *, artifacts_root: str | Path | None = None) -> dict[str, Any]:
        source = self.get_experiment(experiment_id, artifacts_root=artifacts_root)
        config_payload = source["config"]
        if config_payload is None:
            raise FileNotFoundError(f"config payload not found for experiment: {experiment_id}")
        created = self.create_experiment(config_payload)
        return self.start_experiment(created.experiment_id, artifacts_root=artifacts_root)

    def compare_experiments(
        self,
        experiment_ids: list[str] | tuple[str, ...] | None = None,
        *,
        artifacts_root: str | Path | None = None,
    ) -> list[dict[str, Any]]:
        if experiment_ids:
            ids = list(experiment_ids)
        else:
            ids = [row["experiment_id"] for row in self.list_experiments(artifacts_root=artifacts_root)]
        return self._orchestrator.compare_experiments(ids, artifacts_root=artifacts_root or self._default_artifacts_root)

    def _run_background(self, experiment_id: str, artifacts_root: str, stop_event: Event) -> None:
        try:
            result = self._orchestrator.start_experiment(
                experiment_id,
                artifacts_root=artifacts_root,
                stop_requested=stop_event.is_set,
            )
            with self._lock:
                if experiment_id in self._runs:
                    self._runs[experiment_id].last_result = result
        except Exception as exc:
            with self._lock:
                if experiment_id in self._runs:
                    self._runs[experiment_id].error_message = str(exc)
