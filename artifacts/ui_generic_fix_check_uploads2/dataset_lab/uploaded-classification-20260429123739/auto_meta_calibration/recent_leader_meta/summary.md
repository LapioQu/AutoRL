# Real-Stream Benchmark Replay

- dataset: `uploaded-classification calibration`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `12`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `softmax_lr_0_20`
- final_strategy: `softmax_lr_0_20`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.750000 |
| gaussian_nb | 0.583333 |
| knn_classifier | 0.583333 |
| softmax_lr_0_01 | 0.666667 |
| softmax_lr_0_05 | 0.750000 |
| softmax_lr_0_10 | 0.750000 |
| softmax_lr_0_20 | 0.750000 |
| tree_classifier | 0.666667 |

- best_fixed_strategy: `softmax_lr_0_20`
- best_fixed_score: `0.750000`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `0`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
