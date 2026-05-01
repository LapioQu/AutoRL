# Real-Stream Benchmark Replay

- dataset: `InsectsRecurring`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `2048`
- source: USP DS Repository INSECTS recurring-drift stream replayed in temporal order; target is the insect class under recurring concept drift.
- source_url: `https://sites.google.com/view/uspdsrepository`
- start_strategy: `river_logreg`
- final_strategy: `river_logreg`
- switch_count: `3`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.685059 |
| oracle | 0.898438 |
| river_hoeffding_tree | 0.490234 |
| river_logreg | 0.733887 |
| river_nb | 0.612793 |
| windowed_histgb | 0.682129 |
| windowed_rf | 0.710449 |

- best_fixed_strategy: `river_logreg`
- best_fixed_score: `0.733887`
- oracle_score: `0.898438`
- oracle_gain: `0.164551`
- oracle_capture_ratio: `0.000000`
- adaptive_delta_vs_best_fixed: `-0.048828`
- block_delta_mean: `-0.048828`
- block_delta_ci95: `0.060308`
- block_count: `16`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 255 | switch | river_logreg | river_nb |  | 0.002000 | recent_leader_warmup |
| 383 | stay | river_nb | river_nb | 0.000000 | 0.002000 | recent_leader_cooldown |
| 511 | switch | river_nb | windowed_rf | 0.285156 | 0.002000 | recent_leader_advantage |
| 639 | stay | windowed_rf | windowed_rf | 0.000000 | 0.002000 | recent_leader_cooldown |
| 767 | stay | windowed_rf | windowed_rf | 0.000000 | 0.002000 | recent_leader_same |
| 895 | stay | windowed_rf | windowed_histgb | 0.003906 | 0.002000 | recent_leader_incumbent_floor |
| 1023 | switch | windowed_rf | river_logreg | 0.156250 | 0.002000 | recent_leader_advantage |
| 1151 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_cooldown |
| 1279 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_same |
| 1407 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_same |
| 1535 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_same |
| 1663 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_same |
| 1791 | stay | river_logreg | windowed_rf | 0.011719 | 0.002000 | recent_leader_incumbent_floor |
| 1919 | stay | river_logreg | windowed_rf | 0.042969 | 0.002000 | recent_leader_incumbent_floor |
| 2047 | stay | river_logreg | river_nb | 0.011719 | 0.002000 | recent_leader_incumbent_floor |
