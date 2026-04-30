# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `253`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_001`
- final_strategy: `lin_lr_0_001`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.575832 |
| lin_lr_0_001 | 0.575832 |
| lin_lr_0_002 | 0.608665 |
| pa_regressor | 0.669957 |

- best_fixed_strategy: `pa_regressor`
- best_fixed_score: `0.669957`
- adaptive_delta_vs_best_fixed: `-0.094125`
- block_delta_mean: `-0.094680`
- block_delta_ci95: `0.072680`
- block_count: `10`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 71 | stay | lin_lr_0_001 | lin_lr_0_002 | 0.000344 | 0.003000 | high_uncertainty |
| 95 | stay | lin_lr_0_001 | lin_lr_0_002 | 0.003957 | 0.003000 | high_uncertainty |
| 119 | stay | lin_lr_0_001 | lin_lr_0_002 | 0.028707 | 0.003000 | high_uncertainty |
| 143 | stay | lin_lr_0_001 | pa_regressor | 0.127759 | 0.003000 | high_uncertainty |
| 167 | stay | lin_lr_0_001 | pa_regressor | 0.246470 | 0.003000 | high_uncertainty |
| 191 | stay | lin_lr_0_001 | pa_regressor | 0.241902 | 0.003000 | high_uncertainty |
| 215 | stay | lin_lr_0_001 | pa_regressor | 0.165402 | 0.003000 | high_uncertainty |
| 239 | stay | lin_lr_0_001 | pa_regressor | 0.120917 | 0.003000 | high_uncertainty |
