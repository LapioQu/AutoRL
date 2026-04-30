# Real-Stream Benchmark Replay

- dataset: `pollution_4000 calibration`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `879`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.819998 |
| knn_regressor | 0.819998 |
| lin_lr_0_002 | 0.815017 |
| lin_lr_0_005 | 0.819864 |
| lin_lr_0_01 | 0.782051 |
| pa_regressor | 0.805671 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.819998`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `13`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_warmup_same |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 383 | stay | knn_regressor | lin_lr_0_01 | 0.023197 | 0.001000 | recent_leader_incumbent_floor |
| 447 | stay | knn_regressor | lin_lr_0_01 | 0.019005 | 0.001000 | recent_leader_incumbent_floor |
| 511 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 575 | stay | knn_regressor | lin_lr_0_005 | 0.022638 | 0.001000 | recent_leader_incumbent_floor |
| 639 | stay | knn_regressor | lin_lr_0_002 | 0.035103 | 0.001000 | recent_leader_incumbent_floor |
| 703 | stay | knn_regressor | lin_lr_0_002 | 0.028750 | 0.001000 | recent_leader_incumbent_floor |
| 767 | stay | knn_regressor | lin_lr_0_002 | 0.033371 | 0.001000 | recent_leader_incumbent_floor |
| 831 | stay | knn_regressor | lin_lr_0_005 | 0.045081 | 0.001000 | recent_leader_incumbent_floor |
