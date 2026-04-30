# Real-Stream Benchmark Replay

- dataset: `pollution`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `3997`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_002`
- switch_count: `23`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.839442 |
| knn_regressor | 0.816602 |
| lin_lr_0_002 | 0.838480 |
| lin_lr_0_005 | 0.400626 |
| lin_lr_0_01 | 0.324039 |
| pa_regressor | 0.822280 |

- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.838480`
- adaptive_delta_vs_best_fixed: `0.000962`
- block_delta_mean: `0.000969`
- block_delta_ci95: `0.006692`
- block_count: `62`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 383 | switch | knn_regressor | lin_lr_0_01 | 0.153784 | 0.010000 | fixed_share_weight_advantage |
| 447 | switch | lin_lr_0_01 | knn_regressor | 0.150233 | 0.010000 | fixed_share_weight_advantage |
| 511 | stay | knn_regressor | lin_lr_0_005 | 0.009653 | 0.010000 | fixed_share_margin_too_small |
| 575 | switch | knn_regressor | pa_regressor | 0.067427 | 0.010000 | fixed_share_weight_advantage |
| 639 | switch | pa_regressor | lin_lr_0_002 | 0.097086 | 0.010000 | fixed_share_weight_advantage |
| 703 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 767 | stay | lin_lr_0_002 | lin_lr_0_005 | 0.008296 | 0.010000 | fixed_share_margin_too_small |
| 831 | switch | lin_lr_0_002 | pa_regressor | 0.033566 | 0.010000 | fixed_share_weight_advantage |
| 895 | switch | pa_regressor | lin_lr_0_002 | 0.131584 | 0.010000 | fixed_share_weight_advantage |
| 959 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1023 | switch | lin_lr_0_002 | knn_regressor | 0.220522 | 0.010000 | fixed_share_weight_advantage |
| 1087 | switch | knn_regressor | pa_regressor | 0.129896 | 0.010000 | fixed_share_weight_advantage |
| 1151 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1215 | switch | pa_regressor | lin_lr_0_005 | 0.032828 | 0.010000 | fixed_share_weight_advantage |
| 1279 | switch | lin_lr_0_005 | lin_lr_0_01 | 0.031860 | 0.010000 | fixed_share_weight_advantage |

... truncated 42 additional decision rows in `decisions.csv`.
