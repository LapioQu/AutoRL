# Real-Stream Benchmark Replay

- dataset: `Elec2 calibration`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `880`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `tree_classifier`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.823864 |
| knn_classifier | 0.876136 |
| softmax_lr_0_05 | 0.844318 |
| softmax_lr_0_20 | 0.865909 |
| tree_classifier | 0.823864 |

- best_fixed_strategy: `knn_classifier`
- best_fixed_score: `0.876136`
- adaptive_delta_vs_best_fixed: `-0.052273`
- block_delta_mean: `-0.059896`
- block_delta_ci95: `0.070510`
- block_count: `6`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 255 | stay | tree_classifier | softmax_lr_0_20 | 0.117188 | 0.002000 | high_uncertainty |
| 383 | stay | tree_classifier | softmax_lr_0_20 | 0.160156 | 0.002000 | high_uncertainty |
| 511 | stay | tree_classifier | knn_classifier | 0.066406 | 0.002000 | high_uncertainty |
| 639 | stay | tree_classifier | knn_classifier | 0.070312 | 0.002000 | high_uncertainty |
| 767 | stay | tree_classifier | knn_classifier | 0.035156 | 0.002000 | high_uncertainty |
