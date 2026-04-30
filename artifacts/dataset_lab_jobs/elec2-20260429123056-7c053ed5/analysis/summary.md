# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `45312`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_1_0`
- final_strategy: `sgd_lr_0_5`
- switch_count: `11`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.915343 |
| sgd_lr_0_1 | 0.907707 |
| sgd_lr_0_5 | 0.916093 |
| sgd_lr_1_0 | 0.913886 |

- best_fixed_strategy: `sgd_lr_0_5`
- best_fixed_score: `0.916093`
- adaptive_delta_vs_best_fixed: `-0.000750`
- block_delta_mean: `-0.000750`
- block_delta_ci95: `0.000817`
- block_count: `354`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 511 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_warmup_same |
| 639 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 767 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 895 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.003906 | 0.015000 | recent_leader_margin_too_small |
| 1023 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.003906 | 0.015000 | recent_leader_margin_too_small |
| 1151 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.007812 | 0.015000 | recent_leader_margin_too_small |
| 1279 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.011719 | 0.015000 | recent_leader_margin_too_small |
| 1407 | switch | sgd_lr_1_0 | sgd_lr_0_5 | 0.015625 | 0.015000 | recent_leader_advantage |
| 1535 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | recent_leader_cooldown |
| 1663 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | recent_leader_cooldown |
| 1791 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | recent_leader_cooldown |
| 1919 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | recent_leader_cooldown |
| 2047 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | recent_leader_same |
| 2175 | switch | sgd_lr_0_5 | sgd_lr_1_0 | 0.019531 | 0.015000 | recent_leader_advantage |
| 2303 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_cooldown |
| 2431 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_cooldown |
| 2559 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_cooldown |
| 2687 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_cooldown |
| 2815 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.007812 | 0.015000 | recent_leader_margin_too_small |
| 2943 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.011719 | 0.015000 | recent_leader_margin_too_small |

... truncated 331 additional decision rows in `decisions.csv`.
