# Real-Stream Benchmark Replay

- dataset: `TrumpApproval`
- score_name: `normalized_reward`
- policy_name: `hedge_portfolio`
- samples: `512`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_01`
- final_strategy: `sgd_lr_0_05`
- switch_count: `3`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.718184 |
| sgd_lr_0_001 | 0.564354 |
| sgd_lr_0_01 | 0.659141 |
| sgd_lr_0_05 | 0.726360 |

- best_fixed_strategy: `sgd_lr_0_05`
- best_fixed_score: `0.726360`
- adaptive_delta_vs_best_fixed: `-0.008176`
- block_delta_mean: `-0.008176`
- block_delta_ci95: `0.013322`
- block_count: `16`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 31 | switch | sgd_lr_0_01 | sgd_lr_0_05 | 0.117398 | 0.010000 | hedge_weight_advantage |
| 63 | switch | sgd_lr_0_05 | sgd_lr_0_01 |  | 0.010000 | warmup_leader |
| 63 | stay | sgd_lr_0_01 | sgd_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 95 | switch | sgd_lr_0_01 | sgd_lr_0_05 | 0.389142 | 0.010000 | hedge_weight_advantage |
| 127 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
| 159 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
| 191 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
| 223 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
| 255 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
| 287 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
| 319 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
| 351 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
| 383 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
| 415 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
| 447 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
| 479 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
| 511 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
