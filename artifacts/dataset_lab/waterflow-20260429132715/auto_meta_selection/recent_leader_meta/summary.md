# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `256`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `tree_regressor`
- final_strategy: `tree_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.766907 |
| lin_lr_0_001 | 0.507672 |
| lin_lr_0_002 | 0.507672 |
| tree_regressor | 0.766907 |

- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.766907`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `10`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 47 | stay | tree_regressor | tree_regressor | 0.000000 | 0.002000 | recent_leader_warmup_same |
| 71 | stay | tree_regressor | tree_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 95 | stay | tree_regressor | tree_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 119 | stay | tree_regressor | tree_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 143 | stay | tree_regressor | tree_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 167 | stay | tree_regressor | tree_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 191 | stay | tree_regressor | tree_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 215 | stay | tree_regressor | tree_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 239 | stay | tree_regressor | tree_regressor | 0.000000 | 0.002000 | recent_leader_same |
