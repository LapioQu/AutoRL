# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `45312`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `river_logreg`
- final_strategy: `river_logreg`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.876523 |
| river_hoeffding_tree | 0.830067 |
| river_logreg | 0.876832 |
| river_nb | 0.728725 |
| windowed_histgb | 0.787076 |
| windowed_rf | 0.801774 |

- best_fixed_strategy: `river_logreg`
- best_fixed_score: `0.876832`
- adaptive_delta_vs_best_fixed: `-0.000309`
- block_delta_mean: `-0.000309`
- block_delta_ci95: `0.000605`
- block_count: `354`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | river_logreg | river_nb |  | 0.000000 | recent_leader_warmup |
| 255 | switch | river_nb | river_logreg | 0.109375 | 0.000000 | recent_leader_advantage |
| 383 | stay | river_logreg | river_logreg | 0.000000 | 0.000000 | recent_leader_same |
| 511 | stay | river_logreg | river_logreg | 0.000000 | 0.000000 | recent_leader_same |
| 639 | stay | river_logreg | river_logreg | 0.000000 | 0.000000 | recent_leader_same |
| 767 | stay | river_logreg | windowed_rf | 0.031250 | 0.000000 | recent_leader_incumbent_floor |
| 895 | stay | river_logreg | river_logreg | 0.000000 | 0.000000 | recent_leader_same |
| 1023 | stay | river_logreg | river_logreg | 0.000000 | 0.000000 | recent_leader_same |
| 1151 | stay | river_logreg | river_hoeffding_tree | 0.070312 | 0.000000 | recent_leader_incumbent_floor |
| 1279 | stay | river_logreg | river_hoeffding_tree | 0.031250 | 0.000000 | recent_leader_incumbent_floor |
| 1407 | stay | river_logreg | windowed_histgb | 0.054688 | 0.000000 | recent_leader_incumbent_floor |
| 1535 | stay | river_logreg | river_hoeffding_tree | 0.046875 | 0.000000 | recent_leader_incumbent_floor |
| 1663 | stay | river_logreg | river_hoeffding_tree | 0.007812 | 0.000000 | recent_leader_incumbent_floor |
| 1791 | stay | river_logreg | river_nb | 0.062500 | 0.000000 | recent_leader_incumbent_floor |
| 1919 | stay | river_logreg | river_hoeffding_tree | 0.023438 | 0.000000 | recent_leader_incumbent_floor |
| 2047 | stay | river_logreg | river_nb | 0.023438 | 0.000000 | recent_leader_incumbent_floor |
| 2175 | stay | river_logreg | river_logreg | 0.000000 | 0.000000 | recent_leader_same |
| 2303 | stay | river_logreg | windowed_histgb | 0.031250 | 0.000000 | recent_leader_incumbent_floor |
| 2431 | stay | river_logreg | river_logreg | 0.000000 | 0.000000 | recent_leader_same |
| 2559 | stay | river_logreg | windowed_histgb | 0.023438 | 0.000000 | recent_leader_incumbent_floor |

... truncated 334 additional decision rows in `decisions.csv`.
