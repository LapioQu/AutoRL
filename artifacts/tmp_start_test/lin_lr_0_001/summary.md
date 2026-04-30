# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `253`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_001`
- final_strategy: `knn_regressor`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.807845 |
| knn_regressor | 0.927288 |
| lin_lr_0_001 | 0.575832 |
| lin_lr_0_01 | 0.651596 |
| pa_regressor | 0.669957 |
| tree_regressor | 0.749371 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.927288`
- adaptive_delta_vs_best_fixed: `-0.119443`
- block_delta_mean: `-0.119917`
- block_delta_ci95: `0.151785`
- block_count: `12`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 41 | switch | lin_lr_0_001 | knn_regressor |  | 0.001000 | recent_leader_warmup |
| 62 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_cooldown |
| 83 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 104 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 125 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 146 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 167 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 188 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 209 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 230 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 251 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
