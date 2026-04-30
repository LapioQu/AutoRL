# Real-Stream Benchmark Replay

- dataset: `TrumpApproval`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `998`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.817876 |
| knn_regressor | 0.817876 |
| lin_lr_0_0005 | 0.581033 |
| pa_regressor | 0.358650 |
| tree_regressor | 0.558874 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.817876`
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
| 383 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 447 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 511 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 575 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 639 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 703 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 767 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 831 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 895 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 959 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
