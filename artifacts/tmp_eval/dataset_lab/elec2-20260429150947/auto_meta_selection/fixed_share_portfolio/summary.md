# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `4000`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `pa_classifier`
- switch_count: `3`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.946500 |
| knn_classifier | 0.868500 |
| pa_classifier | 0.948250 |
| sgd_lr_0_05 | 0.853000 |
| sgd_lr_0_10 | 0.867250 |
| tree_classifier | 0.859750 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.948250`
- adaptive_delta_vs_best_fixed: `-0.001750`
- block_delta_mean: `-0.001764`
- block_delta_ci95: `0.003401`
- block_count: `31`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | tree_classifier | pa_classifier | 0.043118 | 0.015000 | fixed_share_weight_advantage |
| 255 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 383 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 511 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 639 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 767 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 895 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1023 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1151 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1279 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1407 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1535 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1663 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1791 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1919 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 2047 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 2175 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 2303 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 2431 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 2559 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |

... truncated 11 additional decision rows in `decisions.csv`.
