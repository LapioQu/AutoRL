# Real-Stream Benchmark Replay

- dataset: `WaterFlow calibration`
- score_name: `normalized_reward`
- policy_name: `hedge_portfolio`
- samples: `278`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.908057 |
| knn_regressor | 0.908057 |
| lin_lr_0_002 | 0.541571 |
| lin_lr_0_005 | 0.577097 |
| lin_lr_0_01 | 0.591598 |
| pa_regressor | 0.634937 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.908057`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `4`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
