# Real-Stream Benchmark Replay

- dataset: `Bikes calibration`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `40142`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_0001`
- final_strategy: `tree_regressor`
- switch_count: `201`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.723981 |
| lin_lr_0_0001 | 0.679432 |
| lin_lr_0_0005 | 0.679727 |
| lin_lr_0_001 | 0.680266 |
| lin_lr_0_002 | 0.680713 |
| tree_regressor | 0.695042 |

- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.695042`
- adaptive_delta_vs_best_fixed: `0.028939`
- block_delta_mean: `0.028949`
- block_delta_ci95: `0.005605`
- block_count: `627`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | switch | lin_lr_0_0001 | lin_lr_0_002 | 0.011068 | 0.010000 | fixed_share_weight_advantage |
| 127 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | switch | lin_lr_0_002 | tree_regressor | 0.312385 | 0.010000 | fixed_share_weight_advantage |
| 255 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 319 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 383 | switch | tree_regressor | lin_lr_0_0001 | 0.022788 | 0.010000 | fixed_share_weight_advantage |
| 447 | switch | lin_lr_0_0001 | tree_regressor | 0.224354 | 0.010000 | fixed_share_weight_advantage |
| 511 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 575 | switch | tree_regressor | lin_lr_0_002 | 0.122169 | 0.010000 | fixed_share_weight_advantage |
| 639 | stay | lin_lr_0_002 | lin_lr_0_001 | 0.001892 | 0.010000 | fixed_share_margin_too_small |
| 703 | stay | lin_lr_0_002 | lin_lr_0_001 | 0.006754 | 0.010000 | fixed_share_margin_too_small |
| 767 | switch | lin_lr_0_002 | lin_lr_0_0005 | 0.021334 | 0.010000 | fixed_share_weight_advantage |
| 831 | stay | lin_lr_0_0005 | lin_lr_0_0005 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 895 | stay | lin_lr_0_0005 | lin_lr_0_0005 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 959 | stay | lin_lr_0_0005 | lin_lr_0_001 | 0.000756 | 0.010000 | fixed_share_margin_too_small |
| 1023 | switch | lin_lr_0_0005 | lin_lr_0_002 | 0.038987 | 0.010000 | fixed_share_weight_advantage |
| 1087 | stay | lin_lr_0_002 | lin_lr_0_001 | 0.000838 | 0.010000 | fixed_share_margin_too_small |
| 1151 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1215 | switch | lin_lr_0_002 | lin_lr_0_0001 | 0.038366 | 0.010000 | fixed_share_weight_advantage |
| 1279 | switch | lin_lr_0_0001 | lin_lr_0_002 | 0.018393 | 0.010000 | fixed_share_weight_advantage |

... truncated 607 additional decision rows in `decisions.csv`.
