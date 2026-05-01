# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `1268`
- source: Real pipeline water-flow stream replayed in temporal order.
- source_url: ``
- start_strategy: `river_linreg`
- final_strategy: `windowed_rf`
- switch_count: `6`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.834057 |
| river_hoeffding_tree | 0.719801 |
| river_linreg | 0.803945 |
| river_pa | 0.726507 |
| windowed_histgb | 0.777751 |
| windowed_rf | 0.854192 |

- best_fixed_strategy: `windowed_rf`
- best_fixed_score: `0.854192`
- adaptive_delta_vs_best_fixed: `-0.020135`
- block_delta_mean: `-0.020996`
- block_delta_ci95: `0.076770`
- block_count: `19`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | switch | river_linreg | river_hoeffding_tree |  | 0.010000 | fixed_share_warmup_leader |
| 63 | stay | river_hoeffding_tree | windowed_rf | 0.002459 | 0.010000 | fixed_share_margin_too_small |
| 127 | switch | river_hoeffding_tree | windowed_rf | 0.193460 | 0.010000 | fixed_share_weight_advantage |
| 191 | stay | windowed_rf | windowed_rf | 0.000000 | 0.010000 | fixed_share_same_leader |
| 255 | stay | windowed_rf | windowed_rf | 0.000000 | 0.010000 | fixed_share_same_leader |
| 319 | stay | windowed_rf | windowed_rf | 0.000000 | 0.010000 | fixed_share_same_leader |
| 383 | switch | windowed_rf | river_linreg | 0.366450 | 0.010000 | fixed_share_weight_advantage |
| 447 | stay | river_linreg | windowed_rf | 0.002092 | 0.010000 | fixed_share_margin_too_small |
| 511 | switch | river_linreg | windowed_rf | 0.032624 | 0.010000 | fixed_share_weight_advantage |
| 575 | stay | windowed_rf | windowed_histgb | 0.000325 | 0.010000 | fixed_share_margin_too_small |
| 639 | stay | windowed_rf | windowed_rf | 0.000000 | 0.010000 | fixed_share_same_leader |
| 703 | stay | windowed_rf | windowed_rf | 0.000000 | 0.010000 | fixed_share_same_leader |
| 767 | stay | windowed_rf | river_linreg | 0.008894 | 0.010000 | fixed_share_margin_too_small |
| 831 | stay | windowed_rf | windowed_histgb | 0.004406 | 0.010000 | fixed_share_margin_too_small |
| 895 | stay | windowed_rf | windowed_rf | 0.000000 | 0.010000 | fixed_share_same_leader |
| 959 | switch | windowed_rf | river_linreg | 0.244038 | 0.010000 | fixed_share_weight_advantage |
| 1023 | stay | river_linreg | river_linreg | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1087 | stay | river_linreg | river_linreg | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1151 | stay | river_linreg | windowed_rf | 0.001685 | 0.010000 | fixed_share_margin_too_small |
| 1215 | switch | river_linreg | windowed_rf | 0.024353 | 0.010000 | fixed_share_weight_advantage |
