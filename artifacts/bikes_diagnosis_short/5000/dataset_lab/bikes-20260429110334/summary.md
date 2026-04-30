# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `best_fixed_guard`
- samples: `5000`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_001`
- final_strategy: `sgd_lr_0_001`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.701981 |
| sgd_lr_0_0001 | 0.698787 |
| sgd_lr_0_0005 | 0.701541 |
| sgd_lr_0_001 | 0.701981 |

- best_fixed_strategy: `sgd_lr_0_001`
- best_fixed_score: `0.701981`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `0`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
