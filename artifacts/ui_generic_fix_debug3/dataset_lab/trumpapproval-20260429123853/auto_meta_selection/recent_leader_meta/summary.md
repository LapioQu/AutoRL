# Real-Stream Benchmark Replay

- dataset: `TrumpApproval`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `1001`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_01`
- final_strategy: `sgd_lr_0_05`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.800887 |
| sgd_lr_0_001 | 0.645687 |
| sgd_lr_0_01 | 0.733956 |
| sgd_lr_0_05 | 0.801432 |

- best_fixed_strategy: `sgd_lr_0_05`
- best_fixed_score: `0.801432`
- adaptive_delta_vs_best_fixed: `-0.000545`
- block_delta_mean: `-0.000550`
- block_delta_ci95: `0.001060`
- block_count: `31`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 31 | switch | sgd_lr_0_01 | sgd_lr_0_05 |  | 0.010000 | recent_leader_warmup |
| 63 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_cooldown |
| 95 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_cooldown |
| 127 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_cooldown |
| 159 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_cooldown |
| 191 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |
| 223 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |
| 255 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |
| 287 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |
| 319 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |
| 351 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |
| 383 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |
| 415 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |
| 447 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |
| 479 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |
| 511 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |
| 543 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |
| 575 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |
| 607 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |
| 639 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | recent_leader_same |

... truncated 11 additional decision rows in `decisions.csv`.
