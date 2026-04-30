# Real-Stream Benchmark Replay

- dataset: `ChickWeights calibration`
- score_name: `accuracy`
- policy_name: `hedge_portfolio`
- samples: `512`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `softmax_lr_0_20`
- final_strategy: `knn_classifier`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.060547 |
| gaussian_nb | 0.041016 |
| knn_classifier | 0.064453 |
| softmax_lr_0_05 | 0.056641 |
| softmax_lr_0_20 | 0.060547 |

- best_fixed_strategy: `knn_classifier`
- best_fixed_score: `0.064453`
- adaptive_delta_vs_best_fixed: `-0.003906`
- block_delta_mean: `-0.003906`
- block_delta_ci95: `0.021991`
- block_count: `4`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | softmax_lr_0_20 | softmax_lr_0_20 | 0.000000 | 0.015000 | hedge_same_leader |
| 255 | stay | softmax_lr_0_20 | softmax_lr_0_20 | 0.000000 | 0.015000 | hedge_same_leader |
| 383 | stay | softmax_lr_0_20 | softmax_lr_0_20 | 0.000000 | 0.015000 | hedge_same_leader |
| 511 | switch | softmax_lr_0_20 | knn_classifier | 0.286328 | 0.015000 | hedge_weight_advantage |
