# Phase 4: evaluator and metacontroller

Phase 4 adds the central Stay/Switch logic required by the specification and raises verification from smoke checks to requirement-oriented behavioral checks.

## Implemented scope

- `Evaluator` for:
  - utility computation
  - utility extraction from `WindowMetric` / `MetricsSummary`
  - LCB computation
  - per-strategy evaluation across metric samples
- `MetaController` for:
  - Stay/Switch decisions
  - explicit threshold `delta + Cswitch`
  - structured decision reasons
  - safe fallback on evaluator errors

## Decision reasons

- `switch_advantage`
- `insufficient_samples`
- `missing_metrics`
- `invalid_candidate`
- `high_uncertainty`
- `no_candidate_improvement`
- `safe_stay_after_error`

## Verification emphasis

The Phase 4 test suite now checks:

- exact numeric utility formula from the specification;
- exact LCB formula from the specification;
- `Stay` on insufficient samples;
- `Switch` only when `LCB(candidate) - LCB(current) > delta + Cswitch`;
- `Stay` on high uncertainty;
- `Stay` with explicit safe fallback after internal evaluation failure;
- decision time below the required CPU threshold;
- stronger semantic checks for earlier phases such as stationary-vs-noisy variance and stationary action preference.
