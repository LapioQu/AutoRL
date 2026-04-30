# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `1268`
- source: Real pipeline water-flow stream replayed in temporal order; evaluation includes anomalous low-flow segments and a pumping-induced peak.
- source_url: ``
- start_strategy: `tree_regressor`
- final_strategy: `lin_lr_0_001`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.763715 |
| lin_lr_0_001 | 0.803945 |
| pa_regressor | 0.726507 |
| tree_regressor | 0.723016 |

- best_fixed_strategy: `lin_lr_0_001`
- best_fixed_score: `0.803945`
- adaptive_delta_vs_best_fixed: `-0.040230`
- block_delta_mean: `-0.040875`
- block_delta_ci95: `0.061074`
- block_count: `52`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 71 | stay | tree_regressor | pa_regressor | -0.402020 | 0.003000 | high_uncertainty |
| 95 | stay | tree_regressor | pa_regressor | -0.190834 | 0.003000 | high_uncertainty |
| 119 | stay | tree_regressor | pa_regressor | -0.107023 | 0.003000 | high_uncertainty |
| 143 | stay | tree_regressor | pa_regressor | -0.000180 | 0.003000 | high_uncertainty |
| 167 | stay | tree_regressor | pa_regressor | 0.185568 | 0.003000 | high_uncertainty |
| 191 | stay | tree_regressor | pa_regressor | 0.254163 | 0.003000 | high_uncertainty |
| 215 | stay | tree_regressor | lin_lr_0_001 | 0.215900 | 0.003000 | high_uncertainty |
| 239 | stay | tree_regressor | lin_lr_0_001 | 0.201422 | 0.003000 | high_uncertainty |
| 263 | stay | tree_regressor | pa_regressor | 0.208745 | 0.003000 | high_uncertainty |
| 287 | stay | tree_regressor | pa_regressor | 0.194028 | 0.003000 | high_uncertainty |
| 311 | stay | tree_regressor | lin_lr_0_001 | 0.169182 | 0.003000 | high_uncertainty |
| 335 | stay | tree_regressor | lin_lr_0_001 | 0.241670 | 0.003000 | high_uncertainty |
| 359 | stay | tree_regressor | lin_lr_0_001 | 0.243785 | 0.003000 | high_uncertainty |
| 383 | stay | tree_regressor | lin_lr_0_001 | 0.232489 | 0.003000 | high_uncertainty |
| 407 | stay | tree_regressor | lin_lr_0_001 | 0.256213 | 0.003000 | high_uncertainty |
| 431 | stay | tree_regressor | lin_lr_0_001 | 0.262607 | 0.003000 | high_uncertainty |
| 455 | stay | tree_regressor | lin_lr_0_001 | 0.230358 | 0.003000 | high_uncertainty |
| 479 | stay | tree_regressor | lin_lr_0_001 | 0.198037 | 0.003000 | high_uncertainty |
| 503 | stay | tree_regressor | lin_lr_0_001 | 0.182471 | 0.003000 | high_uncertainty |
| 527 | stay | tree_regressor | lin_lr_0_001 | 0.166957 | 0.003000 | high_uncertainty |

... truncated 30 additional decision rows in `decisions.csv`.
