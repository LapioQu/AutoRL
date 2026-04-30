"""Smoke tests for benchmark replay profile/config assets required by T3."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from autorl.application import BenchmarkReplayRunner


BENCHMARK_PROFILE_DIR = Path(__file__).resolve().parents[1] / "configs" / "benchmark_profiles"


def test_benchmark_profile_files_exist_and_declare_candidate_models() -> None:
    expected_files = {
        "greedy_reward.yaml",
        "h1_drift_aware_v1.yaml",
        "h1_drift_aware_v2.yaml",
        "h2_search.yaml",
        "h2_refined_drift_stable.yaml",
        "h2_refined_correctness_balanced.yaml",
        "h2_tempered_drift.yaml",
        "h2_tempered_correctness.yaml",
        "adaptive_meta_final.yaml",
    }
    existing_files = {path.name for path in BENCHMARK_PROFILE_DIR.glob("*.yaml")}
    assert expected_files <= existing_files

    for path in BENCHMARK_PROFILE_DIR.glob("*.yaml"):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert payload["candidate_models"] == [
            "river_logreg",
            "river_nb",
            "river_hoeffding_tree",
            "windowed_rf",
            "windowed_histgb",
        ]


def test_suite_all_manifest_exists() -> None:
    suite_path = Path(__file__).resolve().parents[1] / "configs" / "suite_all.yaml"
    payload = yaml.safe_load(suite_path.read_text(encoding="utf-8"))
    assert payload["suite_name"] == "suite_all"
    assert isinstance(payload["runs"], list)
    assert len(payload["runs"]) >= 5


@pytest.mark.parametrize(
    ("profile_name", "expected_policy"),
    [
        ("greedy_reward.yaml", "greedy_reward"),
        ("h2_search.yaml", "search_profile"),
        ("h2_tempered_correctness.yaml", "tempered_reward"),
    ],
)
def test_h2_profiles_execute_on_short_elec2_smoke(tmp_path: Path, profile_name: str, expected_policy: str) -> None:
    runner = BenchmarkReplayRunner()
    result = runner.run_profile_benchmark(
        profile_path=BENCHMARK_PROFILE_DIR / profile_name,
        dataset_name="elec2",
        output_root=tmp_path / profile_name.replace(".yaml", ""),
        max_samples=256,
    )

    assert result.policy_name == expected_policy
    assert result.sample_count == 256


def test_exp05_comparator_suite_executes_on_short_elec2_smoke(tmp_path: Path) -> None:
    runner = BenchmarkReplayRunner()
    result = runner.run_profile_suite(
        profile_paths=(
            BENCHMARK_PROFILE_DIR / "adaptive_meta_final.yaml",
            BENCHMARK_PROFILE_DIR / "greedy_reward.yaml",
            BENCHMARK_PROFILE_DIR / "h1_drift_aware_v1.yaml",
            BENCHMARK_PROFILE_DIR / "h1_drift_aware_v2.yaml",
            BENCHMARK_PROFILE_DIR / "h2_tempered_correctness.yaml",
        ),
        dataset_names=("elec2",),
        output_root=tmp_path / "exp05_suite",
        max_samples=256,
    )

    assert len(result.results) == 5
    assert all(item.dataset_name == "Elec2" for item in result.results)
