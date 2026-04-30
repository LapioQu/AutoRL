# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `best_fixed_guard`
- samples: `1024`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `pa_classifier`
- final_strategy: `pa_classifier`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.949219 |
| gaussian_nb | 0.824219 |
| pa_classifier | 0.949219 |
| softmax_lr_0_05 | 0.908203 |
| softmax_lr_0_20 | 0.938477 |
| tree_classifier | 0.846680 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.949219`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `0`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
