# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `256`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `tree_regressor`
- final_strategy: `tree_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.746937 |
| lin_lr_0_001 | 0.507672 |
| lin_lr_0_002 | 0.507672 |
| tree_regressor | 0.746937 |

- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.746937`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `10`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 71 | stay | tree_regressor | lin_lr_0_002 | -0.654491 | 0.003000 | high_uncertainty |
| 95 | stay | tree_regressor | lin_lr_0_002 | -0.553000 | 0.003000 | high_uncertainty |
| 119 | stay | tree_regressor | lin_lr_0_002 | -0.336996 | 0.003000 | high_uncertainty |
| 143 | stay | tree_regressor | lin_lr_0_002 | -0.109383 | 0.003000 | high_uncertainty |
| 167 | stay | tree_regressor | lin_lr_0_002 | -0.040433 | 0.003000 | high_uncertainty |
| 191 | stay | tree_regressor | lin_lr_0_002 | -0.041107 | 0.003000 | high_uncertainty |
| 215 | stay | tree_regressor | lin_lr_0_002 | -0.039797 | 0.003000 | high_uncertainty |
| 239 | stay | tree_regressor | lin_lr_0_002 | -0.045576 | 0.003000 | high_uncertainty |
