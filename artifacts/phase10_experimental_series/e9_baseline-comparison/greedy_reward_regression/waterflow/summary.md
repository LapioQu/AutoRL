# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `1268`
- source: Real pipeline water-flow stream replayed in temporal order; evaluation includes anomalous low-flow segments and a pumping-induced peak.
- source_url: ``
- start_strategy: `pa_regressor`
- final_strategy: `lin_lr_0_001`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.803759 |
| lin_lr_0_0005 | 0.802089 |
| lin_lr_0_001 | 0.803945 |
| pa_regressor | 0.726507 |

- best_fixed_strategy: `lin_lr_0_001`
- best_fixed_score: `0.803945`
- adaptive_delta_vs_best_fixed: `-0.000186`
- block_delta_mean: `-0.000189`
- block_delta_ci95: `0.039127`
- block_count: `52`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 23 | stay | pa_regressor | pa_regressor | 0.000000 | 0.000000 | recent_leader_warmup_same |
| 47 | stay | pa_regressor | pa_regressor | 0.000000 | 0.000000 | recent_leader_same |
| 71 | stay | pa_regressor | pa_regressor | 0.000000 | 0.000000 | recent_leader_same |
| 95 | stay | pa_regressor | pa_regressor | 0.000000 | 0.000000 | recent_leader_same |
| 119 | stay | pa_regressor | pa_regressor | 0.000000 | 0.000000 | recent_leader_same |
| 143 | stay | pa_regressor | pa_regressor | 0.000000 | 0.000000 | recent_leader_same |
| 167 | stay | pa_regressor | pa_regressor | 0.000000 | 0.000000 | recent_leader_same |
| 191 | stay | pa_regressor | lin_lr_0_0005 | 0.182490 | 0.000000 | recent_leader_incumbent_floor |
| 215 | stay | pa_regressor | lin_lr_0_001 | 0.110526 | 0.000000 | recent_leader_incumbent_floor |
| 239 | stay | pa_regressor | pa_regressor | 0.000000 | 0.000000 | recent_leader_same |
| 263 | stay | pa_regressor | pa_regressor | 0.000000 | 0.000000 | recent_leader_same |
| 287 | stay | pa_regressor | lin_lr_0_001 | 0.126235 | 0.000000 | recent_leader_incumbent_floor |
| 311 | stay | pa_regressor | lin_lr_0_001 | 0.222381 | 0.000000 | recent_leader_incumbent_floor |
| 335 | stay | pa_regressor | lin_lr_0_001 | 0.178121 | 0.000000 | recent_leader_incumbent_floor |
| 359 | stay | pa_regressor | lin_lr_0_0005 | 0.151886 | 0.000000 | recent_leader_incumbent_floor |
| 383 | stay | pa_regressor | lin_lr_0_0005 | 0.190357 | 0.000000 | recent_leader_incumbent_floor |
| 407 | stay | pa_regressor | lin_lr_0_001 | 0.181718 | 0.000000 | recent_leader_incumbent_floor |
| 431 | stay | pa_regressor | lin_lr_0_001 | 0.160769 | 0.000000 | recent_leader_incumbent_floor |
| 455 | stay | pa_regressor | lin_lr_0_0005 | 0.150106 | 0.000000 | recent_leader_incumbent_floor |
| 479 | stay | pa_regressor | lin_lr_0_0005 | 0.138383 | 0.000000 | recent_leader_incumbent_floor |

... truncated 32 additional decision rows in `decisions.csv`.
