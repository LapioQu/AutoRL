# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `1268`
- source: Real pipeline water-flow stream replayed in temporal order; evaluation includes anomalous low-flow segments and a pumping-induced peak.
- source_url: ``
- start_strategy: `pa_regressor`
- final_strategy: `lin_lr_0_001`
- switch_count: `4`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.842475 |
| oracle | 0.897982 |
| lin_lr_0_0005 | 0.837308 |
| lin_lr_0_001 | 0.839073 |
| pa_regressor | 0.780066 |

- best_fixed_strategy: `lin_lr_0_001`
- best_fixed_score: `0.839073`
- oracle_score: `0.897982`
- oracle_gain: `0.058908`
- oracle_capture_ratio: `0.057751`
- adaptive_delta_vs_best_fixed: `0.003402`
- block_delta_mean: `0.003457`
- block_delta_ci95: `0.032911`
- block_count: `52`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 71 | stay | pa_regressor | lin_lr_0_001 | -0.281906 | 0.003000 | high_uncertainty |
| 95 | stay | pa_regressor | lin_lr_0_001 | -0.368667 | 0.003000 | high_uncertainty |
| 119 | stay | pa_regressor | lin_lr_0_001 | -0.251551 | 0.003000 | high_uncertainty |
| 143 | stay | pa_regressor | lin_lr_0_001 | -0.151090 | 0.003000 | high_uncertainty |
| 167 | stay | pa_regressor | lin_lr_0_001 | -0.191335 | 0.003000 | high_uncertainty |
| 191 | stay | pa_regressor | lin_lr_0_001 | -0.130575 | 0.003000 | high_uncertainty |
| 215 | stay | pa_regressor | lin_lr_0_001 | 0.040623 | 0.003000 | high_uncertainty |
| 239 | stay | pa_regressor | lin_lr_0_001 | 0.036160 | 0.003000 | high_uncertainty |
| 263 | stay | pa_regressor | lin_lr_0_001 | -0.104541 | 0.003000 | high_uncertainty |
| 287 | stay | pa_regressor | lin_lr_0_001 | -0.099190 | 0.003000 | high_uncertainty |
| 311 | stay | pa_regressor | lin_lr_0_001 | 0.062903 | 0.003000 | high_uncertainty |
| 335 | stay | pa_regressor | lin_lr_0_001 | 0.159191 | 0.003000 | high_uncertainty |
| 359 | stay | pa_regressor | lin_lr_0_001 | 0.144688 | 0.003000 | high_uncertainty |
| 383 | stay | pa_regressor | lin_lr_0_0005 | 0.133150 | 0.003000 | high_uncertainty |
| 407 | stay | pa_regressor | lin_lr_0_0005 | 0.140922 | 0.003000 | high_uncertainty |
| 431 | stay | pa_regressor | lin_lr_0_0005 | 0.137933 | 0.003000 | high_uncertainty |
| 455 | stay | pa_regressor | lin_lr_0_001 | 0.127478 | 0.003000 | high_uncertainty |
| 479 | stay | pa_regressor | lin_lr_0_0005 | 0.117648 | 0.003000 | high_uncertainty |
| 503 | stay | pa_regressor | lin_lr_0_0005 | 0.108077 | 0.003000 | high_uncertainty |
| 527 | stay | pa_regressor | lin_lr_0_0005 | 0.104293 | 0.003000 | high_uncertainty |

... truncated 30 additional decision rows in `decisions.csv`.
