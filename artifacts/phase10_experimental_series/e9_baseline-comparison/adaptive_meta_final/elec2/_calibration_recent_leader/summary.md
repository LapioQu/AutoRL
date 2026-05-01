# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `2048`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `river_logreg`
- final_strategy: `river_logreg`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.879395 |
| river_hoeffding_tree | 0.882324 |
| river_logreg | 0.884766 |
| river_nb | 0.810547 |
| windowed_histgb | 0.781738 |
| windowed_rf | 0.831055 |

- best_fixed_strategy: `river_logreg`
- best_fixed_score: `0.884766`
- adaptive_delta_vs_best_fixed: `-0.005371`
- block_delta_mean: `-0.005371`
- block_delta_ci95: `0.010193`
- block_count: `16`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 255 | switch | river_logreg | river_hoeffding_tree |  | 0.002000 | recent_leader_warmup |
| 383 | stay | river_hoeffding_tree | river_hoeffding_tree | 0.000000 | 0.002000 | recent_leader_cooldown |
| 511 | switch | river_hoeffding_tree | river_logreg | 0.042969 | 0.002000 | recent_leader_advantage |
| 639 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_cooldown |
| 767 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_same |
| 895 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_same |
| 1023 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_same |
| 1151 | stay | river_logreg | river_hoeffding_tree | 0.035156 | 0.002000 | recent_leader_incumbent_floor |
| 1279 | stay | river_logreg | river_hoeffding_tree | 0.050781 | 0.002000 | recent_leader_incumbent_floor |
| 1407 | stay | river_logreg | windowed_histgb | 0.042969 | 0.002000 | recent_leader_incumbent_floor |
| 1535 | stay | river_logreg | windowed_histgb | 0.050781 | 0.002000 | recent_leader_incumbent_floor |
| 1663 | stay | river_logreg | river_hoeffding_tree | 0.027344 | 0.002000 | recent_leader_incumbent_floor |
| 1791 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_same |
| 1919 | stay | river_logreg | river_nb | 0.027344 | 0.002000 | recent_leader_incumbent_floor |
| 2047 | stay | river_logreg | river_nb | 0.007812 | 0.002000 | recent_leader_incumbent_floor |
