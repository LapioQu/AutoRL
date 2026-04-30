# Real-Stream Benchmark Replay

- dataset: `pollution_2000`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `1997`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_002`
- switch_count: `16`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.839362 |
| knn_regressor | 0.829186 |
| lin_lr_0_002 | 0.837381 |
| lin_lr_0_005 | 0.812539 |
| lin_lr_0_01 | 0.663139 |
| pa_regressor | 0.833813 |

- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.837381`
- adaptive_delta_vs_best_fixed: `0.001980`
- block_delta_mean: `0.001993`
- block_delta_ci95: `0.012488`
- block_count: `31`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 383 | switch | knn_regressor | lin_lr_0_01 | 0.148685 | 0.010000 | fixed_share_weight_advantage |
| 447 | switch | lin_lr_0_01 | knn_regressor | 0.133901 | 0.010000 | fixed_share_weight_advantage |
| 511 | stay | knn_regressor | lin_lr_0_005 | 0.008741 | 0.010000 | fixed_share_margin_too_small |
| 575 | switch | knn_regressor | pa_regressor | 0.065061 | 0.010000 | fixed_share_weight_advantage |
| 639 | switch | pa_regressor | lin_lr_0_002 | 0.088052 | 0.010000 | fixed_share_weight_advantage |
| 703 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 767 | stay | lin_lr_0_002 | lin_lr_0_005 | 0.007811 | 0.010000 | fixed_share_margin_too_small |
| 831 | switch | lin_lr_0_002 | pa_regressor | 0.030924 | 0.010000 | fixed_share_weight_advantage |
| 895 | switch | pa_regressor | lin_lr_0_002 | 0.128045 | 0.010000 | fixed_share_weight_advantage |
| 959 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1023 | switch | lin_lr_0_002 | knn_regressor | 0.157017 | 0.010000 | fixed_share_weight_advantage |
| 1087 | switch | knn_regressor | pa_regressor | 0.203882 | 0.010000 | fixed_share_weight_advantage |
| 1151 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1215 | switch | pa_regressor | lin_lr_0_005 | 0.031186 | 0.010000 | fixed_share_weight_advantage |
| 1279 | switch | lin_lr_0_005 | lin_lr_0_01 | 0.029165 | 0.010000 | fixed_share_weight_advantage |

... truncated 11 additional decision rows in `decisions.csv`.
