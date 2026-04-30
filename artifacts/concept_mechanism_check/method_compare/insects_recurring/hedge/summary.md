# Real-Stream Benchmark Replay

- dataset: `InsectsRecurring`
- score_name: `accuracy`
- policy_name: `hedge_portfolio`
- samples: `60000`
- source: Official USP INSECTS recurring-drift stream replayed in temporal order; target is the insect class under incremental recurring concept drift.
- source_url: `https://sites.google.com/view/uspdsrepository`
- start_strategy: `softmax_lr_0_01`
- final_strategy: `softmax_lr_0_01`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.782283 |
| softmax_lr_0_01 | 0.782283 |
| softmax_lr_0_1 | 0.763300 |
| tree_classifier | 0.592083 |

- best_fixed_strategy: `softmax_lr_0_01`
- best_fixed_score: `0.782283`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `234`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 255 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 511 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 767 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 1023 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 1279 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 1535 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 1791 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 2047 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 2303 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 2559 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 2815 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 3071 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 3327 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 3583 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 3839 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 4095 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 4351 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 4607 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 4863 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 5119 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |

... truncated 214 additional decision rows in `decisions.csv`.
