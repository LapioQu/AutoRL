# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
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
| tree_regressor | 0.749371 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.927288`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `12`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 41 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_warmup_same |
| 62 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 83 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 104 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 125 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 146 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 167 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 188 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 209 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 230 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 251 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
