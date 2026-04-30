# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `45312`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `pa_classifier`
- switch_count: `338`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.912738 |
| gaussian_nb | 0.728747 |
| pa_classifier | 0.922714 |
| softmax_lr_0_05 | 0.894288 |
| softmax_lr_0_20 | 0.914173 |
| tree_classifier | 0.811220 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.922714`
- adaptive_delta_vs_best_fixed: `-0.009975`
- block_delta_mean: `-0.009975`
- block_delta_ci95: `0.003207`
- block_count: `944`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 47 | stay | tree_classifier | tree_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 95 | switch | tree_classifier | pa_classifier | 0.038308 | 0.015000 | fixed_share_weight_advantage |
| 143 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 191 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 239 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 287 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 335 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 383 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 431 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 479 | stay | pa_classifier | softmax_lr_0_05 | 0.008330 | 0.015000 | fixed_share_margin_too_small |
| 527 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 575 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 623 | switch | pa_classifier | softmax_lr_0_20 | 0.126137 | 0.015000 | fixed_share_weight_advantage |
| 671 | switch | softmax_lr_0_20 | tree_classifier | 0.136422 | 0.015000 | fixed_share_weight_advantage |
| 719 | switch | tree_classifier | pa_classifier | 0.486352 | 0.015000 | fixed_share_weight_advantage |
| 767 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 815 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 863 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 911 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 959 | switch | pa_classifier | softmax_lr_0_20 | 0.041414 | 0.015000 | fixed_share_weight_advantage |

... truncated 924 additional decision rows in `decisions.csv`.
