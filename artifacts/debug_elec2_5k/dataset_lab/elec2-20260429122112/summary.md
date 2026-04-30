# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `5000`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `pa_classifier`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.947400 |
| gaussian_nb | 0.800600 |
| pa_classifier | 0.952200 |
| softmax_lr_0_05 | 0.913800 |
| softmax_lr_0_20 | 0.943200 |
| tree_classifier | 0.873400 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.952200`
- adaptive_delta_vs_best_fixed: `-0.004800`
- block_delta_mean: `-0.004808`
- block_delta_ci95: `0.006896`
- block_count: `104`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 95 | stay | tree_classifier | tree_classifier | 0.000000 | 0.000000 | recent_leader_warmup_same |
| 143 | switch | tree_classifier | gaussian_nb | 0.013889 | 0.000000 | recent_leader_advantage |
| 191 | stay | gaussian_nb | gaussian_nb | 0.000000 | 0.000000 | recent_leader_cooldown |
| 239 | switch | gaussian_nb | pa_classifier | 0.159722 | 0.000000 | recent_leader_advantage |
| 287 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_cooldown |
| 335 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
| 383 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
| 431 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
| 479 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
| 527 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
| 575 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
| 623 | stay | pa_classifier | softmax_lr_0_20 | 0.006944 | 0.000000 | recent_leader_incumbent_floor |
| 671 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
| 719 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
| 767 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
| 815 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
| 863 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
| 911 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
| 959 | stay | pa_classifier | softmax_lr_0_20 | 0.000000 | 0.000000 | recent_leader_incumbent_floor |
| 1007 | stay | pa_classifier | softmax_lr_0_20 | 0.000000 | 0.000000 | recent_leader_incumbent_floor |

... truncated 83 additional decision rows in `decisions.csv`.
