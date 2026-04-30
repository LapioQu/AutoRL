# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `336`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `tree_classifier`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.854167 |
| gaussian_nb | 0.839286 |
| pa_classifier | 0.943452 |
| softmax_lr_0_05 | 0.898810 |
| softmax_lr_0_20 | 0.922619 |
| tree_classifier | 0.854167 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.943452`
- adaptive_delta_vs_best_fixed: `-0.089286`
- block_delta_mean: `-0.089286`
- block_delta_ci95: `0.078138`
- block_count: `7`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 95 | stay | tree_classifier | softmax_lr_0_20 | 0.000000 | 0.000000 | no_candidate_improvement |
| 143 | stay | tree_classifier | softmax_lr_0_20 | 0.125000 | 0.000000 | high_uncertainty |
| 191 | stay | tree_classifier | softmax_lr_0_20 | 0.125000 | 0.000000 | high_uncertainty |
| 239 | stay | tree_classifier | softmax_lr_0_20 | 0.125000 | 0.000000 | high_uncertainty |
| 287 | stay | tree_classifier | softmax_lr_0_20 | 0.125000 | 0.000000 | high_uncertainty |
| 335 | stay | tree_classifier | softmax_lr_0_20 | 0.125000 | 0.000000 | high_uncertainty |
