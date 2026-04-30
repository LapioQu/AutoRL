# Real-Stream Benchmark Replay

- dataset: `pollution`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `41757`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `softmax_lr_0_20`
- switch_count: `144`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.036904 |
| knn_classifier | 0.042125 |
| softmax_lr_0_10 | 0.025193 |
| softmax_lr_0_20 | 0.032761 |
| tree_classifier | 0.015399 |

- best_fixed_strategy: `knn_classifier`
- best_fixed_score: `0.042125`
- adaptive_delta_vs_best_fixed: `-0.005221`
- block_delta_mean: `-0.005224`
- block_delta_ci95: `0.001538`
- block_count: `326`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | tree_classifier | softmax_lr_0_10 | 0.072645 | 0.015000 | fixed_share_weight_advantage |
| 255 | switch | softmax_lr_0_10 | tree_classifier |  | 0.015000 | fixed_share_warmup_leader |
| 255 | switch | tree_classifier | knn_classifier | 0.223440 | 0.015000 | fixed_share_weight_advantage |
| 383 | stay | knn_classifier | knn_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 511 | switch | knn_classifier | softmax_lr_0_20 | 0.027174 | 0.015000 | fixed_share_weight_advantage |
| 639 | switch | softmax_lr_0_20 | knn_classifier | 0.049822 | 0.015000 | fixed_share_weight_advantage |
| 767 | stay | knn_classifier | softmax_lr_0_20 | 0.007996 | 0.015000 | fixed_share_margin_too_small |
| 895 | stay | knn_classifier | knn_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1023 | stay | knn_classifier | knn_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1151 | switch | knn_classifier | softmax_lr_0_20 | 0.019125 | 0.015000 | fixed_share_weight_advantage |
| 1279 | switch | softmax_lr_0_20 | knn_classifier | 0.131255 | 0.015000 | fixed_share_weight_advantage |
| 1407 | stay | knn_classifier | knn_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1535 | switch | knn_classifier | softmax_lr_0_20 | 0.200728 | 0.015000 | fixed_share_weight_advantage |
| 1663 | stay | softmax_lr_0_20 | softmax_lr_0_20 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1791 | stay | softmax_lr_0_20 | softmax_lr_0_20 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 1919 | switch | softmax_lr_0_20 | knn_classifier | 0.017714 | 0.015000 | fixed_share_weight_advantage |
| 2047 | switch | knn_classifier | softmax_lr_0_20 | 0.094502 | 0.015000 | fixed_share_weight_advantage |
| 2175 | stay | softmax_lr_0_20 | softmax_lr_0_20 | 0.000000 | 0.015000 | fixed_share_same_leader |
| 2303 | switch | softmax_lr_0_20 | knn_classifier | 0.064052 | 0.015000 | fixed_share_weight_advantage |
| 2431 | stay | knn_classifier | knn_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |

... truncated 307 additional decision rows in `decisions.csv`.
