# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `1265`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_001`
- final_strategy: `lin_lr_0_001`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.859351 |
| lin_lr_0_001 | 0.859619 |
| lin_lr_0_002 | 0.869416 |
| pa_regressor | 0.873952 |

- best_fixed_strategy: `pa_regressor`
- best_fixed_score: `0.873952`
- adaptive_delta_vs_best_fixed: `-0.014601`
- block_delta_mean: `-0.015075`
- block_delta_ci95: `0.025540`
- block_count: `52`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 71 | stay | lin_lr_0_001 | lin_lr_0_002 | 0.000370 | 0.003000 | high_uncertainty |
| 95 | stay | lin_lr_0_001 | lin_lr_0_002 | 0.004870 | 0.003000 | high_uncertainty |
| 119 | stay | lin_lr_0_001 | pa_regressor | 0.036290 | 0.003000 | high_uncertainty |
| 143 | stay | lin_lr_0_001 | pa_regressor | 0.161831 | 0.003000 | high_uncertainty |
| 167 | stay | lin_lr_0_001 | pa_regressor | 0.325630 | 0.003000 | high_uncertainty |
| 191 | stay | lin_lr_0_001 | pa_regressor | 0.334941 | 0.003000 | high_uncertainty |
| 215 | stay | lin_lr_0_001 | pa_regressor | 0.237466 | 0.003000 | high_uncertainty |
| 239 | stay | lin_lr_0_001 | pa_regressor | 0.173784 | 0.003000 | high_uncertainty |
| 263 | stay | lin_lr_0_001 | pa_regressor | 0.149601 | 0.003000 | high_uncertainty |
| 287 | stay | lin_lr_0_001 | pa_regressor | 0.123423 | 0.003000 | high_uncertainty |
| 311 | stay | lin_lr_0_001 | pa_regressor | 0.081229 | 0.003000 | high_uncertainty |
| 335 | stay | lin_lr_0_001 | pa_regressor | 0.040672 | 0.003000 | high_uncertainty |
| 359 | stay | lin_lr_0_001 | lin_lr_0_002 | 0.011996 | 0.003000 | high_uncertainty |
| 383 | stay | lin_lr_0_001 | lin_lr_0_002 | 0.006116 | 0.003000 | high_uncertainty |
| 407 | stay | lin_lr_0_001 | lin_lr_0_002 | 0.004217 | 0.003000 | high_uncertainty |
| 431 | stay | lin_lr_0_001 | lin_lr_0_002 | 0.001689 | 0.003000 | high_uncertainty |
| 455 | stay | lin_lr_0_001 | lin_lr_0_002 | -0.000132 | 0.003000 | no_candidate_improvement |
| 479 | stay | lin_lr_0_001 | lin_lr_0_002 | 0.000993 | 0.003000 | high_uncertainty |
| 503 | stay | lin_lr_0_001 | lin_lr_0_002 | 0.001024 | 0.003000 | no_candidate_improvement |
| 527 | stay | lin_lr_0_001 | lin_lr_0_002 | -0.001288 | 0.003000 | high_uncertainty |

... truncated 30 additional decision rows in `decisions.csv`.
