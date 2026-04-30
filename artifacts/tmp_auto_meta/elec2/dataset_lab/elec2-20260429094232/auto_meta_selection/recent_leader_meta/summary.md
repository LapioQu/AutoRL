# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `336`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `pa_classifier`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.934524 |
| gaussian_nb | 0.839286 |
| pa_classifier | 0.943452 |
| softmax_lr_0_05 | 0.898810 |
| softmax_lr_0_20 | 0.922619 |
| tree_classifier | 0.854167 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.943452`
- adaptive_delta_vs_best_fixed: `-0.008929`
- block_delta_mean: `-0.008929`
- block_delta_ci95: `0.042753`
- block_count: `7`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 95 | switch | tree_classifier | softmax_lr_0_20 |  | 0.000000 | recent_leader_warmup |
| 143 | stay | softmax_lr_0_20 | softmax_lr_0_20 | 0.000000 | 0.000000 | recent_leader_cooldown |
| 191 | switch | softmax_lr_0_20 | pa_classifier | 0.027778 | 0.000000 | recent_leader_advantage |
| 239 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_cooldown |
| 287 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
| 335 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
