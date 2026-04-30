# Real-Stream Benchmark Replay

- dataset: `pollution`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `3997`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `lin_lr_0_002`
- switch_count: `4`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.837387 |
| knn_regressor | 0.817489 |
| lin_lr_0_002 | 0.838480 |
| lin_lr_0_01 | 0.324039 |
| pa_regressor | 0.822280 |

- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.838480`
- adaptive_delta_vs_best_fixed: `-0.001093`
- block_delta_mean: `-0.001101`
- block_delta_ci95: `0.007494`
- block_count: `62`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_warmup_same |
| 191 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 255 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 319 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 383 | stay | knn_regressor | lin_lr_0_01 | 0.023197 | 0.001000 | recent_leader_incumbent_floor |
| 447 | stay | knn_regressor | lin_lr_0_01 | 0.019005 | 0.001000 | recent_leader_incumbent_floor |
| 511 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_same |
| 575 | stay | knn_regressor | pa_regressor | 0.022064 | 0.001000 | recent_leader_incumbent_floor |
| 639 | stay | knn_regressor | lin_lr_0_002 | 0.035103 | 0.001000 | recent_leader_incumbent_floor |
| 703 | stay | knn_regressor | lin_lr_0_002 | 0.028750 | 0.001000 | recent_leader_incumbent_floor |
| 767 | stay | knn_regressor | lin_lr_0_002 | 0.033224 | 0.001000 | recent_leader_incumbent_floor |
| 831 | stay | knn_regressor | pa_regressor | 0.047116 | 0.001000 | recent_leader_incumbent_floor |
| 895 | switch | knn_regressor | lin_lr_0_002 | 0.072715 | 0.001000 | recent_leader_advantage |
| 959 | stay | lin_lr_0_002 | lin_lr_0_002 | 0.000000 | 0.001000 | recent_leader_cooldown |
| 1023 | switch | lin_lr_0_002 | knn_regressor | 0.017943 | 0.001000 | recent_leader_advantage |
| 1087 | stay | knn_regressor | knn_regressor | 0.000000 | 0.001000 | recent_leader_cooldown |
| 1151 | stay | knn_regressor | pa_regressor | 0.029382 | 0.001000 | recent_leader_incumbent_floor |
| 1215 | stay | knn_regressor | pa_regressor | 0.050893 | 0.001000 | recent_leader_incumbent_floor |
| 1279 | switch | knn_regressor | pa_regressor | 0.053486 | 0.001000 | recent_leader_advantage |
| 1343 | stay | pa_regressor | pa_regressor | 0.000000 | 0.001000 | recent_leader_cooldown |

... truncated 41 additional decision rows in `decisions.csv`.
