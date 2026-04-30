"""Utility and LCB evaluation for phase 4 metacontroller logic."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean, pstdev

from autorl.domain.errors import ConfigValidationError
from autorl.domain.metrics import MetricsSummary
from autorl.domain.models import MetaControllerConfig, WindowMetric


@dataclass(frozen=True, slots=True)
class UtilityBreakdown:
    """Fully expanded utility computation for one sample."""

    reward_mean: float
    reward_variance: float
    compute_cost: float
    switch_cost: float
    utility: float


@dataclass(frozen=True, slots=True)
class StrategyEvaluation:
    """Aggregated utility evaluation for a strategy across samples."""

    strategy_name: str
    sample_count: int
    utilities: tuple[float, ...]
    mean_utility: float
    std_utility: float
    lcb: float


class Evaluator:
    """Compute utility and lower confidence bounds from metrics."""

    def compute_utility(
        self,
        *,
        reward_mean: float,
        reward_variance: float,
        compute_cost: float,
        switch_cost: float,
        meta_config: MetaControllerConfig,
    ) -> UtilityBreakdown:
        weights = meta_config.utility_weights
        utility = (
            (weights["reward_mean"] * reward_mean)
            - (weights["reward_variance"] * reward_variance)
            - (weights["compute_cost"] * compute_cost)
            - (weights["switch_cost"] * switch_cost)
        )
        return UtilityBreakdown(
            reward_mean=reward_mean,
            reward_variance=reward_variance,
            compute_cost=compute_cost,
            switch_cost=switch_cost,
            utility=utility,
        )

    def compute_utility_from_window(
        self,
        metric: WindowMetric,
        *,
        meta_config: MetaControllerConfig,
        decision_switch_cost: float | None = None,
    ) -> UtilityBreakdown:
        return self.compute_utility(
            reward_mean=metric.reward_mean if metric.utility_reward_mean is None else metric.utility_reward_mean,
            reward_variance=metric.reward_variance if metric.utility_reward_variance is None else metric.utility_reward_variance,
            compute_cost=metric.compute_cost_mean if metric.utility_compute_cost is None else metric.utility_compute_cost,
            switch_cost=metric.utility_switch_cost if decision_switch_cost is None else decision_switch_cost,
            meta_config=meta_config,
        )

    def compute_utility_from_summary(
        self,
        summary: MetricsSummary,
        *,
        meta_config: MetaControllerConfig,
        decision_switch_cost: float | None = None,
    ) -> UtilityBreakdown:
        utility_inputs = summary.utility_inputs
        return self.compute_utility(
            reward_mean=utility_inputs["reward_mean"],
            reward_variance=utility_inputs["reward_variance"],
            compute_cost=utility_inputs["compute_cost"],
            switch_cost=utility_inputs["switch_cost"] if decision_switch_cost is None else decision_switch_cost,
            meta_config=meta_config,
        )

    def compute_lcb(self, utilities: list[float] | tuple[float, ...], *, lambda_value: float) -> tuple[float, float, float]:
        if not utilities:
            raise ConfigValidationError("utilities must not be empty")
        mean_utility = fmean(utilities)
        std_utility = pstdev(utilities) if len(utilities) > 1 else 0.0
        lcb = mean_utility - (lambda_value * std_utility)
        return mean_utility, std_utility, lcb

    def evaluate_strategy(
        self,
        strategy_name: str,
        metrics: list[WindowMetric] | tuple[WindowMetric, ...],
        *,
        meta_config: MetaControllerConfig,
        decision_switch_cost: float | None = None,
    ) -> StrategyEvaluation:
        if not strategy_name.strip():
            raise ConfigValidationError("strategy_name must be non-empty")
        if not metrics:
            raise ConfigValidationError("metrics must not be empty")

        utilities = tuple(
            self.compute_utility_from_window(
                metric,
                meta_config=meta_config,
                decision_switch_cost=decision_switch_cost,
            ).utility
            for metric in metrics
        )
        mean_utility, std_utility, lcb = self.compute_lcb(utilities, lambda_value=meta_config.lambda_value)
        return StrategyEvaluation(
            strategy_name=strategy_name.strip(),
            sample_count=len(utilities),
            utilities=utilities,
            mean_utility=mean_utility,
            std_utility=std_utility,
            lcb=lcb,
        )
