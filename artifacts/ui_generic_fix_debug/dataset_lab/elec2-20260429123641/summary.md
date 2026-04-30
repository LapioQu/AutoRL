# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `45312`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_1_0`
- final_strategy: `sgd_lr_0_5`
- switch_count: `172`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.914703 |
| sgd_lr_0_1 | 0.907707 |
| sgd_lr_0_5 | 0.916093 |
| sgd_lr_1_0 | 0.913886 |

- best_fixed_strategy: `sgd_lr_0_5`
- best_fixed_score: `0.916093`
- adaptive_delta_vs_best_fixed: `-0.001390`
- block_delta_mean: `-0.001390`
- block_delta_ci95: `0.001547`
- block_count: `354`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | sgd_lr_1_0 | sgd_lr_0_5 | 0.085894 | 0.015000 | fixed_share_weight_advantage |
| 255 | switch | sgd_lr_0_5 | sgd_lr_1_0 | 0.036143 | 0.015000 | fixed_share_weight_advantage |
| 383 | switch | sgd_lr_1_0 | sgd_lr_0_1 | 0.052421 | 0.015000 | fixed_share_weight_advantage |
| 511 | switch | sgd_lr_0_1 | sgd_lr_1_0 | 0.116465 | 0.015000 | fixed_share_weight_advantage |
| 639 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 767 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 895 | switch | sgd_lr_1_0 | sgd_lr_0_5 | 0.223292 | 0.015000 | fixed_share_weight_advantage |
| 1023 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1151 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1279 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1407 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1535 | stay | sgd_lr_0_5 | sgd_lr_0_1 | 0.011161 | 0.015000 | fixed_share_margin_too_small |
| 1663 | switch | sgd_lr_0_5 | sgd_lr_0_1 | 0.078325 | 0.015000 | fixed_share_weight_advantage |
| 1791 | switch | sgd_lr_0_1 | sgd_lr_0_5 | 0.161800 | 0.015000 | fixed_share_weight_advantage |
| 1919 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 2047 | switch | sgd_lr_0_5 | sgd_lr_1_0 | 0.017087 | 0.015000 | fixed_share_weight_advantage |
| 2175 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 2303 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 2431 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 2559 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |

... truncated 334 additional decision rows in `decisions.csv`.
