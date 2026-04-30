# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `1024`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `gaussian_nb`
- final_strategy: `gaussian_nb`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.824219 |
| gaussian_nb | 0.824219 |
| pa_classifier | 0.949219 |
| softmax_lr_0_05 | 0.908203 |
| softmax_lr_0_20 | 0.938477 |
| tree_classifier | 0.846680 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.949219`
- adaptive_delta_vs_best_fixed: `-0.125000`
- block_delta_mean: `-0.125000`
- block_delta_ci95: `0.050854`
- block_count: `21`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 95 | stay | gaussian_nb | tree_classifier | 0.000000 | 0.000000 | no_candidate_improvement |
| 143 | stay | gaussian_nb | softmax_lr_0_20 | 0.000000 | 0.000000 | no_candidate_improvement |
| 191 | stay | gaussian_nb | softmax_lr_0_20 | 0.125000 | 0.000000 | high_uncertainty |
| 239 | stay | gaussian_nb | softmax_lr_0_20 | 0.125000 | 0.000000 | high_uncertainty |
| 287 | stay | gaussian_nb | softmax_lr_0_20 | 0.000000 | 0.000000 | no_candidate_improvement |
| 335 | stay | gaussian_nb | softmax_lr_0_20 | 0.125000 | 0.000000 | high_uncertainty |
| 383 | stay | gaussian_nb | softmax_lr_0_05 | 0.375000 | 0.000000 | high_uncertainty |
| 431 | stay | gaussian_nb | softmax_lr_0_05 | 0.250000 | 0.000000 | high_uncertainty |
| 479 | stay | gaussian_nb | softmax_lr_0_05 | 0.000000 | 0.000000 | no_candidate_improvement |
| 527 | stay | gaussian_nb | softmax_lr_0_05 | 0.125000 | 0.000000 | high_uncertainty |
| 575 | stay | gaussian_nb | softmax_lr_0_20 | 0.125000 | 0.000000 | high_uncertainty |
| 623 | stay | gaussian_nb | softmax_lr_0_05 | 0.125000 | 0.000000 | high_uncertainty |
| 671 | stay | gaussian_nb | softmax_lr_0_05 | 0.125000 | 0.000000 | high_uncertainty |
| 719 | stay | gaussian_nb | tree_classifier | 0.000000 | 0.000000 | no_candidate_improvement |
| 767 | stay | gaussian_nb | tree_classifier | 0.000000 | 0.000000 | no_candidate_improvement |
| 815 | stay | gaussian_nb | tree_classifier | 0.000000 | 0.000000 | no_candidate_improvement |
| 863 | stay | gaussian_nb | tree_classifier | 0.000000 | 0.000000 | no_candidate_improvement |
| 911 | stay | gaussian_nb | softmax_lr_0_20 | 0.375000 | 0.000000 | high_uncertainty |
| 959 | stay | gaussian_nb | softmax_lr_0_20 | 0.500000 | 0.000000 | high_uncertainty |
| 1007 | stay | gaussian_nb | pa_classifier | 0.625000 | 0.000000 | high_uncertainty |
