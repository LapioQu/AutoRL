# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `1268`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `pa_regressor`
- final_strategy: `lin_lr_0_0005`
- switch_count: `10`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.836279 |
| lin_lr_0_0005 | 0.802089 |
| lin_lr_0_001 | 0.803945 |
| pa_regressor | 0.726507 |

- best_fixed_strategy: `lin_lr_0_001`
- best_fixed_score: `0.803945`
- adaptive_delta_vs_best_fixed: `0.032334`
- block_delta_mean: `0.032352`
- block_delta_ci95: `0.034086`
- block_count: `52`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 23 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 47 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 71 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 95 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 119 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 143 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 167 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | switch | pa_regressor | lin_lr_0_0005 | 0.278886 | 0.010000 | fixed_share_weight_advantage |
| 215 | switch | lin_lr_0_0005 | lin_lr_0_001 | 0.227930 | 0.010000 | fixed_share_weight_advantage |
| 239 | switch | lin_lr_0_001 | pa_regressor | 0.441048 | 0.010000 | fixed_share_weight_advantage |
| 263 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 287 | switch | pa_regressor | lin_lr_0_001 | 0.182724 | 0.010000 | fixed_share_weight_advantage |
| 311 | stay | lin_lr_0_001 | lin_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 335 | stay | lin_lr_0_001 | lin_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 359 | stay | lin_lr_0_001 | lin_lr_0_0005 | 0.008997 | 0.010000 | fixed_share_margin_too_small |
| 383 | switch | lin_lr_0_001 | lin_lr_0_0005 | 0.046857 | 0.010000 | fixed_share_weight_advantage |
| 407 | stay | lin_lr_0_0005 | lin_lr_0_0005 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 431 | stay | lin_lr_0_0005 | lin_lr_0_0005 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 455 | stay | lin_lr_0_0005 | lin_lr_0_0005 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 479 | stay | lin_lr_0_0005 | lin_lr_0_0005 | 0.000000 | 0.010000 | fixed_share_same_leader |

... truncated 32 additional decision rows in `decisions.csv`.
