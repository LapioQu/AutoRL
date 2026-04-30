# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `1265`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_01`
- switch_count: `5`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.949918 |
| knn_regressor | 0.937528 |
| lin_lr_0_002 | 0.869416 |
| lin_lr_0_005 | 0.877623 |
| lin_lr_0_01 | 0.880854 |
| pa_regressor | 0.873952 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.937528`
- adaptive_delta_vs_best_fixed: `0.012390`
- block_delta_mean: `0.010811`
- block_delta_ci95: `0.006321`
- block_count: `19`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 383 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 447 | switch | knn_regressor | lin_lr_0_01 | 0.015798 | 0.010000 | fixed_share_weight_advantage |
| 511 | stay | lin_lr_0_01 | lin_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 575 | stay | lin_lr_0_01 | lin_lr_0_005 | 0.001618 | 0.010000 | fixed_share_margin_too_small |
| 639 | stay | lin_lr_0_01 | lin_lr_0_005 | 0.006631 | 0.010000 | fixed_share_margin_too_small |
| 703 | stay | lin_lr_0_01 | lin_lr_0_005 | 0.003728 | 0.010000 | fixed_share_margin_too_small |
| 767 | stay | lin_lr_0_01 | lin_lr_0_005 | 0.003861 | 0.010000 | fixed_share_margin_too_small |
| 831 | switch | lin_lr_0_01 | lin_lr_0_002 | 0.012446 | 0.010000 | fixed_share_weight_advantage |
| 895 | switch | lin_lr_0_002 | knn_regressor | 0.085764 | 0.010000 | fixed_share_weight_advantage |
| 959 | switch | knn_regressor | lin_lr_0_002 | 0.112009 | 0.010000 | fixed_share_weight_advantage |
| 1023 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1087 | switch | lin_lr_0_002 | lin_lr_0_01 | 0.018595 | 0.010000 | fixed_share_weight_advantage |
| 1151 | stay | lin_lr_0_01 | lin_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1215 | stay | lin_lr_0_01 | lin_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |
