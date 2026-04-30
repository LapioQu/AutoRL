# Real-Stream Benchmark Replay

- dataset: `Bikes calibration`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `879`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_0005`
- final_strategy: `lin_lr_0_0005`
- switch_count: `5`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.759065 |
| lin_lr_0_0005 | 0.737649 |
| lin_lr_0_001 | 0.737386 |
| lin_lr_0_002 | 0.735688 |
| tree_regressor | 0.754458 |

- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.754458`
- adaptive_delta_vs_best_fixed: `0.004607`
- block_delta_mean: `0.002355`
- block_delta_ci95: `0.018742`
- block_count: `13`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | switch | lin_lr_0_0005 | lin_lr_0_002 | 0.010893 | 0.010000 | fixed_share_weight_advantage |
| 127 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | switch | lin_lr_0_002 | tree_regressor | 0.364595 | 0.010000 | fixed_share_weight_advantage |
| 255 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 319 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 383 | switch | tree_regressor | lin_lr_0_0005 | 0.080003 | 0.010000 | fixed_share_weight_advantage |
| 447 | switch | lin_lr_0_0005 | tree_regressor | 0.202335 | 0.010000 | fixed_share_weight_advantage |
| 511 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 575 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 639 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 703 | stay | tree_regressor | tree_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 767 | switch | tree_regressor | lin_lr_0_0005 | 0.085666 | 0.010000 | fixed_share_weight_advantage |
| 831 | stay | lin_lr_0_0005 | lin_lr_0_0005 | 0.000000 | 0.010000 | fixed_share_same_leader |
