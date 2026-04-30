# Real-Stream Benchmark Replay

- dataset: `TrumpApproval`
- score_name: `normalized_reward`
- policy_name: `hedge_portfolio`
- samples: `160`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_01`
- final_strategy: `sgd_lr_0_05`
- switch_count: `3`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.476408 |
| sgd_lr_0_001 | 0.368332 |
| sgd_lr_0_01 | 0.480301 |
| sgd_lr_0_05 | 0.502570 |

- best_fixed_strategy: `sgd_lr_0_05`
- best_fixed_score: `0.502570`
- adaptive_delta_vs_best_fixed: `-0.026162`
- block_delta_mean: `-0.026162`
- block_delta_ci95: `0.038156`
- block_count: `5`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 31 | switch | sgd_lr_0_01 | sgd_lr_0_05 | 0.117398 | 0.010000 | hedge_weight_advantage |
| 63 | switch | sgd_lr_0_05 | sgd_lr_0_01 |  | 0.010000 | warmup_leader |
| 63 | stay | sgd_lr_0_01 | sgd_lr_0_01 | 0.000000 | 0.010000 | hedge_same_leader |
| 95 | switch | sgd_lr_0_01 | sgd_lr_0_05 | 0.389142 | 0.010000 | hedge_weight_advantage |
| 127 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
| 159 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | hedge_same_leader |
