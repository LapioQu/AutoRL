# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `2048`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `river_logreg`
- final_strategy: `river_hoeffding_tree`
- switch_count: `10`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.868164 |
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
- adaptive_delta_vs_best_fixed: `-0.019043`
- block_delta_mean: `-0.019043`
- block_delta_ci95: `0.025679`
- block_count: `16`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | river_logreg | river_nb |  | 0.010000 | fixed_share_warmup_leader |
| 127 | stay | river_nb | river_nb | 0.000000 | 0.010000 | fixed_share_same_leader |
| 255 | switch | river_nb | river_logreg | 0.139119 | 0.010000 | fixed_share_weight_advantage |
| 383 | stay | river_logreg | river_logreg | 0.000000 | 0.010000 | fixed_share_same_leader |
| 511 | switch | river_logreg | river_nb | 0.024322 | 0.010000 | fixed_share_weight_advantage |
| 639 | switch | river_nb | river_hoeffding_tree | 0.154849 | 0.010000 | fixed_share_weight_advantage |
| 767 | switch | river_hoeffding_tree | windowed_rf | 0.040072 | 0.010000 | fixed_share_weight_advantage |
| 895 | switch | windowed_rf | windowed_histgb | 0.186563 | 0.010000 | fixed_share_weight_advantage |
| 1023 | switch | windowed_histgb | river_logreg | 0.105859 | 0.010000 | fixed_share_weight_advantage |
| 1151 | switch | river_logreg | river_hoeffding_tree | 0.028725 | 0.010000 | fixed_share_weight_advantage |
| 1279 | stay | river_hoeffding_tree | windowed_histgb | 0.007974 | 0.010000 | fixed_share_margin_too_small |
| 1407 | stay | river_hoeffding_tree | windowed_histgb | 0.000842 | 0.010000 | fixed_share_margin_too_small |
| 1535 | stay | river_hoeffding_tree | windowed_histgb | 0.000000 | 0.010000 | fixed_share_margin_too_small |
| 1663 | switch | river_hoeffding_tree | windowed_rf | 0.041800 | 0.010000 | fixed_share_weight_advantage |
| 1791 | switch | windowed_rf | river_hoeffding_tree | 0.070903 | 0.010000 | fixed_share_weight_advantage |
| 1919 | stay | river_hoeffding_tree | river_hoeffding_tree | 0.000000 | 0.010000 | fixed_share_same_leader |
| 2047 | stay | river_hoeffding_tree | river_hoeffding_tree | 0.000000 | 0.010000 | fixed_share_same_leader |
