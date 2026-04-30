# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `45312`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `sgd_lr_1_0`
- final_strategy: `sgd_lr_0_5`
- switch_count: `7`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.916645 |
| sgd_lr_0_1 | 0.894928 |
| sgd_lr_0_5 | 0.916005 |
| sgd_lr_1_0 | 0.915122 |

- best_fixed_strategy: `sgd_lr_0_5`
- best_fixed_score: `0.916005`
- adaptive_delta_vs_best_fixed: `0.000640`
- block_delta_mean: `0.000640`
- block_delta_ci95: `0.000893`
- block_count: `354`

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

... truncated 331 additional decision rows in `decisions.csv`.
