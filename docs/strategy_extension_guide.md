# Strategy Extension Guide

## Runtime Strategy Extension

Runtime strategies live in:
- `src/autorl/domain/strategy_runtime.py`

To add a new strategy:
1. Subclass `LearningStrategyPolicy`.
2. Implement `select_action(...)`.
3. Reuse shared helpers such as:
   - `_mean_reward`
   - `_reward_std`
   - `_success_rate`
   - `_fit_to_regime`
   - `_compute_cost`
4. Register the class in `build_runtime_strategy(...)`.
5. Add unit tests in `tests/test_strategies_and_metrics.py`.

## Benchmark Replay Candidate Models

Replay candidate models are defined through:
- `ReplayStrategySpec`
- `build_candidate_model_registry(...)`

Supported registry names now include:
- `river_logreg`
- `river_nb`
- `river_hoeffding_tree`
- `windowed_rf`
- `windowed_histgb`

To add a replay candidate:
1. Add a new `model_kind` handler in `benchmark_replay.py`.
2. Register it in `build_candidate_model_registry(...)`.
3. Add a trace-builder smoke test in `tests/test_benchmark_replay.py`.

## Comparator Policies

Comparator strategies supported by the runtime:
- `greedy_reward`
- `random`
- `negative_control`
- `drift_aware`
- `lcb_conservative`
- `tempered_reward`
- `adaptive_meta`

These are available for controlled comparisons and validation, not only for product defaults.
