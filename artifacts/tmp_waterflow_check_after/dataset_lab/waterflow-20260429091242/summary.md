# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `253`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.927288 |
| knn_regressor | 0.927288 |
| lin_lr_0_001 | 0.575832 |
| lin_lr_0_01 | 0.651596 |
| pa_regressor | 0.669957 |
| tree_regressor | 0.746755 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.927288`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `12`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 41 | stay | knn_regressor | tree_regressor | -0.012015 | 0.001000 | high_uncertainty |
| 62 | stay | knn_regressor | tree_regressor | -0.011701 | 0.001000 | high_uncertainty |
| 83 | stay | knn_regressor | tree_regressor | -0.008337 | 0.001000 | high_uncertainty |
| 104 | stay | knn_regressor | lin_lr_0_01 | -0.195337 | 0.001000 | high_uncertainty |
| 125 | stay | knn_regressor | lin_lr_0_01 | -0.097726 | 0.001000 | high_uncertainty |
| 146 | stay | knn_regressor | pa_regressor | -0.015294 | 0.001000 | high_uncertainty |
| 167 | stay | knn_regressor | pa_regressor | -0.004014 | 0.001000 | high_uncertainty |
| 188 | stay | knn_regressor | pa_regressor | 0.008452 | 0.001000 | high_uncertainty |
| 209 | stay | knn_regressor | pa_regressor | 0.004643 | 0.001000 | high_uncertainty |
| 230 | stay | knn_regressor | pa_regressor | -0.009876 | 0.001000 | high_uncertainty |
| 251 | stay | knn_regressor | pa_regressor | -0.017522 | 0.001000 | high_uncertainty |
