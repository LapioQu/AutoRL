# Real-Stream Benchmark Replay

- dataset: `pollution calibration`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `879`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `pa_regressor`
- switch_count: `5`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.827079 |
| knn_regressor | 0.816649 |
| lin_lr_0_002 | 0.815017 |
| lin_lr_0_01 | 0.782051 |
| pa_regressor | 0.805671 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.816649`
- adaptive_delta_vs_best_fixed: `0.010431`
- block_delta_mean: `0.008958`
- block_delta_ci95: `0.011690`
- block_count: `13`

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
| 639 | switch | pa_regressor | lin_lr_0_002 | 0.126103 | 0.010000 | fixed_share_weight_advantage |
| 703 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 767 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 831 | switch | lin_lr_0_002 | pa_regressor | 0.036188 | 0.010000 | fixed_share_weight_advantage |
