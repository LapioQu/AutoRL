# Real-Stream Benchmark Replay

- dataset: `pollution_8000 calibration`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `1759`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_002`
- switch_count: `3`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.844067 |
| knn_regressor | 0.845342 |
| lin_lr_0_002 | 0.846360 |
| lin_lr_0_005 | 0.843745 |
| lin_lr_0_01 | 0.761065 |
| pa_regressor | 0.842640 |

- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.846360`
- adaptive_delta_vs_best_fixed: `-0.002293`
- block_delta_mean: `-0.002334`
- block_delta_ci95: `0.014649`
- block_count: `27`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_warmup_same |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 383 | stay | knn_regressor | lin_lr_0_01 | 0.021751 | 0.001000 | recent_leader_incumbent_floor |
| 447 | stay | knn_regressor | lin_lr_0_01 | 0.018695 | 0.001000 | recent_leader_incumbent_floor |
| 511 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 575 | stay | knn_regressor | lin_lr_0_005 | 0.021170 | 0.001000 | recent_leader_incumbent_floor |
| 639 | stay | knn_regressor | lin_lr_0_002 | 0.032291 | 0.001000 | recent_leader_incumbent_floor |
| 703 | stay | knn_regressor | lin_lr_0_002 | 0.025768 | 0.001000 | recent_leader_incumbent_floor |
| 767 | stay | knn_regressor | lin_lr_0_002 | 0.029278 | 0.001000 | recent_leader_incumbent_floor |
| 831 | stay | knn_regressor | lin_lr_0_005 | 0.040888 | 0.001000 | recent_leader_incumbent_floor |
| 895 | switch | knn_regressor | lin_lr_0_005 | 0.034604 | 0.001000 | recent_leader_advantage |
| 959 | stay | lin_lr_0_005 | lin_lr_0_005 | 0.000000 | 0.001000 | recent_leader_cooldown |
| 1023 | switch | lin_lr_0_005 | knn_regressor | 0.037274 | 0.001000 | recent_leader_advantage |
| 1087 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_cooldown |
| 1151 | stay | knn_regressor | pa_regressor | 0.022576 | 0.001000 | recent_leader_incumbent_floor |
| 1215 | stay | knn_regressor | pa_regressor | 0.032346 | 0.001000 | recent_leader_incumbent_floor |
| 1279 | stay | knn_regressor | pa_regressor | 0.032273 | 0.001000 | recent_leader_incumbent_floor |
| 1343 | stay | knn_regressor | lin_lr_0_01 | 0.029281 | 0.001000 | recent_leader_incumbent_floor |

... truncated 6 additional decision rows in `decisions.csv`.
