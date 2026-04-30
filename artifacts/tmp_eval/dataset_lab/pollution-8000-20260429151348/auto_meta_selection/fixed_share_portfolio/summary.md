# Real-Stream Benchmark Replay

- dataset: `pollution_8000`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `7997`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_002`
- switch_count: `27`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.864866 |
| knn_regressor | 0.842263 |
| lin_lr_0_002 | 0.864799 |
| lin_lr_0_005 | 0.209182 |
| lin_lr_0_01 | 0.167514 |
| pa_regressor | 0.842907 |

- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.864799`
- adaptive_delta_vs_best_fixed: `0.000067`
- block_delta_mean: `0.000067`
- block_delta_ci95: `0.003196`
- block_count: `124`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 383 | switch | knn_regressor | lin_lr_0_01 | 0.145620 | 0.010000 | fixed_share_weight_advantage |
| 447 | switch | lin_lr_0_01 | knn_regressor | 0.125425 | 0.010000 | fixed_share_weight_advantage |
| 511 | stay | knn_regressor | lin_lr_0_005 | 0.008331 | 0.010000 | fixed_share_margin_too_small |
| 575 | switch | knn_regressor | pa_regressor | 0.063686 | 0.010000 | fixed_share_weight_advantage |
| 639 | switch | pa_regressor | lin_lr_0_002 | 0.083379 | 0.010000 | fixed_share_weight_advantage |
| 703 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 767 | stay | lin_lr_0_002 | lin_lr_0_005 | 0.007521 | 0.010000 | fixed_share_margin_too_small |
| 831 | switch | lin_lr_0_002 | pa_regressor | 0.029311 | 0.010000 | fixed_share_weight_advantage |
| 895 | switch | pa_regressor | lin_lr_0_002 | 0.109662 | 0.010000 | fixed_share_weight_advantage |
| 959 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1023 | switch | lin_lr_0_002 | knn_regressor | 0.156735 | 0.010000 | fixed_share_weight_advantage |
| 1087 | switch | knn_regressor | pa_regressor | 0.082479 | 0.010000 | fixed_share_weight_advantage |
| 1151 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1215 | switch | pa_regressor | lin_lr_0_005 | 0.029347 | 0.010000 | fixed_share_weight_advantage |
| 1279 | switch | lin_lr_0_005 | lin_lr_0_01 | 0.025414 | 0.010000 | fixed_share_weight_advantage |

... truncated 104 additional decision rows in `decisions.csv`.
