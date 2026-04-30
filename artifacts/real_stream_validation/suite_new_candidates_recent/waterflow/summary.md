# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `1268`
- source: Real pipeline water-flow stream replayed in temporal order; evaluation includes anomalous low-flow segments and a pumping-induced peak.
- source_url: ``
- start_strategy: `sgd_lr_0_001`
- final_strategy: `sgd_lr_0_005`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.814846 |
| sgd_lr_0_0005 | 0.802089 |
| sgd_lr_0_001 | 0.803945 |
| sgd_lr_0_005 | 0.817426 |

- best_fixed_strategy: `sgd_lr_0_005`
- best_fixed_score: `0.817426`
- adaptive_delta_vs_best_fixed: `-0.002579`
- block_delta_mean: `-0.002621`
- block_delta_ci95: `0.004264`
- block_count: `52`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 47 | switch | sgd_lr_0_001 | sgd_lr_0_005 |  | 0.001000 | recent_leader_warmup |
| 71 | stay | sgd_lr_0_005 | sgd_lr_0_005 | 0.000000 | 0.001000 | recent_leader_cooldown |
| 95 | stay | sgd_lr_0_005 | sgd_lr_0_005 | 0.000000 | 0.001000 | recent_leader_same |
| 119 | stay | sgd_lr_0_005 | sgd_lr_0_005 | 0.000000 | 0.001000 | recent_leader_same |
| 143 | stay | sgd_lr_0_005 | sgd_lr_0_005 | 0.000000 | 0.001000 | recent_leader_same |
| 167 | stay | sgd_lr_0_005 | sgd_lr_0_005 | 0.000000 | 0.001000 | recent_leader_same |
| 191 | stay | sgd_lr_0_005 | sgd_lr_0_0005 | 0.003069 | 0.001000 | recent_leader_incumbent_floor |
| 215 | stay | sgd_lr_0_005 | sgd_lr_0_001 | 0.132101 | 0.001000 | recent_leader_incumbent_floor |
| 239 | stay | sgd_lr_0_005 | sgd_lr_0_001 | 0.073964 | 0.001000 | recent_leader_incumbent_floor |
| 263 | stay | sgd_lr_0_005 | sgd_lr_0_005 | 0.000000 | 0.001000 | recent_leader_same |
| 287 | stay | sgd_lr_0_005 | sgd_lr_0_005 | 0.000000 | 0.001000 | recent_leader_same |
| 311 | stay | sgd_lr_0_005 | sgd_lr_0_005 | 0.000000 | 0.001000 | recent_leader_same |
| 335 | stay | sgd_lr_0_005 | sgd_lr_0_005 | 0.000000 | 0.001000 | recent_leader_same |
| 359 | stay | sgd_lr_0_005 | sgd_lr_0_005 | 0.000000 | 0.001000 | recent_leader_same |
| 383 | stay | sgd_lr_0_005 | sgd_lr_0_0005 | 0.026722 | 0.001000 | recent_leader_incumbent_floor |
| 407 | stay | sgd_lr_0_005 | sgd_lr_0_0005 | 0.005856 | 0.001000 | recent_leader_incumbent_floor |
| 431 | stay | sgd_lr_0_005 | sgd_lr_0_001 | 0.002491 | 0.001000 | recent_leader_incumbent_floor |
| 455 | stay | sgd_lr_0_005 | sgd_lr_0_005 | 0.000000 | 0.001000 | recent_leader_same |
| 479 | stay | sgd_lr_0_005 | sgd_lr_0_005 | 0.000000 | 0.001000 | recent_leader_same |
| 503 | stay | sgd_lr_0_005 | sgd_lr_0_005 | 0.000000 | 0.001000 | recent_leader_same |

... truncated 31 additional decision rows in `decisions.csv`.
