# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `2048`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `river_logreg`
- final_strategy: `river_logreg`
- switch_count: `9`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.880859 |
| river_hoeffding_tree | 0.882324 |
| river_logreg | 0.884766 |
| river_nb | 0.810547 |
| windowed_histgb | 0.781738 |
| windowed_rf | 0.831055 |

- best_fixed_strategy: `river_logreg`
- best_fixed_score: `0.884766`
- adaptive_delta_vs_best_fixed: `-0.003906`
- block_delta_mean: `-0.003906`
- block_delta_ci95: `0.023598`
- block_count: `16`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | river_logreg | river_hoeffding_tree |  | 0.010000 | fixed_share_warmup_leader |
| 127 | stay | river_hoeffding_tree | river_nb | 0.000000 | 0.010000 | fixed_share_margin_too_small |
| 255 | switch | river_hoeffding_tree | river_logreg | 0.179732 | 0.010000 | fixed_share_weight_advantage |
| 383 | stay | river_logreg | river_logreg | 0.000000 | 0.010000 | fixed_share_same_leader |
| 511 | switch | river_logreg | river_nb | 0.022033 | 0.010000 | fixed_share_weight_advantage |
| 639 | switch | river_nb | river_logreg | 0.078598 | 0.010000 | fixed_share_weight_advantage |
| 767 | switch | river_logreg | windowed_rf | 0.039769 | 0.010000 | fixed_share_weight_advantage |
| 895 | switch | windowed_rf | windowed_histgb | 0.186444 | 0.010000 | fixed_share_weight_advantage |
| 1023 | switch | windowed_histgb | river_hoeffding_tree | 0.119285 | 0.010000 | fixed_share_weight_advantage |
| 1151 | stay | river_hoeffding_tree | windowed_rf | 0.005638 | 0.010000 | fixed_share_margin_too_small |
| 1279 | stay | river_hoeffding_tree | windowed_histgb | 0.004430 | 0.010000 | fixed_share_margin_too_small |
| 1407 | stay | river_hoeffding_tree | windowed_histgb | 0.000842 | 0.010000 | fixed_share_margin_too_small |
| 1535 | stay | river_hoeffding_tree | windowed_histgb | 0.000000 | 0.010000 | fixed_share_margin_too_small |
| 1663 | stay | river_hoeffding_tree | river_hoeffding_tree | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1791 | stay | river_hoeffding_tree | river_hoeffding_tree | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1919 | switch | river_hoeffding_tree | river_nb | 0.109736 | 0.010000 | fixed_share_weight_advantage |
| 2047 | switch | river_nb | river_logreg | 0.189464 | 0.010000 | fixed_share_weight_advantage |
