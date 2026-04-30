# Real-Stream Benchmark Replay

- dataset: `WaterFlow calibration`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `256`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.913504 |
| knn_regressor | 0.913504 |
| lin_lr_0_002 | 0.552863 |
| lin_lr_0_005 | 0.587367 |
| lin_lr_0_01 | 0.602381 |
| pa_regressor | 0.634452 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.913504`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `4`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_warmup_same |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
