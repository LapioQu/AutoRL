# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `best_fixed_guard`
- samples: `4000`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `softmax_lr_0_20`
- final_strategy: `softmax_lr_0_20`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.881250 |
| knn_classifier | 0.867500 |
| softmax_lr_0_05 | 0.853000 |
| softmax_lr_0_20 | 0.881250 |
| tree_classifier | 0.849500 |

- best_fixed_strategy: `softmax_lr_0_20`
- best_fixed_score: `0.881250`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `0`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
