# Real-Stream Benchmark Replay

- dataset: `pollution-8000 calibration`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `1759`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_002`
- switch_count: `3`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.847384 |
| knn_regressor | 0.839243 |
| lin_lr_0_002 | 0.846360 |
| lin_lr_0_01 | 0.761065 |
| pa_regressor | 0.842640 |

- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.846360`
- adaptive_delta_vs_best_fixed: `0.001024`
- block_delta_mean: `0.001043`
- block_delta_ci95: `0.013796`
- block_count: `27`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 191 | stay | knn_regressor | lin_lr_0_01 | -0.034922 | 0.003000 | high_uncertainty |
| 255 | stay | knn_regressor | lin_lr_0_01 | -0.019090 | 0.003000 | high_uncertainty |
| 319 | stay | knn_regressor | lin_lr_0_01 | -0.010950 | 0.003000 | high_uncertainty |
| 383 | stay | knn_regressor | lin_lr_0_01 | 0.006355 | 0.003000 | high_uncertainty |
| 447 | stay | knn_regressor | lin_lr_0_01 | 0.020223 | 0.003000 | high_uncertainty |
| 511 | stay | knn_regressor | lin_lr_0_01 | -0.000002 | 0.003000 | high_uncertainty |
| 575 | stay | knn_regressor | lin_lr_0_002 | 0.003525 | 0.003000 | high_uncertainty |
| 639 | stay | knn_regressor | lin_lr_0_002 | 0.026242 | 0.003000 | high_uncertainty |
| 703 | stay | knn_regressor | lin_lr_0_002 | 0.029030 | 0.003000 | high_uncertainty |
| 767 | stay | knn_regressor | lin_lr_0_002 | 0.027444 | 0.003000 | high_uncertainty |
| 831 | stay | knn_regressor | lin_lr_0_002 | 0.032204 | 0.003000 | high_uncertainty |
| 895 | switch | knn_regressor | lin_lr_0_002 | 0.038994 | 0.003000 | switch_advantage |
| 959 | stay | lin_lr_0_002 | pa_regressor | -0.025747 | 0.003000 | high_uncertainty |
| 1023 | stay | lin_lr_0_002 | knn_regressor | 0.002029 | 0.003000 | high_uncertainty |
| 1087 | stay | lin_lr_0_002 | knn_regressor | 0.029013 | 0.003000 | high_uncertainty |
| 1151 | stay | lin_lr_0_002 | pa_regressor | 0.040413 | 0.003000 | high_uncertainty |
| 1215 | stay | lin_lr_0_002 | pa_regressor | 0.022342 | 0.003000 | high_uncertainty |
| 1279 | switch | lin_lr_0_002 | pa_regressor | 0.011775 | 0.003000 | switch_advantage |
| 1343 | stay | pa_regressor | lin_lr_0_01 | -0.000700 | 0.003000 | high_uncertainty |
| 1407 | stay | pa_regressor | lin_lr_0_002 | 0.002486 | 0.003000 | high_uncertainty |

... truncated 5 additional decision rows in `decisions.csv`.
