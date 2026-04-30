# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `1268`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `tree_regressor`
- final_strategy: `tree_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.863013 |
| lin_lr_0_001 | 0.792031 |
| lin_lr_0_002 | 0.792031 |
| tree_regressor | 0.863013 |

- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.863013`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `52`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 71 | stay | tree_regressor | lin_lr_0_002 | -0.740571 | 0.003000 | high_uncertainty |
| 95 | stay | tree_regressor | lin_lr_0_002 | -0.657960 | 0.003000 | high_uncertainty |
| 119 | stay | tree_regressor | lin_lr_0_002 | -0.425337 | 0.003000 | high_uncertainty |
| 143 | stay | tree_regressor | lin_lr_0_002 | -0.158884 | 0.003000 | high_uncertainty |
| 167 | stay | tree_regressor | lin_lr_0_002 | -0.091806 | 0.003000 | high_uncertainty |
| 191 | stay | tree_regressor | lin_lr_0_002 | -0.127920 | 0.003000 | high_uncertainty |
| 215 | stay | tree_regressor | lin_lr_0_002 | -0.130963 | 0.003000 | high_uncertainty |
| 239 | stay | tree_regressor | lin_lr_0_002 | -0.088981 | 0.003000 | high_uncertainty |
| 263 | stay | tree_regressor | lin_lr_0_002 | -0.039625 | 0.003000 | high_uncertainty |
| 287 | stay | tree_regressor | lin_lr_0_002 | -0.030071 | 0.003000 | high_uncertainty |
| 311 | stay | tree_regressor | lin_lr_0_002 | -0.034029 | 0.003000 | high_uncertainty |
| 335 | stay | tree_regressor | lin_lr_0_002 | -0.048286 | 0.003000 | high_uncertainty |
| 359 | stay | tree_regressor | lin_lr_0_002 | -0.046182 | 0.003000 | high_uncertainty |
| 383 | stay | tree_regressor | lin_lr_0_002 | -0.023072 | 0.003000 | high_uncertainty |
| 407 | stay | tree_regressor | lin_lr_0_002 | -0.016292 | 0.003000 | high_uncertainty |
| 431 | stay | tree_regressor | lin_lr_0_002 | -0.011443 | 0.003000 | high_uncertainty |
| 455 | stay | tree_regressor | lin_lr_0_002 | -0.001314 | 0.003000 | no_candidate_improvement |
| 479 | stay | tree_regressor | lin_lr_0_002 | 0.000291 | 0.003000 | high_uncertainty |
| 503 | stay | tree_regressor | lin_lr_0_002 | -0.001115 | 0.003000 | high_uncertainty |
| 527 | stay | tree_regressor | lin_lr_0_002 | -0.000873 | 0.003000 | high_uncertainty |

... truncated 30 additional decision rows in `decisions.csv`.
