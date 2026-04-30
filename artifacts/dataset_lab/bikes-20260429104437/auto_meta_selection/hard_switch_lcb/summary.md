# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `1268`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0005`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.670508 |
| sgd_lr_0_0001 | 0.669348 |
| sgd_lr_0_0005 | 0.670508 |
| sgd_lr_0_001 | 0.670316 |

- best_fixed_strategy: `sgd_lr_0_0005`
- best_fixed_score: `0.670508`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `9`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 383 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.001548 | 0.010000 | no_candidate_improvement |
| 511 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.001628 | 0.010000 | high_uncertainty |
| 639 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000641 | 0.010000 | high_uncertainty |
| 767 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.002226 | 0.010000 | high_uncertainty |
| 895 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000093 | 0.010000 | high_uncertainty |
| 1023 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | -0.000657 | 0.010000 | high_uncertainty |
| 1151 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.001372 | 0.010000 | high_uncertainty |
