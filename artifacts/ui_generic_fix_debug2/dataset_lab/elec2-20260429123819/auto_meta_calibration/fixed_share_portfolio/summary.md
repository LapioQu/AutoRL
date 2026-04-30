# Real-Stream Benchmark Replay

- dataset: `Elec2 calibration`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `9968`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_1_0`
- final_strategy: `sgd_lr_1_0`
- switch_count: `29`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.944522 |
| sgd_lr_0_1 | 0.911116 |
| sgd_lr_0_5 | 0.943720 |
| sgd_lr_1_0 | 0.945827 |

- best_fixed_strategy: `sgd_lr_1_0`
- best_fixed_score: `0.945827`
- adaptive_delta_vs_best_fixed: `-0.001304`
- block_delta_mean: `-0.001319`
- block_delta_ci95: `0.001997`
- block_count: `77`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 255 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 383 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 511 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 639 | switch | sgd_lr_1_0 | sgd_lr_0_5 | 0.019587 | 0.015000 | fixed_share_weight_advantage |
| 767 | switch | sgd_lr_0_5 | sgd_lr_1_0 | 0.025071 | 0.015000 | fixed_share_weight_advantage |
| 895 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1023 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1151 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1279 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1407 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1535 | switch | sgd_lr_1_0 | sgd_lr_0_5 | 0.017376 | 0.015000 | fixed_share_weight_advantage |
| 1663 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1791 | switch | sgd_lr_0_5 | sgd_lr_1_0 | 0.045993 | 0.015000 | fixed_share_weight_advantage |
| 1919 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 2047 | switch | sgd_lr_1_0 | sgd_lr_0_5 | 0.021169 | 0.015000 | fixed_share_weight_advantage |
| 2175 | switch | sgd_lr_0_5 | sgd_lr_1_0 | 0.207598 | 0.015000 | fixed_share_weight_advantage |
| 2303 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 2431 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.007940 | 0.015000 | fixed_share_margin_too_small |
| 2559 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | fixed_share_same_leader |

... truncated 57 additional decision rows in `decisions.csv`.
