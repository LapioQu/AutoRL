# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `253`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_001`
- final_strategy: `lin_lr_0_001`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.575832 |
| knn_regressor | 0.927288 |
| lin_lr_0_001 | 0.575832 |
| lin_lr_0_01 | 0.651596 |
| pa_regressor | 0.669957 |
| tree_regressor | 0.747718 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.927288`
- adaptive_delta_vs_best_fixed: `-0.351456`
- block_delta_mean: `-0.352561`
- block_delta_ci95: `0.124529`
- block_count: `12`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 41 | stay | lin_lr_0_001 | knn_regressor | 0.702416 | 0.001000 | high_uncertainty |
| 62 | stay | lin_lr_0_001 | knn_regressor | 0.600725 | 0.001000 | high_uncertainty |
| 83 | stay | lin_lr_0_001 | knn_regressor | 0.504604 | 0.001000 | high_uncertainty |
| 104 | stay | lin_lr_0_001 | knn_regressor | 0.402624 | 0.001000 | high_uncertainty |
| 125 | stay | lin_lr_0_001 | knn_regressor | 0.367874 | 0.001000 | high_uncertainty |
| 146 | stay | lin_lr_0_001 | knn_regressor | 0.349234 | 0.001000 | high_uncertainty |
| 167 | stay | lin_lr_0_001 | knn_regressor | 0.253576 | 0.001000 | high_uncertainty |
| 188 | stay | lin_lr_0_001 | pa_regressor | 0.187113 | 0.001000 | high_uncertainty |
| 209 | stay | lin_lr_0_001 | pa_regressor | 0.095655 | 0.001000 | high_uncertainty |
| 230 | stay | lin_lr_0_001 | knn_regressor | 0.095322 | 0.001000 | high_uncertainty |
| 251 | stay | lin_lr_0_001 | knn_regressor | 0.125383 | 0.001000 | high_uncertainty |
