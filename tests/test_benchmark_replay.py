"""Tests for real-stream benchmark replay support."""

from __future__ import annotations

import json
from pathlib import Path

from autorl.application import BenchmarkReplayRunner, OutcomeTrace, PredictionTrace
from autorl.application.benchmark_replay import (
    build_candidate_model_registry,
    build_river_binary_prediction_trace,
    build_river_multioutput_regression_outcome_trace,
    build_river_regression_outcome_trace,
)
from autorl.domain import MetaControllerConfig


def test_benchmark_replay_switches_and_persists_summary(tmp_path: Path) -> None:
    trace = PredictionTrace(
        dataset_name="toy_drift_trace",
        targets=(
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
        ),
        predictions_by_strategy={
            "fixed_cold": (
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
            ),
            "fixed_hot": (
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
            ),
        },
        source_description="Toy drift trace used for unit validation.",
        source_url="memory://toy_drift_trace",
    )
    meta_config = MetaControllerConfig(
        window_size=4,
        min_samples=2,
        delta=0.0,
        lambda_value=0.0,
        switch_cost=0.25,
        utility_weights={
            "reward_mean": 1.0,
            "reward_variance": 0.0,
            "compute_cost": 0.0,
            "switch_cost": 0.0,
        },
    )

    result = BenchmarkReplayRunner().run_prediction_trace(
        trace=trace,
        output_root=tmp_path / "benchmark",
        meta_config=meta_config,
        evaluation_interval=2,
        start_strategy="fixed_cold",
    )

    assert result.switch_count >= 1
    assert result.adaptive_score >= result.best_fixed_score
    assert result.score_name == "accuracy"
    assert Path(result.decision_csv_path).exists()
    assert Path(result.summary_json_path).exists()
    assert Path(result.report_md_path).exists()

    summary = json.loads(Path(result.summary_json_path).read_text(encoding="utf-8"))
    assert summary["dataset_name"] == "toy_drift_trace"
    assert summary["score_name"] == "accuracy"
    assert summary["delta_vs_best_fixed"] >= 0.0
    assert summary["switch_count"] >= 1


def test_benchmark_replay_hedge_mode_is_not_worse_than_best_fixed_on_toy_trace(tmp_path: Path) -> None:
    trace = OutcomeTrace(
        dataset_name="toy_hedge_trace",
        score_name="accuracy",
        rewards_by_strategy={
            "fixed_left": (1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
            "fixed_right": (0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0),
        },
        successes_by_strategy={
            "fixed_left": (True, True, True, True, False, False, False, False),
            "fixed_right": (False, False, False, False, True, True, True, True),
        },
        source_description="Toy trace for hedge replay validation.",
        source_url="memory://toy_hedge_trace",
    )

    result = BenchmarkReplayRunner().run_outcome_trace_with_hedge(
        trace=trace,
        output_root=tmp_path / "hedge",
        evaluation_interval=2,
        start_strategy="fixed_left",
    )

    assert result.policy_name == "hedge_portfolio"
    assert result.adaptive_score >= result.best_fixed_score
    assert result.switch_count >= 0
    assert Path(result.summary_json_path).exists()


def test_benchmark_replay_recent_leader_mode_switches_on_toy_trace(tmp_path: Path) -> None:
    trace = OutcomeTrace(
        dataset_name="toy_recent_leader_trace",
        score_name="accuracy",
        rewards_by_strategy={
            "fixed_left": (1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
            "fixed_right": (0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0),
        },
        successes_by_strategy={
            "fixed_left": (True, True, True, True, False, False, False, False),
            "fixed_right": (False, False, False, False, True, True, True, True),
        },
        source_description="Toy trace for recent-leader replay validation.",
        source_url="memory://toy_recent_leader_trace",
    )

    result = BenchmarkReplayRunner().run_outcome_trace_with_recent_leader(
        trace=trace,
        output_root=tmp_path / "recent_leader",
        evaluation_interval=2,
        start_strategy="fixed_left",
        lookback_blocks=1,
        margin=0.0,
        warmup_blocks=1,
        cooldown_blocks=0,
        incumbent_floor=0.0,
    )

    assert result.policy_name == "recent_leader_meta"
    assert result.adaptive_score >= result.best_fixed_score
    assert result.switch_count >= 1
    assert Path(result.summary_json_path).exists()


def test_benchmark_replay_fixed_share_mode_tracks_switching_toy_trace(tmp_path: Path) -> None:
    trace = OutcomeTrace(
        dataset_name="toy_fixed_share_trace",
        score_name="accuracy",
        rewards_by_strategy={
            "fixed_left": (1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
            "fixed_right": (0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0),
        },
        successes_by_strategy={
            "fixed_left": (True, True, True, True, False, False, False, False),
            "fixed_right": (False, False, False, False, True, True, True, True),
        },
        source_description="Toy trace for fixed-share replay validation.",
        source_url="memory://toy_fixed_share_trace",
    )

    result = BenchmarkReplayRunner().run_outcome_trace_with_fixed_share(
        trace=trace,
        output_root=tmp_path / "fixed_share",
        evaluation_interval=2,
        start_strategy="fixed_left",
        eta=0.5,
        share_alpha=0.1,
        switch_threshold=0.0,
        warmup_samples=2,
    )

    assert result.policy_name == "fixed_share_portfolio"
    assert result.adaptive_score >= result.best_fixed_score
    assert result.switch_count >= 1
    assert Path(result.summary_json_path).exists()


def test_hard_switch_lcb_stays_in_stationary_trace(tmp_path: Path) -> None:
    trace = OutcomeTrace(
        dataset_name="toy_stationary_trace",
        score_name="accuracy",
        rewards_by_strategy={
            "fixed_a": (0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7),
            "fixed_b": (0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7),
        },
        successes_by_strategy={
            "fixed_a": (True, True, True, True, True, True, True, True),
            "fixed_b": (True, True, True, True, True, True, True, True),
        },
        source_description="Toy stationary trace for LCB no-switch validation.",
        source_url="memory://toy_stationary_trace",
    )
    result = BenchmarkReplayRunner().run_outcome_trace(
        trace=trace,
        output_root=tmp_path / "stationary_lcb",
        meta_config=MetaControllerConfig(
            window_size=4,
            min_samples=2,
            delta=0.02,
            lambda_value=0.8,
            switch_cost=0.1,
            utility_weights={
                "reward_mean": 1.0,
                "reward_variance": 0.25,
                "compute_cost": 0.0,
                "switch_cost": 0.0,
            },
        ),
        evaluation_interval=2,
        start_strategy="fixed_a",
    )

    assert result.policy_name == "hard_switch_lcb"
    assert result.switch_count == 0


def test_hard_switch_lcb_reduces_noise_driven_switches_against_recent_leader(tmp_path: Path) -> None:
    trace = OutcomeTrace(
        dataset_name="toy_noisy_trace",
        score_name="accuracy",
        rewards_by_strategy={
            "fixed_a": (0.76, 0.74, 0.77, 0.73, 0.75, 0.72, 0.76, 0.74, 0.77, 0.73, 0.75, 0.72),
            "fixed_b": (0.74, 0.78, 0.72, 0.79, 0.73, 0.80, 0.74, 0.78, 0.72, 0.79, 0.73, 0.80),
        },
        successes_by_strategy={
            "fixed_a": (True,) * 12,
            "fixed_b": (True,) * 12,
        },
        source_description="Toy noisy stationary trace for LCB false-switch validation.",
        source_url="memory://toy_noisy_trace",
    )
    lcb_result = BenchmarkReplayRunner().run_outcome_trace(
        trace=trace,
        output_root=tmp_path / "noisy_lcb",
        meta_config=MetaControllerConfig(
            window_size=4,
            min_samples=2,
            delta=0.02,
            lambda_value=1.0,
            switch_cost=0.15,
            utility_weights={
                "reward_mean": 1.0,
                "reward_variance": 0.30,
                "compute_cost": 0.0,
                "switch_cost": 0.0,
            },
        ),
        evaluation_interval=2,
        start_strategy="fixed_a",
    )
    recent_result = BenchmarkReplayRunner().run_outcome_trace_with_recent_leader(
        trace=trace,
        output_root=tmp_path / "noisy_recent",
        evaluation_interval=2,
        start_strategy="fixed_a",
        lookback_blocks=1,
        margin=0.0,
        warmup_blocks=1,
        cooldown_blocks=0,
        incumbent_floor=0.0,
    )

    assert lcb_result.switch_count <= recent_result.switch_count


def test_multioutput_regression_trace_builder_shapes_rewards() -> None:
    stream = [
        ({"t": 1, "region": "R1"}, {"a": 10.0, "b": 20.0}),
        ({"t": 2, "region": "R1"}, {"a": 11.0, "b": 19.0}),
        ({"t": 3, "region": "R2"}, {"a": 12.0, "b": 18.0}),
    ]

    trace = build_river_multioutput_regression_outcome_trace(
        dataset_name="toy_multioutput",
        stream=stream,
        strategies=(
            type("Spec", (), {"name": "lr_small", "learning_rate": 0.001})(),
            type("Spec", (), {"name": "lr_big", "learning_rate": 0.01})(),
        ),
        source_description="Toy multi-output stream.",
        source_url="memory://toy_multioutput",
    )

    assert trace.dataset_name == "toy_multioutput"
    assert trace.score_name == "normalized_multioutput_reward"
    assert set(trace.rewards_by_strategy) == {"lr_small", "lr_big"}
    assert all(len(rewards) == 3 for rewards in trace.rewards_by_strategy.values())
    assert all(len(successes) == 3 for successes in trace.successes_by_strategy.values())


def test_trace_builders_support_heterogeneous_model_kinds() -> None:
    classification_stream = [
        ({"x": 0.0, "group": "a"}, False),
        ({"x": 1.0, "group": "b"}, True),
        ({"x": 2.0, "group": "a"}, True),
    ]
    prediction_trace = build_river_binary_prediction_trace(
        dataset_name="toy_binary",
        stream=classification_stream,
        strategies=(
            type("Spec", (), {"name": "pa", "learning_rate": 0.0, "model_kind": "pa_classifier"})(),
            type("Spec", (), {"name": "nb", "learning_rate": 0.0, "model_kind": "gaussian_nb"})(),
        ),
        source_description="Toy binary stream.",
        source_url="memory://toy_binary",
    )
    assert set(prediction_trace.predictions_by_strategy) == {"pa", "nb"}
    assert len(prediction_trace.targets) == 3

    regression_stream = [
        ({"x": 0.0}, 0.0),
        ({"x": 1.0}, 1.0),
        ({"x": 2.0}, 2.0),
    ]
    outcome_trace = build_river_regression_outcome_trace(
        dataset_name="toy_regression",
        stream=regression_stream,
        strategies=(
            type("Spec", (), {"name": "pa_r", "learning_rate": 0.0, "model_kind": "pa_regressor"})(),
            type("Spec", (), {"name": "tree_r", "learning_rate": 0.0, "model_kind": "hoeffding_tree_regressor"})(),
        ),
        source_description="Toy regression stream.",
        source_url="memory://toy_regression",
    )
    assert set(outcome_trace.rewards_by_strategy) == {"pa_r", "tree_r"}
    assert all(len(rewards) == 3 for rewards in outcome_trace.rewards_by_strategy.values())


def test_candidate_model_registry_exposes_required_h1_h2_names_and_builds_traces() -> None:
    classification_specs = build_candidate_model_registry("classification")
    assert {spec.name for spec in classification_specs} == {
        "river_logreg",
        "river_nb",
        "river_hoeffding_tree",
        "windowed_rf",
        "windowed_histgb",
    }
    classification_trace = build_river_binary_prediction_trace(
        dataset_name="registry_binary",
        stream=[
            ({"x": 0.0, "group": "a"}, False),
            ({"x": 1.0, "group": "b"}, True),
            ({"x": 2.0, "group": "a"}, True),
            ({"x": 3.0, "group": "b"}, False),
            ({"x": 4.0, "group": "a"}, True),
        ],
        strategies=classification_specs,
        source_description="Registry smoke binary stream.",
        source_url="memory://registry_binary",
    )
    assert set(classification_trace.predictions_by_strategy) == {
        "river_logreg",
        "river_nb",
        "river_hoeffding_tree",
        "windowed_rf",
        "windowed_histgb",
    }

    regression_specs = build_candidate_model_registry("regression")
    assert {"windowed_rf", "windowed_histgb", "river_hoeffding_tree"} <= {spec.name for spec in regression_specs}
    regression_trace = build_river_regression_outcome_trace(
        dataset_name="registry_regression",
        stream=[
            ({"x": 0.0, "group": "a"}, 0.0),
            ({"x": 1.0, "group": "b"}, 1.0),
            ({"x": 2.0, "group": "a"}, 2.0),
            ({"x": 3.0, "group": "b"}, 3.0),
            ({"x": 4.0, "group": "a"}, 4.0),
            ({"x": 5.0, "group": "b"}, 5.0),
        ],
        strategies=regression_specs,
        source_description="Registry smoke regression stream.",
        source_url="memory://registry_regression",
    )
    assert "windowed_rf" in regression_trace.rewards_by_strategy
    assert "windowed_histgb" in regression_trace.rewards_by_strategy


def test_profile_policy_runner_supports_tempered_and_prefix_selected_modes(tmp_path: Path) -> None:
    trace = OutcomeTrace(
        dataset_name="toy_profile_trace",
        score_name="accuracy",
        rewards_by_strategy={
            "fixed_left": (1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
            "fixed_right": (0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0),
        },
        successes_by_strategy={
            "fixed_left": (True, True, True, True, False, False, False, False),
            "fixed_right": (False, False, False, False, True, True, True, True),
        },
        source_description="Toy trace for benchmark profile controller validation.",
        source_url="memory://toy_profile_trace",
    )
    runner = BenchmarkReplayRunner()

    tempered = runner._run_profile_policy(
        trace=trace,
        controller_policy="tempered_reward",
        output_root=tmp_path / "tempered",
    )
    search = runner._run_profile_policy(
        trace=trace,
        controller_policy="search_profile",
        output_root=tmp_path / "search",
    )

    assert tempered.switch_count >= 0
    assert tempered.adaptive_score >= 0.0
    assert search.adaptive_score >= search.best_fixed_score
    assert Path(search.summary_json_path).exists()


def test_profile_benchmark_runner_executes_real_registry_profile_on_elec2_smoke(tmp_path: Path) -> None:
    runner = BenchmarkReplayRunner()
    result = runner.run_profile_benchmark(
        profile_path=Path("configs/benchmark_profiles/h1_drift_aware_v2.yaml"),
        dataset_name="elec2",
        output_root=tmp_path / "profile_elec2",
        max_samples=1024,
    )

    assert result.dataset_name == "Elec2"
    assert result.policy_name == "hard_switch_lcb"
    assert result.sample_count == 1024
    assert Path(result.summary_json_path).exists()


def test_profile_suite_executes_multiple_profiles_with_smoke_sample_cap(tmp_path: Path) -> None:
    runner = BenchmarkReplayRunner()
    result = runner.run_profile_suite(
        profile_paths=(
            Path("configs/benchmark_profiles/h1_drift_aware_v2.yaml"),
            Path("configs/benchmark_profiles/adaptive_meta_final.yaml"),
        ),
        dataset_names=("elec2",),
        output_root=tmp_path / "profile_suite",
        max_samples=512,
    )

    assert len(result.results) == 2
    assert Path(result.summary_json_path).exists()
    assert Path(result.report_md_path).exists()
