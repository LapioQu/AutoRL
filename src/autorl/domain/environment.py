"""Controlled RL-like environment for phase 2 experiments."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Any

from autorl.domain.errors import ConfigValidationError
from autorl.domain.models import Config, LearningStrategy, ScenarioName


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


@dataclass(frozen=True, slots=True)
class EnvironmentObservation:
    """Observable environment state exposed after reset/step."""

    episode_index: int
    step_index: int
    mastery: float
    regime_strength: float
    regime_index: int
    previous_reward: float
    previous_success: bool
    last_action: str | None
    failure_streak: int
    fallback_triggered: bool


@dataclass(frozen=True, slots=True)
class EnvironmentStep:
    """Structured step result for callers that prefer a typed wrapper."""

    observation: EnvironmentObservation
    reward: float
    terminated: bool
    truncated: bool
    info: dict[str, Any]


class AdaptiveLearningEnv:
    """A seed-controlled Gym-like environment for adaptive strategy selection."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._strategies = tuple(strategy for strategy in config.strategies if strategy.enabled)
        if not self._strategies:
            raise ConfigValidationError("environment requires at least one enabled strategy")

        self._rng = random.Random(config.seed)
        self._terminated = False
        self._seed = config.seed
        self._episode_index = 0
        self._step_index = 0
        self._mastery = 0.0
        self._last_reward = 0.0
        self._last_success = False
        self._last_action_name: str | None = None
        self._failure_streak = 0
        self._fallback_triggered = False
        self._regime_strength = 0.0
        self._regime_index = 0
        self._reset_internal_state(config.seed)

    @property
    def action_space_size(self) -> int:
        return len(self._strategies)

    @property
    def config(self) -> Config:
        return self._config

    def reset(self, *, seed: int | None = None) -> tuple[EnvironmentObservation, dict[str, Any]]:
        """Reset the environment and return the initial observation."""
        actual_seed = self._config.seed if seed is None else seed
        self._seed = actual_seed
        self._reset_internal_state(actual_seed)
        observation = self._build_observation()
        info = {
            "seed": actual_seed,
            "scenario": self._config.scenario.name.value,
            "regime_strength": self._regime_strength,
            "regime_index": self._regime_index,
        }
        return observation, info

    def step(self, action: int | str) -> tuple[EnvironmentObservation, float, bool, bool, dict[str, Any]]:
        """Advance the environment by one step using a strategy action."""
        if self._terminated:
            raise RuntimeError("environment is terminated; call reset() before stepping again")

        strategy_index = self._resolve_action(action)
        strategy = self._strategies[strategy_index]
        regime_strength = self._regime_strength_for_episode(self._episode_index)
        regime_index = 0 if regime_strength < 0.5 else 1
        action_profile = self._action_profile(strategy_index)
        action_quality = 1.0 - abs(action_profile - regime_strength)
        action_quality = _clamp(action_quality, 0.0, 1.0)

        mastery_target = _clamp(0.25 + 0.65 * action_quality, 0.0, 1.0)
        learning_rate = 0.04 + 0.08 * action_quality
        if self._config.scenario.name is ScenarioName.FALLBACK:
            learning_rate *= 0.75

        previous_mastery = self._mastery
        self._mastery = _clamp(
            self._mastery + learning_rate * (mastery_target - self._mastery),
            0.0,
            1.0,
        )
        learning_progress = self._mastery - previous_mastery

        reward_noise = self._sample_reward_noise()
        fallback_penalty = 0.0
        if self._config.scenario.name is ScenarioName.FALLBACK and self._failure_streak >= max(
            0,
            (self._config.scenario.fallback_patience or 1) - 1,
        ):
            self._fallback_triggered = True
            fallback_penalty = 0.18
        else:
            self._fallback_triggered = False

        reward = (
            self._mastery
            + 0.35 * action_quality
            - 0.20 * strategy.compute_cost
            - fallback_penalty
            + reward_noise
        )
        reward = _clamp(reward, -1.0, 1.5)
        success_threshold = 0.68 if self._config.scenario.name is not ScenarioName.FALLBACK else 0.72
        success = reward >= success_threshold and action_quality >= 0.45

        if success:
            self._failure_streak = 0
        else:
            self._failure_streak += 1

        self._last_reward = reward
        self._last_success = success
        self._last_action_name = strategy.name

        info = {
            "seed": self._seed,
            "scenario": self._config.scenario.name.value,
            "episode_index": self._episode_index,
            "step_index": self._step_index,
            "action_index": strategy_index,
            "action_name": strategy.name,
            "action_quality": action_quality,
            "action_profile": action_profile,
            "regime_strength": regime_strength,
            "regime_index": regime_index,
            "reward_noise": reward_noise,
            "success": success,
            "learning_progress": learning_progress,
            "mastery": self._mastery,
            "fallback_triggered": self._fallback_triggered,
            "failure_streak": self._failure_streak,
        }

        self._advance_time()
        observation = self._build_observation()
        return observation, reward, self._terminated, False, info

    def step_result(self, action: int | str) -> EnvironmentStep:
        """Return a typed step result wrapper around step()."""
        observation, reward, terminated, truncated, info = self.step(action)
        return EnvironmentStep(
            observation=observation,
            reward=reward,
            terminated=terminated,
            truncated=truncated,
            info=info,
        )

    def _reset_internal_state(self, seed: int) -> None:
        self._rng = random.Random(seed)
        self._terminated = False
        self._episode_index = 0
        self._step_index = 0
        self._mastery = 0.18 + (self._rng.random() * 0.04)
        self._last_reward = 0.0
        self._last_success = False
        self._last_action_name = None
        self._failure_streak = 0
        self._fallback_triggered = False
        self._regime_strength = self._regime_strength_for_episode(0)
        self._regime_index = 0 if self._regime_strength < 0.5 else 1

    def _build_observation(self) -> EnvironmentObservation:
        return EnvironmentObservation(
            episode_index=self._episode_index,
            step_index=self._step_index,
            mastery=self._mastery,
            regime_strength=self._regime_strength,
            regime_index=self._regime_index,
            previous_reward=self._last_reward,
            previous_success=self._last_success,
            last_action=self._last_action_name,
            failure_streak=self._failure_streak,
            fallback_triggered=self._fallback_triggered,
        )

    def _advance_time(self) -> None:
        self._step_index += 1
        if self._step_index >= self._config.scenario.steps_per_episode:
            self._step_index = 0
            self._episode_index += 1

        if self._episode_index >= self._config.scenario.episodes:
            self._terminated = True
            self._episode_index = self._config.scenario.episodes
            self._regime_strength = self._regime_strength_for_episode(self._config.scenario.episodes - 1)
        else:
            self._regime_strength = self._regime_strength_for_episode(self._episode_index)
        self._regime_index = 0 if self._regime_strength < 0.5 else 1

    def _resolve_action(self, action: int | str) -> int:
        if isinstance(action, str):
            for index, strategy in enumerate(self._strategies):
                if strategy.name == action:
                    return index
            raise ConfigValidationError(f"unknown strategy action: {action!r}")
        if isinstance(action, bool) or not isinstance(action, int):
            raise ConfigValidationError("action must be an integer index or strategy name")
        if not 0 <= action < len(self._strategies):
            raise ConfigValidationError(f"action index must be between 0 and {len(self._strategies) - 1}")
        return action

    def _action_profile(self, action_index: int) -> float:
        if len(self._strategies) == 1:
            return 0.5
        return action_index / (len(self._strategies) - 1)

    def _sample_reward_noise(self) -> float:
        scenario = self._config.scenario.name
        if scenario is ScenarioName.NOISY_REWARD:
            std = self._config.scenario.reward_noise_std
            return self._rng.gauss(0.0, std)
        if scenario is ScenarioName.REPRODUCIBILITY:
            return 0.0
        return self._rng.gauss(0.0, 0.01)

    def _regime_strength_for_episode(self, episode_index: int) -> float:
        scenario = self._config.scenario
        if scenario.name in {ScenarioName.STATIONARY, ScenarioName.NOISY_REWARD, ScenarioName.REPRODUCIBILITY}:
            return 0.25
        if scenario.name is ScenarioName.ABRUPT_DRIFT:
            return 0.20 if episode_index < (scenario.drift_episode or 0) else 0.80
        if scenario.name is ScenarioName.GRADUAL_DRIFT:
            start = scenario.drift_start_episode or 0
            end = scenario.drift_end_episode or start
            if episode_index <= start:
                return 0.20
            if episode_index >= end:
                return 0.80
            progress = (episode_index - start) / (end - start)
            return 0.20 + (0.60 * progress)
        if scenario.name is ScenarioName.FALLBACK:
            return 0.10
        raise ConfigValidationError(f"unsupported scenario for environment: {scenario.name.value}")


def build_default_env_config(
    *,
    scenario_name: ScenarioName,
    episodes: int,
    steps_per_episode: int,
    strategies: tuple[LearningStrategy, ...],
    seed: int = 42,
) -> Config:
    """Test-friendly helper kept local to the environment module."""
    from autorl.domain.models import Config, MetaControllerConfig, RunMode, ScenarioConfig

    scenario_kwargs: dict[str, Any] = {
        "name": scenario_name,
        "episodes": episodes,
        "steps_per_episode": steps_per_episode,
    }
    if scenario_name is ScenarioName.ABRUPT_DRIFT:
        scenario_kwargs["drift_episode"] = max(1, episodes // 2)
    elif scenario_name is ScenarioName.GRADUAL_DRIFT:
        scenario_kwargs["drift_start_episode"] = max(1, episodes // 3)
        scenario_kwargs["drift_end_episode"] = max(2, (episodes * 2) // 3)
    elif scenario_name is ScenarioName.NOISY_REWARD:
        scenario_kwargs["reward_noise_std"] = 0.25
    elif scenario_name is ScenarioName.FALLBACK:
        scenario_kwargs["fallback_patience"] = 3

    return Config(
        schema_version="1.0",
        experiment_name=f"{scenario_name.value}-environment-test",
        seed=seed,
        mode=RunMode.ADAPTIVE,
        scenario=ScenarioConfig(**scenario_kwargs),
        strategies=strategies,
        meta_controller=MetaControllerConfig(
            window_size=6,
            min_samples=3,
            delta=0.05,
            lambda_value=1.0,
            switch_cost=0.1,
        ),
    )
