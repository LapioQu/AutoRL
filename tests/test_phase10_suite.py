from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from autorl.application import Phase10ExperimentalSeriesRunner


def test_phase10_runner_generates_e1_to_e9_artifacts(tmp_path: Path) -> None:
    runner = Phase10ExperimentalSeriesRunner(root=tmp_path / "phase10")

    result = runner.run_phase10_suite(
        seeds=(41,),
        benchmark_datasets=("elec2",),
        benchmark_max_samples=128,
        reproducibility_repeats=3,
    )

    assert len(result.series) == 9
    assert Path(result.summary_json_path).exists()
    assert Path(result.report_md_path).exists()

    series_ids = {series.series_id for series in result.series}
    assert series_ids == {"E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9"}

    e7_series = next(series for series in result.series if series.series_id == "E7")
    e7_payload = json.loads(Path(e7_series.summary_json_path).read_text(encoding="utf-8"))
    assert e7_payload["reproducibility"]["all_reward_means_identical"] is True
    assert e7_payload["reproducibility"]["all_switch_counts_identical"] is True
    assert e7_payload["reproducibility"]["all_final_strategies_identical"] is True

    e9_series = next(series for series in result.series if series.series_id == "E9")
    e9_payload = json.loads(Path(e9_series.summary_json_path).read_text(encoding="utf-8"))
    assert any(row["policy_name"] == "hard_switch_lcb" for row in e9_payload["policy_aggregates"])


def test_cli_phase10_suite_smoke(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "autorl",
            "phase10-suite",
            "--artifacts-root",
            str(tmp_path / "cli_phase10"),
            "--seeds",
            "41",
            "--benchmark-datasets",
            "elec2",
            "--benchmark-max-samples",
            "128",
            "--series",
            "E1",
            "E7",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    assert "series_count: 2" in result.stdout
    assert "summary_json_path:" in result.stdout
    assert "report_md_path:" in result.stdout


def test_cli_phase10_suite_can_filter_profile_chunks(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "autorl",
            "phase10-suite",
            "--artifacts-root",
            str(tmp_path / "cli_phase10_profile_chunk"),
            "--series",
            "E9",
            "--benchmark-datasets",
            "elec2",
            "--benchmark-max-samples",
            "128",
            "--profile-names",
            "hard_switch_lcb",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    assert "series_count: 1" in result.stdout
    summary_path = None
    for line in result.stdout.splitlines():
        if line.startswith("summary_json_path: "):
            summary_path = Path(line.removeprefix("summary_json_path: ").strip())
            break
    assert summary_path is not None and summary_path.exists()
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    assert payload["series"][0]["series_id"] == "E9"


def test_phase10_profile_summary_accumulates_chunked_results(tmp_path: Path) -> None:
    runner = Phase10ExperimentalSeriesRunner(root=tmp_path / "phase10_chunked")

    runner.run_phase10_suite(
        series_ids=("E9",),
        benchmark_datasets=("elec2",),
        benchmark_max_samples=64,
        profile_names=("adaptive_meta_final",),
    )
    result = runner.run_phase10_suite(
        series_ids=("E9",),
        benchmark_datasets=("insects_recurring",),
        benchmark_max_samples=64,
        profile_names=("hard_switch_lcb",),
    )

    e9_series = next(series for series in result.series if series.series_id == "E9")
    payload = json.loads(Path(e9_series.summary_json_path).read_text(encoding="utf-8"))
    assert sorted(payload["dataset_names"]) == ["Elec2", "InsectsRecurring"]
    assert sorted(payload["profile_names"]) == ["adaptive_meta_final", "hard_switch_lcb"]
    assert payload["seed_protocol"] == "deterministic_temporal_replay_no_rng"
    assert "benchmark_protocol" in payload
    assert payload["benchmark_protocol"]["consistent_sample_count"] is True
    first_result = payload["results"][0]
    assert "artifact_root_path" in first_result
    assert "config_path" in first_result
    assert "metrics_path" in first_result
    assert "plots_path" in first_result
    assert "decision_csv_path" in first_result
    assert "report_md_path" in first_result
    assert Path(first_result["metrics_path"]).exists()
    assert Path(first_result["plots_path"]).exists()

    suite_payload = json.loads((Path(e9_series.root_path) / "suite_summary.json").read_text(encoding="utf-8"))
    assert suite_payload["dataset_count"] == 2
    assert suite_payload["profile_count"] == 2
    assert len(suite_payload["results"]) == 2
    assert "delta_ci95" in suite_payload
    assert "paired_sign_test_p_value" in suite_payload

    top_level_payload = json.loads(Path(result.summary_json_path).read_text(encoding="utf-8"))
    assert top_level_payload["requested_series_ids"] == top_level_payload["realized_series_ids"]
    assert top_level_payload["summary_scope"] == "accumulated_artifact_root"
