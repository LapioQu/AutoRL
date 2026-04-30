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
| adaptive | 0.863475 |
| lin_lr_0_001 | 0.792031 |
| lin_lr_0_002 | 0.792031 |
| tree_regressor | 0.863475 |

- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.863475`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `52`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 71 | stay | tree_regressor | lin_lr_0_002 | -0.740908 | 0.003000 | high_uncertainty |
| 95 | stay | tree_regressor | lin_lr_0_002 | -0.658177 | 0.003000 | high_uncertainty |
| 119 | stay | tree_regressor | lin_lr_0_002 | -0.426995 | 0.003000 | high_uncertainty |
| 143 | stay | tree_regressor | lin_lr_0_002 | -0.163425 | 0.003000 | high_uncertainty |
| 167 | stay | tree_regressor | lin_lr_0_002 | -0.096677 | 0.003000 | high_uncertainty |
| 191 | stay | tree_regressor | lin_lr_0_002 | -0.107266 | 0.003000 | high_uncertainty |
| 215 | stay | tree_regressor | lin_lr_0_002 | -0.078973 | 0.003000 | high_uncertainty |
| 239 | stay | tree_regressor | lin_lr_0_002 | -0.056492 | 0.003000 | high_uncertainty |
| 263 | stay | tree_regressor | lin_lr_0_002 | -0.043837 | 0.003000 | high_uncertainty |
| 287 | stay | tree_regressor | lin_lr_0_002 | -0.059289 | 0.003000 | high_uncertainty |
| 311 | stay | tree_regressor | lin_lr_0_002 | -0.080590 | 0.003000 | high_uncertainty |
| 335 | stay | tree_regressor | lin_lr_0_002 | -0.080539 | 0.003000 | high_uncertainty |
| 359 | stay | tree_regressor | lin_lr_0_002 | -0.055057 | 0.003000 | high_uncertainty |
| 383 | stay | tree_regressor | lin_lr_0_002 | -0.023003 | 0.003000 | high_uncertainty |
| 407 | stay | tree_regressor | lin_lr_0_002 | -0.012878 | 0.003000 | high_uncertainty |
| 431 | stay | tree_regressor | lin_lr_0_002 | -0.009016 | 0.003000 | high_uncertainty |
| 455 | stay | tree_regressor | lin_lr_0_002 | -0.001092 | 0.003000 | no_candidate_improvement |
| 479 | stay | tree_regressor | lin_lr_0_002 | 0.000736 | 0.003000 | high_uncertainty |
| 503 | stay | tree_regressor | lin_lr_0_002 | -0.000625 | 0.003000 | high_uncertainty |
| 527 | stay | tree_regressor | lin_lr_0_002 | -0.001185 | 0.003000 | high_uncertainty |

... truncated 30 additional decision rows in `decisions.csv`.
