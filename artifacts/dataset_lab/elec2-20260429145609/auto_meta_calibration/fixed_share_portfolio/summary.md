# Real-Stream Benchmark Replay

- dataset: `Elec2 calibration`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `880`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `softmax_lr_0_20`
- switch_count: `3`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.851136 |
| knn_classifier | 0.876136 |
| softmax_lr_0_05 | 0.844318 |
| softmax_lr_0_20 | 0.865909 |
| tree_classifier | 0.823864 |

- best_fixed_strategy: `knn_classifier`
- best_fixed_score: `0.876136`
- adaptive_delta_vs_best_fixed: `-0.025000`
- block_delta_mean: `-0.033854`
- block_delta_ci95: `0.061108`
- block_count: `6`

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
