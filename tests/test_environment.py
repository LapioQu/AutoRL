"""Phase 2 tests for the controlled RL-like environment."""

from __future__ import annotations

from pathlib import Path
from statistics import mean, pvariance

import pytest

from autorl.application import load_config
from autorl.domain import AdaptiveLearningEnv, ConfigValidationError, LearningStrategy, ScenarioName
from autorl.domain.environment import build_default_env_config


EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "configs" / "examples"


def _rollout_rewards(env: AdaptiveLearningEnv, actions: list[int]) -> list[tuple[float, dict]]:
    rewards: list[tuple[float, dict]] = []
    env.reset()
    for action in actions:
        _, reward, terminated, _, info = env.step(action)
        rewards.append((reward, info))
        if terminated:
            break
    return rewards


def test_environment_reproducibility_with_same_seed() -> None:
    config = load_config(EXAMPLES_DIR / "reproducibility.json")
    actions = [0, 1, 0, 1, 0, 1, 1, 0]

    env_a = AdaptiveLearningEnv(config)
    env_b = AdaptiveLearningEnv(config)

    rollout_a = _rollout_rewards(env_a, actions)
    rollout_b = _rollout_rewards(env_b, actions)

    assert rollout_a == rollout_b


def test_environment_reset_with_different_seed_changes_rollout() -> None:
    config = build_default_env_config(
        scenario_name=ScenarioName.NOISY_REWARD,
        episodes=8,
        steps_per_episode=1,
        strategies=(
            LearningStrategy(name="low_bias"),
            LearningStrategy(name="high_bias"),
        ),
        seed=100,
    )
    env = AdaptiveLearningEnv(config)
    actions = [0] * 6

    env.reset(seed=100)
    rollout_a = [env.step(action)[1] for action in actions]

    env.reset(seed=101)
    rollout_b = [env.step(action)[1] for action in actions]

    assert rollout_a != rollout_b


def test_abrupt_drift_changes_reward_regime_for_same_action() -> None:
    config = build_default_env_config(
        scenario_name=ScenarioName.ABRUPT_DRIFT,
        episodes=8,
        steps_per_episode=1,
        strategies=(
            LearningStrategy(name="early_regime"),
            LearningStrategy(name="late_regime"),
        ),
        seed=21,
    )
    env = AdaptiveLearningEnv(config)
    rewards = _rollout_rewards(env, [0] * 8)

    before = [reward for reward, info in rewards if info["episode_index"] < config.scenario.drift_episode]
    after = [reward for reward, info in rewards if info["episode_index"] >= config.scenario.drift_episode]

    assert before
    assert after
    assert mean(before) > mean(after)


def test_gradual_drift_progressively_changes_regime_strength() -> None:
    config = build_default_env_config(
        scenario_name=ScenarioName.GRADUAL_DRIFT,
        episodes=9,
        steps_per_episode=1,
        strategies=(
            LearningStrategy(name="low_bias"),
            LearningStrategy(name="high_bias"),
        ),
        seed=31,
    )
    env = AdaptiveLearningEnv(config)
    rollout = _rollout_rewards(env, [0] * 9)

    strengths = [info["regime_strength"] for _, info in rollout]
    assert strengths == sorted(strengths)
    assert strengths[0] < strengths[-1]


def test_noisy_reward_emits_non_zero_noise_signal() -> None:
    config = build_default_env_config(
        scenario_name=ScenarioName.NOISY_REWARD,
        episodes=12,
        steps_per_episode=1,
        strategies=(
            LearningStrategy(name="stable"),
            LearningStrategy(name="risky"),
        ),
        seed=41,
    )
    env = AdaptiveLearningEnv(config)
    rollout = _rollout_rewards(env, [0] * 12)

    noises = [abs(info["reward_noise"]) for _, info in rollout]
    assert any(noise > 0.0 for noise in noises)


def test_stationary_reward_is_more_consistent_than_noisy_reward() -> None:
    stationary = build_default_env_config(
        scenario_name=ScenarioName.STATIONARY,
        episodes=12,
        steps_per_episode=1,
        strategies=(
            LearningStrategy(name="stable"),
            LearningStrategy(name="risky"),
        ),
        seed=71,
    )
    noisy = build_default_env_config(
        scenario_name=ScenarioName.NOISY_REWARD,
        episodes=12,
        steps_per_episode=1,
        strategies=(
            LearningStrategy(name="stable"),
            LearningStrategy(name="risky"),
        ),
        seed=71,
    )
    stationary_rollout = _rollout_rewards(AdaptiveLearningEnv(stationary), [0] * 12)
    noisy_rollout = _rollout_rewards(AdaptiveLearningEnv(noisy), [0] * 12)

    stationary_rewards = [reward for reward, _ in stationary_rollout]
    noisy_rewards = [reward for reward, _ in noisy_rollout]
    assert pvariance(noisy_rewards) > pvariance(stationary_rewards)


def test_stationary_regime_prefers_low_profile_action() -> None:
    config = build_default_env_config(
        scenario_name=ScenarioName.STATIONARY,
        episodes=8,
        steps_per_episode=1,
        strategies=(
            LearningStrategy(name="low_profile"),
            LearningStrategy(name="high_profile"),
        ),
        seed=81,
    )
    low_rollout = _rollout_rewards(AdaptiveLearningEnv(config), [0] * 8)
    high_rollout = _rollout_rewards(AdaptiveLearningEnv(config), [1] * 8)

    assert mean(reward for reward, _ in low_rollout) > mean(reward for reward, _ in high_rollout)


def test_fallback_scenario_triggers_guard_after_repeated_failures() -> None:
    config = build_default_env_config(
        scenario_name=ScenarioName.FALLBACK,
        episodes=6,
        steps_per_episode=1,
        strategies=(
            LearningStrategy(name="always_bad"),
            LearningStrategy(name="less_bad"),
        ),
        seed=51,
    )
    env = AdaptiveLearningEnv(config)
    rollout = _rollout_rewards(env, [1] * 6)

    assert any(info["fallback_triggered"] for _, info in rollout)


def test_environment_raises_on_unknown_action_name() -> None:
    config = build_default_env_config(
        scenario_name=ScenarioName.STATIONARY,
        episodes=4,
        steps_per_episode=1,
        strategies=(
            LearningStrategy(name="fixed"),
            LearningStrategy(name="adaptive"),
        ),
        seed=61,
    )
    env = AdaptiveLearningEnv(config)
    env.reset()

    with pytest.raises(ConfigValidationError, match="unknown strategy action"):
        env.step("missing")
