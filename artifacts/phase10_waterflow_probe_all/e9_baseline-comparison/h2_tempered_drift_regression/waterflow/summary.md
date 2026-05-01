# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `1268`
- source: Real pipeline water-flow stream replayed in temporal order.
- source_url: ``
- start_strategy: `river_linreg`
- final_strategy: `windowed_rf`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.824297 |
| river_hoeffding_tree | 0.776688 |
| river_linreg | 0.839073 |
| river_pa | 0.780066 |
| windowed_histgb | 0.816860 |
| windowed_rf | 0.878059 |

- best_fixed_strategy: `windowed_rf`
- best_fixed_score: `0.878059`
- adaptive_delta_vs_best_fixed: `-0.053762`
- block_delta_mean: `-0.056061`
- block_delta_ci95: `0.073733`
- block_count: `19`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 191 | stay | river_linreg | windowed_rf | 0.368183 | 0.007000 | high_uncertainty |
| 255 | stay | river_linreg | windowed_rf | 0.220501 | 0.007000 | high_uncertainty |
| 319 | stay | river_linreg | windowed_rf | 0.094096 | 0.007000 | high_uncertainty |
| 383 | stay | river_linreg | windowed_rf | -0.040461 | 0.007000 | high_uncertainty |
| 447 | stay | river_linreg | windowed_rf | -0.104463 | 0.007000 | high_uncertainty |
| 511 | stay | river_linreg | windowed_rf | -0.058228 | 0.007000 | high_uncertainty |
| 575 | stay | river_linreg | windowed_rf | 0.006892 | 0.007000 | high_uncertainty |
| 639 | switch | river_linreg | windowed_rf | 0.023980 | 0.007000 | switch_advantage |
| 703 | stay | windowed_rf | windowed_histgb | -0.006277 | 0.007000 | no_candidate_improvement |
| 767 | stay | windowed_rf | windowed_histgb | -0.001724 | 0.007000 | no_candidate_improvement |
| 831 | stay | windowed_rf | windowed_histgb | 0.003302 | 0.007000 | no_candidate_improvement |
| 895 | stay | windowed_rf | windowed_histgb | 0.000847 | 0.007000 | high_uncertainty |
| 959 | stay | windowed_rf | river_linreg | -0.010304 | 0.007000 | high_uncertainty |
| 1023 | stay | windowed_rf | river_hoeffding_tree | 0.097373 | 0.007000 | high_uncertainty |
| 1087 | stay | windowed_rf | river_linreg | 0.158182 | 0.007000 | high_uncertainty |
| 1151 | stay | windowed_rf | river_linreg | 0.114198 | 0.007000 | high_uncertainty |
| 1215 | stay | windowed_rf | river_linreg | 0.024128 | 0.007000 | high_uncertainty |
