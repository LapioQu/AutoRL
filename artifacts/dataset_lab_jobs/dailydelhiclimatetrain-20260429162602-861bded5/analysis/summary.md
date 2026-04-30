# Real-Stream Benchmark Replay

- dataset: `DailyDelhiClimateTrain`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `1459`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.980527 |
| knn_regressor | 0.980527 |
| lin_lr_0_0001 | 0.853603 |
| lin_lr_0_0005 | 0.818435 |
| lin_lr_0_002 | 0.801329 |
| tree_regressor | 0.932083 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.980527`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `22`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 191 | stay | knn_regressor | tree_regressor | -0.026012 | 0.003000 | high_uncertainty |
| 255 | stay | knn_regressor | tree_regressor | -0.028616 | 0.003000 | no_candidate_improvement |
| 319 | stay | knn_regressor | tree_regressor | -0.020851 | 0.003000 | high_uncertainty |
| 383 | stay | knn_regressor | tree_regressor | -0.022245 | 0.003000 | high_uncertainty |
| 447 | stay | knn_regressor | tree_regressor | -0.030112 | 0.003000 | no_candidate_improvement |
| 511 | stay | knn_regressor | tree_regressor | -0.022322 | 0.003000 | high_uncertainty |
| 575 | stay | knn_regressor | tree_regressor | -0.016755 | 0.003000 | high_uncertainty |
| 639 | stay | knn_regressor | tree_regressor | -0.022984 | 0.003000 | no_candidate_improvement |
| 703 | stay | knn_regressor | tree_regressor | -0.022474 | 0.003000 | high_uncertainty |
| 767 | stay | knn_regressor | tree_regressor | -0.027190 | 0.003000 | high_uncertainty |
| 831 | stay | knn_regressor | tree_regressor | -0.032269 | 0.003000 | no_candidate_improvement |
| 895 | stay | knn_regressor | tree_regressor | -0.023279 | 0.003000 | high_uncertainty |
| 959 | stay | knn_regressor | tree_regressor | -0.022444 | 0.003000 | high_uncertainty |
| 1023 | stay | knn_regressor | tree_regressor | -0.024907 | 0.003000 | high_uncertainty |
| 1087 | stay | knn_regressor | tree_regressor | -0.021973 | 0.003000 | no_candidate_improvement |
| 1151 | stay | knn_regressor | tree_regressor | -0.028276 | 0.003000 | high_uncertainty |
| 1215 | stay | knn_regressor | tree_regressor | -0.036170 | 0.003000 | high_uncertainty |
| 1279 | stay | knn_regressor | tree_regressor | -0.049021 | 0.003000 | high_uncertainty |
| 1343 | stay | knn_regressor | tree_regressor | -0.076666 | 0.003000 | high_uncertainty |
| 1407 | stay | knn_regressor | lin_lr_0_0001 | -0.075923 | 0.003000 | high_uncertainty |
