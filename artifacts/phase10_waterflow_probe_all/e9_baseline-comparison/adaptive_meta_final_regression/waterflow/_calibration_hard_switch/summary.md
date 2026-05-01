# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `317`
- source: Real pipeline water-flow stream replayed in temporal order.
- source_url: ``
- start_strategy: `river_linreg`
- final_strategy: `river_linreg`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.510585 |
| river_hoeffding_tree | 0.613862 |
| river_linreg | 0.510585 |
| river_pa | 0.630479 |
| windowed_histgb | 0.650393 |
| windowed_rf | 0.801567 |

- best_fixed_strategy: `windowed_rf`
- best_fixed_score: `0.801567`
- adaptive_delta_vs_best_fixed: `-0.290982`
- block_delta_mean: `-0.369060`
- block_delta_ci95: `0.208826`
- block_count: `4`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 191 | stay | river_linreg | windowed_rf | 0.434952 | 0.007000 | high_uncertainty |
| 255 | stay | river_linreg | windowed_rf | 0.269395 | 0.007000 | high_uncertainty |
