# Real-Stream Benchmark Replay

- dataset: `bikes`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `512`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0001`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.656688 |
| sgd_lr_0_0001 | 0.657233 |
| sgd_lr_0_0005 | 0.656026 |
| sgd_lr_0_001 | 0.654848 |

- best_fixed_strategy: `sgd_lr_0_0001`
- best_fixed_score: `0.657233`
- adaptive_delta_vs_best_fixed: `-0.000545`
- block_delta_mean: `-0.000545`
- block_delta_ci95: `0.001169`
- block_count: `4`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 255 | switch | sgd_lr_0_0005 | sgd_lr_0_0001 |  | 0.000500 | recent_leader_warmup |
| 383 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.000500 | recent_leader_same |
| 511 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.000500 | recent_leader_same |
