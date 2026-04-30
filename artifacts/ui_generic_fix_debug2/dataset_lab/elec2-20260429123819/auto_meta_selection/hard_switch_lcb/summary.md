# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `45312`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_1_0`
- final_strategy: `sgd_lr_0_5`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.916159 |
| sgd_lr_0_1 | 0.894951 |
| sgd_lr_0_5 | 0.916027 |
| sgd_lr_1_0 | 0.915144 |

- best_fixed_strategy: `sgd_lr_0_5`
- best_fixed_score: `0.916027`
- adaptive_delta_vs_best_fixed: `0.000132`
- block_delta_mean: `0.000132`
- block_delta_ci95: `0.000731`
- block_count: `354`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 255 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.003906 | 0.002000 | high_uncertainty |
| 383 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.007812 | 0.002000 | high_uncertainty |
| 511 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.003906 | 0.002000 | high_uncertainty |
| 639 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.000000 | 0.002000 | high_uncertainty |
| 767 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.000000 | 0.002000 | high_uncertainty |
| 895 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.011719 | 0.002000 | high_uncertainty |
| 1023 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.007812 | 0.002000 | high_uncertainty |
| 1151 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.007812 | 0.002000 | high_uncertainty |
| 1279 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.015625 | 0.002000 | high_uncertainty |
| 1407 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.011719 | 0.002000 | high_uncertainty |
| 1535 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.000000 | 0.002000 | high_uncertainty |
| 1663 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.007812 | 0.002000 | high_uncertainty |
| 1791 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.007812 | 0.002000 | high_uncertainty |
| 1919 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.003906 | 0.002000 | high_uncertainty |
| 2047 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.007812 | 0.002000 | high_uncertainty |
| 2175 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.007812 | 0.002000 | high_uncertainty |
| 2303 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.019531 | 0.002000 | high_uncertainty |
| 2431 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.007812 | 0.002000 | high_uncertainty |
| 2559 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.003906 | 0.002000 | high_uncertainty |
| 2687 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.007812 | 0.002000 | high_uncertainty |

... truncated 333 additional decision rows in `decisions.csv`.
