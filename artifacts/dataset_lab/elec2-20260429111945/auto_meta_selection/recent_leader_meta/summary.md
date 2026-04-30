# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `1268`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `gaussian_nb`
- final_strategy: `pa_classifier`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.951104 |
| gaussian_nb | 0.820978 |
| pa_classifier | 0.952681 |
| softmax_lr_0_05 | 0.910883 |
| softmax_lr_0_20 | 0.936909 |
| tree_classifier | 0.873028 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.952681`
- adaptive_delta_vs_best_fixed: `-0.001577`
- block_delta_mean: `-0.001603`
- block_delta_ci95: `0.010634`
- block_count: `26`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 95 | switch | gaussian_nb | softmax_lr_0_20 |  | 0.000000 | recent_leader_warmup |
| 143 | stay | softmax_lr_0_20 | softmax_lr_0_20 | 0.000000 | 0.000000 | recent_leader_cooldown |
| 191 | switch | softmax_lr_0_20 | pa_classifier | 0.027778 | 0.000000 | recent_leader_advantage |
| 239 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_cooldown |
| 287 | stay | pa_classifier | pa_classifier | 0.000000 | 0.000000 | recent_leader_same |
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

... truncated 5 additional decision rows in `decisions.csv`.
