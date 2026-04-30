# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `5000`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0005`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.701541 |
| sgd_lr_0_0001 | 0.698787 |
| sgd_lr_0_0005 | 0.701541 |
| sgd_lr_0_001 | 0.701981 |

- best_fixed_strategy: `sgd_lr_0_001`
- best_fixed_score: `0.701981`
- adaptive_delta_vs_best_fixed: `-0.000440`
- block_delta_mean: `-0.000425`
- block_delta_ci95: `0.001621`
- block_count: `39`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 383 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.001364 | 0.010000 | no_candidate_improvement |
| 511 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.001412 | 0.010000 | high_uncertainty |
| 639 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000524 | 0.010000 | high_uncertainty |
| 767 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001931 | 0.010000 | high_uncertainty |
| 895 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000108 | 0.010000 | high_uncertainty |
| 1023 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.000623 | 0.010000 | high_uncertainty |
| 1151 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001040 | 0.010000 | high_uncertainty |
| 1279 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000489 | 0.010000 | high_uncertainty |
| 1407 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.000068 | 0.010000 | no_candidate_improvement |
| 1535 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001578 | 0.010000 | no_candidate_improvement |
| 1663 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001890 | 0.010000 | no_candidate_improvement |
| 1791 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001721 | 0.010000 | high_uncertainty |
| 1919 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.000079 | 0.010000 | high_uncertainty |
| 2047 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.003548 | 0.010000 | high_uncertainty |
| 2175 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.001063 | 0.010000 | high_uncertainty |
| 2303 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.002019 | 0.010000 | high_uncertainty |
| 2431 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.002015 | 0.010000 | no_candidate_improvement |
| 2559 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.002073 | 0.010000 | high_uncertainty |
| 2687 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.001959 | 0.010000 | high_uncertainty |
| 2815 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.005663 | 0.010000 | no_candidate_improvement |

... truncated 17 additional decision rows in `decisions.csv`.
