# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `hedge_portfolio`
- samples: `182470`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0005`
- switch_count: `5`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.140652 |
| sgd_lr_0_0001 | 0.669679 |
| sgd_lr_0_0005 | 0.140659 |
| sgd_lr_0_001 | 0.126785 |

- best_fixed_strategy: `sgd_lr_0_0001`
- best_fixed_score: `0.669679`
- adaptive_delta_vs_best_fixed: `-0.529027`
- block_delta_mean: `-0.529113`
- block_delta_ci95: `0.013761`
- block_count: `1425`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001145 | 0.010000 | hedge_margin_too_small |
| 255 | switch | sgd_lr_0_0005 | sgd_lr_0_0001 |  | 0.010000 | warmup_leader |
| 255 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | hedge_same_leader |
| 383 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | hedge_same_leader |
| 511 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | hedge_same_leader |
| 639 | switch | sgd_lr_0_0001 | sgd_lr_0_001 | 0.048126 | 0.010000 | hedge_weight_advantage |
| 767 | stay | sgd_lr_0_001 | sgd_lr_0_0005 | 0.008069 | 0.010000 | hedge_margin_too_small |
| 895 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.054118 | 0.010000 | hedge_weight_advantage |
| 1023 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.004517 | 0.010000 | hedge_margin_too_small |
| 1151 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.006498 | 0.010000 | hedge_margin_too_small |
| 1279 | stay | sgd_lr_0_0005 | sgd_lr_0_0005 | 0.000000 | 0.010000 | hedge_same_leader |
| 1407 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.032080 | 0.010000 | hedge_weight_advantage |
| 1535 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | hedge_same_leader |
| 1663 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | hedge_same_leader |
| 1791 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | hedge_same_leader |
| 1919 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.041404 | 0.010000 | hedge_weight_advantage |
| 2047 | stay | sgd_lr_0_0005 | sgd_lr_0_0005 | 0.000000 | 0.010000 | hedge_same_leader |
| 2175 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | nan | 0.010000 | hedge_margin_too_small |
| 2303 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | nan | 0.010000 | hedge_margin_too_small |
| 2431 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | nan | 0.010000 | hedge_margin_too_small |

... truncated 1406 additional decision rows in `decisions.csv`.
