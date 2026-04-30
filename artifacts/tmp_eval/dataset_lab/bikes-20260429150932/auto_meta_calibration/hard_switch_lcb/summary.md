# Real-Stream Benchmark Replay

- dataset: `Bikes calibration`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `879`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_0001`
- final_strategy: `lin_lr_0_0001`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.736289 |
| lin_lr_0_0001 | 0.736289 |
| lin_lr_0_0005 | 0.737649 |
| lin_lr_0_001 | 0.737386 |
| lin_lr_0_002 | 0.735688 |
| tree_regressor | 0.753647 |

- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.753647`
- adaptive_delta_vs_best_fixed: `-0.017357`
- block_delta_mean: `-0.020659`
- block_delta_ci95: `0.029648`
- block_count: `13`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 191 | stay | lin_lr_0_0001 | lin_lr_0_002 | 0.005031 | 0.003000 | high_uncertainty |
| 255 | stay | lin_lr_0_0001 | tree_regressor | 0.053168 | 0.003000 | high_uncertainty |
| 319 | stay | lin_lr_0_0001 | tree_regressor | 0.089867 | 0.003000 | high_uncertainty |
| 383 | stay | lin_lr_0_0001 | tree_regressor | 0.050045 | 0.003000 | high_uncertainty |
| 447 | stay | lin_lr_0_0001 | tree_regressor | 0.011170 | 0.003000 | high_uncertainty |
| 511 | stay | lin_lr_0_0001 | tree_regressor | 0.033823 | 0.003000 | high_uncertainty |
| 575 | stay | lin_lr_0_0001 | tree_regressor | 0.056082 | 0.003000 | high_uncertainty |
| 639 | stay | lin_lr_0_0001 | tree_regressor | 0.038113 | 0.003000 | high_uncertainty |
| 703 | stay | lin_lr_0_0001 | tree_regressor | 0.020967 | 0.003000 | high_uncertainty |
| 767 | stay | lin_lr_0_0001 | tree_regressor | 0.024255 | 0.003000 | high_uncertainty |
| 831 | stay | lin_lr_0_0001 | lin_lr_0_0005 | 0.002368 | 0.003000 | high_uncertainty |
