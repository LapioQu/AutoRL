# Real-Stream Benchmark Replay

- dataset: `Elec2 calibration`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `880`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `pa_classifier`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.876136 |
| knn_classifier | 0.876136 |
| pa_classifier | 0.944318 |
| sgd_lr_0_05 | 0.844318 |
| sgd_lr_0_10 | 0.860227 |
| tree_classifier | 0.826136 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.944318`
- adaptive_delta_vs_best_fixed: `-0.068182`
- block_delta_mean: `-0.078125`
- block_delta_ci95: `0.103666`
- block_count: `6`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 383 | switch | tree_classifier | pa_classifier |  | 0.010000 | recent_leader_warmup |
| 511 | stay | pa_classifier | pa_classifier | 0.000000 | 0.010000 | recent_leader_cooldown |
| 639 | stay | pa_classifier | pa_classifier | 0.000000 | 0.010000 | recent_leader_cooldown |
| 767 | stay | pa_classifier | pa_classifier | 0.000000 | 0.010000 | recent_leader_same |
