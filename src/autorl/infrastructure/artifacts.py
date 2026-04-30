"""Filesystem artifact storage and experiment bundle creation."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum
import csv
import json
from pathlib import Path
import platform
from importlib.metadata import distributions

import yaml

from autorl.domain.models import Artifact, ArtifactKind, Config, Decision, EpisodeMetric, Experiment, WindowMetric
from autorl.infrastructure.pathguard import PathGuard
from autorl.infrastructure.repository import SQLiteRepository


def _serialize_value(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    if is_dataclass(value):
        return {key: _serialize_value(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _serialize_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_serialize_value(item) for item in value]
    return value


class ExperimentArtifactStore:
    """Create experiment folders and persist artifact files under a guarded root."""

    def __init__(self, artifacts_root: str | Path, repository: SQLiteRepository) -> None:
        self._root_guard = PathGuard(artifacts_root)
        self._repository = repository

    def create_experiment_bundle(
        self,
        experiment: Experiment,
        *,
        source_config_path: str | Path | None = None,
    ) -> Path:
        experiment_relative_dir = self._experiment_relative_dir(experiment.experiment_id)
        experiment_dir = self._root_guard.ensure_directory(experiment_relative_dir)
        experiment_guard = PathGuard(experiment_dir)

        if source_config_path is None:
            config_path = experiment_guard.write_text(
                "config.yaml",
                yaml.safe_dump(experiment.config.to_dict(), sort_keys=False, allow_unicode=False),
            )
        else:
            config_path = experiment_guard.copy_file(source_config_path, "config.yaml")

        hash_path = experiment_guard.write_text("config_hash.txt", f"{experiment.config_hash}\n")
        versions_payload = self._collect_versions()
        versions_path = experiment_guard.write_text(
            "versions.json",
            json.dumps(versions_payload, ensure_ascii=True, indent=2, sort_keys=True),
        )
        events_path = experiment_guard.write_text("events.log", "")

        self._repository.save_config(experiment.config)
        self._repository.save_experiment(experiment, artifacts_path=str(experiment_dir))
        self._repository.save_artifacts(
            experiment.experiment_id,
            [
                Artifact(kind=ArtifactKind.CONFIG, path=str(config_path), description="Experiment config snapshot"),
                Artifact(kind=ArtifactKind.CONFIG, path=str(hash_path), description="Stable configuration hash"),
                Artifact(kind=ArtifactKind.OTHER, path=str(versions_path), description="Environment package versions"),
                Artifact(kind=ArtifactKind.LOG, path=str(events_path), description="Experiment event log"),
            ],
        )
        self.append_event(
            experiment.experiment_id,
            level="INFO",
            message="Experiment artifact bundle initialized.",
            details={"artifacts_path": str(experiment_dir)},
        )
        return experiment_dir

    def write_episode_metrics(self, experiment_id: str, metrics: list[EpisodeMetric] | tuple[EpisodeMetric, ...]) -> Path:
        rows = [
            {
                "episode_index": metric.episode_index,
                "reward": metric.reward,
                "success": metric.success,
                "active_strategy": metric.active_strategy,
                "steps": metric.steps,
                "compute_cost": metric.compute_cost,
                "learning_progress": metric.learning_progress,
                "fallback_triggered": metric.fallback_triggered,
            }
            for metric in metrics
        ]
        path = self._write_csv(experiment_id, "metrics.csv", rows)
        self._repository.save_episode_metrics(experiment_id, metrics)
        self._repository.save_artifacts(
            experiment_id,
            [Artifact(kind=ArtifactKind.METRICS, path=str(path), description="Episode metrics CSV")],
        )
        return path

    def write_window_metrics(self, experiment_id: str, metrics: list[WindowMetric] | tuple[WindowMetric, ...]) -> Path:
        rows = [
            {
                "window_index": metric.window_index,
                "start_episode": metric.start_episode,
                "end_episode": metric.end_episode,
                "reward_mean": metric.reward_mean,
                "reward_variance": metric.reward_variance,
                "success_rate": metric.success_rate,
                "cumulative_reward": metric.cumulative_reward,
                "switches": metric.switches,
                "compute_cost_mean": metric.compute_cost_mean,
                "recovery_time": metric.recovery_time,
                "learning_progress_mean": metric.learning_progress_mean,
                "utility_reward_mean": metric.utility_reward_mean,
                "utility_reward_variance": metric.utility_reward_variance,
                "utility_compute_cost": metric.utility_compute_cost,
                "utility_switch_cost": metric.utility_switch_cost,
            }
            for metric in metrics
        ]
        path = self._write_csv(experiment_id, "window_metrics.csv", rows)
        self._repository.save_window_metrics(experiment_id, metrics)
        self._repository.save_artifacts(
            experiment_id,
            [Artifact(kind=ArtifactKind.METRICS, path=str(path), description="Window metrics CSV")],
        )
        return path

    def write_decisions(self, experiment_id: str, decisions: list[Decision] | tuple[Decision, ...]) -> Path:
        rows = [
            {
                "evaluation_index": decision.evaluation_index,
                "action": decision.action.value,
                "current_strategy": decision.current_strategy,
                "candidate_strategy": decision.candidate_strategy,
                "reason": decision.reason,
                "utility_current": decision.utility_current,
                "utility_candidate": decision.utility_candidate,
                "lcb_current": decision.lcb_current,
                "lcb_candidate": decision.lcb_candidate,
                "switched": decision.switched,
                "reason_code": None if decision.reason_code is None else decision.reason_code.value,
                "decision_margin": decision.decision_margin,
                "decision_threshold": decision.decision_threshold,
                "is_fallback": decision.is_fallback,
            }
            for decision in decisions
        ]
        path = self._write_csv(experiment_id, "decisions.csv", rows)
        self._repository.save_decisions(experiment_id, decisions)
        self._repository.save_artifacts(
            experiment_id,
            [Artifact(kind=ArtifactKind.DECISIONS, path=str(path), description="Decision log CSV")],
        )
        return path

    def append_event(
        self,
        experiment_id: str,
        *,
        level: str,
        message: str,
        details: dict[str, object] | None = None,
    ) -> Path:
        event_row = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "level": level,
            "message": message,
            "details": None if details is None else _serialize_value(details),
        }
        experiment_guard = self._experiment_guard(experiment_id)
        path = experiment_guard.append_text("events.log", json.dumps(event_row, ensure_ascii=True, sort_keys=True) + "\n")
        self._repository.append_event(experiment_id, level=level, message=message, details=details)
        return path

    def write_text_artifact(
        self,
        experiment_id: str,
        relative_path: str | Path,
        content: str,
        *,
        kind: ArtifactKind = ArtifactKind.OTHER,
        description: str | None = None,
    ) -> Path:
        experiment_guard = self._experiment_guard(experiment_id)
        try:
            path = experiment_guard.write_text(relative_path, content)
        except Exception as exc:
            self.append_event(
                experiment_id,
                level="ERROR",
                message="Artifact write failed.",
                details={"relative_path": str(relative_path), "error": str(exc)},
            )
            raise
        self._repository.save_artifacts(
            experiment_id,
            [Artifact(kind=kind, path=str(path), description=description)],
        )
        return path

    def write_bytes_artifact(
        self,
        experiment_id: str,
        relative_path: str | Path,
        content: bytes,
        *,
        kind: ArtifactKind = ArtifactKind.OTHER,
        description: str | None = None,
    ) -> Path:
        experiment_guard = self._experiment_guard(experiment_id)
        try:
            path = experiment_guard.write_bytes(relative_path, content)
        except Exception as exc:
            self.append_event(
                experiment_id,
                level="ERROR",
                message="Artifact write failed.",
                details={"relative_path": str(relative_path), "error": str(exc)},
            )
            raise
        self._repository.save_artifacts(
            experiment_id,
            [Artifact(kind=kind, path=str(path), description=description)],
        )
        return path

    def _write_csv(self, experiment_id: str, file_name: str, rows: list[dict[str, object]]) -> Path:
        experiment_guard = self._experiment_guard(experiment_id)
        if not rows:
            return experiment_guard.write_text(file_name, "")

        path = experiment_guard.resolve_relative(file_name)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            for row in rows:
                writer.writerow({key: _serialize_value(value) for key, value in row.items()})
        return path

    def _experiment_relative_dir(self, experiment_id: str) -> Path:
        return Path("experiments") / experiment_id

    def _experiment_guard(self, experiment_id: str) -> PathGuard:
        experiment_dir = self._root_guard.ensure_directory(self._experiment_relative_dir(experiment_id))
        return PathGuard(experiment_dir)

    def _collect_versions(self) -> dict[str, object]:
        packages = {
            dist.metadata.get("Name", dist.metadata.get("Summary", "unknown")): dist.version
            for dist in distributions()
            if dist.metadata.get("Name")
        }
        return {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "packages": dict(sorted(packages.items())),
        }
