# Real-Stream Benchmark Replay

- dataset: `TrumpApproval`
- score_name: `normalized_reward`
- policy_name: `hedge_portfolio`
- samples: `1001`
- source: Real approval-rating regression stream replayed in temporal order; used as a compact regression case where one fixed learner may dominate.
- source_url: `https://riverml.xyz/`
- start_strategy: `sgd_lr_0_01`
- final_strategy: `sgd_lr_0_05`
- switch_count: `3`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.797304 |
| sgd_lr_0_001 | 0.645687 |
| sgd_lr_0_01 | 0.733956 |
| sgd_lr_0_05 | 0.801432 |

- best_fixed_strategy: `sgd_lr_0_05`
- best_fixed_score: `0.801432`
- adaptive_delta_vs_best_fixed: `-0.004128`
- block_delta_mean: `-0.004165`
- block_delta_ci95: `0.006959`
- block_count: `31`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 31 | switch | sgd_lr_0_01 | sgd_lr_0_05 | 0.154781 | 0.005000 | hedge_weight_advantage |
| 63 | switch | sgd_lr_0_05 | sgd_lr_0_01 |  | 0.005000 | warmup_leader |
| 63 | stay | sgd_lr_0_01 | sgd_lr_0_01 | 0.000000 | 0.005000 | hedge_same_leader |
| 95 | switch | sgd_lr_0_01 | sgd_lr_0_05 | 0.472783 | 0.005000 | hedge_weight_advantage |
| 127 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 159 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 191 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 223 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 255 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 287 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 319 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 351 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 383 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 415 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 447 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 479 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 511 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 543 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 575 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |
| 607 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.005000 | hedge_same_leader |

... truncated 12 additional decision rows in `decisions.csv`.
