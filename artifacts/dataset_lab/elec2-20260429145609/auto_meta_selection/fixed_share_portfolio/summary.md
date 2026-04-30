# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `4000`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `tree_classifier`
- switch_count: `19`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.864750 |
| knn_classifier | 0.867500 |
| softmax_lr_0_05 | 0.853000 |
| softmax_lr_0_20 | 0.881250 |
| tree_classifier | 0.849500 |

- best_fixed_strategy: `softmax_lr_0_20`
- best_fixed_score: `0.881250`
- adaptive_delta_vs_best_fixed: `-0.016500`
- block_delta_mean: `-0.016633`
- block_delta_ci95: `0.026790`
- block_count: `31`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | tree_classifier | tree_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 255 | switch | tree_classifier | softmax_lr_0_20 |  | 0.015000 | fixed_share_warmup_leader |
| 255 | stay | softmax_lr_0_20 | softmax_lr_0_20 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 383 | switch | softmax_lr_0_20 | knn_classifier | 0.509676 | 0.015000 | fixed_share_weight_advantage |
| 511 | stay | knn_classifier | knn_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 639 | stay | knn_classifier | knn_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 767 | switch | knn_classifier | softmax_lr_0_20 | 0.175201 | 0.015000 | fixed_share_weight_advantage |
| 895 | switch | softmax_lr_0_20 | tree_classifier | 0.153933 | 0.015000 | fixed_share_weight_advantage |
| 1023 | switch | tree_classifier | knn_classifier | 0.029295 | 0.015000 | fixed_share_weight_advantage |
| 1151 | switch | knn_classifier | softmax_lr_0_20 | 0.412422 | 0.015000 | fixed_share_weight_advantage |
| 1279 | stay | softmax_lr_0_20 | softmax_lr_0_05 | 0.014298 | 0.015000 | fixed_share_margin_too_small |
| 1407 | switch | softmax_lr_0_20 | tree_classifier | 0.378660 | 0.015000 | fixed_share_weight_advantage |
| 1535 | stay | tree_classifier | tree_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1663 | stay | tree_classifier | tree_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1791 | switch | tree_classifier | softmax_lr_0_20 | 0.547760 | 0.015000 | fixed_share_weight_advantage |
| 1919 | switch | softmax_lr_0_20 | softmax_lr_0_05 | 0.122754 | 0.015000 | fixed_share_weight_advantage |
| 2047 | switch | softmax_lr_0_05 | softmax_lr_0_20 | 0.544292 | 0.015000 | fixed_share_weight_advantage |
| 2175 | switch | softmax_lr_0_20 | knn_classifier | 0.094982 | 0.015000 | fixed_share_weight_advantage |
| 2303 | stay | knn_classifier | knn_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 2431 | stay | knn_classifier | knn_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |

... truncated 12 additional decision rows in `decisions.csv`.
