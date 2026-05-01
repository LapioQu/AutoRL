# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `1265`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_01`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.949776 |
| knn_regressor | 0.937458 |
| lin_lr_0_002 | 0.869416 |
| lin_lr_0_005 | 0.877623 |
| lin_lr_0_01 | 0.880854 |
| pa_regressor | 0.873952 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.937458`
- adaptive_delta_vs_best_fixed: `0.012318`
- block_delta_mean: `0.010737`
- block_delta_ci95: `0.006206`
- block_count: `19`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 191 | stay | knn_regressor | pa_regressor | -0.374559 | 0.003000 | high_uncertainty |
| 255 | stay | knn_regressor | pa_regressor | -0.103642 | 0.003000 | high_uncertainty |
| 319 | stay | knn_regressor | pa_regressor | -0.026473 | 0.003000 | high_uncertainty |
| 383 | stay | knn_regressor | pa_regressor | -0.023244 | 0.003000 | high_uncertainty |
| 447 | stay | knn_regressor | lin_lr_0_01 | -0.007844 | 0.003000 | high_uncertainty |
| 511 | stay | knn_regressor | lin_lr_0_01 | 0.009798 | 0.003000 | high_uncertainty |
| 575 | switch | knn_regressor | lin_lr_0_01 | 0.011870 | 0.003000 | switch_advantage |
| 639 | stay | lin_lr_0_01 | lin_lr_0_005 | 0.000695 | 0.003000 | no_candidate_improvement |
| 703 | stay | lin_lr_0_01 | lin_lr_0_005 | 0.001297 | 0.003000 | no_candidate_improvement |
| 767 | stay | lin_lr_0_01 | lin_lr_0_005 | 0.000989 | 0.003000 | no_candidate_improvement |
| 831 | stay | lin_lr_0_01 | lin_lr_0_005 | 0.001673 | 0.003000 | no_candidate_improvement |
| 895 | stay | lin_lr_0_01 | lin_lr_0_005 | 0.003879 | 0.003000 | high_uncertainty |
| 959 | stay | lin_lr_0_01 | lin_lr_0_002 | 0.005098 | 0.003000 | high_uncertainty |
| 1023 | stay | lin_lr_0_01 | lin_lr_0_002 | 0.018278 | 0.003000 | high_uncertainty |
| 1087 | stay | lin_lr_0_01 | lin_lr_0_002 | 0.008334 | 0.003000 | high_uncertainty |
| 1151 | stay | lin_lr_0_01 | lin_lr_0_005 | -0.002724 | 0.003000 | no_candidate_improvement |
| 1215 | stay | lin_lr_0_01 | lin_lr_0_005 | -0.002815 | 0.003000 | no_candidate_improvement |
