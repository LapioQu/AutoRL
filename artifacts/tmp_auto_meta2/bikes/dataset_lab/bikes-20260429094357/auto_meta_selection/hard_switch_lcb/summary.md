# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `512`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0005`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.656026 |
| sgd_lr_0_0001 | 0.657233 |
| sgd_lr_0_0005 | 0.656026 |
| sgd_lr_0_001 | 0.654848 |

- best_fixed_strategy: `sgd_lr_0_0001`
- best_fixed_score: `0.657233`
- adaptive_delta_vs_best_fixed: `-0.001207`
- block_delta_mean: `-0.001207`
- block_delta_ci95: `0.001162`
- block_count: `4`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 383 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.001706 | 0.010000 | no_candidate_improvement |
| 511 | stay | sgd_lr_0_0005 | sgd_lr_0_0001 | 0.001823 | 0.010000 | high_uncertainty |
