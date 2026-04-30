"""Phase 6-7 end-to-end, reporting, and CLI smoke tests."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from autorl.application import ExperimentOrchestrator, load_config, load_config_from_mapping
from autorl.domain import ArtifactKind
from autorl.infrastructure import SQLiteRepository


EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "configs" / "examples"


def _small_config(example_name: str, artifacts_root: Path) -> object:
    config = load_config(EXAMPLES_DIR / example_name)
    payload = config.to_dict()
    payload["artifacts_root"] = str(artifacts_root)
    payload["scenario"]["episodes"] = 18
    payload["scenario"]["steps_per_episode"] = 10
    payload["meta_controller"]["window_size"] = 4
    payload["meta_controller"]["min_samples"] = 3
    payload["meta_controller"]["delta"] = 0.02
    payload["meta_controller"]["switch_cost"] = 0.02
    payload["meta_controller"]["lambda"] = 0.6
    return load_config_from_mapping(payload)


def _abrupt_switch_config(artifacts_root: Path) -> object:
    config = load_config(EXAMPLES_DIR / "abrupt_drift.yaml")
    payload = config.to_dict()
    payload["artifacts_root"] = str(artifacts_root)
    payload["scenario"]["episodes"] = 22
    payload["scenario"]["steps_per_episode"] = 10
    payload["scenario"]["drift_episode"] = 11
    payload["meta_controller"]["window_size"] = 4
    payload["meta_controller"]["min_samples"] = 3
    payload["meta_controller"]["delta"] = 0.01
    payload["meta_controller"]["switch_cost"] = 0.01
    payload["meta_controller"]["lambda"] = 0.3
    return load_config_from_mapping(payload)


def _normalize_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ignored = {"id", "experiment_id"}
    return [{key: value for key, value in row.items() if key not in ignored} for row in rows]


def test_orchestrator_runs_stationary_end_to_end(tmp_path: Path) -> None:
    artifacts_root = tmp_path / "artifacts"
    config = _small_config("stationary.yaml", artifacts_root)
    orchestrator = ExperimentOrchestrator()

    result = orchestrator.run(config)

    assert result.status == "completed"
    assert result.episode_count == config.scenario.episodes
    assert Path(result.artifacts_path).exists()
    assert Path(result.metrics_path).exists()
    assert Path(result.window_metrics_path).exists()
    assert Path(result.decisions_path).exists()
    assert Path(result.report_path).exists()
    assert Path(result.html_report_path).exists()
    assert Path(result.reward_curve_path).exists()
    assert Path(result.strategy_timeline_path).exists()
    assert Path(result.utility_lcb_path).exists()
    repository = SQLiteRepository(artifacts_root / "autorl.db")
    experiment = repository.get_experiment(result.experiment_id)
    assert experiment is not None
    assert experiment["status"] == "completed"
    assert len(repository.list_episode_metrics(result.experiment_id)) == config.scenario.episodes
    assert len(repository.list_window_metrics(result.experiment_id)) == config.scenario.episodes - config.meta_controller.window_size + 1
    assert len(repository.list_decisions(result.experiment_id)) > 0
    artifacts = repository.list_artifacts(result.experiment_id)
    assert any(row["kind"] == ArtifactKind.REPORT.value for row in artifacts)
    assert sum(1 for row in artifacts if row["kind"] == ArtifactKind.PLOT.value) >= 3
    assert any(str(row["path"]).endswith("report.html") for row in artifacts)
    report = orchestrator.report_experiment(result.experiment_id, artifacts_root=artifacts_root)
    assert "AutoRL Experiment Report" in report
    assert "## Config Snapshot" in report
    assert "## Stay/Switch Summary" in report
    assert str(config.seed) in report
    assert config.config_hash in report
    assert "Average Reward" in report
    assert Path(result.reward_curve_path).read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert Path(result.strategy_timeline_path).read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert Path(result.utility_lcb_path).read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert "<!doctype html>" in Path(result.html_report_path).read_text(encoding="utf-8").lower()


def test_orchestrator_switches_under_abrupt_drift(tmp_path: Path) -> None:
    artifacts_root = tmp_path / "artifacts"
    config = _abrupt_switch_config(artifacts_root)
    orchestrator = ExperimentOrchestrator()

    result = orchestrator.run(config)

    decisions = SQLiteRepository(artifacts_root / "autorl.db").list_decisions(result.experiment_id)
    assert result.status == "completed"
    assert decisions
    assert any(row["switched"] == 1 for row in decisions)


def test_reproducibility_same_seed_same_metrics_and_decisions(tmp_path: Path) -> None:
    artifacts_root = tmp_path / "artifacts"
    config = _small_config("reproducibility.json", artifacts_root)
    orchestrator = ExperimentOrchestrator()

    first = orchestrator.run(config)
    second = orchestrator.run(config)
    repository = SQLiteRepository(artifacts_root / "autorl.db")

    first_metrics = _normalize_rows(repository.list_episode_metrics(first.experiment_id))
    second_metrics = _normalize_rows(repository.list_episode_metrics(second.experiment_id))
    first_decisions = _normalize_rows(repository.list_decisions(first.experiment_id))
    second_decisions = _normalize_rows(repository.list_decisions(second.experiment_id))

    assert first_metrics == second_metrics
    assert first_decisions == second_decisions


def test_cli_run_list_report_and_rerun(tmp_path: Path) -> None:
    artifacts_root = tmp_path / "artifacts"
    config = _small_config("stationary.yaml", artifacts_root)
    config_path = tmp_path / "cli-stationary.json"
    config_path.write_text(json.dumps(config.to_dict(), ensure_ascii=True, indent=2), encoding="utf-8")

    run_completed = subprocess.run(
        [sys.executable, "-m", "autorl", "run", "--config", str(config_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert run_completed.returncode == 0, run_completed.stderr
    assert "experiment_id:" in run_completed.stdout
    experiment_id = next(
        line.split(":", maxsplit=1)[1].strip()
        for line in run_completed.stdout.splitlines()
        if line.startswith("experiment_id:")
    )

    list_completed = subprocess.run(
        [sys.executable, "-m", "autorl", "list", "--artifacts-root", str(artifacts_root)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert list_completed.returncode == 0, list_completed.stderr
    assert experiment_id in list_completed.stdout

    report_completed = subprocess.run(
        [sys.executable, "-m", "autorl", "report", "--experiment-id", experiment_id, "--artifacts-root", str(artifacts_root)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert report_completed.returncode == 0, report_completed.stderr
    assert "AutoRL Experiment Report" in report_completed.stdout
    assert "## Stay/Switch Summary" in report_completed.stdout

    rerun_completed = subprocess.run(
        [sys.executable, "-m", "autorl", "rerun", "--experiment-id", experiment_id, "--artifacts-root", str(artifacts_root)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert rerun_completed.returncode == 0, rerun_completed.stderr
    assert "source_experiment_id:" in rerun_completed.stdout
    rerun_experiment_id = next(
        line.split(":", maxsplit=1)[1].strip()
        for line in rerun_completed.stdout.splitlines()
        if line.startswith("experiment_id:")
    )

    status_completed = subprocess.run(
        [sys.executable, "-m", "autorl", "status", "--experiment-id", rerun_experiment_id, "--artifacts-root", str(artifacts_root)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert status_completed.returncode == 0, status_completed.stderr
    assert "source_experiment_id:" in status_completed.stdout
    assert experiment_id in status_completed.stdout

    export_html_completed = subprocess.run(
        [sys.executable, "-m", "autorl", "export", "--experiment-id", experiment_id, "--artifacts-root", str(artifacts_root), "--format", "html"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert export_html_completed.returncode == 0, export_html_completed.stderr
    assert "export_path:" in export_html_completed.stdout

    export_zip_completed = subprocess.run(
        [sys.executable, "-m", "autorl", "export", "--experiment-id", experiment_id, "--artifacts-root", str(artifacts_root), "--format", "zip"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert export_zip_completed.returncode == 0, export_zip_completed.stderr
    export_zip_path = next(
        line.split(":", maxsplit=1)[1].strip()
        for line in export_zip_completed.stdout.splitlines()
        if line.startswith("export_path:")
    )
    assert Path(export_zip_path).exists()


def test_cli_validate_config_and_validate_suite(tmp_path: Path) -> None:
    artifacts_root = tmp_path / "validation-suite"
    config = _small_config("stationary.yaml", tmp_path / "stationary-artifacts")
    config_path = tmp_path / "validate-config.json"
    config_path.write_text(json.dumps(config.to_dict(), ensure_ascii=True, indent=2), encoding="utf-8")

    validate_config_completed = subprocess.run(
        [sys.executable, "-m", "autorl", "validate-config", "--config", str(config_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert validate_config_completed.returncode == 0, validate_config_completed.stderr
    assert "config_hash:" in validate_config_completed.stdout

    validate_suite_completed = subprocess.run(
        [sys.executable, "-m", "autorl", "validate-suite", "--artifacts-root", str(artifacts_root), "--seeds", "41", "42"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert validate_suite_completed.returncode == 0, validate_suite_completed.stderr
    assert "summary_json_path:" in validate_suite_completed.stdout

    run_suite_completed = subprocess.run(
        [sys.executable, "-m", "autorl", "run-suite", "--config", str(config_path), "--artifacts-root", str(tmp_path / "suite"), "--seeds", "41", "42"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert run_suite_completed.returncode == 0, run_suite_completed.stderr
    assert "summary_json_path:" in run_suite_completed.stdout

    suite_manifest_path = tmp_path / "suite_manifest.yaml"
    suite_manifest_path.write_text(
        "\n".join(
            [
                "suite_name: cli-suite",
                f"artifacts_root: {str(tmp_path / 'suite_manifest_artifacts')}",
                "runs:",
                f"  - label: stationary_small",
                f"    config: {config_path.name}",
                "    seeds: [41, 42]",
            ]
        ),
        encoding="utf-8",
    )
    manifest_completed = subprocess.run(
        [sys.executable, "-m", "autorl", "run-suite", "--config", str(suite_manifest_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert manifest_completed.returncode == 0, manifest_completed.stderr
    assert "suite_name: cli-suite" in manifest_completed.stdout


def test_cli_benchmark_profile_and_hypothesis_suite(tmp_path: Path) -> None:
    profile_path = Path("configs/benchmark_profiles/h1_drift_aware_v2.yaml").resolve()

    profile_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "autorl",
            "benchmark-profile",
            "--profile",
            str(profile_path),
            "--dataset",
            "elec2",
            "--artifacts-root",
            str(tmp_path / "profile"),
            "--max-samples",
            "512",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert profile_completed.returncode == 0, profile_completed.stderr
    assert "profile_policy: hard_switch_lcb" in profile_completed.stdout

    suite_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "autorl",
            "benchmark-hypothesis-suite",
            "--profiles",
            str(profile_path),
            str(Path("configs/benchmark_profiles/adaptive_meta_final.yaml").resolve()),
            "--datasets",
            "elec2",
            "--artifacts-root",
            str(tmp_path / "hypothesis_suite"),
            "--max-samples",
            "512",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert suite_completed.returncode == 0, suite_completed.stderr
    assert "summary_json_path:" in suite_completed.stdout


def test_cli_benchmark_elec2_and_benchmark_suite_smoke(tmp_path: Path) -> None:
    benchmark_elec2_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "autorl",
            "benchmark-elec2",
            "--artifacts-root",
            str(tmp_path / "benchmark_elec2"),
            "--max-samples",
            "512",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert benchmark_elec2_completed.returncode == 0, benchmark_elec2_completed.stderr
    assert "summary_json_path:" in benchmark_elec2_completed.stdout

    benchmark_suite_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "autorl",
            "benchmark-suite",
            "--artifacts-root",
            str(tmp_path / "benchmark_suite"),
            "--datasets",
            "elec2",
            "--max-samples",
            "512",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert benchmark_suite_completed.returncode == 0, benchmark_suite_completed.stderr
    assert "summary_json_path:" in benchmark_suite_completed.stdout
