# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `408`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `pa_regressor`
- final_strategy: `pa_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.656879 |
| lin_lr_0_0005 | 0.589506 |
| lin_lr_0_001 | 0.601602 |
| pa_regressor | 0.656879 |

- best_fixed_strategy: `pa_regressor`
- best_fixed_score: `0.656879`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `17`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 71 | stay | pa_regressor | lin_lr_0_001 | -0.313963 | 0.003000 | high_uncertainty |
| 95 | stay | pa_regressor | lin_lr_0_001 | -0.423889 | 0.003000 | high_uncertainty |
| 119 | stay | pa_regressor | lin_lr_0_001 | -0.295249 | 0.003000 | high_uncertainty |
| 143 | stay | pa_regressor | lin_lr_0_001 | -0.175735 | 0.003000 | high_uncertainty |
| 167 | stay | pa_regressor | lin_lr_0_001 | -0.224606 | 0.003000 | high_uncertainty |
| 191 | stay | pa_regressor | lin_lr_0_001 | -0.160760 | 0.003000 | high_uncertainty |
| 215 | stay | pa_regressor | lin_lr_0_001 | 0.039271 | 0.003000 | high_uncertainty |
| 239 | stay | pa_regressor | lin_lr_0_001 | 0.040332 | 0.003000 | high_uncertainty |
| 263 | stay | pa_regressor | lin_lr_0_001 | -0.125568 | 0.003000 | high_uncertainty |
| 287 | stay | pa_regressor | lin_lr_0_001 | -0.126015 | 0.003000 | high_uncertainty |
| 311 | stay | pa_regressor | lin_lr_0_001 | 0.064730 | 0.003000 | high_uncertainty |
| 335 | stay | pa_regressor | lin_lr_0_001 | 0.187279 | 0.003000 | high_uncertainty |
| 359 | stay | pa_regressor | lin_lr_0_001 | 0.177154 | 0.003000 | high_uncertainty |
| 383 | stay | pa_regressor | lin_lr_0_0005 | 0.165334 | 0.003000 | high_uncertainty |
| 407 | stay | pa_regressor | lin_lr_0_0005 | 0.176957 | 0.003000 | high_uncertainty |
