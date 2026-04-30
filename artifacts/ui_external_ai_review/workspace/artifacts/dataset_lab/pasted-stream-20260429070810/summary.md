# Real-Stream Benchmark Replay

- dataset: `pasted-stream`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `9`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_001`
- final_strategy: `knn_regressor`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.158670 |
| knn_regressor | 0.525045 |
| lin_lr_0_001 | 0.121170 |
| lin_lr_0_01 | 0.146064 |
| pa_regressor | 0.129132 |
| tree_regressor | 0.429850 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.525045`
- adaptive_delta_vs_best_fixed: `-0.366375`
- block_delta_mean: `-0.412171`
- block_delta_ci95: `0.000000`
- block_count: `1`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 7 | switch | lin_lr_0_001 | knn_regressor |  | 0.001000 | recent_leader_warmup |
