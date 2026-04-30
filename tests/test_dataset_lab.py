"""Dataset upload and forecasting tests."""

from __future__ import annotations

import json
from pathlib import Path

import time

from autorl.application import DatasetLabJobService, DatasetLabService
from autorl.application.dataset_lab import _resolve_replay_preset


def test_dataset_lab_service_runs_regression_replay(tmp_path: Path) -> None:
    service = DatasetLabService(default_artifacts_root=tmp_path / "artifacts")
    csv_text = "\n".join(
        [
            "timestamp,temperature,target",
            "1,10.0,100.0",
            "2,10.2,102.0",
            "3,10.5,104.0",
            "4,11.0,107.0",
            "5,11.8,111.0",
            "6,12.1,116.0",
            "7,12.7,122.0",
            "8,13.0,129.0",
            "9,13.4,137.0",
            "10,13.9,146.0",
        ]
    )

    result = service.analyze_csv(
        dataset_name="water-demand-like",
        csv_text=csv_text,
        target_column="target",
        task_type="regression",
        order_column="timestamp",
        lag_count=3,
        policy_name="recent_leader_meta",
        artifacts_root=tmp_path / "artifacts",
        max_rows=100,
    )

    assert result.task_type == "regression"
    assert result.source_row_count == 10
    assert result.source_rows_used == 10
    assert result.sample_count == 7
    assert result.feature_count >= 4
    assert result.next_prediction
    assert result.preview_rows
    assert result.oracle_score >= result.best_fixed_score
    assert 0.0 <= result.oracle_capture_ratio <= 1.0
    assert Path(result.input_manifest_path).exists()
    assert not Path(result.artifact_root, "input.csv").exists()
    assert Path(result.summary_json_path).exists()
    assert Path(result.report_md_path).exists()
    assert Path(result.decision_csv_path).exists()
    assert Path(result.score_plot_path).exists()
    assert Path(result.portfolio_plot_path).exists()
    assert Path(result.switch_plot_path).exists()
    report_text = Path(result.report_md_path).read_text(encoding="utf-8")
    assert "Dataset Lab Report" in report_text
    assert "oracle_capture_ratio" in report_text

    payload = json.loads(Path(result.summary_json_path).read_text(encoding="utf-8"))
    assert payload["dataset_name"] == "water-demand-like"
    assert payload["target_column"] == "target"
    assert payload["source_row_count"] == 10
    assert payload["source_rows_used"] == 10
    assert "next_prediction" in payload
    assert "oracle_score" in payload
    assert "oracle_capture_ratio" in payload
    assert "preview_rows" not in payload
    assert "forecast_row_preview" not in payload
    assert payload["raw_input_persisted"] is False
    history = service.list_dataset_lab_analyses(artifacts_root=tmp_path / "artifacts")
    assert history
    assert history[0]["dataset_name"] == "water-demand-like"


def test_dataset_lab_service_interprets_manual_rows_and_predicts_blank_target_row(tmp_path: Path) -> None:
    service = DatasetLabService(default_artifacts_root=tmp_path / "artifacts")
    base_csv = "\n".join(
        [
            "timestamp,signal,target",
            "1,0.1,10",
            "2,0.2,11",
            "3,0.4,13",
            "4,0.7,16",
            "5,1.0,20",
            "6,1.1,25",
            "7,1.4,31",
            "8,1.9,38",
            "9,2.1,46",
            "10,2.4,55",
        ]
    )

    interpreted = service.interpret_manual_rows(
        base_csv_text=base_csv,
        manual_text="timestamp=11, signal=2.8, target=",
        target_column="target",
    )
    combined_csv = service.append_manual_rows(base_csv_text=base_csv, normalized_rows_csv=interpreted.normalized_rows_csv)

    result = service.analyze_csv(
        dataset_name="manual-forecast-row",
        csv_text=combined_csv,
        target_column="target",
        task_type="regression",
        order_column="timestamp",
        lag_count=3,
        policy_name="recent_leader_meta",
        artifacts_root=tmp_path / "artifacts",
        max_rows=100,
    )

    assert interpreted.appended_row_count == 1
    assert interpreted.blank_target_row_count == 1
    assert result.prediction_mode == "manual_row"
    assert result.forecast_row_preview["timestamp"] == "11"
    assert result.forecast_row_preview["target"] == ""
    assert result.next_prediction


def test_dataset_lab_service_lists_builtin_datasets() -> None:
    service = DatasetLabService()
    dataset_ids = {item.dataset_id for item in service.available_builtin_datasets()}
    assert {"waterflow", "bikes", "elec2", "trump_approval"} <= dataset_ids


def test_dataset_lab_auto_meta_never_drops_below_best_fixed_on_builtin_dataset(tmp_path: Path) -> None:
    service = DatasetLabService(default_artifacts_root=tmp_path / "artifacts")

    result = service.analyze_builtin_dataset(
        dataset_id="waterflow",
        row_count=256,
        policy_name="auto_meta",
        artifacts_root=tmp_path / "artifacts",
    )

    assert result.policy_name in {"hard_switch_lcb", "recent_leader_meta", "hedge_portfolio", "fixed_share_portfolio", "best_fixed_guard"}
    assert result.delta_vs_best_fixed >= 0.0


def test_dataset_lab_auto_meta_never_drops_below_best_fixed_on_uploaded_classification_dataset(tmp_path: Path) -> None:
    service = DatasetLabService(default_artifacts_root=tmp_path / "artifacts")
    csv_text = "\n".join(
        [
            "moment,signal_a,signal_b,target",
            "1,0.10,1.0,low",
            "2,0.15,1.0,low",
            "3,0.20,1.1,low",
            "4,0.40,1.3,mid",
            "5,0.45,1.4,mid",
            "6,0.55,1.5,mid",
            "7,0.80,1.8,high",
            "8,0.85,1.9,high",
            "9,0.95,2.0,high",
            "10,0.30,1.2,low",
            "11,0.35,1.2,low",
            "12,0.60,1.6,mid",
        ]
    )

    result = service.analyze_csv(
        dataset_name="uploaded-classification",
        csv_text=csv_text,
        target_column="target",
        task_type="classification",
        order_column="moment",
        policy_name="auto_meta",
        artifacts_root=tmp_path / "artifacts",
        max_rows=100,
    )

    assert result.task_type == "classification"
    assert result.delta_vs_best_fixed >= 0.0
    assert result.policy_name in {"recent_leader_meta", "hard_switch_lcb", "hedge_portfolio", "fixed_share_portfolio", "best_fixed_guard"}


def test_dataset_profile_does_not_change_universal_preset() -> None:
    generic_preset = _resolve_replay_preset(dataset_profile=None, task_type="classification")
    profiled_preset = _resolve_replay_preset(dataset_profile="elec2", task_type="classification")

    assert generic_preset is not None
    assert profiled_preset is not None
    assert generic_preset == profiled_preset


def test_builtin_dataset_row_count_is_available() -> None:
    service = DatasetLabService()
    assert service.builtin_dataset_row_count("waterflow") >= 1000


def test_dataset_lab_job_service_persists_background_analysis(tmp_path: Path) -> None:
    service = DatasetLabJobService(default_artifacts_root=tmp_path / "artifacts")
    csv_text = "\n".join(
        [
            "timestamp,signal,target",
            "1,0.1,10",
            "2,0.2,11",
            "3,0.4,13",
            "4,0.7,16",
            "5,1.0,20",
            "6,1.1,25",
            "7,1.4,31",
            "8,1.9,38",
            "9,2.1,46",
            "10,2.4,55",
        ]
    )

    started = service.start_csv_job(
        dataset_name="job-run",
        csv_text=csv_text,
        target_column="target",
        task_type="regression",
        order_column="timestamp",
        artifacts_root=tmp_path / "artifacts",
    )

    deadline = time.time() + 10.0
    while time.time() < deadline:
        status = service.get_job_status(started.job_id, artifacts_root=tmp_path / "artifacts")
        if status.status in {"completed", "failed"}:
            break
        time.sleep(0.05)
    else:
        raise AssertionError("dataset lab background job did not complete in time")

    assert status.status == "completed"
    assert status.summary_json_path
    assert status.report_md_path
    result = service.load_completed_result(started.job_id, artifacts_root=tmp_path / "artifacts")
    assert result.dataset_name == "job-run"
    assert Path(result.report_md_path).exists()
    assert any(job.job_id == started.job_id for job in service.list_jobs(artifacts_root=tmp_path / "artifacts"))
