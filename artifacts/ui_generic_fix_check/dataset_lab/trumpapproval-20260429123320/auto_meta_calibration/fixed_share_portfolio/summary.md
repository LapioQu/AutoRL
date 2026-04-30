# Real-Stream Benchmark Replay

- dataset: `TrumpApproval calibration`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `250`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_01`
- final_strategy: `sgd_lr_0_05`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.579584 |
| sgd_lr_0_001 | 0.439159 |
| sgd_lr_0_01 | 0.542691 |
| sgd_lr_0_05 | 0.586433 |

- best_fixed_strategy: `sgd_lr_0_05`
- best_fixed_score: `0.586433`
- adaptive_delta_vs_best_fixed: `-0.006849`
- block_delta_mean: `-0.007644`
- block_delta_ci95: `0.037385`
- block_count: `7`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 31 | stay | sgd_lr_0_01 | sgd_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 63 | stay | sgd_lr_0_01 | sgd_lr_0_01 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 95 | switch | sgd_lr_0_01 | sgd_lr_0_05 | 0.349770 | 0.010000 | fixed_share_weight_advantage |
| 127 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 159 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | fixed_share_same_leader |
| 223 | stay | sgd_lr_0_05 | sgd_lr_0_05 | 0.000000 | 0.010000 | fixed_share_same_leader |
