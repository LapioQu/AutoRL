# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `317`
- source: Real pipeline water-flow stream replayed in temporal order.
- source_url: ``
- start_strategy: `river_linreg`
- final_strategy: `windowed_rf`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.585697 |
| river_hoeffding_tree | 0.613862 |
| river_linreg | 0.510585 |
| river_pa | 0.630479 |
| windowed_histgb | 0.650393 |
| windowed_rf | 0.801567 |

- best_fixed_strategy: `windowed_rf`
- best_fixed_score: `0.801567`
- adaptive_delta_vs_best_fixed: `-0.215871`
- block_delta_mean: `-0.267308`
- block_delta_ci95: `0.285443`
- block_count: `4`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | river_linreg | windowed_rf |  | 0.002000 | recent_leader_warmup |
| 191 | stay | windowed_rf | windowed_rf | 0.000000 | 0.002000 | recent_leader_cooldown |
| 255 | stay | windowed_rf | windowed_rf | 0.000000 | 0.002000 | recent_leader_same |
