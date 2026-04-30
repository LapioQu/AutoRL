"""Stay/Switch metacontroller for phase 4."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from autorl.domain.errors import ConfigValidationError
from autorl.domain.evaluation import Evaluator, StrategyEvaluation
from autorl.domain.models import Decision, DecisionAction, DecisionReason, MetaControllerConfig, WindowMetric


@dataclass(frozen=True, slots=True)
class MetaDecision:
    """Decision plus derived evaluator context."""

    decision: Decision
    current_evaluation: StrategyEvaluation | None
    candidate_evaluation: StrategyEvaluation | None
    decision_time_seconds: float


class MetaController:
    """Central Stay/Switch decision logic."""

    def __init__(self, evaluator: Evaluator | None = None) -> None:
        self._evaluator = evaluator or Evaluator()

    def decide(
        self,
        *,
        evaluation_index: int,
        current_strategy: str,
        candidate_strategy: str | None,
        current_metrics: list[WindowMetric] | tuple[WindowMetric, ...] | None,
        candidate_metrics: list[WindowMetric] | tuple[WindowMetric, ...] | None,
        meta_config: MetaControllerConfig,
    ) -> MetaDecision:
        started_at = perf_counter()
        try:
            decision, current_eval, candidate_eval = self._decide_internal(
                evaluation_index=evaluation_index,
                current_strategy=current_strategy,
                candidate_strategy=candidate_strategy,
                current_metrics=current_metrics,
                candidate_metrics=candidate_metrics,
                meta_config=meta_config,
            )
        except Exception as exc:
            safe_decision = self._fallback_decision(
                evaluation_index=evaluation_index,
                current_strategy=current_strategy,
                candidate_strategy=candidate_strategy,
                reason_code=DecisionReason.SAFE_STAY_AFTER_ERROR,
                reason=f"Safe stay after evaluator error: {exc}",
                meta_config=meta_config,
            )
            return MetaDecision(
                decision=safe_decision,
                current_evaluation=None,
                candidate_evaluation=None,
                decision_time_seconds=perf_counter() - started_at,
            )

        return MetaDecision(
            decision=decision,
            current_evaluation=current_eval,
            candidate_evaluation=candidate_eval,
            decision_time_seconds=perf_counter() - started_at,
        )

    def _decide_internal(
        self,
        *,
        evaluation_index: int,
        current_strategy: str,
        candidate_strategy: str | None,
        current_metrics: list[WindowMetric] | tuple[WindowMetric, ...] | None,
        candidate_metrics: list[WindowMetric] | tuple[WindowMetric, ...] | None,
        meta_config: MetaControllerConfig,
    ) -> tuple[Decision, StrategyEvaluation | None, StrategyEvaluation | None]:
        threshold = meta_config.delta + meta_config.switch_cost

        if not current_metrics or not candidate_metrics:
            return (
                self._fallback_decision(
                    evaluation_index=evaluation_index,
                    current_strategy=current_strategy,
                    candidate_strategy=candidate_strategy,
                    reason_code=DecisionReason.MISSING_METRICS,
                    reason="Stay because current or candidate metrics are missing.",
                    meta_config=meta_config,
                ),
                None,
                None,
            )

        if not candidate_strategy or not candidate_strategy.strip() or candidate_strategy.strip() == current_strategy.strip():
            return (
                self._fallback_decision(
                    evaluation_index=evaluation_index,
                    current_strategy=current_strategy,
                    candidate_strategy=candidate_strategy,
                    reason_code=DecisionReason.INVALID_CANDIDATE,
                    reason="Stay because candidate strategy is invalid or equal to the current strategy.",
                    meta_config=meta_config,
                ),
                None,
                None,
            )

        if len(current_metrics) < meta_config.min_samples or len(candidate_metrics) < meta_config.min_samples:
            return (
                self._fallback_decision(
                    evaluation_index=evaluation_index,
                    current_strategy=current_strategy,
                    candidate_strategy=candidate_strategy,
                    reason_code=DecisionReason.INSUFFICIENT_SAMPLES,
                    reason="Stay because there are not enough metric samples for a stable comparison.",
                    meta_config=meta_config,
                ),
                None,
                None,
            )

        current_eval = self._evaluator.evaluate_strategy(
            current_strategy,
            current_metrics[-meta_config.min_samples :],
            meta_config=meta_config,
            decision_switch_cost=0.0,
        )
        candidate_eval = self._evaluator.evaluate_strategy(
            candidate_strategy,
            candidate_metrics[-meta_config.min_samples :],
            meta_config=meta_config,
            decision_switch_cost=meta_config.switch_cost,
        )

        if max(current_eval.std_utility, candidate_eval.std_utility) > threshold:
            decision = self._fallback_decision(
                evaluation_index=evaluation_index,
                current_strategy=current_strategy,
                candidate_strategy=candidate_strategy,
                reason_code=DecisionReason.HIGH_UNCERTAINTY,
                reason=(
                    "Stay because utility uncertainty is too high: "
                    f"current_std={current_eval.std_utility:.4f}, candidate_std={candidate_eval.std_utility:.4f}, "
                    f"threshold={threshold:.4f}."
                ),
                meta_config=meta_config,
                current_eval=current_eval,
                candidate_eval=candidate_eval,
            )
            return decision, current_eval, candidate_eval

        decision_margin = candidate_eval.lcb - current_eval.lcb
        if decision_margin > threshold:
            return (
                Decision(
                    evaluation_index=evaluation_index,
                    action=DecisionAction.SWITCH,
                    current_strategy=current_strategy,
                    candidate_strategy=candidate_strategy,
                    reason=(
                        "Switch because candidate LCB exceeds current LCB beyond the decision threshold: "
                        f"{candidate_eval.lcb:.4f} - {current_eval.lcb:.4f} = {decision_margin:.4f} > {threshold:.4f}."
                    ),
                    utility_current=current_eval.mean_utility,
                    utility_candidate=candidate_eval.mean_utility,
                    lcb_current=current_eval.lcb,
                    lcb_candidate=candidate_eval.lcb,
                    switched=True,
                    reason_code=DecisionReason.SWITCH_ADVANTAGE,
                    decision_margin=decision_margin,
                    decision_threshold=threshold,
                    is_fallback=False,
                ),
                current_eval,
                candidate_eval,
            )

        decision = Decision(
            evaluation_index=evaluation_index,
            action=DecisionAction.STAY,
            current_strategy=current_strategy,
            candidate_strategy=candidate_strategy,
            reason=(
                "Stay because candidate improvement is not sufficient after LCB comparison: "
                f"margin={decision_margin:.4f}, threshold={threshold:.4f}."
            ),
            utility_current=current_eval.mean_utility,
            utility_candidate=candidate_eval.mean_utility,
            lcb_current=current_eval.lcb,
            lcb_candidate=candidate_eval.lcb,
            switched=False,
            reason_code=DecisionReason.NO_CANDIDATE_IMPROVEMENT,
            decision_margin=decision_margin,
            decision_threshold=threshold,
            is_fallback=False,
        )
        return decision, current_eval, candidate_eval

    def _fallback_decision(
        self,
        *,
        evaluation_index: int,
        current_strategy: str,
        candidate_strategy: str | None,
        reason_code: DecisionReason,
        reason: str,
        meta_config: MetaControllerConfig,
        current_eval: StrategyEvaluation | None = None,
        candidate_eval: StrategyEvaluation | None = None,
    ) -> Decision:
        threshold = meta_config.delta + meta_config.switch_cost
        return Decision(
            evaluation_index=evaluation_index,
            action=DecisionAction.STAY,
            current_strategy=current_strategy,
            candidate_strategy=candidate_strategy,
            reason=reason,
            utility_current=None if current_eval is None else current_eval.mean_utility,
            utility_candidate=None if candidate_eval is None else candidate_eval.mean_utility,
            lcb_current=None if current_eval is None else current_eval.lcb,
            lcb_candidate=None if candidate_eval is None else candidate_eval.lcb,
            switched=False,
            reason_code=reason_code,
            decision_margin=None if current_eval is None or candidate_eval is None else candidate_eval.lcb - current_eval.lcb,
            decision_threshold=threshold,
            is_fallback=True,
        )
