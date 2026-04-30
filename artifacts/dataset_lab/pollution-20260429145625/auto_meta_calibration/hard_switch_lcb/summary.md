# Real-Stream Benchmark Replay

- dataset: `pollution calibration`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `879`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.816649 |
| knn_regressor | 0.816649 |
| lin_lr_0_002 | 0.815017 |
| lin_lr_0_01 | 0.782051 |
| pa_regressor | 0.805671 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.816649`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `13`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 191 | stay | knn_regressor | lin_lr_0_01 | -0.039973 | 0.003000 | high_uncertainty |
| 255 | stay | knn_regressor | lin_lr_0_01 | -0.022295 | 0.003000 | high_uncertainty |
| 319 | stay | knn_regressor | lin_lr_0_01 | -0.012935 | 0.003000 | high_uncertainty |
| 383 | stay | knn_regressor | lin_lr_0_01 | 0.006291 | 0.003000 | high_uncertainty |
| 447 | stay | knn_regressor | lin_lr_0_01 | 0.021101 | 0.003000 | high_uncertainty |
| 511 | stay | knn_regressor | lin_lr_0_01 | -0.001604 | 0.003000 | high_uncertainty |
| 575 | stay | knn_regressor | lin_lr_0_002 | 0.003230 | 0.003000 | high_uncertainty |
| 639 | stay | knn_regressor | lin_lr_0_002 | 0.028375 | 0.003000 | high_uncertainty |
| 703 | stay | knn_regressor | lin_lr_0_002 | 0.031974 | 0.003000 | high_uncertainty |
| 767 | stay | knn_regressor | lin_lr_0_002 | 0.030890 | 0.003000 | high_uncertainty |
| 831 | stay | knn_regressor | lin_lr_0_002 | 0.041317 | 0.003000 | high_uncertainty |
