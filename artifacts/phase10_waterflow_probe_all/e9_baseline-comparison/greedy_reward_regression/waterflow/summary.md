# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `1268`
- source: Real pipeline water-flow stream replayed in temporal order.
- source_url: ``
- start_strategy: `river_linreg`
- final_strategy: `windowed_rf`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.814857 |
| river_hoeffding_tree | 0.719801 |
| river_linreg | 0.803945 |
| river_pa | 0.726507 |
| windowed_histgb | 0.777751 |
| windowed_rf | 0.854192 |

- best_fixed_strategy: `windowed_rf`
- best_fixed_score: `0.854192`
- adaptive_delta_vs_best_fixed: `-0.039335`
- block_delta_mean: `-0.041017`
- block_delta_ci95: `0.070127`
- block_count: `19`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | switch | river_linreg | river_hoeffding_tree |  | 0.000000 | recent_leader_warmup |
| 127 | switch | river_hoeffding_tree | windowed_rf | 0.081106 | 0.000000 | recent_leader_advantage |
| 191 | stay | windowed_rf | windowed_rf | 0.000000 | 0.000000 | recent_leader_same |
| 255 | stay | windowed_rf | windowed_rf | 0.000000 | 0.000000 | recent_leader_same |
| 319 | stay | windowed_rf | river_linreg | 0.031565 | 0.000000 | recent_leader_incumbent_floor |
| 383 | stay | windowed_rf | river_linreg | 0.193180 | 0.000000 | recent_leader_incumbent_floor |
| 447 | stay | windowed_rf | river_linreg | 0.045763 | 0.000000 | recent_leader_incumbent_floor |
| 511 | stay | windowed_rf | windowed_rf | 0.000000 | 0.000000 | recent_leader_same |
| 575 | stay | windowed_rf | windowed_histgb | 0.001384 | 0.000000 | recent_leader_incumbent_floor |
| 639 | stay | windowed_rf | windowed_rf | 0.000000 | 0.000000 | recent_leader_same |
| 703 | stay | windowed_rf | windowed_rf | 0.000000 | 0.000000 | recent_leader_same |
| 767 | stay | windowed_rf | windowed_histgb | 0.008823 | 0.000000 | recent_leader_incumbent_floor |
| 831 | stay | windowed_rf | windowed_histgb | 0.000199 | 0.000000 | recent_leader_incumbent_floor |
| 895 | stay | windowed_rf | windowed_rf | 0.000000 | 0.000000 | recent_leader_same |
| 959 | stay | windowed_rf | river_pa | 0.229885 | 0.000000 | recent_leader_incumbent_floor |
| 1023 | stay | windowed_rf | river_linreg | 0.226946 | 0.000000 | recent_leader_incumbent_floor |
| 1087 | stay | windowed_rf | river_linreg | 0.160273 | 0.000000 | recent_leader_incumbent_floor |
| 1151 | stay | windowed_rf | windowed_rf | 0.000000 | 0.000000 | recent_leader_same |
| 1215 | stay | windowed_rf | windowed_rf | 0.000000 | 0.000000 | recent_leader_same |
