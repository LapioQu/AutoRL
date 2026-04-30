# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `253`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0005`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.644693 |
| sgd_lr_0_0001 | 0.643946 |
| sgd_lr_0_0005 | 0.644693 |
| sgd_lr_0_001 | 0.645910 |

- best_fixed_strategy: `sgd_lr_0_001`
- best_fixed_score: `0.645910`
- adaptive_delta_vs_best_fixed: `-0.001217`
- block_delta_mean: `-0.001103`
- block_delta_ci95: `0.000000`
- block_count: `1`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
