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
| adaptive | 0.818182 |
| knn_classifier | 0.875000 |
| pa_classifier | 0.944318 |
| sgd_lr_0_05 | 0.844318 |
| sgd_lr_0_10 | 0.860227 |
| tree_classifier | 0.818182 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.944318`
- adaptive_delta_vs_best_fixed: `-0.126136`
- block_delta_mean: `-0.131510`
- block_delta_ci95: `0.104630`
- block_count: `6`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 255 | stay | tree_classifier | pa_classifier | 0.210938 | 0.002000 | high_uncertainty |
| 383 | stay | tree_classifier | pa_classifier | 0.257812 | 0.002000 | high_uncertainty |
| 511 | stay | tree_classifier | pa_classifier | 0.066406 | 0.002000 | high_uncertainty |
| 639 | stay | tree_classifier | pa_classifier | 0.082031 | 0.002000 | high_uncertainty |
| 767 | stay | tree_classifier | pa_classifier | 0.117188 | 0.002000 | high_uncertainty |
