# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `best_fixed_guard`
- samples: `4000`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `pa_classifier`
- final_strategy: `pa_classifier`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.948250 |
| knn_classifier | 0.870750 |
| pa_classifier | 0.948250 |
| sgd_lr_0_05 | 0.853000 |
| sgd_lr_0_10 | 0.867250 |
| tree_classifier | 0.850000 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.948250`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `0`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
