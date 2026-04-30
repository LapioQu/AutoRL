"""Phase 4 tests for utility, LCB, and Stay/Switch decisions."""

from __future__ import annotations

from statistics import pvariance

from autorl.domain import (
    DecisionAction,
    DecisionReason,
    Evaluator,
    MetaController,
    MetaControllerConfig,
    WindowMetric,
)


def _meta_config() -> MetaControllerConfig:
    return MetaControllerConfig(
        window_size=5,
        min_samples=3,
        delta=0.05,
        lambda_value=1.0,
        switch_cost=0.10,
        utility_weights={
            "reward_mean": 1.0,
            "reward_variance": 0.5,
            "compute_cost": 0.25,
            "switch_cost": 0.5,
        },
    )


def _window(
    idx: int,
    *,
    reward_mean: float,
    reward_variance: float,
    compute_cost: float,
    switches: int = 0,
    success_rate: float = 0.8,
    cumulative_reward: float | None = None,
    learning_progress_mean: float = 0.03,
    switch_cost_metric: float | None = None,
) -> WindowMetric:
    cumulative = reward_mean if cumulative_reward is None else cumulative_reward
    return WindowMetric(
        window_index=idx,
        start_episode=idx * 5,
        end_episode=(idx * 5) + 4,
        reward_mean=reward_mean,
        reward_variance=reward_variance,
        success_rate=success_rate,
        cumulative_reward=cumulative,
        switches=switches,
        compute_cost_mean=compute_cost,
        recovery_time=1.0,
        learning_progress_mean=learning_progress_mean,
        utility_reward_mean=reward_mean,
        utility_reward_variance=reward_variance,
        utility_compute_cost=compute_cost,
        utility_switch_cost=0.0 if switch_cost_metric is None else switch_cost_metric,
    )


def test_utility_formula_matches_spec() -> None:
    evaluator = Evaluator()
    meta_config = _meta_config()

    breakdown = evaluator.compute_utility(
        reward_mean=0.80,
        reward_variance=0.10,
        compute_cost=0.20,
        switch_cost=0.30,
        meta_config=meta_config,
    )

    expected = (1.0 * 0.80) - (0.5 * 0.10) - (0.25 * 0.20) - (0.5 * 0.30)
    assert round(breakdown.utility, 8) == round(expected, 8)


def test_lcb_formula_matches_spec() -> None:
    evaluator = Evaluator()
    utilities = [0.4, 0.6, 0.8]

    mean_utility, std_utility, lcb = evaluator.compute_lcb(utilities, lambda_value=1.25)

    expected_mean = sum(utilities) / len(utilities)
    expected_std = pvariance(utilities) ** 0.5
    expected_lcb = expected_mean - (1.25 * expected_std)
    assert round(mean_utility, 8) == round(expected_mean, 8)
    assert round(std_utility, 8) == round(expected_std, 8)
    assert round(lcb, 8) == round(expected_lcb, 8)


def test_stay_on_insufficient_samples() -> None:
    controller = MetaController()
    decision = controller.decide(
        evaluation_index=0,
        current_strategy="fixed",
        candidate_strategy="greedy",
        current_metrics=[_window(0, reward_mean=0.5, reward_variance=0.1, compute_cost=0.1)],
        candidate_metrics=[_window(0, reward_mean=0.8, reward_variance=0.1, compute_cost=0.1)],
        meta_config=_meta_config(),
    )

    assert decision.decision.action is DecisionAction.STAY
    assert decision.decision.reason_code is DecisionReason.INSUFFICIENT_SAMPLES
    assert decision.decision.is_fallback is True


def test_switch_when_candidate_has_sufficient_lcb_advantage() -> None:
    controller = MetaController()
    meta_config = _meta_config()
    current_metrics = [
        _window(0, reward_mean=0.45, reward_variance=0.02, compute_cost=0.10),
        _window(1, reward_mean=0.47, reward_variance=0.02, compute_cost=0.10),
        _window(2, reward_mean=0.46, reward_variance=0.02, compute_cost=0.10),
    ]
    candidate_metrics = [
        _window(0, reward_mean=0.85, reward_variance=0.01, compute_cost=0.08),
        _window(1, reward_mean=0.82, reward_variance=0.01, compute_cost=0.08),
        _window(2, reward_mean=0.84, reward_variance=0.01, compute_cost=0.08),
    ]

    decision = controller.decide(
        evaluation_index=1,
        current_strategy="fixed",
        candidate_strategy="adaptive_meta",
        current_metrics=current_metrics,
        candidate_metrics=candidate_metrics,
        meta_config=meta_config,
    )

    assert decision.decision.action is DecisionAction.SWITCH
    assert decision.decision.reason_code is DecisionReason.SWITCH_ADVANTAGE
    assert decision.decision.switched is True
    assert decision.decision.decision_margin is not None
    assert decision.decision.decision_margin > decision.decision.decision_threshold


def test_stay_when_uncertainty_is_high() -> None:
    controller = MetaController()
    meta_config = _meta_config()
    current_metrics = [
        _window(0, reward_mean=0.5, reward_variance=0.01, compute_cost=0.10),
        _window(1, reward_mean=0.52, reward_variance=0.01, compute_cost=0.10),
        _window(2, reward_mean=0.48, reward_variance=0.01, compute_cost=0.10),
    ]
    candidate_metrics = [
        _window(0, reward_mean=1.4, reward_variance=0.01, compute_cost=0.05),
        _window(1, reward_mean=-0.2, reward_variance=0.01, compute_cost=0.05),
        _window(2, reward_mean=1.3, reward_variance=0.01, compute_cost=0.05),
    ]

    decision = controller.decide(
        evaluation_index=2,
        current_strategy="fixed",
        candidate_strategy="greedy",
        current_metrics=current_metrics,
        candidate_metrics=candidate_metrics,
        meta_config=meta_config,
    )

    assert decision.decision.action is DecisionAction.STAY
    assert decision.decision.reason_code is DecisionReason.HIGH_UNCERTAINTY
    assert decision.decision.is_fallback is True


def test_stay_when_candidate_does_not_clear_threshold() -> None:
    controller = MetaController()
    meta_config = _meta_config()
    current_metrics = [
        _window(0, reward_mean=0.70, reward_variance=0.02, compute_cost=0.10),
        _window(1, reward_mean=0.71, reward_variance=0.02, compute_cost=0.10),
        _window(2, reward_mean=0.69, reward_variance=0.02, compute_cost=0.10),
    ]
    candidate_metrics = [
        _window(0, reward_mean=0.73, reward_variance=0.02, compute_cost=0.10),
        _window(1, reward_mean=0.72, reward_variance=0.02, compute_cost=0.10),
        _window(2, reward_mean=0.71, reward_variance=0.02, compute_cost=0.10),
    ]

    decision = controller.decide(
        evaluation_index=3,
        current_strategy="fixed",
        candidate_strategy="greedy",
        current_metrics=current_metrics,
        candidate_metrics=candidate_metrics,
        meta_config=meta_config,
    )

    assert decision.decision.action is DecisionAction.STAY
    assert decision.decision.reason_code is DecisionReason.NO_CANDIDATE_IMPROVEMENT
    assert decision.decision.is_fallback is False


def test_safe_stay_after_error() -> None:
    controller = MetaController()
    meta_config = _meta_config()
    broken_candidate_metrics = [
        _window(0, reward_mean=0.8, reward_variance=0.02, compute_cost=0.10),
        _window(1, reward_mean=0.82, reward_variance=0.02, compute_cost=0.10),
        None,
    ]

    decision = controller.decide(
        evaluation_index=4,
        current_strategy="fixed",
        candidate_strategy="greedy",
        current_metrics=[
            _window(0, reward_mean=0.6, reward_variance=0.02, compute_cost=0.10),
            _window(1, reward_mean=0.61, reward_variance=0.02, compute_cost=0.10),
            _window(2, reward_mean=0.62, reward_variance=0.02, compute_cost=0.10),
        ],
        candidate_metrics=broken_candidate_metrics,  # type: ignore[arg-type]
        meta_config=meta_config,
    )

    assert decision.decision.action is DecisionAction.STAY
    assert decision.decision.reason_code is DecisionReason.SAFE_STAY_AFTER_ERROR
    assert decision.decision.is_fallback is True


def test_decision_time_is_small() -> None:
    controller = MetaController()
    meta_config = _meta_config()
    decision = controller.decide(
        evaluation_index=5,
        current_strategy="fixed",
        candidate_strategy="adaptive_meta",
        current_metrics=[
            _window(0, reward_mean=0.4, reward_variance=0.02, compute_cost=0.10),
            _window(1, reward_mean=0.41, reward_variance=0.02, compute_cost=0.10),
            _window(2, reward_mean=0.42, reward_variance=0.02, compute_cost=0.10),
        ],
        candidate_metrics=[
            _window(0, reward_mean=0.9, reward_variance=0.01, compute_cost=0.08),
            _window(1, reward_mean=0.91, reward_variance=0.01, compute_cost=0.08),
            _window(2, reward_mean=0.92, reward_variance=0.01, compute_cost=0.08),
        ],
        meta_config=meta_config,
    )

    assert decision.decision_time_seconds < 0.5
