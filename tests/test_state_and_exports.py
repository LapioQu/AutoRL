"""State model, export, and performance regression tests."""

from __future__ import annotations

import json
from pathlib import Path
import tracemalloc

from autorl.application import ExperimentOrchestrator, load_config, load_config_from_mapping
from autorl.domain import ConfigValidationError, ensure_experiment_status_transition


EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "configs" / "examples"


def _small_stationary_config(artifacts_root: Path) -> object:
    config = load_config(EXAMPLES_DIR / "stationary.yaml")
    payload = config.to_dict()
    payload["artifacts_root"] = str(artifacts_root)
    payload["scenario"]["episodes"] = 12
    payload["scenario"]["steps_per_episode"] = 8
    payload["meta_controller"]["window_size"] = 4
    payload["meta_controller"]["min_samples"] = 3
    return load_config_from_mapping(payload)


def test_state_model_rejects_invalid_transition() -> None:
    try:
        ensure_experiment_status_transition("created", "completed")
    except ConfigValidationError as exc:
        assert "invalid experiment status transition" in str(exc)
    else:
        raise AssertionError("expected ConfigValidationError")


def test_export_json_contains_lineage_and_generated_reports(tmp_path: Path) -> None:
    artifacts_root = tmp_path / "artifacts"
    orchestrator = ExperimentOrchestrator()
    config = _small_stationary_config(artifacts_root)

    first = orchestrator.run(config)
    rerun = orchestrator.rerun_experiment(first.experiment_id, artifacts_root=artifacts_root)
    export_path = Path(orchestrator.export_experiment(rerun.experiment_id, artifacts_root=artifacts_root, output_format="json"))

    assert export_path.exists()
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    assert payload["experiment"]["source_experiment_id"] == first.experiment_id
    assert payload["generated_report_paths"]["html"].endswith("report.html")
    assert payload["generated_report_paths"]["markdown"].endswith("report.md")


def test_small_run_peak_memory_stays_below_512mb(tmp_path: Path) -> None:
    artifacts_root = tmp_path / "artifacts"
    config = _small_stationary_config(artifacts_root)
    orchestrator = ExperimentOrchestrator()

    tracemalloc.start()
    try:
        orchestrator.run(config)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    assert peak < 512 * 1024 * 1024
