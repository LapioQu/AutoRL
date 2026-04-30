# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `hedge_portfolio`
- samples: `40000`
- source: Real Toulouse bike-availability stream replayed in temporal order; evaluation uses the first 40,000 samples for a reproducible CPU-bound benchmark.
- source_url: `https://maxhalford.github.io/files/datasets/toulouse_bikes.zip`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0005`
- switch_count: `6`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.575900 |
| sgd_lr_0_0001 | 0.676251 |
| sgd_lr_0_0005 | 0.575938 |
| sgd_lr_0_001 | 0.574939 |

- best_fixed_strategy: `sgd_lr_0_0001`
- best_fixed_score: `0.676251`
- adaptive_delta_vs_best_fixed: `-0.100351`
- block_delta_mean: `-0.099509`
- block_delta_ci95: `0.026689`
- block_count: `312`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | sgd_lr_0_0005 | sgd_lr_0_001 |  | 0.010000 | warmup_leader |
| 127 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | hedge_same_leader |
| 255 | switch | sgd_lr_0_001 | sgd_lr_0_0001 | 0.074056 | 0.010000 | hedge_weight_advantage |
| 383 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | hedge_same_leader |
| 511 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | hedge_same_leader |
| 639 | switch | sgd_lr_0_0001 | sgd_lr_0_001 | 0.048976 | 0.010000 | hedge_weight_advantage |
| 767 | stay | sgd_lr_0_001 | sgd_lr_0_0005 | 0.007990 | 0.010000 | hedge_margin_too_small |
| 895 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.054691 | 0.010000 | hedge_weight_advantage |
| 1023 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.005249 | 0.010000 | hedge_margin_too_small |
| 1151 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.007246 | 0.010000 | hedge_margin_too_small |
| 1279 | stay | sgd_lr_0_0005 | sgd_lr_0_0005 | 0.000000 | 0.010000 | hedge_same_leader |
| 1407 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.032966 | 0.010000 | hedge_weight_advantage |
| 1535 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | hedge_same_leader |
| 1663 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | hedge_same_leader |
| 1791 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | hedge_same_leader |
| 1919 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.039213 | 0.010000 | hedge_weight_advantage |
| 2047 | stay | sgd_lr_0_0005 | sgd_lr_0_0005 | 0.000000 | 0.010000 | hedge_same_leader |
| 2175 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | nan | 0.010000 | hedge_margin_too_small |
| 2303 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | nan | 0.010000 | hedge_margin_too_small |
| 2431 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | nan | 0.010000 | hedge_margin_too_small |

... truncated 293 additional decision rows in `decisions.csv`.
