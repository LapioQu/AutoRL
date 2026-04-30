# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `256`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0001`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.641709 |
| sgd_lr_0_0001 | 0.642812 |
| sgd_lr_0_0005 | 0.641709 |
| sgd_lr_0_001 | 0.640444 |

- best_fixed_strategy: `sgd_lr_0_0001`
- best_fixed_score: `0.642812`
- adaptive_delta_vs_best_fixed: `-0.001103`
- block_delta_mean: `-0.001103`
- block_delta_ci95: `0.002209`
- block_count: `2`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 255 | switch | sgd_lr_0_0005 | sgd_lr_0_0001 |  | 0.000500 | recent_leader_warmup |
