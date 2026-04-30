"""Requirement-audit validation tests for phases 0-7."""

from __future__ import annotations

from pathlib import Path

from autorl.application import PhaseValidationRunner
from autorl.domain import LearningStrategy, build_runtime_strategy


def test_fixed_runtime_strategy_honors_prefixed_name_and_action_index() -> None:
    actions = (
        LearningStrategy(name="fixed_low"),
        LearningStrategy(name="fixed_mid"),
        LearningStrategy(name="fixed_high"),
        LearningStrategy(name="adaptive_meta_final"),
    )
    strategy = build_runtime_strategy(
        "fixed_high",
        actions,
        parameters={"fixed_action_index": 3},
    )

    assert strategy.__class__.__name__ == "FixedStrategy"
    assert strategy.fixed_action_index == 3


def test_phase_validation_runner_generates_summary_and_adaptive_is_not_worse_than_best_fixed(tmp_path: Path) -> None:
    runner = PhaseValidationRunner(root=tmp_path / "validation")

    result = runner.run_nonstationary_suite(seeds=(41, 42))

    assert Path(result.summary_json_path).exists()
    assert Path(result.report_md_path).exists()
    assert len(result.summaries) == 2
    for summary in result.summaries:
        assert summary.scenario_name in {"abrupt_drift", "gradual_drift"}
        assert summary.delta_mean >= 0.0
        assert summary.best_fixed_label in {"fixed_low", "fixed_mid", "fixed_high", "adaptive_meta_final"}
        assert summary.paired_sign_test_p_value is None or 0.0 <= summary.paired_sign_test_p_value <= 1.0
