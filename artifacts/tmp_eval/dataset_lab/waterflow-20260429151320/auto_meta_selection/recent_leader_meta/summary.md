# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `1265`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.937470 |
| knn_regressor | 0.937470 |
| lin_lr_0_002 | 0.869416 |
| lin_lr_0_005 | 0.877623 |
| lin_lr_0_01 | 0.880854 |
| pa_regressor | 0.873952 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.937470`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `19`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_warmup_same |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 383 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 447 | stay | knn_regressor | lin_lr_0_01 | 0.006725 | 0.001000 | recent_leader_incumbent_floor |
| 511 | stay | knn_regressor | lin_lr_0_01 | 0.012870 | 0.001000 | recent_leader_incumbent_floor |
| 575 | stay | knn_regressor | lin_lr_0_01 | 0.010870 | 0.001000 | recent_leader_incumbent_floor |
| 639 | stay | knn_regressor | lin_lr_0_005 | 0.018650 | 0.001000 | recent_leader_incumbent_floor |
| 703 | stay | knn_regressor | lin_lr_0_005 | 0.030626 | 0.001000 | recent_leader_incumbent_floor |
| 767 | stay | knn_regressor | lin_lr_0_005 | 0.027716 | 0.001000 | recent_leader_incumbent_floor |
| 831 | stay | knn_regressor | lin_lr_0_005 | 0.022750 | 0.001000 | recent_leader_incumbent_floor |
| 895 | stay | knn_regressor | lin_lr_0_005 | 0.012493 | 0.001000 | recent_leader_incumbent_floor |
| 959 | stay | knn_regressor | lin_lr_0_002 | 0.012120 | 0.001000 | recent_leader_incumbent_floor |
| 1023 | stay | knn_regressor | lin_lr_0_002 | 0.029090 | 0.001000 | recent_leader_incumbent_floor |
| 1087 | stay | knn_regressor | lin_lr_0_01 | 0.023482 | 0.001000 | recent_leader_incumbent_floor |
| 1151 | stay | knn_regressor | lin_lr_0_01 | 0.028651 | 0.001000 | recent_leader_incumbent_floor |
| 1215 | stay | knn_regressor | lin_lr_0_01 | 0.031928 | 0.001000 | recent_leader_incumbent_floor |
