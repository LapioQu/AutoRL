# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `1268`
- source: Real pipeline water-flow stream replayed in temporal order; evaluation includes anomalous low-flow segments and a pumping-induced peak.
- source_url: ``
- start_strategy: `tree_regressor`
- final_strategy: `lin_lr_0_001`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.803182 |
| lin_lr_0_001 | 0.803945 |
| pa_regressor | 0.726507 |
| tree_regressor | 0.747194 |

- best_fixed_strategy: `lin_lr_0_001`
- best_fixed_score: `0.803945`
- adaptive_delta_vs_best_fixed: `-0.000762`
- block_delta_mean: `-0.000775`
- block_delta_ci95: `0.056338`
- block_count: `52`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 47 | stay | tree_regressor | tree_regressor | 0.000000 | 0.002000 | recent_leader_warmup_same |
| 71 | stay | tree_regressor | tree_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 95 | stay | tree_regressor | tree_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 119 | stay | tree_regressor | tree_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 143 | stay | tree_regressor | pa_regressor | 0.026409 | 0.002000 | recent_leader_incumbent_floor |
| 167 | stay | tree_regressor | pa_regressor | 0.188107 | 0.002000 | recent_leader_incumbent_floor |
| 191 | stay | tree_regressor | pa_regressor | 0.232612 | 0.002000 | recent_leader_incumbent_floor |
| 215 | stay | tree_regressor | lin_lr_0_001 | 0.237237 | 0.002000 | recent_leader_incumbent_floor |
| 239 | stay | tree_regressor | lin_lr_0_001 | 0.195777 | 0.002000 | recent_leader_incumbent_floor |
| 263 | switch | tree_regressor | pa_regressor | 0.238589 | 0.002000 | recent_leader_advantage |
| 287 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_cooldown |
| 311 | stay | pa_regressor | lin_lr_0_001 | 0.044228 | 0.002000 | recent_leader_incumbent_floor |
| 335 | stay | pa_regressor | lin_lr_0_001 | 0.175579 | 0.002000 | recent_leader_incumbent_floor |
| 359 | stay | pa_regressor | lin_lr_0_001 | 0.176832 | 0.002000 | recent_leader_incumbent_floor |
| 383 | stay | pa_regressor | lin_lr_0_001 | 0.161656 | 0.002000 | recent_leader_incumbent_floor |
| 407 | stay | pa_regressor | lin_lr_0_001 | 0.162855 | 0.002000 | recent_leader_incumbent_floor |
| 431 | stay | pa_regressor | lin_lr_0_001 | 0.173113 | 0.002000 | recent_leader_incumbent_floor |
| 455 | stay | pa_regressor | lin_lr_0_001 | 0.163267 | 0.002000 | recent_leader_incumbent_floor |
| 479 | stay | pa_regressor | lin_lr_0_001 | 0.148739 | 0.002000 | recent_leader_incumbent_floor |
| 503 | stay | pa_regressor | lin_lr_0_001 | 0.135013 | 0.002000 | recent_leader_incumbent_floor |

... truncated 31 additional decision rows in `decisions.csv`.
