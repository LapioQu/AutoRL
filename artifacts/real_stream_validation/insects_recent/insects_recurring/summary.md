# Real-Stream Benchmark Replay

- dataset: `InsectsRecurring`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
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
| tree_classifier | 0.635217 |

- best_fixed_strategy: `softmax_lr_0_01`
- best_fixed_score: `0.782283`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `234`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 511 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_warmup_same |
| 767 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 1023 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 1279 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 1535 | stay | softmax_lr_0_01 | softmax_lr_0_1 | 0.011719 | 0.002000 | recent_leader_incumbent_floor |
| 1791 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 2047 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 2303 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 2559 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 2815 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 3071 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 3327 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 3583 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 3839 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 4095 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 4351 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 4607 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 4863 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 5119 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 5375 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |

... truncated 213 additional decision rows in `decisions.csv`.
