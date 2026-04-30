# Real-Stream Benchmark Replay

- dataset: `Bikes calibration`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `40142`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_0001`
- final_strategy: `tree_regressor`
- switch_count: `26`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.695551 |
| lin_lr_0_0001 | 0.679432 |
| lin_lr_0_0005 | 0.679727 |
| lin_lr_0_001 | 0.680266 |
| lin_lr_0_002 | 0.680713 |
| tree_regressor | 0.695042 |

- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.695042`
- adaptive_delta_vs_best_fixed: `0.000510`
- block_delta_mean: `0.000510`
- block_delta_ci95: `0.004923`
- block_count: `627`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | lin_lr_0_0001 | lin_lr_0_002 |  | 0.001000 | recent_leader_warmup |
| 191 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.001000 | recent_leader_cooldown |
| 255 | switch | lin_lr_0_002 | tree_regressor | 0.095429 | 0.001000 | recent_leader_advantage |
| 319 | stay | tree_regressor | tree_regressor | 0.000000 | 0.001000 | recent_leader_cooldown |
| 383 | stay | tree_regressor | tree_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 447 | stay | tree_regressor | tree_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 511 | stay | tree_regressor | tree_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 575 | stay | tree_regressor | tree_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 639 | stay | tree_regressor | lin_lr_0_001 | 0.087998 | 0.001000 | recent_leader_incumbent_floor |
| 703 | stay | tree_regressor | lin_lr_0_001 | 0.074060 | 0.001000 | recent_leader_incumbent_floor |
| 767 | stay | tree_regressor | lin_lr_0_0005 | 0.026006 | 0.001000 | recent_leader_incumbent_floor |
| 831 | switch | tree_regressor | lin_lr_0_0005 | 0.069084 | 0.001000 | recent_leader_advantage |
| 895 | stay | lin_lr_0_0005 | lin_lr_0_0005 | 0.000000 | 0.001000 | recent_leader_cooldown |
| 959 | stay | lin_lr_0_0005 | lin_lr_0_0005 | 0.000000 | 0.001000 | recent_leader_same |
| 1023 | stay | lin_lr_0_0005 | lin_lr_0_002 | 0.004983 | 0.001000 | recent_leader_incumbent_floor |
| 1087 | stay | lin_lr_0_0005 | lin_lr_0_002 | 0.006283 | 0.001000 | recent_leader_incumbent_floor |
| 1151 | switch | lin_lr_0_0005 | lin_lr_0_002 | 0.001841 | 0.001000 | recent_leader_advantage |
| 1215 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.001000 | recent_leader_cooldown |
| 1279 | switch | lin_lr_0_002 | lin_lr_0_0001 | 0.006297 | 0.001000 | recent_leader_advantage |
| 1343 | stay | lin_lr_0_0001 | lin_lr_0_0001 | 0.000000 | 0.001000 | recent_leader_cooldown |

... truncated 606 additional decision rows in `decisions.csv`.
