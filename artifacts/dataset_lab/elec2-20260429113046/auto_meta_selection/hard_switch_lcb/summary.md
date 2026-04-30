# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `45312`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `pa_classifier`
- switch_count: `24`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.859375 |
| gaussian_nb | 0.728747 |
| pa_classifier | 0.922714 |
| softmax_lr_0_05 | 0.894288 |
| softmax_lr_0_20 | 0.914173 |
| tree_classifier | 0.828655 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.922714`
- adaptive_delta_vs_best_fixed: `-0.063339`
- block_delta_mean: `-0.063339`
- block_delta_ci95: `0.008233`
- block_count: `944`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 95 | stay | tree_classifier | softmax_lr_0_20 | 0.000000 | 0.000000 | no_candidate_improvement |
| 143 | stay | tree_classifier | softmax_lr_0_20 | 0.125000 | 0.000000 | high_uncertainty |
| 191 | stay | tree_classifier | softmax_lr_0_20 | 0.250000 | 0.000000 | high_uncertainty |
| 239 | stay | tree_classifier | softmax_lr_0_20 | 0.250000 | 0.000000 | high_uncertainty |
| 287 | stay | tree_classifier | softmax_lr_0_20 | 0.125000 | 0.000000 | high_uncertainty |
| 335 | stay | tree_classifier | softmax_lr_0_20 | 0.125000 | 0.000000 | high_uncertainty |
| 383 | stay | tree_classifier | softmax_lr_0_05 | 0.375000 | 0.000000 | high_uncertainty |
| 431 | stay | tree_classifier | softmax_lr_0_05 | 0.250000 | 0.000000 | high_uncertainty |
| 479 | stay | tree_classifier | softmax_lr_0_05 | 0.000000 | 0.000000 | no_candidate_improvement |
| 527 | stay | tree_classifier | softmax_lr_0_05 | 0.000000 | 0.000000 | no_candidate_improvement |
| 575 | stay | tree_classifier | softmax_lr_0_20 | 0.000000 | 0.000000 | no_candidate_improvement |
| 623 | stay | tree_classifier | softmax_lr_0_05 | 0.000000 | 0.000000 | no_candidate_improvement |
| 671 | stay | tree_classifier | softmax_lr_0_05 | 0.000000 | 0.000000 | no_candidate_improvement |
| 719 | stay | tree_classifier | softmax_lr_0_20 | 0.000000 | 0.000000 | no_candidate_improvement |
| 767 | stay | tree_classifier | softmax_lr_0_20 | 0.000000 | 0.000000 | no_candidate_improvement |
| 815 | stay | tree_classifier | softmax_lr_0_20 | 0.000000 | 0.000000 | no_candidate_improvement |
| 863 | stay | tree_classifier | softmax_lr_0_20 | 0.000000 | 0.000000 | no_candidate_improvement |
| 911 | stay | tree_classifier | softmax_lr_0_20 | 0.375000 | 0.000000 | high_uncertainty |
| 959 | stay | tree_classifier | softmax_lr_0_20 | 0.375000 | 0.000000 | high_uncertainty |
| 1007 | stay | tree_classifier | pa_classifier | 0.500000 | 0.000000 | high_uncertainty |

... truncated 923 additional decision rows in `decisions.csv`.
