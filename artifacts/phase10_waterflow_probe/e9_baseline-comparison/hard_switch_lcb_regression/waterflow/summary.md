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
| adaptive | 0.789125 |
| river_hoeffding_tree | 0.722908 |
| river_linreg | 0.803945 |
| river_pa | 0.726507 |
| windowed_histgb | 0.777751 |
| windowed_rf | 0.854192 |

- best_fixed_strategy: `windowed_rf`
- best_fixed_score: `0.854192`
- adaptive_delta_vs_best_fixed: `-0.065067`
- block_delta_mean: `-0.067849`
- block_delta_ci95: `0.085192`
- block_count: `19`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 191 | stay | river_linreg | windowed_rf | 0.434952 | 0.007000 | high_uncertainty |
| 255 | stay | river_linreg | windowed_rf | 0.269395 | 0.007000 | high_uncertainty |
| 319 | stay | river_linreg | windowed_rf | 0.120721 | 0.007000 | high_uncertainty |
| 383 | stay | river_linreg | windowed_rf | -0.037217 | 0.007000 | high_uncertainty |
| 447 | stay | river_linreg | windowed_rf | -0.115922 | 0.007000 | high_uncertainty |
| 511 | stay | river_linreg | windowed_rf | -0.065034 | 0.007000 | high_uncertainty |
| 575 | stay | river_linreg | windowed_rf | 0.011190 | 0.007000 | high_uncertainty |
| 639 | switch | river_linreg | windowed_rf | 0.031196 | 0.007000 | switch_advantage |
| 703 | stay | windowed_rf | windowed_histgb | -0.008267 | 0.007000 | no_candidate_improvement |
| 767 | stay | windowed_rf | windowed_histgb | -0.002263 | 0.007000 | high_uncertainty |
| 831 | stay | windowed_rf | windowed_histgb | 0.004354 | 0.007000 | no_candidate_improvement |
| 895 | stay | windowed_rf | windowed_histgb | 0.001043 | 0.007000 | high_uncertainty |
| 959 | stay | windowed_rf | river_linreg | -0.022895 | 0.007000 | high_uncertainty |
| 1023 | stay | windowed_rf | river_linreg | 0.081594 | 0.007000 | high_uncertainty |
| 1087 | stay | windowed_rf | river_linreg | 0.176685 | 0.007000 | high_uncertainty |
| 1151 | stay | windowed_rf | river_linreg | 0.132683 | 0.007000 | high_uncertainty |
| 1215 | stay | windowed_rf | river_linreg | 0.026629 | 0.007000 | high_uncertainty |
