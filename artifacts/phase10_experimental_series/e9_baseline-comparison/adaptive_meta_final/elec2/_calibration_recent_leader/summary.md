# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `2048`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `river_logreg`
- final_strategy: `river_hoeffding_tree`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.884766 |
| oracle | 0.966797 |
| river_hoeffding_tree | 0.887207 |
| river_logreg | 0.884766 |
| river_nb | 0.810547 |
| windowed_histgb | 0.781738 |
| windowed_rf | 0.831055 |

- best_fixed_strategy: `river_hoeffding_tree`
- best_fixed_score: `0.887207`
- oracle_score: `0.966797`
- oracle_gain: `0.079590`
- oracle_capture_ratio: `0.000000`
- adaptive_delta_vs_best_fixed: `-0.002441`
- block_delta_mean: `-0.002441`
- block_delta_ci95: `0.027295`
- block_count: `16`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 255 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_warmup_same |
| 383 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_same |
| 511 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_same |
| 639 | stay | river_logreg | river_hoeffding_tree | 0.011719 | 0.002000 | recent_leader_incumbent_floor |
| 767 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_same |
| 895 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_same |
| 1023 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_same |
| 1151 | stay | river_logreg | river_hoeffding_tree | 0.042969 | 0.002000 | recent_leader_incumbent_floor |
| 1279 | stay | river_logreg | river_hoeffding_tree | 0.046875 | 0.002000 | recent_leader_incumbent_floor |
| 1407 | stay | river_logreg | windowed_histgb | 0.042969 | 0.002000 | recent_leader_incumbent_floor |
| 1535 | stay | river_logreg | windowed_histgb | 0.050781 | 0.002000 | recent_leader_incumbent_floor |
| 1663 | stay | river_logreg | river_hoeffding_tree | 0.015625 | 0.002000 | recent_leader_incumbent_floor |
| 1791 | stay | river_logreg | river_logreg | 0.000000 | 0.002000 | recent_leader_same |
| 1919 | stay | river_logreg | river_nb | 0.027344 | 0.002000 | recent_leader_incumbent_floor |
| 2047 | switch | river_logreg | river_hoeffding_tree | 0.046875 | 0.002000 | recent_leader_advantage |
