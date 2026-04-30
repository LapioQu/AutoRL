# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `1268`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `gaussian_nb`
- final_strategy: `pa_classifier`
- switch_count: `6`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.947950 |
| gaussian_nb | 0.820978 |
| pa_classifier | 0.952681 |
| softmax_lr_0_05 | 0.910883 |
| softmax_lr_0_20 | 0.936909 |
| tree_classifier | 0.873028 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.952681`
- adaptive_delta_vs_best_fixed: `-0.004732`
- block_delta_mean: `-0.004808`
- block_delta_ci95: `0.012227`
- block_count: `26`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 47 | stay | gaussian_nb | gaussian_nb | 0.000000 | 0.015000 | fixed_share_same_leader |
| 95 | switch | gaussian_nb | pa_classifier | 0.062654 | 0.015000 | fixed_share_weight_advantage |
| 143 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 191 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 239 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 287 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 335 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 383 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 431 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 479 | stay | pa_classifier | softmax_lr_0_05 | 0.005348 | 0.015000 | fixed_share_margin_too_small |
| 527 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 575 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 623 | switch | pa_classifier | softmax_lr_0_20 | 0.129494 | 0.015000 | fixed_share_weight_advantage |
| 671 | switch | softmax_lr_0_20 | tree_classifier | 0.070401 | 0.015000 | fixed_share_weight_advantage |
| 719 | switch | tree_classifier | pa_classifier | 0.301745 | 0.015000 | fixed_share_weight_advantage |
| 767 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 815 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 863 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 911 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 959 | switch | pa_classifier | softmax_lr_0_20 | 0.042520 | 0.015000 | fixed_share_weight_advantage |

... truncated 6 additional decision rows in `decisions.csv`.
