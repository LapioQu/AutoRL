# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `256`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `pa_regressor`
- final_strategy: `pa_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.697019 |
| lin_lr_0_0005 | 0.534182 |
| lin_lr_0_001 | 0.547883 |
| pa_regressor | 0.697019 |

- best_fixed_strategy: `pa_regressor`
- best_fixed_score: `0.697019`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `10`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 47 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_warmup_same |
| 71 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 95 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 119 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 143 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 167 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 191 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 215 | stay | pa_regressor | lin_lr_0_001 | 0.015483 | 0.002000 | recent_leader_incumbent_floor |
| 239 | stay | pa_regressor | lin_lr_0_001 | 0.022232 | 0.002000 | recent_leader_incumbent_floor |
