# Real-Stream Benchmark Replay

- dataset: `InsectsRecurring`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `60000`
- source: Official USP INSECTS recurring-drift stream replayed in temporal order; target is the insect class under incremental recurring concept drift.
- source_url: `https://sites.google.com/view/uspdsrepository`
- start_strategy: `softmax_lr_0_01`
- final_strategy: `softmax_lr_0_01`
- switch_count: `4`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.787667 |
| softmax_lr_0_01 | 0.782283 |
| softmax_lr_0_1 | 0.763300 |
| tree_classifier | 0.626600 |

- best_fixed_strategy: `softmax_lr_0_01`
- best_fixed_score: `0.782283`
- adaptive_delta_vs_best_fixed: `0.005383`
- block_delta_mean: `0.005392`
- block_delta_ci95: `0.004703`
- block_count: `234`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 511 | stay | softmax_lr_0_01 | softmax_lr_0_1 | -0.015625 | 0.006000 | high_uncertainty |
| 767 | stay | softmax_lr_0_01 | softmax_lr_0_1 | -0.042969 | 0.006000 | high_uncertainty |
| 1023 | stay | softmax_lr_0_01 | softmax_lr_0_1 | -0.005859 | 0.006000 | high_uncertainty |
| 1279 | stay | softmax_lr_0_01 | softmax_lr_0_1 | 0.025391 | 0.006000 | high_uncertainty |
| 1535 | stay | softmax_lr_0_01 | softmax_lr_0_1 | -0.011719 | 0.006000 | high_uncertainty |
| 1791 | stay | softmax_lr_0_01 | softmax_lr_0_1 | -0.035156 | 0.006000 | high_uncertainty |
| 2047 | stay | softmax_lr_0_01 | tree_classifier | -0.039062 | 0.006000 | high_uncertainty |
| 2303 | stay | softmax_lr_0_01 | tree_classifier | -0.023438 | 0.006000 | high_uncertainty |
| 2559 | stay | softmax_lr_0_01 | softmax_lr_0_1 | -0.019531 | 0.006000 | high_uncertainty |
| 2815 | stay | softmax_lr_0_01 | softmax_lr_0_1 | -0.025391 | 0.006000 | high_uncertainty |
| 3071 | stay | softmax_lr_0_01 | tree_classifier | -0.025391 | 0.006000 | high_uncertainty |
| 3327 | stay | softmax_lr_0_01 | tree_classifier | -0.039062 | 0.006000 | high_uncertainty |
| 3583 | stay | softmax_lr_0_01 | tree_classifier | -0.074219 | 0.006000 | no_candidate_improvement |
| 3839 | stay | softmax_lr_0_01 | tree_classifier | -0.060547 | 0.006000 | high_uncertainty |
| 4095 | stay | softmax_lr_0_01 | softmax_lr_0_1 | -0.052734 | 0.006000 | high_uncertainty |
| 4351 | stay | softmax_lr_0_01 | softmax_lr_0_1 | -0.017578 | 0.006000 | high_uncertainty |
| 4607 | stay | softmax_lr_0_01 | softmax_lr_0_1 | -0.011719 | 0.006000 | high_uncertainty |
| 4863 | stay | softmax_lr_0_01 | softmax_lr_0_1 | -0.041016 | 0.006000 | high_uncertainty |
| 5119 | stay | softmax_lr_0_01 | softmax_lr_0_1 | -0.064453 | 0.006000 | high_uncertainty |
| 5375 | stay | softmax_lr_0_01 | softmax_lr_0_1 | -0.060547 | 0.006000 | high_uncertainty |

... truncated 213 additional decision rows in `decisions.csv`.
