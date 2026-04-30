# Real-Stream Benchmark Replay

- dataset: `TrumpApproval`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `160`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_01`
- final_strategy: `sgd_lr_0_01`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.480301 |
| sgd_lr_0_001 | 0.368332 |
| sgd_lr_0_01 | 0.480301 |
| sgd_lr_0_05 | 0.502570 |

- best_fixed_strategy: `sgd_lr_0_05`
- best_fixed_score: `0.502570`
- adaptive_delta_vs_best_fixed: `-0.022269`
- block_delta_mean: `-0.022269`
- block_delta_ci95: `0.055223`
- block_count: `5`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 95 | stay | sgd_lr_0_01 | sgd_lr_0_05 | -0.003918 | 0.010000 | high_uncertainty |
| 127 | stay | sgd_lr_0_01 | sgd_lr_0_05 | 0.053801 | 0.010000 | high_uncertainty |
| 159 | stay | sgd_lr_0_01 | sgd_lr_0_05 | 0.057511 | 0.010000 | high_uncertainty |
