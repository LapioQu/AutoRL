# Real-Stream Benchmark Replay

- dataset: `Elec2 calibration`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `880`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `softmax_lr_0_20`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.822727 |
| knn_classifier | 0.876136 |
| softmax_lr_0_05 | 0.844318 |
| softmax_lr_0_20 | 0.865909 |
| tree_classifier | 0.823864 |

- best_fixed_strategy: `knn_classifier`
- best_fixed_score: `0.876136`
- adaptive_delta_vs_best_fixed: `-0.053409`
- block_delta_mean: `-0.066406`
- block_delta_ci95: `0.074383`
- block_count: `6`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 383 | switch | tree_classifier | softmax_lr_0_20 |  | 0.010000 | recent_leader_warmup |
| 511 | stay | softmax_lr_0_20 | softmax_lr_0_20 | 0.000000 | 0.010000 | recent_leader_cooldown |
| 639 | stay | softmax_lr_0_20 | softmax_lr_0_20 | 0.000000 | 0.010000 | recent_leader_cooldown |
| 767 | stay | softmax_lr_0_20 | knn_classifier | 0.003906 | 0.010000 | recent_leader_margin_too_small |
