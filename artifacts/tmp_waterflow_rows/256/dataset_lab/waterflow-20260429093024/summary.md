# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `253`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_001`
- final_strategy: `pa_regressor`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.651012 |
| lin_lr_0_001 | 0.575832 |
| lin_lr_0_002 | 0.608665 |
| pa_regressor | 0.669957 |

- best_fixed_strategy: `pa_regressor`
- best_fixed_score: `0.669957`
- adaptive_delta_vs_best_fixed: `-0.018945`
- block_delta_mean: `-0.019971`
- block_delta_ci95: `0.056416`
- block_count: `10`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 47 | stay | lin_lr_0_001 | lin_lr_0_001 | 0.000000 | 0.002000 | recent_leader_warmup_same |
| 71 | stay | lin_lr_0_001 | lin_lr_0_002 | 0.000251 | 0.002000 | recent_leader_margin_too_small |
| 95 | switch | lin_lr_0_001 | lin_lr_0_002 | 0.004886 | 0.002000 | recent_leader_advantage |
| 119 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.002000 | recent_leader_cooldown |
| 143 | switch | lin_lr_0_002 | pa_regressor | 0.094945 | 0.002000 | recent_leader_advantage |
| 167 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_cooldown |
| 191 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 215 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 239 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
