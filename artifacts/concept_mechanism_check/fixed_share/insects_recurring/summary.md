# Real-Stream Benchmark Replay

- dataset: `InsectsRecurring`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `60000`
- source: InsectsRecurring
- source_url: `https://sites.google.com/view/uspdsrepository`
- start_strategy: `softmax_lr_0_01`
- final_strategy: `softmax_lr_0_01`
- switch_count: `68`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.784233 |
| softmax_lr_0_01 | 0.782283 |
| softmax_lr_0_1 | 0.763300 |
| tree_classifier | 0.602300 |

- best_fixed_strategy: `softmax_lr_0_01`
- best_fixed_score: `0.782283`
- adaptive_delta_vs_best_fixed: `0.001950`
- block_delta_mean: `0.001953`
- block_delta_ci95: `0.005361`
- block_count: `234`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 255 | switch | softmax_lr_0_01 | softmax_lr_0_1 | 0.283661 | 0.010000 | fixed_share_weight_advantage |
| 511 | switch | softmax_lr_0_1 | softmax_lr_0_01 |  | 0.010000 | fixed_share_warmup_leader |
| 511 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 767 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1023 | switch | softmax_lr_0_01 | softmax_lr_0_1 | 0.225454 | 0.010000 | fixed_share_weight_advantage |
| 1279 | switch | softmax_lr_0_1 | softmax_lr_0_01 | 0.327417 | 0.010000 | fixed_share_weight_advantage |
| 1535 | switch | softmax_lr_0_01 | softmax_lr_0_1 | 0.236347 | 0.010000 | fixed_share_weight_advantage |
| 1791 | switch | softmax_lr_0_1 | softmax_lr_0_01 | 0.227278 | 0.010000 | fixed_share_weight_advantage |
| 2047 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 2303 | switch | softmax_lr_0_01 | softmax_lr_0_1 | 0.128026 | 0.010000 | fixed_share_weight_advantage |
| 2559 | switch | softmax_lr_0_1 | softmax_lr_0_01 | 0.280408 | 0.010000 | fixed_share_weight_advantage |
| 2815 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 3071 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 3327 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 3583 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 3839 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 4095 | switch | softmax_lr_0_01 | softmax_lr_0_1 | 0.278116 | 0.010000 | fixed_share_weight_advantage |
| 4351 | switch | softmax_lr_0_1 | softmax_lr_0_01 | 0.513812 | 0.010000 | fixed_share_weight_advantage |
| 4607 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 4863 | stay | softmax_lr_0_01 | softmax_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |

... truncated 215 additional decision rows in `decisions.csv`.
