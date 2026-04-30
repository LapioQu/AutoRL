# Real-Stream Benchmark Replay

- dataset: `pollution calibration`
- score_name: `normalized_reward`
- policy_name: `hedge_portfolio`
- samples: `879`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.817943 |
| knn_regressor | 0.817943 |
| lin_lr_0_002 | 0.815017 |
| lin_lr_0_005 | 0.819864 |
| lin_lr_0_01 | 0.782051 |
| pa_regressor | 0.805671 |

- best_fixed_strategy: `lin_lr_0_005`
- best_fixed_score: `0.819864`
- adaptive_delta_vs_best_fixed: `-0.001921`
- block_delta_mean: `0.001831`
- block_delta_ci95: `0.024711`
- block_count: `13`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 383 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 447 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 511 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 575 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 639 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 703 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 767 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 831 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
