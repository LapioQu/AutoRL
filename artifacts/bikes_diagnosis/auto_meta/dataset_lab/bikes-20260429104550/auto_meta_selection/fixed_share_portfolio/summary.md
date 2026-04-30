# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `182470`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0001`
- switch_count: `100`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.670058 |
| sgd_lr_0_0001 | 0.669679 |
| sgd_lr_0_0005 | 0.140659 |
| sgd_lr_0_001 | 0.126785 |

- best_fixed_strategy: `sgd_lr_0_0001`
- best_fixed_score: `0.669679`
- adaptive_delta_vs_best_fixed: `0.000378`
- block_delta_mean: `0.000379`
- block_delta_ci95: `0.000211`
- block_count: `1425`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.004227 | 0.010000 | fixed_share_margin_too_small |
| 255 | switch | sgd_lr_0_0005 | sgd_lr_0_0001 |  | 0.010000 | fixed_share_warmup_leader |
| 255 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 383 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 511 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 639 | switch | sgd_lr_0_0001 | sgd_lr_0_001 | 0.054048 | 0.010000 | fixed_share_weight_advantage |
| 767 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.014719 | 0.010000 | fixed_share_weight_advantage |
| 895 | stay | sgd_lr_0_0005 | sgd_lr_0_0005 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1023 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.023647 | 0.010000 | fixed_share_weight_advantage |
| 1151 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1279 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1407 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1535 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1663 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1791 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1919 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.163480 | 0.010000 | fixed_share_weight_advantage |
| 2047 | stay | sgd_lr_0_0005 | sgd_lr_0_0005 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 2175 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.028265 | 0.010000 | fixed_share_weight_advantage |
| 2303 | stay | sgd_lr_0_001 | sgd_lr_0_0001 | 0.001977 | 0.010000 | fixed_share_margin_too_small |
| 2431 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |

... truncated 1406 additional decision rows in `decisions.csv`.
