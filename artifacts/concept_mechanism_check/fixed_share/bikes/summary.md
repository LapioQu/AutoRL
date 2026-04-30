# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `40000`
- source: Bikes
- source_url: `https://maxhalford.github.io/files/datasets/toulouse_bikes.zip`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0001`
- switch_count: `94`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.678200 |
| sgd_lr_0_0001 | 0.676251 |
| sgd_lr_0_0005 | 0.575938 |
| sgd_lr_0_001 | 0.574939 |

- best_fixed_strategy: `sgd_lr_0_0001`
- best_fixed_score: `0.676251`
- adaptive_delta_vs_best_fixed: `0.001949`
- block_delta_mean: `0.001953`
- block_delta_ci95: `0.000974`
- block_count: `312`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | sgd_lr_0_0005 | sgd_lr_0_001 |  | 0.010000 | fixed_share_warmup_leader |
| 127 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 255 | switch | sgd_lr_0_001 | sgd_lr_0_0001 | 0.041384 | 0.010000 | fixed_share_weight_advantage |
| 383 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 511 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 639 | switch | sgd_lr_0_0001 | sgd_lr_0_001 | 0.081140 | 0.010000 | fixed_share_weight_advantage |
| 767 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.013898 | 0.010000 | fixed_share_weight_advantage |
| 895 | stay | sgd_lr_0_0005 | sgd_lr_0_0005 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1023 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.031142 | 0.010000 | fixed_share_weight_advantage |
| 1151 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1279 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1407 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1535 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1663 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1791 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1919 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.183165 | 0.010000 | fixed_share_weight_advantage |
| 2047 | stay | sgd_lr_0_0005 | sgd_lr_0_0005 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 2175 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.039691 | 0.010000 | fixed_share_weight_advantage |
| 2303 | stay | sgd_lr_0_001 | sgd_lr_0_0005 | 0.002777 | 0.010000 | fixed_share_margin_too_small |
| 2431 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |

... truncated 293 additional decision rows in `decisions.csv`.
