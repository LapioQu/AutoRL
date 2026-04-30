# Real-Stream Benchmark Replay

- dataset: `ChickWeights`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `578`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `softmax_lr_0_20`
- final_strategy: `knn_classifier`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.058824 |
| gaussian_nb | 0.036332 |
| knn_classifier | 0.057093 |
| softmax_lr_0_05 | 0.050173 |
| softmax_lr_0_20 | 0.053633 |

- best_fixed_strategy: `knn_classifier`
- best_fixed_score: `0.057093`
- adaptive_delta_vs_best_fixed: `0.001730`
- block_delta_mean: `0.001953`
- block_delta_ci95: `0.019045`
- block_count: `4`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 383 | switch | softmax_lr_0_20 | knn_classifier |  | 0.010000 | recent_leader_warmup |
| 511 | stay | knn_classifier | knn_classifier | 0.000000 | 0.010000 | recent_leader_cooldown |
