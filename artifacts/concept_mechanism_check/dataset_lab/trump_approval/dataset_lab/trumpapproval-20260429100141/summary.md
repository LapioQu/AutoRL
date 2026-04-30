# Real-Stream Benchmark Replay

- dataset: `TrumpApproval`
- score_name: `normalized_reward`
- policy_name: `best_fixed_guard`
- samples: `512`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_05`
- final_strategy: `sgd_lr_0_05`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.726360 |
| sgd_lr_0_001 | 0.564354 |
| sgd_lr_0_01 | 0.659141 |
| sgd_lr_0_05 | 0.726360 |

- best_fixed_strategy: `sgd_lr_0_05`
- best_fixed_score: `0.726360`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `0`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
