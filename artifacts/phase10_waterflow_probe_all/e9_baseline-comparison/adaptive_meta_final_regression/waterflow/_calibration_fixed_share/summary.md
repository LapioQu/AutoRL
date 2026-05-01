# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `317`
- source: Real pipeline water-flow stream replayed in temporal order.
- source_url: ``
- start_strategy: `river_linreg`
- final_strategy: `windowed_rf`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.646040 |
| river_hoeffding_tree | 0.613862 |
| river_linreg | 0.510585 |
| river_pa | 0.630479 |
| windowed_histgb | 0.650393 |
| windowed_rf | 0.801567 |

- best_fixed_strategy: `windowed_rf`
- best_fixed_score: `0.801567`
- adaptive_delta_vs_best_fixed: `-0.155527`
- block_delta_mean: `-0.192586`
- block_delta_ci95: `0.282874`
- block_count: `4`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 63 | switch | river_linreg | river_hoeffding_tree |  | 0.010000 | fixed_share_warmup_leader |
| 63 | stay | river_hoeffding_tree | windowed_rf | 0.002459 | 0.010000 | fixed_share_margin_too_small |
| 127 | switch | river_hoeffding_tree | windowed_rf | 0.193460 | 0.010000 | fixed_share_weight_advantage |
| 191 | stay | windowed_rf | windowed_rf | 0.000000 | 0.010000 | fixed_share_same_leader |
| 255 | stay | windowed_rf | windowed_rf | 0.000000 | 0.010000 | fixed_share_same_leader |
