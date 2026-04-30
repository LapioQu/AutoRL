# Real-Stream Benchmark Replay

- dataset: `pollution`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `1997`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_002`
- switch_count: `14`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.842885 |
| knn_regressor | 0.836566 |
| lin_lr_0_002 | 0.837381 |
| lin_lr_0_01 | 0.663139 |
| pa_regressor | 0.833813 |

- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.837381`
- adaptive_delta_vs_best_fixed: `0.005504`
- block_delta_mean: `0.005540`
- block_delta_ci95: `0.012526`
- block_count: `31`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 383 | switch | knn_regressor | lin_lr_0_01 | 0.188957 | 0.010000 | fixed_share_weight_advantage |
| 447 | switch | lin_lr_0_01 | knn_regressor | 0.160025 | 0.010000 | fixed_share_weight_advantage |
| 511 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 575 | switch | knn_regressor | pa_regressor | 0.084930 | 0.010000 | fixed_share_weight_advantage |
| 639 | switch | pa_regressor | lin_lr_0_002 | 0.114128 | 0.010000 | fixed_share_weight_advantage |
| 703 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 767 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 831 | switch | lin_lr_0_002 | pa_regressor | 0.033770 | 0.010000 | fixed_share_weight_advantage |
| 895 | switch | pa_regressor | lin_lr_0_002 | 0.175581 | 0.010000 | fixed_share_weight_advantage |
| 959 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1023 | switch | lin_lr_0_002 | pa_regressor | 0.161146 | 0.010000 | fixed_share_weight_advantage |
| 1087 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1151 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1215 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1279 | stay | pa_regressor | lin_lr_0_01 | 0.003600 | 0.010000 | fixed_share_margin_too_small |

... truncated 11 additional decision rows in `decisions.csv`.
