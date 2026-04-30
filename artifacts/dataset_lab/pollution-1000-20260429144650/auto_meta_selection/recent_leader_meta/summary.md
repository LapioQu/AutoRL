# Real-Stream Benchmark Replay

- dataset: `pollution-1000`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `997`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.844537 |
| knn_regressor | 0.844537 |
| lin_lr_0_002 | 0.838594 |
| lin_lr_0_01 | 0.795778 |
| pa_regressor | 0.830709 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.844537`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `15`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_warmup_same |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 383 | stay | knn_regressor | lin_lr_0_01 | 0.021906 | 0.001000 | recent_leader_incumbent_floor |
| 447 | stay | knn_regressor | lin_lr_0_01 | 0.018744 | 0.001000 | recent_leader_incumbent_floor |
| 511 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 575 | stay | knn_regressor | pa_regressor | 0.021273 | 0.001000 | recent_leader_incumbent_floor |
| 639 | stay | knn_regressor | lin_lr_0_002 | 0.032578 | 0.001000 | recent_leader_incumbent_floor |
| 703 | stay | knn_regressor | lin_lr_0_002 | 0.026065 | 0.001000 | recent_leader_incumbent_floor |
| 767 | stay | knn_regressor | lin_lr_0_002 | 0.030492 | 0.001000 | recent_leader_incumbent_floor |
| 831 | stay | knn_regressor | pa_regressor | 0.040424 | 0.001000 | recent_leader_incumbent_floor |
| 895 | stay | knn_regressor | lin_lr_0_002 | 0.033653 | 0.001000 | recent_leader_incumbent_floor |
| 959 | stay | knn_regressor | lin_lr_0_002 | 0.016601 | 0.001000 | recent_leader_incumbent_floor |
