# Real-Stream Benchmark Replay

- dataset: `Bikes calibration`
- score_name: `normalized_reward`
- policy_name: `hedge_portfolio`
- samples: `40142`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_0001`
- final_strategy: `lin_lr_0_001`
- switch_count: `8`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.680210 |
| lin_lr_0_0001 | 0.679432 |
| lin_lr_0_0005 | 0.679727 |
| lin_lr_0_001 | 0.680266 |
| lin_lr_0_002 | 0.680713 |
| tree_regressor | 0.695042 |

- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.695042`
- adaptive_delta_vs_best_fixed: `-0.014832`
- block_delta_mean: `-0.014808`
- block_delta_ci95: `0.009181`
- block_count: `627`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | switch | lin_lr_0_0001 | lin_lr_0_002 | 0.012134 | 0.010000 | hedge_weight_advantage |
| 127 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | hedge_same_leader |
| 191 | switch | lin_lr_0_002 | tree_regressor | 0.031427 | 0.010000 | hedge_weight_advantage |
| 255 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 319 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 383 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 447 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 511 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 575 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 639 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 703 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 767 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 831 | switch | tree_regressor | lin_lr_0_0005 | 0.104905 | 0.010000 | hedge_weight_advantage |
| 895 | stay | lin_lr_0_0005 | lin_lr_0_0005 | 0.000000 | 0.010000 | hedge_same_leader |
| 959 | stay | lin_lr_0_0005 | lin_lr_0_0005 | 0.000000 | 0.010000 | hedge_same_leader |
| 1023 | switch | lin_lr_0_0005 | lin_lr_0_001 | 0.016455 | 0.010000 | hedge_weight_advantage |
| 1087 | stay | lin_lr_0_001 | lin_lr_0_001 | 0.000000 | 0.010000 | hedge_same_leader |
| 1151 | stay | lin_lr_0_001 | lin_lr_0_001 | 0.000000 | 0.010000 | hedge_same_leader |
| 1215 | switch | lin_lr_0_001 | lin_lr_0_0005 | 0.018403 | 0.010000 | hedge_weight_advantage |
| 1279 | stay | lin_lr_0_0005 | lin_lr_0_0005 | 0.000000 | 0.010000 | hedge_same_leader |

... truncated 607 additional decision rows in `decisions.csv`.
