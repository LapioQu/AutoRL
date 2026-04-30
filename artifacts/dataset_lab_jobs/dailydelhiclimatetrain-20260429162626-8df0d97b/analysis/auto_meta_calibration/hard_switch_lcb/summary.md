# Real-Stream Benchmark Replay

- dataset: `DailyDelhiClimateTrain calibration`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `320`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.982493 |
| knn_regressor | 0.982493 |
| lin_lr_0_0001 | 0.689600 |
| lin_lr_0_0005 | 0.663761 |
| lin_lr_0_002 | 0.635365 |
| tree_regressor | 0.960597 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.982493`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `5`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 191 | stay | knn_regressor | tree_regressor | -0.025955 | 0.003000 | high_uncertainty |
| 255 | stay | knn_regressor | tree_regressor | -0.027937 | 0.003000 | no_candidate_improvement |
| 319 | stay | knn_regressor | tree_regressor | -0.020209 | 0.003000 | high_uncertainty |
