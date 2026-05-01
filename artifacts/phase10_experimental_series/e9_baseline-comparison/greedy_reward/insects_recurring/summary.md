# Real-Stream Benchmark Replay

- dataset: `InsectsRecurring`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `79986`
- source: USP DS Repository INSECTS recurring-drift stream replayed in temporal order; target is the insect class under recurring concept drift.
- source_url: `https://sites.google.com/view/uspdsrepository`
- start_strategy: `river_logreg`
- final_strategy: `river_logreg`
- switch_count: `11`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.771372 |
| oracle | 0.924987 |
| river_hoeffding_tree | 0.558648 |
| river_logreg | 0.772510 |
| river_nb | 0.487035 |
| windowed_histgb | 0.765434 |
| windowed_rf | 0.766697 |

- best_fixed_strategy: `river_logreg`
- best_fixed_score: `0.772510`
- oracle_score: `0.924987`
- oracle_gain: `0.152477`
- oracle_capture_ratio: `0.000000`
- adaptive_delta_vs_best_fixed: `-0.001138`
- block_delta_mean: `-0.001139`
- block_delta_ci95: `0.002413`
- block_count: `624`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | river_logreg | river_nb |  | 0.000000 | recent_leader_warmup |
| 255 | stay | river_nb | river_logreg | 0.070312 | 0.000000 | recent_leader_incumbent_floor |
| 383 | switch | river_nb | windowed_rf | 0.250000 | 0.000000 | recent_leader_advantage |
| 511 | stay | windowed_rf | river_logreg | 0.007812 | 0.000000 | recent_leader_incumbent_floor |
| 639 | stay | windowed_rf | windowed_rf | 0.000000 | 0.000000 | recent_leader_same |
| 767 | stay | windowed_rf | windowed_histgb | 0.023438 | 0.000000 | recent_leader_incumbent_floor |
| 895 | stay | windowed_rf | windowed_rf | 0.000000 | 0.000000 | recent_leader_same |
| 1023 | switch | windowed_rf | river_logreg | 0.351562 | 0.000000 | recent_leader_advantage |
| 1151 | stay | river_logreg | river_logreg | 0.000000 | 0.000000 | recent_leader_same |
| 1279 | stay | river_logreg | windowed_rf | 0.023438 | 0.000000 | recent_leader_incumbent_floor |
| 1407 | stay | river_logreg | river_logreg | 0.000000 | 0.000000 | recent_leader_same |
| 1535 | stay | river_logreg | windowed_rf | 0.007812 | 0.000000 | recent_leader_incumbent_floor |
| 1663 | stay | river_logreg | river_logreg | 0.000000 | 0.000000 | recent_leader_same |
| 1791 | stay | river_logreg | windowed_rf | 0.031250 | 0.000000 | recent_leader_incumbent_floor |
| 1919 | stay | river_logreg | river_hoeffding_tree | 0.062500 | 0.000000 | recent_leader_incumbent_floor |
| 2047 | stay | river_logreg | river_logreg | 0.000000 | 0.000000 | recent_leader_same |
| 2175 | stay | river_logreg | river_logreg | 0.000000 | 0.000000 | recent_leader_same |
| 2303 | stay | river_logreg | river_hoeffding_tree | 0.007812 | 0.000000 | recent_leader_incumbent_floor |
| 2431 | stay | river_logreg | river_logreg | 0.000000 | 0.000000 | recent_leader_same |
| 2559 | stay | river_logreg | windowed_rf | 0.031250 | 0.000000 | recent_leader_incumbent_floor |

... truncated 604 additional decision rows in `decisions.csv`.
