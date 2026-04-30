# Real-Stream Benchmark Replay

- dataset: `pollution calibration`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `439`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_01`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.828335 |
| knn_regressor | 0.827199 |
| lin_lr_0_002 | 0.791929 |
| lin_lr_0_01 | 0.817255 |
| pa_regressor | 0.796462 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.827199`
- adaptive_delta_vs_best_fixed: `0.001136`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `6`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 383 | switch | knn_regressor | lin_lr_0_01 | 0.188957 | 0.010000 | fixed_share_weight_advantage |
