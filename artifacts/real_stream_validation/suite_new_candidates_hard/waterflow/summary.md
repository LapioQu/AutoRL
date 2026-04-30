# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `1268`
- source: Real pipeline water-flow stream replayed in temporal order; evaluation includes anomalous low-flow segments and a pumping-induced peak.
- source_url: ``
- start_strategy: `sgd_lr_0_001`
- final_strategy: `sgd_lr_0_001`
- switch_count: `3`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.803869 |
| sgd_lr_0_0005 | 0.802089 |
| sgd_lr_0_001 | 0.803945 |
| sgd_lr_0_005 | 0.817426 |

- best_fixed_strategy: `sgd_lr_0_005`
- best_fixed_score: `0.817426`
- adaptive_delta_vs_best_fixed: `-0.013556`
- block_delta_mean: `-0.014126`
- block_delta_ci95: `0.017846`
- block_count: `52`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 71 | stay | sgd_lr_0_001 | sgd_lr_0_005 | 0.108978 | 0.003000 | high_uncertainty |
| 95 | stay | sgd_lr_0_001 | sgd_lr_0_005 | 0.163500 | 0.003000 | high_uncertainty |
| 119 | stay | sgd_lr_0_001 | sgd_lr_0_005 | 0.129051 | 0.003000 | high_uncertainty |
| 143 | stay | sgd_lr_0_001 | sgd_lr_0_005 | 0.060151 | 0.003000 | high_uncertainty |
| 167 | stay | sgd_lr_0_001 | sgd_lr_0_005 | 0.078380 | 0.003000 | high_uncertainty |
| 191 | stay | sgd_lr_0_001 | sgd_lr_0_005 | 0.060390 | 0.003000 | high_uncertainty |
| 215 | stay | sgd_lr_0_001 | sgd_lr_0_0005 | -0.012798 | 0.003000 | high_uncertainty |
| 239 | stay | sgd_lr_0_001 | sgd_lr_0_0005 | -0.042793 | 0.003000 | high_uncertainty |
| 263 | stay | sgd_lr_0_001 | sgd_lr_0_0005 | -0.027150 | 0.003000 | high_uncertainty |
| 287 | stay | sgd_lr_0_001 | sgd_lr_0_005 | 0.033759 | 0.003000 | high_uncertainty |
| 311 | stay | sgd_lr_0_001 | sgd_lr_0_005 | 0.074408 | 0.003000 | high_uncertainty |
| 335 | stay | sgd_lr_0_001 | sgd_lr_0_005 | 0.076265 | 0.003000 | high_uncertainty |
| 359 | stay | sgd_lr_0_001 | sgd_lr_0_005 | 0.046294 | 0.003000 | high_uncertainty |
| 383 | stay | sgd_lr_0_001 | sgd_lr_0_0005 | 0.011594 | 0.003000 | high_uncertainty |
| 407 | stay | sgd_lr_0_001 | sgd_lr_0_0005 | 0.010603 | 0.003000 | high_uncertainty |
| 431 | stay | sgd_lr_0_001 | sgd_lr_0_0005 | 0.000020 | 0.003000 | high_uncertainty |
| 455 | stay | sgd_lr_0_001 | sgd_lr_0_005 | 0.000375 | 0.003000 | high_uncertainty |
| 479 | stay | sgd_lr_0_001 | sgd_lr_0_005 | 0.010324 | 0.003000 | high_uncertainty |
| 503 | stay | sgd_lr_0_001 | sgd_lr_0_005 | 0.024214 | 0.003000 | high_uncertainty |
| 527 | stay | sgd_lr_0_001 | sgd_lr_0_005 | 0.028579 | 0.003000 | high_uncertainty |

... truncated 30 additional decision rows in `decisions.csv`.
