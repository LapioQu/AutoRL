# Real-Stream Benchmark Replay

- dataset: `pollution`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `3997`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_002`
- switch_count: `3`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.839153 |
| knn_regressor | 0.821448 |
| lin_lr_0_002 | 0.838480 |
| lin_lr_0_01 | 0.324039 |
| pa_regressor | 0.822280 |

- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.838480`
- adaptive_delta_vs_best_fixed: `0.000672`
- block_delta_mean: `0.000677`
- block_delta_ci95: `0.006598`
- block_count: `62`

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
| 639 | stay | knn_regressor | lin_lr_0_002 | 0.028286 | 0.003000 | high_uncertainty |
| 703 | stay | knn_regressor | lin_lr_0_002 | 0.031926 | 0.003000 | high_uncertainty |
| 767 | stay | knn_regressor | lin_lr_0_002 | 0.030567 | 0.003000 | high_uncertainty |
| 831 | stay | knn_regressor | lin_lr_0_002 | 0.036559 | 0.003000 | high_uncertainty |
| 895 | switch | knn_regressor | lin_lr_0_002 | 0.042461 | 0.003000 | switch_advantage |
| 959 | stay | lin_lr_0_002 | pa_regressor | -0.029700 | 0.003000 | high_uncertainty |
| 1023 | stay | lin_lr_0_002 | knn_regressor | 0.003739 | 0.003000 | high_uncertainty |
| 1087 | stay | lin_lr_0_002 | knn_regressor | 0.040569 | 0.003000 | high_uncertainty |
| 1151 | stay | lin_lr_0_002 | pa_regressor | 0.045552 | 0.003000 | high_uncertainty |
| 1215 | stay | lin_lr_0_002 | pa_regressor | 0.025386 | 0.003000 | high_uncertainty |
| 1279 | switch | lin_lr_0_002 | pa_regressor | 0.013278 | 0.003000 | switch_advantage |
| 1343 | stay | pa_regressor | lin_lr_0_01 | -0.000260 | 0.003000 | high_uncertainty |
| 1407 | stay | pa_regressor | lin_lr_0_002 | 0.002491 | 0.003000 | high_uncertainty |

... truncated 40 additional decision rows in `decisions.csv`.
