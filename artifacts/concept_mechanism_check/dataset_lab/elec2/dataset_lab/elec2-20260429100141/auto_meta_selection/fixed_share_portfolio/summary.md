# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `1024`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `pa_classifier`
- switch_count: `6`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.938477 |
| gaussian_nb | 0.824219 |
| pa_classifier | 0.949219 |
| softmax_lr_0_05 | 0.908203 |
| softmax_lr_0_20 | 0.938477 |
| tree_classifier | 0.842773 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.949219`
- adaptive_delta_vs_best_fixed: `-0.010742`
- block_delta_mean: `-0.010913`
- block_delta_ci95: `0.024382`
- block_count: `21`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 47 | stay | tree_classifier | tree_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 95 | switch | tree_classifier | gaussian_nb |  | 0.015000 | fixed_share_warmup_leader |
| 95 | switch | gaussian_nb | pa_classifier | 0.063666 | 0.015000 | fixed_share_weight_advantage |
| 143 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 191 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 239 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 287 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 335 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 383 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 431 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 479 | stay | pa_classifier | softmax_lr_0_05 | 0.005997 | 0.015000 | fixed_share_margin_too_small |
| 527 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 575 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 623 | switch | pa_classifier | tree_classifier | 0.129844 | 0.015000 | fixed_share_weight_advantage |
| 671 | stay | tree_classifier | tree_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 719 | switch | tree_classifier | pa_classifier | 0.468272 | 0.015000 | fixed_share_weight_advantage |
| 767 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 815 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 863 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 911 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |

... truncated 2 additional decision rows in `decisions.csv`.
