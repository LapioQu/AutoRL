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
| adaptive | 0.806041 |
| oracle | 0.874010 |
| lin_lr_0_0005 | 0.802089 |
| lin_lr_0_001 | 0.803945 |
| pa_regressor | 0.726507 |

- best_fixed_strategy: `lin_lr_0_001`
- best_fixed_score: `0.803945`
- oracle_score: `0.874010`
- oracle_gain: `0.070065`
- oracle_capture_ratio: `0.029925`
- adaptive_delta_vs_best_fixed: `0.002097`
- block_delta_mean: `0.002130`
- block_delta_ci95: `0.038776`
- block_count: `52`

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
| 431 | stay | pa_regressor | lin_lr_0_0005 | 0.175284 | 0.003000 | high_uncertainty |
| 455 | stay | pa_regressor | lin_lr_0_001 | 0.162642 | 0.003000 | high_uncertainty |
| 479 | stay | pa_regressor | lin_lr_0_0005 | 0.149730 | 0.003000 | high_uncertainty |
| 503 | stay | pa_regressor | lin_lr_0_0005 | 0.137137 | 0.003000 | high_uncertainty |
| 527 | stay | pa_regressor | lin_lr_0_0005 | 0.131486 | 0.003000 | high_uncertainty |

... truncated 30 additional decision rows in `decisions.csv`.
