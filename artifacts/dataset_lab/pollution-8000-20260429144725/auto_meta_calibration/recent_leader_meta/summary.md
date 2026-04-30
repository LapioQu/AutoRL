# Real-Stream Benchmark Replay

- dataset: `pollution-8000 calibration`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `1759`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_002`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.843590 |
| knn_regressor | 0.839243 |
| lin_lr_0_002 | 0.846360 |
| lin_lr_0_01 | 0.761065 |
| pa_regressor | 0.842640 |

- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.846360`
- adaptive_delta_vs_best_fixed: `-0.002769`
- block_delta_mean: `-0.002819`
- block_delta_ci95: `0.015808`
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
| 575 | stay | knn_regressor | pa_regressor | 0.021168 | 0.001000 | recent_leader_incumbent_floor |
| 639 | stay | knn_regressor | lin_lr_0_002 | 0.032291 | 0.001000 | recent_leader_incumbent_floor |
| 703 | stay | knn_regressor | lin_lr_0_002 | 0.025768 | 0.001000 | recent_leader_incumbent_floor |
| 767 | stay | knn_regressor | lin_lr_0_002 | 0.029119 | 0.001000 | recent_leader_incumbent_floor |
| 831 | stay | knn_regressor | pa_regressor | 0.036633 | 0.001000 | recent_leader_incumbent_floor |
| 895 | stay | knn_regressor | lin_lr_0_002 | 0.042700 | 0.001000 | recent_leader_incumbent_floor |
| 959 | stay | knn_regressor | lin_lr_0_002 | 0.021469 | 0.001000 | recent_leader_incumbent_floor |
| 1023 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 1087 | stay | knn_regressor | pa_regressor | 0.014316 | 0.001000 | recent_leader_incumbent_floor |
| 1151 | stay | knn_regressor | pa_regressor | 0.032026 | 0.001000 | recent_leader_incumbent_floor |
| 1215 | stay | knn_regressor | pa_regressor | 0.033151 | 0.001000 | recent_leader_incumbent_floor |
| 1279 | stay | knn_regressor | pa_regressor | 0.047848 | 0.001000 | recent_leader_incumbent_floor |
| 1343 | stay | knn_regressor | lin_lr_0_01 | 0.054673 | 0.001000 | recent_leader_incumbent_floor |

... truncated 6 additional decision rows in `decisions.csv`.
