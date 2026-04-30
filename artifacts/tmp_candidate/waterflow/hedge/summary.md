# Real-Stream Benchmark Replay

- dataset: `waterflow`
- score_name: `normalized_reward`
- policy_name: `hedge_portfolio`
- samples: `1268`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `pa_regressor`
- final_strategy: `lin_lr_0_001`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.803759 |
| lin_lr_0_0005 | 0.802089 |
| lin_lr_0_001 | 0.803945 |
| pa_regressor | 0.726507 |

- best_fixed_strategy: `lin_lr_0_001`
- best_fixed_score: `0.803945`
- adaptive_delta_vs_best_fixed: `-0.000186`
- block_delta_mean: `-0.000189`
- block_delta_ci95: `0.039127`
- block_count: `52`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 23 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 47 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 71 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 95 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 119 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 143 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 167 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 191 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 215 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 239 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 263 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 287 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 311 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 335 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 359 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 383 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 407 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 431 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 455 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 479 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | hedge_same_leader |

... truncated 32 additional decision rows in `decisions.csv`.
