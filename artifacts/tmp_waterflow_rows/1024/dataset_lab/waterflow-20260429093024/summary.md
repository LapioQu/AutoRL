# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `1021`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_001`
- final_strategy: `pa_regressor`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.853895 |
| lin_lr_0_001 | 0.839389 |
| lin_lr_0_002 | 0.851002 |
| pa_regressor | 0.861576 |

- best_fixed_strategy: `pa_regressor`
- best_fixed_score: `0.861576`
- adaptive_delta_vs_best_fixed: `-0.007680`
- block_delta_mean: `-0.007779`
- block_delta_ci95: `0.017299`
- block_count: `42`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 47 | stay | lin_lr_0_001 | lin_lr_0_001 | 0.000000 | 0.002000 | recent_leader_warmup_same |
| 71 | stay | lin_lr_0_001 | lin_lr_0_002 | 0.000310 | 0.002000 | recent_leader_margin_too_small |
| 95 | switch | lin_lr_0_001 | lin_lr_0_002 | 0.005955 | 0.002000 | recent_leader_advantage |
| 119 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.002000 | recent_leader_cooldown |
| 143 | switch | lin_lr_0_002 | pa_regressor | 0.125332 | 0.002000 | recent_leader_advantage |
| 167 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_cooldown |
| 191 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 215 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 239 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 263 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 287 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 311 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 335 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 359 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 383 | stay | pa_regressor | lin_lr_0_002 | 0.007650 | 0.002000 | recent_leader_incumbent_floor |
| 407 | stay | pa_regressor | lin_lr_0_002 | 0.009956 | 0.002000 | recent_leader_incumbent_floor |
| 431 | stay | pa_regressor | lin_lr_0_002 | 0.013824 | 0.002000 | recent_leader_incumbent_floor |
| 455 | stay | pa_regressor | lin_lr_0_002 | 0.016601 | 0.002000 | recent_leader_incumbent_floor |
| 479 | stay | pa_regressor | lin_lr_0_002 | 0.012499 | 0.002000 | recent_leader_incumbent_floor |
| 503 | stay | pa_regressor | lin_lr_0_002 | 0.013107 | 0.002000 | recent_leader_incumbent_floor |

... truncated 21 additional decision rows in `decisions.csv`.
