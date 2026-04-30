# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `5000`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0005`
- switch_count: `11`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.701658 |
| sgd_lr_0_0001 | 0.698787 |
| sgd_lr_0_0005 | 0.701541 |
| sgd_lr_0_001 | 0.701981 |

- best_fixed_strategy: `sgd_lr_0_001`
- best_fixed_score: `0.701981`
- adaptive_delta_vs_best_fixed: `-0.000323`
- block_delta_mean: `-0.000308`
- block_delta_ci95: `0.000757`
- block_count: `39`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 255 | switch | sgd_lr_0_0005 | sgd_lr_0_0001 |  | 0.000500 | recent_leader_warmup |
| 383 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.000500 | recent_leader_same |
| 511 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.000500 | recent_leader_same |
| 639 | switch | sgd_lr_0_0001 | sgd_lr_0_001 | 0.010993 | 0.000500 | recent_leader_advantage |
| 767 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.000882 | 0.000500 | recent_leader_advantage |
| 895 | stay | sgd_lr_0_0005 | sgd_lr_0_0005 | 0.000000 | 0.000500 | recent_leader_same |
| 1023 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.003257 | 0.000500 | recent_leader_advantage |
| 1151 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.000500 | recent_leader_same |
| 1279 | switch | sgd_lr_0_001 | sgd_lr_0_0001 | 0.002427 | 0.000500 | recent_leader_advantage |
| 1407 | switch | sgd_lr_0_0001 | sgd_lr_0_001 | 0.004795 | 0.000500 | recent_leader_advantage |
| 1535 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.000500 | recent_leader_same |
| 1663 | stay | sgd_lr_0_001 | sgd_lr_0_0005 | 0.000269 | 0.000500 | recent_leader_margin_too_small |
| 1791 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.000500 | recent_leader_same |
| 1919 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.009643 | 0.000500 | recent_leader_advantage |
| 2047 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000299 | 0.000500 | recent_leader_margin_too_small |
| 2175 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.004792 | 0.000500 | recent_leader_advantage |
| 2303 | stay | sgd_lr_0_001 | sgd_lr_0_0001 | 0.002326 | 0.000500 | recent_leader_incumbent_floor |
| 2431 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.000500 | recent_leader_same |
| 2559 | stay | sgd_lr_0_001 | sgd_lr_0_0001 | 0.009573 | 0.000500 | recent_leader_incumbent_floor |
| 2687 | stay | sgd_lr_0_001 | sgd_lr_0_0001 | 0.013462 | 0.000500 | recent_leader_incumbent_floor |

... truncated 18 additional decision rows in `decisions.csv`.
