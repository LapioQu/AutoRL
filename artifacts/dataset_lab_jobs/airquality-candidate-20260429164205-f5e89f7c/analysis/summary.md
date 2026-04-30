# Real-Stream Benchmark Replay

- dataset: `AirQuality_candidate`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `9354`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `tree_regressor`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.993305 |
| knn_regressor | 0.986403 |
| lin_lr_0_001 | 0.956614 |
| lin_lr_0_002 | 0.964057 |
| pa_regressor | 0.923224 |
| tree_regressor | 0.951977 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.986403`
- adaptive_delta_vs_best_fixed: `0.006903`
- block_delta_mean: `0.006910`
- block_delta_ci95: `0.002780`
- block_count: `146`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 191 | stay | knn_regressor | tree_regressor | -0.021075 | 0.003000 | no_candidate_improvement |
| 255 | stay | knn_regressor | tree_regressor | -0.020468 | 0.003000 | high_uncertainty |
| 319 | stay | knn_regressor | tree_regressor | -0.013955 | 0.003000 | high_uncertainty |
| 383 | stay | knn_regressor | tree_regressor | -0.037890 | 0.003000 | high_uncertainty |
| 447 | stay | knn_regressor | lin_lr_0_001 | -0.044836 | 0.003000 | no_candidate_improvement |
| 511 | stay | knn_regressor | tree_regressor | -0.036009 | 0.003000 | high_uncertainty |
| 575 | stay | knn_regressor | tree_regressor | -0.009608 | 0.003000 | no_candidate_improvement |
| 639 | stay | knn_regressor | tree_regressor | -0.008987 | 0.003000 | high_uncertainty |
| 703 | stay | knn_regressor | tree_regressor | -0.014915 | 0.003000 | high_uncertainty |
| 767 | stay | knn_regressor | tree_regressor | -0.022024 | 0.003000 | no_candidate_improvement |
| 831 | stay | knn_regressor | tree_regressor | -0.018248 | 0.003000 | no_candidate_improvement |
| 895 | stay | knn_regressor | lin_lr_0_002 | -0.042934 | 0.003000 | high_uncertainty |
| 959 | stay | knn_regressor | lin_lr_0_002 | -0.060928 | 0.003000 | high_uncertainty |
| 1023 | stay | knn_regressor | tree_regressor | -0.056954 | 0.003000 | high_uncertainty |
| 1087 | stay | knn_regressor | tree_regressor | -0.017279 | 0.003000 | high_uncertainty |
| 1151 | stay | knn_regressor | tree_regressor | -0.006833 | 0.003000 | high_uncertainty |
| 1215 | stay | knn_regressor | pa_regressor | -0.016305 | 0.003000 | no_candidate_improvement |
| 1279 | stay | knn_regressor | pa_regressor | -0.014098 | 0.003000 | no_candidate_improvement |
| 1343 | stay | knn_regressor | pa_regressor | -0.013760 | 0.003000 | no_candidate_improvement |
| 1407 | stay | knn_regressor | pa_regressor | -0.013748 | 0.003000 | no_candidate_improvement |

... truncated 124 additional decision rows in `decisions.csv`.
