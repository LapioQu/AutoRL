# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `256`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `pa_regressor`
- final_strategy: `pa_regressor`
- switch_count: `3`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.683044 |
| lin_lr_0_0005 | 0.534182 |
| lin_lr_0_001 | 0.547883 |
| pa_regressor | 0.697019 |

- best_fixed_strategy: `pa_regressor`
- best_fixed_score: `0.697019`
- adaptive_delta_vs_best_fixed: `-0.013974`
- block_delta_mean: `-0.014906`
- block_delta_ci95: `0.029608`
- block_count: `10`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 23 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 47 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 71 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 95 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 119 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 143 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 167 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | switch | pa_regressor | lin_lr_0_0005 | 0.236307 | 0.010000 | fixed_share_weight_advantage |
| 215 | switch | lin_lr_0_0005 | lin_lr_0_001 | 0.154138 | 0.010000 | fixed_share_weight_advantage |
| 239 | switch | lin_lr_0_001 | pa_regressor | 0.341927 | 0.010000 | fixed_share_weight_advantage |
