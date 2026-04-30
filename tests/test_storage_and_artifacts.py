"""Phase 5 integration tests for storage, logs, and artifacts."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from autorl.application import load_config
from autorl.domain import (
    ArtifactKind,
    ConfigValidationError,
    Decision,
    DecisionAction,
    DecisionReason,
    EpisodeMetric,
    Experiment,
    WindowMetric,
)
from autorl.infrastructure import ExperimentArtifactStore, PathGuard, SQLiteRepository


EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "configs" / "examples"


def _experiment() -> Experiment:
    config = load_config(EXAMPLES_DIR / "stationary.yaml")
    return Experiment(
        experiment_id="exp-phase5-001",
        config=config,
        seed=config.seed,
        config_hash=config.config_hash,
    )


def test_pathguard_blocks_paths_outside_root(tmp_path: Path) -> None:
    guard = PathGuard(tmp_path / "artifacts")

    with pytest.raises(ConfigValidationError, match="path escapes artifacts root"):
        guard.write_text("../escape.txt", "blocked")


def test_storage_creates_artifacts_and_sqlite_roundtrip(tmp_path: Path) -> None:
    repository = SQLiteRepository(tmp_path / "data" / "autorl.db")
    store = ExperimentArtifactStore(tmp_path / "artifacts", repository)
    experiment = _experiment()

    experiment_dir = store.create_experiment_bundle(
        experiment,
        source_config_path=EXAMPLES_DIR / "stationary.yaml",
    )
    metrics_path = store.write_episode_metrics(
        experiment.experiment_id,
        [
            EpisodeMetric(episode_index=0, reward=0.4, success=False, active_strategy="fixed", steps=10, compute_cost=0.1, learning_progress=0.02),
            EpisodeMetric(episode_index=1, reward=0.9, success=True, active_strategy="adaptive_meta", steps=10, compute_cost=0.2, learning_progress=0.06),
        ],
    )
    window_path = store.write_window_metrics(
        experiment.experiment_id,
        [
            WindowMetric(
                window_index=0,
                start_episode=0,
                end_episode=1,
                reward_mean=0.65,
                reward_variance=0.0625,
                success_rate=0.5,
                cumulative_reward=1.3,
                switches=1,
                compute_cost_mean=0.15,
                recovery_time=1.0,
                learning_progress_mean=0.04,
                utility_reward_mean=0.65,
                utility_reward_variance=0.0625,
                utility_compute_cost=0.15,
                utility_switch_cost=0.5,
            )
        ],
    )
    decisions_path = store.write_decisions(
        experiment.experiment_id,
        [
            Decision(
                evaluation_index=0,
                action=DecisionAction.STAY,
                current_strategy="fixed",
                candidate_strategy="adaptive_meta",
                reason="Stay because margin is insufficient.",
                utility_current=0.5,
                utility_candidate=0.55,
                lcb_current=0.45,
                lcb_candidate=0.50,
                switched=False,
                reason_code=DecisionReason.NO_CANDIDATE_IMPROVEMENT,
                decision_margin=0.05,
                decision_threshold=0.15,
            )
        ],
    )
    event_path = store.append_event(
        experiment.experiment_id,
        level="INFO",
        message="Metrics and decisions persisted.",
        details={"metrics_path": str(metrics_path)},
    )

    assert experiment_dir.exists()
    assert (experiment_dir / "config.yaml").exists()
    assert (experiment_dir / "config_hash.txt").read_text(encoding="utf-8").strip() == experiment.config_hash
    versions = json.loads((experiment_dir / "versions.json").read_text(encoding="utf-8"))
    assert "python" in versions
    assert metrics_path.exists()
    assert window_path.exists()
    assert decisions_path.exists()
    assert event_path.exists()

    db_experiment = repository.get_experiment(experiment.experiment_id)
    assert db_experiment is not None
    assert db_experiment["config_hash"] == experiment.config_hash
    db_config = repository.get_config(experiment.config_hash)
    assert db_config is not None
    episode_rows = repository.list_episode_metrics(experiment.experiment_id)
    window_rows = repository.list_window_metrics(experiment.experiment_id)
    decision_rows = repository.list_decisions(experiment.experiment_id)
    artifact_rows = repository.list_artifacts(experiment.experiment_id)
    event_rows = repository.list_events(experiment.experiment_id)

    assert len(episode_rows) == 2
    assert episode_rows[1]["active_strategy"] == "adaptive_meta"
    assert len(window_rows) == 1
    assert window_rows[0]["switches"] == 1
    assert len(decision_rows) == 1
    assert decision_rows[0]["reason_code"] == DecisionReason.NO_CANDIDATE_IMPROVEMENT.value
    assert any(row["kind"] == ArtifactKind.METRICS.value for row in artifact_rows)
    assert any(row["kind"] == ArtifactKind.DECISIONS.value for row in artifact_rows)
    assert len(event_rows) >= 2


def test_partial_logs_are_preserved_on_artifact_write_error(tmp_path: Path) -> None:
    repository = SQLiteRepository(tmp_path / "data" / "autorl.db")
    store = ExperimentArtifactStore(tmp_path / "artifacts", repository)
    experiment = _experiment()
    experiment_id = experiment.experiment_id

    experiment_dir = store.create_experiment_bundle(experiment)
    store.append_event(experiment_id, level="INFO", message="Start write sequence.")

    with pytest.raises(ConfigValidationError, match="path escapes artifacts root"):
        store.write_text_artifact(
            experiment_id,
            "../escape.txt",
            "should fail",
            kind=ArtifactKind.OTHER,
            description="forbidden write",
        )

    event_lines = (experiment_dir / "events.log").read_text(encoding="utf-8").strip().splitlines()
    assert len(event_lines) >= 3
    parsed = [json.loads(line) for line in event_lines]
    assert parsed[-1]["level"] == "ERROR"
    assert "Artifact write failed" in parsed[-1]["message"]
    db_events = repository.list_events(experiment_id)
    assert db_events[-1]["level"] == "ERROR"
