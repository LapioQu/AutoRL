# Real-Stream Validation Suite

This document records the current real-stream replay suite executed on multiple datasets outside the synthetic phase 0-7 environment.

## Scope

The suite currently covers:

- `Elec2` as a real non-stationary streaming classification task;
- `Bikes` as a real temporal regression task on bike availability;
- `TrumpApproval` as a compact real temporal regression stream.

The suite artifacts are stored in:

- `artifacts/real_stream_validation/suite/suite_summary.json`
- `artifacts/real_stream_validation/suite/suite_summary.md`

Run command:

```bash
python -m autorl benchmark-suite --artifacts-root artifacts/real_stream_validation/suite
```

## Aggregate Result

| Dataset | Score | Adaptive | Best Fixed | Delta | Switches | Block CI95 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Elec2 | `accuracy` | 0.916159 | 0.916005 | +0.000154 | 5 | 0.001199 |
| Bikes | `normalized_reward` | 0.677074 | 0.676251 | +0.000823 | 1 | 0.000765 |
| TrumpApproval | `normalized_reward` | 0.783516 | 0.801432 | -0.017916 | 1 | 0.015584 |

Summary:

- wins vs best fixed: `2/3`
- non-losses vs best fixed: `2/3`

## Interpretation

### Elec2

- The adaptive controller is slightly above the best fixed baseline.
- The gain is only `+0.000154`.
- The blockwise CI95 (`0.001199`) is much larger than the mean delta, so this is not strong evidence of a practically robust win by itself.
- Interpretation: adaptive switching is real and non-destructive here, but the effect is weak.

### Bikes

- The adaptive controller is above the best fixed baseline by `+0.000823`.
- The blockwise CI95 (`0.000765`) is slightly smaller than the observed delta.
- Interpretation: within this current replay setup, Bikes is the strongest real-stream case that the present system handles well.

### TrumpApproval

- The adaptive controller switches once, but still ends below the best fixed strategy.
- This is a clear signal that the current portfolio is not rich enough and that late switching from a weaker initial policy can leave too much regret.
- Interpretation: this dataset is evidence against overclaiming the system's current generality.

## Current Engineering Conclusion

The current real-stream evidence supports a stronger statement than before:

> The system can now be validated on multiple real streams, performs real strategy switching outside the synthetic environment, and can beat the best tested stationary baseline on more than one dataset.

It also supports a necessary limitation:

> The current controller and strategy registry are not yet strong enough to claim consistent superiority across real datasets.

## Next Improvement Priorities

1. Expand the stationary strategy registry beyond learning-rate variants of one linear model.
2. Add anti-oscillation logic and stronger candidate filtering in the metacontroller.
3. Add more real datasets, especially stronger drift benchmarks and additional classification streams.
4. Add formal paired statistical tests on replay blocks instead of relying only on blockwise CI summaries.
