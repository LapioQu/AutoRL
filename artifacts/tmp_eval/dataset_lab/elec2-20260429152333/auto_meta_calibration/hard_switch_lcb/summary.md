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
| adaptive | 0.826136 |
| knn_classifier | 0.876136 |
| pa_classifier | 0.944318 |
| sgd_lr_0_05 | 0.844318 |
| sgd_lr_0_10 | 0.860227 |
| tree_classifier | 0.826136 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.944318`
- adaptive_delta_vs_best_fixed: `-0.118182`
- block_delta_mean: `-0.122396`
- block_delta_ci95: `0.088529`
- block_count: `6`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 255 | stay | tree_classifier | pa_classifier | 0.175781 | 0.002000 | high_uncertainty |
| 383 | stay | tree_classifier | pa_classifier | 0.234375 | 0.002000 | high_uncertainty |
| 511 | stay | tree_classifier | pa_classifier | 0.085938 | 0.002000 | high_uncertainty |
| 639 | stay | tree_classifier | pa_classifier | 0.089844 | 0.002000 | high_uncertainty |
| 767 | stay | tree_classifier | pa_classifier | 0.105469 | 0.002000 | high_uncertainty |
