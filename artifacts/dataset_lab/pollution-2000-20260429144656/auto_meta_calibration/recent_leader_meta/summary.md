# Real-Stream Benchmark Replay

- dataset: `pollution-2000 calibration`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `439`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.827199 |
| knn_regressor | 0.827199 |
| lin_lr_0_002 | 0.791929 |
| lin_lr_0_01 | 0.817255 |
| pa_regressor | 0.796462 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.827199`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `6`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_warmup_same |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 383 | stay | knn_regressor | lin_lr_0_01 | 0.022287 | 0.001000 | recent_leader_incumbent_floor |
