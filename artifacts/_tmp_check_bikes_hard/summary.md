# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `40000`
- source: Real Toulouse bike-availability stream replayed in temporal order; evaluation uses the first 40,000 samples for a reproducible CPU-bound benchmark.
- source_url: `https://maxhalford.github.io/files/datasets/toulouse_bikes.zip`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0001`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.677074 |
| sgd_lr_0_0001 | 0.676251 |
| sgd_lr_0_0005 | 0.575938 |
| sgd_lr_0_001 | 0.574939 |

- best_fixed_strategy: `sgd_lr_0_0001`
- best_fixed_score: `0.676251`
- adaptive_delta_vs_best_fixed: `0.000823`
- block_delta_mean: `0.000824`
- block_delta_ci95: `0.000765`
- block_count: `312`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 383 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.001266 | 0.010000 | no_candidate_improvement |
| 511 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.001301 | 0.010000 | high_uncertainty |
| 639 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000473 | 0.010000 | high_uncertainty |
| 767 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001781 | 0.010000 | high_uncertainty |
| 895 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000104 | 0.010000 | high_uncertainty |
| 1023 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.000608 | 0.010000 | high_uncertainty |
| 1151 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000891 | 0.010000 | high_uncertainty |
| 1279 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000433 | 0.010000 | high_uncertainty |
| 1407 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.000027 | 0.010000 | no_candidate_improvement |
| 1535 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001479 | 0.010000 | no_candidate_improvement |
| 1663 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001744 | 0.010000 | no_candidate_improvement |
| 1791 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001627 | 0.010000 | high_uncertainty |
| 1919 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.000161 | 0.010000 | high_uncertainty |
| 2047 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.003611 | 0.010000 | high_uncertainty |
| 2175 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.001273 | 0.010000 | high_uncertainty |
| 2303 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001727 | 0.010000 | high_uncertainty |
| 2431 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001796 | 0.010000 | no_candidate_improvement |
| 2559 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001837 | 0.010000 | high_uncertainty |
| 2687 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.001993 | 0.010000 | high_uncertainty |
| 2815 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.005529 | 0.010000 | no_candidate_improvement |

... truncated 290 additional decision rows in `decisions.csv`.
