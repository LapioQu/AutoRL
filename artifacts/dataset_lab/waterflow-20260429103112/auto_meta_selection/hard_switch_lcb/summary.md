# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `256`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `pa_regressor`
- final_strategy: `pa_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.697019 |
| lin_lr_0_0005 | 0.534182 |
| lin_lr_0_001 | 0.547883 |
| pa_regressor | 0.697019 |

- best_fixed_strategy: `pa_regressor`
- best_fixed_score: `0.697019`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `10`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 71 | stay | pa_regressor | lin_lr_0_001 | -0.290948 | 0.003000 | high_uncertainty |
| 95 | stay | pa_regressor | lin_lr_0_001 | -0.368823 | 0.003000 | high_uncertainty |
| 119 | stay | pa_regressor | lin_lr_0_001 | -0.245933 | 0.003000 | high_uncertainty |
| 143 | stay | pa_regressor | lin_lr_0_001 | -0.149248 | 0.003000 | high_uncertainty |
| 167 | stay | pa_regressor | lin_lr_0_001 | -0.187229 | 0.003000 | high_uncertainty |
| 191 | stay | pa_regressor | lin_lr_0_001 | -0.120443 | 0.003000 | high_uncertainty |
| 215 | stay | pa_regressor | lin_lr_0_001 | 0.047452 | 0.003000 | high_uncertainty |
| 239 | stay | pa_regressor | lin_lr_0_001 | 0.037007 | 0.003000 | high_uncertainty |
