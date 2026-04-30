# Real-Stream Benchmark Replay

- dataset: `bikes`
- score_name: `normalized_reward`
- policy_name: `hedge_portfolio`
- samples: `512`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0001`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.656726 |
| sgd_lr_0_0001 | 0.657233 |
| sgd_lr_0_0005 | 0.656026 |
| sgd_lr_0_001 | 0.654848 |

- best_fixed_strategy: `sgd_lr_0_0001`
- best_fixed_score: `0.657233`
- adaptive_delta_vs_best_fixed: `-0.000508`
- block_delta_mean: `-0.000508`
- block_delta_ci95: `0.001107`
- block_count: `4`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.003408 | 0.010000 | hedge_margin_too_small |
| 255 | switch | sgd_lr_0_0005 | sgd_lr_0_0001 |  | 0.010000 | warmup_leader |
| 255 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | hedge_same_leader |
| 383 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | hedge_same_leader |
| 511 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | hedge_same_leader |
