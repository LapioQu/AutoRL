# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `hedge_portfolio`
- samples: `1268`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_001`
- switch_count: `4`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.669328 |
| sgd_lr_0_0001 | 0.669348 |
| sgd_lr_0_0005 | 0.670508 |
| sgd_lr_0_001 | 0.670316 |

- best_fixed_strategy: `sgd_lr_0_0005`
- best_fixed_score: `0.670508`
- adaptive_delta_vs_best_fixed: `-0.001180`
- block_delta_mean: `-0.000962`
- block_delta_ci95: `0.001670`
- block_count: `9`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.002345 | 0.010000 | hedge_margin_too_small |
| 255 | switch | sgd_lr_0_0005 | sgd_lr_0_0001 |  | 0.010000 | warmup_leader |
| 255 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | hedge_same_leader |
| 383 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | hedge_same_leader |
| 511 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | hedge_same_leader |
| 639 | switch | sgd_lr_0_0001 | sgd_lr_0_001 | 0.069764 | 0.010000 | hedge_weight_advantage |
| 767 | stay | sgd_lr_0_001 | sgd_lr_0_0005 | 0.004762 | 0.010000 | hedge_margin_too_small |
| 895 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.065876 | 0.010000 | hedge_weight_advantage |
| 1023 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.023913 | 0.010000 | hedge_weight_advantage |
| 1151 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | hedge_same_leader |
