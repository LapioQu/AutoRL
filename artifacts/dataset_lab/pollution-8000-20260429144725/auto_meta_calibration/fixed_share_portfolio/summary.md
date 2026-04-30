# Real-Stream Benchmark Replay

- dataset: `pollution-8000 calibration`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `1759`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_002`
- switch_count: `11`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.851883 |
| knn_regressor | 0.839243 |
| lin_lr_0_002 | 0.846360 |
| lin_lr_0_01 | 0.761065 |
| pa_regressor | 0.842640 |

- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.846360`
- adaptive_delta_vs_best_fixed: `0.005523`
- block_delta_mean: `0.005622`
- block_delta_ci95: `0.013163`
- block_count: `27`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 383 | switch | knn_regressor | lin_lr_0_01 | 0.185156 | 0.010000 | fixed_share_weight_advantage |
| 447 | switch | lin_lr_0_01 | knn_regressor | 0.150233 | 0.010000 | fixed_share_weight_advantage |
| 511 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 575 | switch | knn_regressor | pa_regressor | 0.083058 | 0.010000 | fixed_share_weight_advantage |
| 639 | switch | pa_regressor | lin_lr_0_002 | 0.107966 | 0.010000 | fixed_share_weight_advantage |
| 703 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 767 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 831 | switch | lin_lr_0_002 | pa_regressor | 0.032893 | 0.010000 | fixed_share_weight_advantage |
| 895 | switch | pa_regressor | lin_lr_0_002 | 0.184610 | 0.010000 | fixed_share_weight_advantage |
| 959 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1023 | switch | lin_lr_0_002 | knn_regressor | 0.169970 | 0.010000 | fixed_share_weight_advantage |
| 1087 | switch | knn_regressor | pa_regressor | 0.230926 | 0.010000 | fixed_share_weight_advantage |
| 1151 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1215 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1279 | stay | pa_regressor | lin_lr_0_01 | 0.003149 | 0.010000 | fixed_share_margin_too_small |

... truncated 7 additional decision rows in `decisions.csv`.
