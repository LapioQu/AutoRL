# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `best_fixed_guard`
- samples: `45312`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_5`
- final_strategy: `sgd_lr_0_5`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.916093 |
| sgd_lr_0_1 | 0.907707 |
| sgd_lr_0_5 | 0.916093 |
| sgd_lr_1_0 | 0.913886 |

- best_fixed_strategy: `sgd_lr_0_5`
- best_fixed_score: `0.916093`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `0`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
