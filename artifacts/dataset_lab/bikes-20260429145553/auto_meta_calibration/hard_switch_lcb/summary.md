# Real-Stream Benchmark Replay

- dataset: `Bikes calibration`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `879`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_0005`
- final_strategy: `lin_lr_0_0005`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.737649 |
| lin_lr_0_0005 | 0.737649 |
| lin_lr_0_001 | 0.737386 |
| lin_lr_0_002 | 0.735688 |
| tree_regressor | 0.754458 |

- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.754458`
- adaptive_delta_vs_best_fixed: `-0.016809`
- block_delta_mean: `-0.020271`
- block_delta_ci95: `0.030781`
- block_count: `13`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 191 | stay | lin_lr_0_0005 | lin_lr_0_002 | 0.003841 | 0.003000 | high_uncertainty |
| 255 | stay | lin_lr_0_0005 | tree_regressor | 0.063675 | 0.003000 | high_uncertainty |
| 319 | stay | lin_lr_0_0005 | tree_regressor | 0.094569 | 0.003000 | high_uncertainty |
| 383 | stay | lin_lr_0_0005 | tree_regressor | 0.041868 | 0.003000 | high_uncertainty |
| 447 | stay | lin_lr_0_0005 | tree_regressor | -0.001702 | 0.003000 | high_uncertainty |
| 511 | stay | lin_lr_0_0005 | tree_regressor | 0.025127 | 0.003000 | high_uncertainty |
| 575 | stay | lin_lr_0_0005 | tree_regressor | 0.055811 | 0.003000 | high_uncertainty |
| 639 | stay | lin_lr_0_0005 | tree_regressor | 0.043450 | 0.003000 | high_uncertainty |
| 703 | stay | lin_lr_0_0005 | tree_regressor | 0.024173 | 0.003000 | high_uncertainty |
| 767 | stay | lin_lr_0_0005 | tree_regressor | 0.022518 | 0.003000 | high_uncertainty |
| 831 | stay | lin_lr_0_0005 | lin_lr_0_001 | -0.001502 | 0.003000 | high_uncertainty |
