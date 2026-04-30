# Real-Stream Benchmark Replay

- dataset: `Bikes calibration`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `879`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_0001`
- final_strategy: `tree_regressor`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.744264 |
| lin_lr_0_0001 | 0.736289 |
| lin_lr_0_0005 | 0.737649 |
| lin_lr_0_001 | 0.737386 |
| lin_lr_0_002 | 0.735688 |
| tree_regressor | 0.753647 |

- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.753647`
- adaptive_delta_vs_best_fixed: `-0.009382`
- block_delta_mean: `-0.009912`
- block_delta_ci95: `0.021008`
- block_count: `13`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | lin_lr_0_0001 | lin_lr_0_002 |  | 0.001000 | recent_leader_warmup |
| 191 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.001000 | recent_leader_cooldown |
| 255 | switch | lin_lr_0_002 | tree_regressor | 0.086987 | 0.001000 | recent_leader_advantage |
| 319 | stay | tree_regressor | tree_regressor | 0.000000 | 0.001000 | recent_leader_cooldown |
| 383 | stay | tree_regressor | tree_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 447 | stay | tree_regressor | tree_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 511 | stay | tree_regressor | tree_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 575 | stay | tree_regressor | tree_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 639 | stay | tree_regressor | tree_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 703 | stay | tree_regressor | tree_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 767 | stay | tree_regressor | tree_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 831 | stay | tree_regressor | lin_lr_0_0005 | 0.048566 | 0.001000 | recent_leader_incumbent_floor |
