# Phase 3: runtime strategies and metrics

Phase 3 adds the behavioral strategy layer and metrics aggregation needed before the metacontroller logic of Phase 4.

## Implemented scope

- runtime strategy interface in `autorl.domain.strategy_runtime`;
- concrete strategies:
  - `FixedStrategy`
  - `GreedyRewardStrategy`
  - `DriftAwareStrategy`
  - `LCBConservativeStrategy`
  - `TemperedRewardStrategy`
  - `AdaptiveMetaStrategy`
- `MetricsCollector` with aggregate summary and rolling window metrics;
- utility input metrics for the next phase: `reward_mean`, `reward_variance`, `compute_cost`, `switch_cost`.

## Strategy behavior

- `FixedStrategy`: deterministic action pinning;
- `GreedyRewardStrategy`: exploit highest historical mean reward;
- `DriftAwareStrategy`: bias toward regime fit after drift or repeated failures;
- `LCBConservativeStrategy`: prefer stronger lower confidence bound under uncertainty;
- `TemperedRewardStrategy`: temperature-controlled reward softmax;
- `AdaptiveMetaStrategy`: combine reward, success, recency, regime fit, and compute cost.

## Metrics behavior

- episode-level capture includes reward, success, active strategy, compute cost, and learning progress;
- summary metrics include `reward_mean`, `reward_variance`, `cumulative_reward`, `success_rate`, `switches`, `recovery_time`, `compute_cost_mean`, `learning_progress_mean`;
- rolling windows produce `WindowMetric` records with utility input fields for the next phase.
