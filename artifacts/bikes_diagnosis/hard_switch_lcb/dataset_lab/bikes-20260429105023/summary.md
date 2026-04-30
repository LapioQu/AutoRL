# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `182470`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0001`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.669857 |
| sgd_lr_0_0001 | 0.669679 |
| sgd_lr_0_0005 | 0.140659 |
| sgd_lr_0_001 | 0.126785 |

- best_fixed_strategy: `sgd_lr_0_0001`
- best_fixed_score: `0.669679`
- adaptive_delta_vs_best_fixed: `0.000178`
- block_delta_mean: `0.000178`
- block_delta_ci95: `0.000167`
- block_count: `1425`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 383 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.001251 | 0.010000 | no_candidate_improvement |
| 511 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.001284 | 0.010000 | high_uncertainty |
| 639 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000466 | 0.010000 | high_uncertainty |
| 767 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001758 | 0.010000 | high_uncertainty |
| 895 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000103 | 0.010000 | high_uncertainty |
| 1023 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.000605 | 0.010000 | high_uncertainty |
| 1151 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000870 | 0.010000 | high_uncertainty |
| 1279 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000426 | 0.010000 | high_uncertainty |
| 1407 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.000022 | 0.010000 | no_candidate_improvement |
| 1535 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001464 | 0.010000 | no_candidate_improvement |
| 1663 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001723 | 0.010000 | no_candidate_improvement |
| 1791 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001613 | 0.010000 | high_uncertainty |
| 1919 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.000173 | 0.010000 | high_uncertainty |
| 2047 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.003617 | 0.010000 | high_uncertainty |
| 2175 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.001301 | 0.010000 | high_uncertainty |
| 2303 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001685 | 0.010000 | high_uncertainty |
| 2431 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001765 | 0.010000 | no_candidate_improvement |
| 2559 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001803 | 0.010000 | high_uncertainty |
| 2687 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.001995 | 0.010000 | high_uncertainty |
| 2815 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.005505 | 0.010000 | no_candidate_improvement |

... truncated 1403 additional decision rows in `decisions.csv`.
