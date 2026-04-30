# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `1268`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_001`
- switch_count: `4`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.669605 |
| sgd_lr_0_0001 | 0.669348 |
| sgd_lr_0_0005 | 0.670508 |
| sgd_lr_0_001 | 0.670316 |

- best_fixed_strategy: `sgd_lr_0_0005`
- best_fixed_score: `0.670508`
- adaptive_delta_vs_best_fixed: `-0.000903`
- block_delta_mean: `-0.000657`
- block_delta_ci95: `0.001616`
- block_count: `9`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 255 | switch | sgd_lr_0_0005 | sgd_lr_0_0001 |  | 0.000500 | recent_leader_warmup |
| 383 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.000500 | recent_leader_same |
| 511 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.000500 | recent_leader_same |
| 639 | switch | sgd_lr_0_0001 | sgd_lr_0_001 | 0.012662 | 0.000500 | recent_leader_advantage |
| 767 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.001025 | 0.000500 | recent_leader_advantage |
| 895 | stay | sgd_lr_0_0005 | sgd_lr_0_0005 | 0.000000 | 0.000500 | recent_leader_same |
| 1023 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.004128 | 0.000500 | recent_leader_advantage |
| 1151 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.000500 | recent_leader_same |
