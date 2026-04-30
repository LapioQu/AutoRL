# Real-Stream Benchmark Replay

- dataset: `Bikes calibration`
- score_name: `normalized_reward`
- policy_name: `hedge_portfolio`
- samples: `879`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_0005`
- final_strategy: `tree_regressor`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.754146 |
| lin_lr_0_0005 | 0.737649 |
| lin_lr_0_001 | 0.737386 |
| lin_lr_0_002 | 0.735688 |
| tree_regressor | 0.754458 |

- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.754458`
- adaptive_delta_vs_best_fixed: `-0.000312`
- block_delta_mean: `-0.000330`
- block_delta_ci95: `0.012739`
- block_count: `13`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | switch | lin_lr_0_0005 | lin_lr_0_002 | 0.012261 | 0.010000 | hedge_weight_advantage |
| 127 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | hedge_same_leader |
| 191 | switch | lin_lr_0_002 | tree_regressor | 0.023832 | 0.010000 | hedge_weight_advantage |
| 255 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 319 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 383 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 447 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 511 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 575 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 639 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 703 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 767 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 831 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | hedge_same_leader |
