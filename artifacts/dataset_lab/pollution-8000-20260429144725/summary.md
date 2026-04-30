# Real-Stream Benchmark Replay

- dataset: `pollution-8000`
- score_name: `normalized_reward`
- policy_name: `best_fixed_guard`
- samples: `7997`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_002`
- final_strategy: `lin_lr_0_002`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.864799 |
| knn_regressor | 0.840992 |
| lin_lr_0_002 | 0.864799 |
| lin_lr_0_01 | 0.167514 |
| pa_regressor | 0.842907 |

- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.864799`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `0`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
