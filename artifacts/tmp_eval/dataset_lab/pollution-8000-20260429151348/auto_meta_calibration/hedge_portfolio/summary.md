# Real-Stream Benchmark Replay

- dataset: `pollution_8000 calibration`
- score_name: `normalized_reward`
- policy_name: `hedge_portfolio`
- samples: `1759`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_002`
- switch_count: `3`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.842513 |
| knn_regressor | 0.845342 |
| lin_lr_0_002 | 0.846360 |
| lin_lr_0_005 | 0.843745 |
| lin_lr_0_01 | 0.761065 |
| pa_regressor | 0.842640 |

- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.846360`
- adaptive_delta_vs_best_fixed: `-0.003847`
- block_delta_mean: `-0.003916`
- block_delta_ci95: `0.014781`
- block_count: `27`

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
| 895 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 959 | switch | knn_regressor | lin_lr_0_005 | 0.019627 | 0.010000 | hedge_weight_advantage |
| 1023 | switch | lin_lr_0_005 | knn_regressor | 0.779815 | 0.010000 | hedge_weight_advantage |
| 1087 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 1151 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 1215 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |
| 1279 | stay | knn_regressor | knn_regressor | 0.000000 | 0.010000 | hedge_same_leader |

... truncated 7 additional decision rows in `decisions.csv`.
