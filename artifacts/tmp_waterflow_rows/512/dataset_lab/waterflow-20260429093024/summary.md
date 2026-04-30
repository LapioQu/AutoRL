# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `509`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_001`
- final_strategy: `pa_regressor`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.780817 |
| lin_lr_0_001 | 0.731759 |
| lin_lr_0_002 | 0.754601 |
| pa_regressor | 0.794574 |

- best_fixed_strategy: `pa_regressor`
- best_fixed_score: `0.794574`
- adaptive_delta_vs_best_fixed: `-0.013758`
- block_delta_mean: `-0.013894`
- block_delta_ci95: `0.032297`
- block_count: `21`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 47 | stay | lin_lr_0_001 | lin_lr_0_001 | 0.000000 | 0.002000 | recent_leader_warmup_same |
| 71 | stay | lin_lr_0_001 | lin_lr_0_002 | 0.000301 | 0.002000 | recent_leader_margin_too_small |
| 95 | switch | lin_lr_0_001 | lin_lr_0_002 | 0.005705 | 0.002000 | recent_leader_advantage |
| 119 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.002000 | recent_leader_cooldown |
| 143 | switch | lin_lr_0_002 | pa_regressor | 0.116917 | 0.002000 | recent_leader_advantage |
| 167 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_cooldown |
| 191 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 215 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 239 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 263 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 287 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 311 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 335 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 359 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 383 | stay | pa_regressor | lin_lr_0_002 | 0.006905 | 0.002000 | recent_leader_incumbent_floor |
| 407 | stay | pa_regressor | lin_lr_0_002 | 0.008890 | 0.002000 | recent_leader_incumbent_floor |
| 431 | stay | pa_regressor | lin_lr_0_002 | 0.012355 | 0.002000 | recent_leader_incumbent_floor |
| 455 | stay | pa_regressor | lin_lr_0_002 | 0.014819 | 0.002000 | recent_leader_incumbent_floor |
| 479 | stay | pa_regressor | lin_lr_0_002 | 0.011148 | 0.002000 | recent_leader_incumbent_floor |
| 503 | stay | pa_regressor | lin_lr_0_002 | 0.011707 | 0.002000 | recent_leader_incumbent_floor |
