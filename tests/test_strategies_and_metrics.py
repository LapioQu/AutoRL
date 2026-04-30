"""Phase 3 tests for runtime strategies and metrics aggregation."""

from __future__ import annotations

from autorl.domain import (
    AdaptiveMetaStrategy,
    DecisionReason,
    ConfigValidationError,
    DriftAwareStrategy,
    FixedStrategy,
    GreedyRewardStrategy,
    LCBConservativeStrategy,
    LearningStrategy,
    MetricsCollector,
    NegativeControlStrategy,
    RandomStrategy,
    TemperedRewardStrategy,
)
from autorl.domain.environment import EnvironmentObservation


def _actions() -> tuple[LearningStrategy, ...]:
    return (
        LearningStrategy(name="low_cost", compute_cost=0.05),
        LearningStrategy(name="high_reward", compute_cost=0.10),
        LearningStrategy(name="drift_specialist", compute_cost=0.15),
    )


def _obs(
    *,
    regime_strength: float = 0.25,
    previous_reward: float = 0.0,
    previous_success: bool = False,
    failure_streak: int = 0,
    episode_index: int = 0,
) -> EnvironmentObservation:
    return EnvironmentObservation(
        episode_index=episode_index,
        step_index=0,
        mastery=0.3,
        regime_strength=regime_strength,
        regime_index=0 if regime_strength < 0.5 else 1,
        previous_reward=previous_reward,
        previous_success=previous_success,
        last_action=None,
        failure_streak=failure_streak,
        fallback_triggered=False,
    )


def test_fixed_strategy_returns_same_action() -> None:
    strategy = FixedStrategy(_actions(), fixed_action_index=1)
    decision = strategy.select_action(_obs())
    repeated = strategy.select_action(_obs(previous_reward=0.9, previous_success=True, failure_streak=3))

    assert decision.action_index == 1
    assert decision.action_name == "high_reward"
    assert repeated.action_index == 1


def test_greedy_reward_prefers_highest_mean_reward() -> None:
    strategy = GreedyRewardStrategy(_actions())
    observation = _obs()
    for action_index, reward in ((0, 0.2), (1, 0.9), (2, 0.4), (1, 0.8)):
        strategy.update(observation, action_index=action_index, reward=reward, success=True)

    decision = strategy.select_action(observation)

    assert decision.action_name == "high_reward"


def test_random_strategy_returns_valid_action() -> None:
    strategy = RandomStrategy(_actions(), seed=7)
    decision = strategy.select_action(_obs())

    assert 0 <= decision.action_index < len(_actions())
    assert decision.action_name in {action.name for action in _actions()}


def test_negative_control_prefers_bad_regime_fit_and_high_cost() -> None:
    strategy = NegativeControlStrategy(_actions())
    decision = strategy.select_action(_obs(regime_strength=0.05))

    assert decision.action_name == "drift_specialist"


def test_drift_aware_reacts_to_regime_shift() -> None:
    strategy = DriftAwareStrategy(_actions(), parameters={"drift_threshold": 0.15})
    strategy.update(_obs(regime_strength=0.20), action_index=0, reward=0.7, success=True)

    decision = strategy.select_action(_obs(regime_strength=0.95, failure_streak=2))

    assert decision.action_name == "drift_specialist"


def test_lcb_conservative_prefers_stable_action() -> None:
    strategy = LCBConservativeStrategy(_actions(), parameters={"lambda_value": 1.5})
    observation = _obs()
    stable_rewards = [0.72, 0.74, 0.73]
    noisy_rewards = [0.95, 0.20, 0.98]
    medium_rewards = [0.60, 0.61, 0.59]

    for reward in stable_rewards:
        strategy.update(observation, action_index=0, reward=reward, success=True)
    for reward in noisy_rewards:
        strategy.update(observation, action_index=1, reward=reward, success=reward > 0.5)
    for reward in medium_rewards:
        strategy.update(observation, action_index=2, reward=reward, success=True)

    decision = strategy.select_action(observation)

    assert decision.action_name == "low_cost"


def test_tempered_reward_prefers_best_action_at_low_temperature() -> None:
    strategy = TemperedRewardStrategy(_actions(), parameters={"temperature": 0.05})
    observation = _obs()
    for reward in (0.2, 0.3):
        strategy.update(observation, action_index=0, reward=reward, success=False)
    for reward in (0.8, 0.9):
        strategy.update(observation, action_index=1, reward=reward, success=True)
    for reward in (0.4, 0.45):
        strategy.update(observation, action_index=2, reward=reward, success=False)

    decision = strategy.select_action(observation)

    assert decision.action_name == "high_reward"


def test_adaptive_meta_combines_reward_success_and_regime_fit() -> None:
    strategy = AdaptiveMetaStrategy(_actions())
    observation = _obs(regime_strength=0.95)
    for reward in (0.55, 0.60):
        strategy.update(observation, action_index=0, reward=reward, success=True)
    for reward in (0.70, 0.72):
        strategy.update(observation, action_index=1, reward=reward, success=True)
    for reward in (0.68, 0.67):
        strategy.update(observation, action_index=2, reward=reward, success=True)

    decision = strategy.select_action(observation)

    assert decision.action_name == "drift_specialist"


def test_strategy_rejects_empty_action_list() -> None:
    try:
        FixedStrategy(())
    except ConfigValidationError as exc:
        assert "available_actions must not be empty" in str(exc)
    else:
        raise AssertionError("expected ConfigValidationError")


def test_metrics_collector_aggregates_summary() -> None:
    collector = MetricsCollector()
    collector.record_episode(episode_index=0, reward=0.4, success=False, active_strategy="fixed", steps=10, compute_cost=0.1, learning_progress=0.02)
    collector.record_episode(episode_index=1, reward=0.8, success=True, active_strategy="fixed", steps=10, compute_cost=0.1, learning_progress=0.03)
    collector.record_episode(episode_index=2, reward=0.7, success=True, active_strategy="greedy", steps=10, compute_cost=0.2, learning_progress=0.05)

    summary = collector.summary(switch_cost=0.5)

    assert round(summary.reward_mean, 4) == round((0.4 + 0.8 + 0.7) / 3, 4)
    assert summary.cumulative_reward == 1.9
    assert round(summary.success_rate, 4) == round(2 / 3, 4)
    assert summary.switches == 1
    assert summary.recovery_time == 1.0
    assert round(summary.compute_cost_mean, 4) == round((0.1 + 0.1 + 0.2) / 3, 4)
    assert summary.utility_inputs["switch_cost"] == 0.5
    assert summary.utility_inputs["reward_mean"] == summary.reward_mean


def test_metrics_collector_window_metrics_support_rolling_aggregation() -> None:
    collector = MetricsCollector()
    records = [
        (0, 0.2, False, "fixed"),
        (1, 0.4, True, "fixed"),
        (2, 0.6, True, "greedy"),
        (3, 0.8, True, "greedy"),
    ]
    for episode_index, reward, success, strategy_name in records:
        collector.record_episode(
            episode_index=episode_index,
            reward=reward,
            success=success,
            active_strategy=strategy_name,
            steps=8,
            compute_cost=0.1,
            learning_progress=0.02 * (episode_index + 1),
        )

    windows = collector.window_metrics(window_size=2, switch_cost=0.25, rolling=True)

    assert len(windows) == 3
    assert windows[0].start_episode == 0
    assert windows[0].end_episode == 1
    assert windows[0].switches == 0
    assert windows[1].switches == 1
    assert round(windows[2].reward_mean, 4) == 0.7
    assert windows[1].utility_switch_cost == 0.25
