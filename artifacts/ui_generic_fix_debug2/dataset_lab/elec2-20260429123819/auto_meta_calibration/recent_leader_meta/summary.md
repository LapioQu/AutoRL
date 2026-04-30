# Real-Stream Benchmark Replay

- dataset: `Elec2 calibration`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `9968`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_1_0`
- final_strategy: `sgd_lr_0_5`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.945124 |
| sgd_lr_0_1 | 0.911116 |
| sgd_lr_0_5 | 0.943720 |
| sgd_lr_1_0 | 0.945827 |

- best_fixed_strategy: `sgd_lr_1_0`
- best_fixed_score: `0.945827`
- adaptive_delta_vs_best_fixed: `-0.000702`
- block_delta_mean: `-0.000710`
- block_delta_ci95: `0.001059`
- block_count: `77`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 511 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_warmup_same |
| 639 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 767 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 895 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 1023 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 1151 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 1279 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 1407 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 1535 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 1663 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.007812 | 0.015000 | recent_leader_margin_too_small |
| 1791 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.007812 | 0.015000 | recent_leader_margin_too_small |
| 1919 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 2047 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 2175 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 2303 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 2431 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 2559 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.003906 | 0.015000 | recent_leader_margin_too_small |
| 2687 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.007812 | 0.015000 | recent_leader_margin_too_small |
| 2815 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |
| 2943 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | recent_leader_same |

... truncated 54 additional decision rows in `decisions.csv`.
