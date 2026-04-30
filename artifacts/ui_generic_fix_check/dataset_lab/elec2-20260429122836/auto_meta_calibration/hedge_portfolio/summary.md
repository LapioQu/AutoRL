# Real-Stream Benchmark Replay

- dataset: `Elec2 calibration`
- score_name: `accuracy`
- policy_name: `hedge_portfolio`
- samples: `9968`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_1_0`
- final_strategy: `sgd_lr_0_5`
- switch_count: `3`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.945526 |
| sgd_lr_0_1 | 0.928872 |
| sgd_lr_0_5 | 0.945927 |
| sgd_lr_1_0 | 0.944924 |

- best_fixed_strategy: `sgd_lr_0_5`
- best_fixed_score: `0.945927`
- adaptive_delta_vs_best_fixed: `-0.000401`
- block_delta_mean: `-0.000406`
- block_delta_ci95: `0.000479`
- block_count: `77`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | sgd_lr_1_0 | sgd_lr_0_5 | 0.143730 | 0.015000 | hedge_weight_advantage |
| 255 | stay | sgd_lr_0_5 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_margin_too_small |
| 383 | stay | sgd_lr_0_5 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_margin_too_small |
| 511 | stay | sgd_lr_0_5 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_margin_too_small |
| 639 | switch | sgd_lr_0_5 | sgd_lr_1_0 | 0.171725 | 0.015000 | hedge_weight_advantage |
| 767 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 895 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 1023 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 1151 | switch | sgd_lr_1_0 | sgd_lr_0_5 | 0.336358 | 0.015000 | hedge_weight_advantage |
| 1279 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | hedge_same_leader |
| 1407 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | hedge_same_leader |
| 1535 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | hedge_same_leader |
| 1663 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | hedge_same_leader |
| 1791 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | hedge_same_leader |
| 1919 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | hedge_same_leader |
| 2047 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | hedge_same_leader |
| 2175 | stay | sgd_lr_0_5 | sgd_lr_0_1 | nan | 0.015000 | hedge_margin_too_small |
| 2303 | stay | sgd_lr_0_5 | sgd_lr_0_1 | nan | 0.015000 | hedge_margin_too_small |
| 2431 | stay | sgd_lr_0_5 | sgd_lr_0_1 | nan | 0.015000 | hedge_margin_too_small |
| 2559 | stay | sgd_lr_0_5 | sgd_lr_0_1 | nan | 0.015000 | hedge_margin_too_small |

... truncated 57 additional decision rows in `decisions.csv`.
