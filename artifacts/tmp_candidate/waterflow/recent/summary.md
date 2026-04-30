# Real-Stream Benchmark Replay

- dataset: `waterflow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `1268`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `pa_regressor`
- final_strategy: `lin_lr_0_001`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.799125 |
| lin_lr_0_0005 | 0.802089 |
| lin_lr_0_001 | 0.803945 |
| pa_regressor | 0.726507 |

- best_fixed_strategy: `lin_lr_0_001`
- best_fixed_score: `0.803945`
- adaptive_delta_vs_best_fixed: `-0.004819`
- block_delta_mean: `-0.004897`
- block_delta_ci95: `0.039646`
- block_count: `52`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 47 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_warmup_same |
| 71 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 95 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 119 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 143 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 167 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 191 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 215 | stay | pa_regressor | lin_lr_0_001 | 0.006125 | 0.002000 | recent_leader_incumbent_floor |
| 239 | stay | pa_regressor | lin_lr_0_001 | 0.016934 | 0.002000 | recent_leader_incumbent_floor |
| 263 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 287 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 311 | stay | pa_regressor | lin_lr_0_001 | 0.044228 | 0.002000 | recent_leader_incumbent_floor |
| 335 | stay | pa_regressor | lin_lr_0_001 | 0.175579 | 0.002000 | recent_leader_incumbent_floor |
| 359 | stay | pa_regressor | lin_lr_0_001 | 0.176832 | 0.002000 | recent_leader_incumbent_floor |
| 383 | stay | pa_regressor | lin_lr_0_0005 | 0.169817 | 0.002000 | recent_leader_incumbent_floor |
| 407 | stay | pa_regressor | lin_lr_0_0005 | 0.172490 | 0.002000 | recent_leader_incumbent_floor |
| 431 | stay | pa_regressor | lin_lr_0_0005 | 0.175303 | 0.002000 | recent_leader_incumbent_floor |
| 455 | stay | pa_regressor | lin_lr_0_001 | 0.163267 | 0.002000 | recent_leader_incumbent_floor |
| 479 | stay | pa_regressor | lin_lr_0_0005 | 0.149604 | 0.002000 | recent_leader_incumbent_floor |
| 503 | stay | pa_regressor | lin_lr_0_0005 | 0.136721 | 0.002000 | recent_leader_incumbent_floor |

... truncated 31 additional decision rows in `decisions.csv`.
