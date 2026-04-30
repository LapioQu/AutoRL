# Real-Stream Benchmark Replay

- dataset: `pollution`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `3997`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_002`
- switch_count: `21`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.840605 |
| knn_regressor | 0.822649 |
| lin_lr_0_002 | 0.838480 |
| lin_lr_0_01 | 0.324039 |
| pa_regressor | 0.822280 |

- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.838480`
- adaptive_delta_vs_best_fixed: `0.002125`
- block_delta_mean: `0.002141`
- block_delta_ci95: `0.006856`
- block_count: `62`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 383 | switch | knn_regressor | lin_lr_0_01 | 0.195213 | 0.010000 | fixed_share_weight_advantage |
| 447 | switch | lin_lr_0_01 | knn_regressor | 0.178765 | 0.010000 | fixed_share_weight_advantage |
| 511 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 575 | switch | knn_regressor | pa_regressor | 0.088168 | 0.010000 | fixed_share_weight_advantage |
| 639 | switch | pa_regressor | lin_lr_0_002 | 0.126042 | 0.010000 | fixed_share_weight_advantage |
| 703 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 767 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 831 | switch | lin_lr_0_002 | pa_regressor | 0.035940 | 0.010000 | fixed_share_weight_advantage |
| 895 | switch | pa_regressor | lin_lr_0_002 | 0.175968 | 0.010000 | fixed_share_weight_advantage |
| 959 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1023 | switch | lin_lr_0_002 | knn_regressor | 0.239740 | 0.010000 | fixed_share_weight_advantage |
| 1087 | switch | knn_regressor | pa_regressor | 0.013109 | 0.010000 | fixed_share_weight_advantage |
| 1151 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1215 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1279 | stay | pa_regressor | lin_lr_0_01 | 0.006192 | 0.010000 | fixed_share_margin_too_small |

... truncated 42 additional decision rows in `decisions.csv`.
