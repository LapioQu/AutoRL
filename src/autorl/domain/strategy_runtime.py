"""Runtime learning strategy implementations for phase 3."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import math
import random
from statistics import fmean, pstdev
from typing import Any, Mapping

from autorl.domain.environment import EnvironmentObservation
from autorl.domain.errors import ConfigValidationError
from autorl.domain.models import LearningStrategy


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


@dataclass(frozen=True, slots=True)
class StrategyDecision:
    """A single strategy selection result."""

    action_index: int
    action_name: str
    scores: dict[str, float]
    rationale: str


class LearningStrategyPolicy(ABC):
    """Behavioral interface for runtime strategy selection."""

    strategy_type = "base"

    def __init__(
        self,
        available_actions: tuple[LearningStrategy, ...],
        *,
        seed: int | None = None,
        parameters: Mapping[str, Any] | None = None,
    ) -> None:
        if not available_actions:
            raise ConfigValidationError("available_actions must not be empty")
        self.available_actions = available_actions
        self.parameters = dict(parameters or {})
        self._rng = random.Random(seed)
        self._seed = seed
        self.reset(seed=seed)

    def reset(self, *, seed: int | None = None) -> None:
        actual_seed = self._seed if seed is None else seed
        self._rng = random.Random(actual_seed)
        self._reward_history = [[] for _ in self.available_actions]
        self._success_history = [[] for _ in self.available_actions]
        self._recent_rewards = [[] for _ in self.available_actions]
        self._selection_counts = [0 for _ in self.available_actions]
        self._last_observation: EnvironmentObservation | None = None
        self._last_action_index: int | None = None

    @abstractmethod
    def select_action(self, observation: EnvironmentObservation) -> StrategyDecision:
        """Pick the next action for the current observation."""

    def update(
        self,
        observation: EnvironmentObservation,
        *,
        action_index: int,
        reward: float,
        success: bool,
        info: Mapping[str, Any] | None = None,
    ) -> None:
        if not 0 <= action_index < len(self.available_actions):
            raise ConfigValidationError(f"action_index must be between 0 and {len(self.available_actions) - 1}")
        self._reward_history[action_index].append(float(reward))
        self._success_history[action_index].append(1.0 if success else 0.0)
        recent = self._recent_rewards[action_index]
        recent.append(float(reward))
        if len(recent) > 5:
            recent.pop(0)
        self._selection_counts[action_index] += 1
        self._last_observation = observation
        self._last_action_index = action_index

    def _mean_reward(self, action_index: int) -> float:
        history = self._reward_history[action_index]
        return fmean(history) if history else 0.0

    def _reward_std(self, action_index: int) -> float:
        history = self._reward_history[action_index]
        return pstdev(history) if len(history) > 1 else 0.0

    def _success_rate(self, action_index: int) -> float:
        history = self._success_history[action_index]
        return fmean(history) if history else 0.0

    def _recent_reward(self, action_index: int) -> float:
        history = self._recent_rewards[action_index]
        return fmean(history) if history else 0.0

    def _action_profile(self, action_index: int) -> float:
        if len(self.available_actions) == 1:
            return 0.5
        return action_index / (len(self.available_actions) - 1)

    def _fit_to_regime(self, action_index: int, regime_strength: float) -> float:
        return 1.0 - abs(self._action_profile(action_index) - regime_strength)

    def _compute_cost(self, action_index: int) -> float:
        return self.available_actions[action_index].compute_cost

    def _best_untried(self) -> int | None:
        for index, count in enumerate(self._selection_counts):
            if count == 0:
                return index
        return None


class FixedStrategy(LearningStrategyPolicy):
    """Always select the same configured action."""

    strategy_type = "fixed"

    def __init__(
        self,
        available_actions: tuple[LearningStrategy, ...],
        *,
        fixed_action_index: int = 0,
        seed: int | None = None,
        parameters: Mapping[str, Any] | None = None,
    ) -> None:
        self.fixed_action_index = fixed_action_index
        super().__init__(available_actions, seed=seed, parameters=parameters)

    def select_action(self, observation: EnvironmentObservation) -> StrategyDecision:
        if not 0 <= self.fixed_action_index < len(self.available_actions):
            raise ConfigValidationError(f"fixed_action_index must be between 0 and {len(self.available_actions) - 1}")
        return StrategyDecision(
            action_index=self.fixed_action_index,
            action_name=self.available_actions[self.fixed_action_index].name,
            scores={"fixed": 1.0},
            rationale="fixed action index",
        )


class RandomStrategy(LearningStrategyPolicy):
    """Uniform random comparator used as a stochastic control baseline."""

    strategy_type = "random"

    def select_action(self, observation: EnvironmentObservation) -> StrategyDecision:
        action_index = self._rng.randrange(len(self.available_actions))
        return StrategyDecision(
            action_index=action_index,
            action_name=self.available_actions[action_index].name,
            scores={action.name: 1.0 / len(self.available_actions) for action in self.available_actions},
            rationale="uniform random comparator",
        )


class GreedyRewardStrategy(LearningStrategyPolicy):
    """Choose the action with the highest mean observed reward."""

    strategy_type = "greedy_reward"

    def select_action(self, observation: EnvironmentObservation) -> StrategyDecision:
        untried = self._best_untried()
        if untried is not None:
            return StrategyDecision(untried, self.available_actions[untried].name, {"exploration": 1.0}, "untried action exploration")

        scores = {
            self.available_actions[index].name: self._mean_reward(index) - (0.05 * self._compute_cost(index))
            for index in range(len(self.available_actions))
        }
        best_index = max(range(len(self.available_actions)), key=lambda idx: scores[self.available_actions[idx].name])
        return StrategyDecision(best_index, self.available_actions[best_index].name, scores, "highest mean reward")


class DriftAwareStrategy(LearningStrategyPolicy):
    """Bias toward actions that fit the currently observed regime after drift."""

    strategy_type = "drift_aware"

    def select_action(self, observation: EnvironmentObservation) -> StrategyDecision:
        drift_threshold = float(self.parameters.get("drift_threshold", 0.20))
        fit_weight = float(self.parameters.get("fit_weight", 0.75))
        reward_weight = float(self.parameters.get("reward_weight", 0.25))
        previous_regime = self._last_observation.regime_strength if self._last_observation is not None else observation.regime_strength
        drift_detected = abs(observation.regime_strength - previous_regime) >= drift_threshold or observation.failure_streak >= 2

        scores: dict[str, float] = {}
        for index, action in enumerate(self.available_actions):
            fit = self._fit_to_regime(index, observation.regime_strength)
            reward_signal = self._recent_reward(index)
            score = fit if drift_detected else (fit_weight * fit) + (reward_weight * reward_signal)
            scores[action.name] = score

        best_index = max(range(len(self.available_actions)), key=lambda idx: scores[self.available_actions[idx].name])
        rationale = "drift fit" if drift_detected else "mixed fit and recent reward"
        return StrategyDecision(best_index, self.available_actions[best_index].name, scores, rationale)


class LCBConservativeStrategy(LearningStrategyPolicy):
    """Choose the action with the strongest lower confidence bound."""

    strategy_type = "lcb_conservative"

    def select_action(self, observation: EnvironmentObservation) -> StrategyDecision:
        untried = self._best_untried()
        if untried is not None:
            return StrategyDecision(untried, self.available_actions[untried].name, {"exploration": 1.0}, "untried action exploration")

        lambda_value = float(self.parameters.get("lambda_value", 1.0))
        cost_weight = float(self.parameters.get("cost_weight", 0.1))
        scores = {}
        for index, action in enumerate(self.available_actions):
            lcb = self._mean_reward(index) - (lambda_value * self._reward_std(index)) - (cost_weight * self._compute_cost(index))
            scores[action.name] = lcb

        best_index = max(range(len(self.available_actions)), key=lambda idx: scores[self.available_actions[idx].name])
        return StrategyDecision(best_index, self.available_actions[best_index].name, scores, "highest lower confidence bound")


class TemperedRewardStrategy(LearningStrategyPolicy):
    """Softmax over mean rewards with a temperature parameter."""

    strategy_type = "tempered_reward"

    def select_action(self, observation: EnvironmentObservation) -> StrategyDecision:
        untried = self._best_untried()
        if untried is not None:
            return StrategyDecision(untried, self.available_actions[untried].name, {"exploration": 1.0}, "untried action exploration")

        temperature = max(float(self.parameters.get("temperature", 0.5)), 0.01)
        cost_weight = float(self.parameters.get("cost_weight", 0.05))
        base_scores = [
            self._mean_reward(index) - (cost_weight * self._compute_cost(index))
            for index in range(len(self.available_actions))
        ]
        named_scores = {self.available_actions[index].name: score for index, score in enumerate(base_scores)}

        if temperature <= 0.10:
            best_index = max(range(len(self.available_actions)), key=lambda idx: base_scores[idx])
            return StrategyDecision(best_index, self.available_actions[best_index].name, named_scores, "low-temperature argmax")

        logits = [score / temperature for score in base_scores]
        max_logit = max(logits)
        weights = [math.exp(logit - max_logit) for logit in logits]
        selected_index = self._rng.choices(range(len(self.available_actions)), weights=weights, k=1)[0]
        return StrategyDecision(selected_index, self.available_actions[selected_index].name, named_scores, "softmax reward sampling")


class AdaptiveMetaStrategy(LearningStrategyPolicy):
    """Combine reward, success, recency, regime fit, and compute cost signals."""

    strategy_type = "adaptive_meta"

    def select_action(self, observation: EnvironmentObservation) -> StrategyDecision:
        untried = self._best_untried()
        if untried is not None:
            return StrategyDecision(untried, self.available_actions[untried].name, {"exploration": 1.0}, "untried action exploration")

        reward_weight = float(self.parameters.get("reward_weight", 0.35))
        success_weight = float(self.parameters.get("success_weight", 0.25))
        fit_weight = float(self.parameters.get("fit_weight", 0.25))
        recency_weight = float(self.parameters.get("recency_weight", 0.20))
        cost_weight = float(self.parameters.get("cost_weight", 0.15))

        scores: dict[str, float] = {}
        for index, action in enumerate(self.available_actions):
            reward_signal = self._mean_reward(index)
            success_signal = self._success_rate(index)
            fit_signal = self._fit_to_regime(index, observation.regime_strength)
            recency_signal = self._recent_reward(index)
            cost_penalty = self._compute_cost(index)
            score = (
                (reward_weight * reward_signal)
                + (success_weight * success_signal)
                + (fit_weight * fit_signal)
                + (recency_weight * recency_signal)
                - (cost_weight * cost_penalty)
            )
            scores[action.name] = score

        best_index = max(range(len(self.available_actions)), key=lambda idx: scores[self.available_actions[idx].name])
        return StrategyDecision(best_index, self.available_actions[best_index].name, scores, "weighted meta score")


class NegativeControlStrategy(LearningStrategyPolicy):
    """Intentionally poor comparator used as a negative control."""

    strategy_type = "negative_control"

    def select_action(self, observation: EnvironmentObservation) -> StrategyDecision:
        scores: dict[str, float] = {}
        for index, action in enumerate(self.available_actions):
            fit_penalty = self._fit_to_regime(index, observation.regime_strength)
            reward_signal = self._recent_reward(index)
            cost_signal = self._compute_cost(index)
            score = (0.55 * cost_signal) - (0.35 * fit_penalty) - (0.10 * reward_signal)
            scores[action.name] = score
        worst_index = max(range(len(self.available_actions)), key=lambda idx: scores[self.available_actions[idx].name])
        return StrategyDecision(
            action_index=worst_index,
            action_name=self.available_actions[worst_index].name,
            scores=scores,
            rationale="negative control favouring high-cost, low-fit actions",
        )


def build_runtime_strategy(
    strategy_type: str,
    available_actions: tuple[LearningStrategy, ...],
    *,
    seed: int | None = None,
    parameters: Mapping[str, Any] | None = None,
) -> LearningStrategyPolicy:
    """Factory for runtime learning strategies."""
    normalized = strategy_type.strip().lower()
    registry = {
        "fixed": FixedStrategy,
        "random": RandomStrategy,
        "greedyreward": GreedyRewardStrategy,
        "greedy_reward": GreedyRewardStrategy,
        "driftaware": DriftAwareStrategy,
        "drift_aware": DriftAwareStrategy,
        "lcbconservative": LCBConservativeStrategy,
        "lcb_conservative": LCBConservativeStrategy,
        "temperedreward": TemperedRewardStrategy,
        "tempered_reward": TemperedRewardStrategy,
        "adaptivemeta": AdaptiveMetaStrategy,
        "adaptive_meta": AdaptiveMetaStrategy,
        "negativecontrol": NegativeControlStrategy,
        "negative_control": NegativeControlStrategy,
    }
    strategy_cls = registry.get(normalized)
    if strategy_cls is None:
        prefix_registry = (
            ("fixed", FixedStrategy),
            ("random", RandomStrategy),
            ("greedy_reward", GreedyRewardStrategy),
            ("greedyreward", GreedyRewardStrategy),
            ("drift_aware", DriftAwareStrategy),
            ("driftaware", DriftAwareStrategy),
            ("lcb_conservative", LCBConservativeStrategy),
            ("lcbconservative", LCBConservativeStrategy),
            ("tempered_reward", TemperedRewardStrategy),
            ("temperedreward", TemperedRewardStrategy),
            ("adaptive_meta", AdaptiveMetaStrategy),
            ("adaptivemeta", AdaptiveMetaStrategy),
            ("negative_control", NegativeControlStrategy),
            ("negativecontrol", NegativeControlStrategy),
        )
        for prefix, candidate_cls in prefix_registry:
            if normalized.startswith(prefix):
                strategy_cls = candidate_cls
                break
    if strategy_cls is None:
        raise ConfigValidationError(f"unsupported runtime strategy: {strategy_type!r}")

    normalized_parameters = dict(parameters or {})
    if strategy_cls is FixedStrategy:
        fixed_action_index = int(normalized_parameters.get("fixed_action_index", 0))
        return strategy_cls(
            available_actions,
            fixed_action_index=fixed_action_index,
            seed=seed,
            parameters=normalized_parameters,
        )
    if strategy_cls is LCBConservativeStrategy and "confidence_lambda" in normalized_parameters:
        normalized_parameters.setdefault("lambda_value", normalized_parameters["confidence_lambda"])
    return strategy_cls(available_actions, seed=seed, parameters=normalized_parameters)
