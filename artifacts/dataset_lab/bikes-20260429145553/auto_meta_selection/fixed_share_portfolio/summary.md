# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `3997`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_0005`
- final_strategy: `lin_lr_0_002`
- switch_count: `24`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.728225 |
| lin_lr_0_0005 | 0.689551 |
| lin_lr_0_001 | 0.690565 |
| lin_lr_0_002 | 0.690515 |
| tree_regressor | 0.698542 |

- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.698542`
- adaptive_delta_vs_best_fixed: `0.029684`
- block_delta_mean: `0.029002`
- block_delta_ci95: `0.015104`
- block_count: `62`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | switch | lin_lr_0_0005 | lin_lr_0_002 | 0.010893 | 0.010000 | fixed_share_weight_advantage |
| 127 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | switch | lin_lr_0_002 | tree_regressor | 0.364595 | 0.010000 | fixed_share_weight_advantage |
| 255 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 319 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 383 | switch | tree_regressor | lin_lr_0_0005 | 0.080003 | 0.010000 | fixed_share_weight_advantage |
| 447 | switch | lin_lr_0_0005 | tree_regressor | 0.202335 | 0.010000 | fixed_share_weight_advantage |
| 511 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 575 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 639 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 703 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 767 | switch | tree_regressor | lin_lr_0_0005 | 0.085666 | 0.010000 | fixed_share_weight_advantage |
| 831 | stay | lin_lr_0_0005 | lin_lr_0_0005 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 895 | switch | lin_lr_0_0005 | tree_regressor | 0.032897 | 0.010000 | fixed_share_weight_advantage |
| 959 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1023 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1087 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1151 | switch | tree_regressor | lin_lr_0_002 | 0.159024 | 0.010000 | fixed_share_weight_advantage |
| 1215 | switch | lin_lr_0_002 | lin_lr_0_0005 | 0.044987 | 0.010000 | fixed_share_weight_advantage |
| 1279 | switch | lin_lr_0_0005 | lin_lr_0_002 | 0.019212 | 0.010000 | fixed_share_weight_advantage |

... truncated 42 additional decision rows in `decisions.csv`.
