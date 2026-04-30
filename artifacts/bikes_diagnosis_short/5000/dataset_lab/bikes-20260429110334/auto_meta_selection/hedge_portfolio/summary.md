# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `hedge_portfolio`
- samples: `5000`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_001`
- switch_count: `8`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.701581 |
| sgd_lr_0_0001 | 0.698787 |
| sgd_lr_0_0005 | 0.701541 |
| sgd_lr_0_001 | 0.701981 |

- best_fixed_strategy: `sgd_lr_0_001`
- best_fixed_score: `0.701981`
- adaptive_delta_vs_best_fixed: `-0.000400`
- block_delta_mean: `-0.000401`
- block_delta_ci95: `0.000654`
- block_count: `39`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001519 | 0.010000 | hedge_margin_too_small |
| 255 | switch | sgd_lr_0_0005 | sgd_lr_0_0001 |  | 0.010000 | warmup_leader |
| 255 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | hedge_same_leader |
| 383 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | hedge_same_leader |
| 511 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | hedge_same_leader |
| 639 | switch | sgd_lr_0_0001 | sgd_lr_0_001 | 0.055073 | 0.010000 | hedge_weight_advantage |
| 767 | stay | sgd_lr_0_001 | sgd_lr_0_0005 | 0.007271 | 0.010000 | hedge_margin_too_small |
| 895 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.058475 | 0.010000 | hedge_weight_advantage |
| 1023 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.010628 | 0.010000 | hedge_weight_advantage |
| 1151 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | hedge_same_leader |
| 1279 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.020614 | 0.010000 | hedge_weight_advantage |
| 1407 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.039251 | 0.010000 | hedge_weight_advantage |
| 1535 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | hedge_same_leader |
| 1663 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | hedge_same_leader |
| 1791 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | hedge_same_leader |
| 1919 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.022902 | 0.010000 | hedge_weight_advantage |
| 2047 | stay | sgd_lr_0_0005 | sgd_lr_0_0005 | 0.000000 | 0.010000 | hedge_same_leader |
| 2175 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.121842 | 0.010000 | hedge_weight_advantage |
| 2303 | stay | sgd_lr_0_001 | sgd_lr_0_0001 | nan | 0.010000 | hedge_margin_too_small |
| 2431 | stay | sgd_lr_0_001 | sgd_lr_0_0001 | nan | 0.010000 | hedge_margin_too_small |

... truncated 20 additional decision rows in `decisions.csv`.
