# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `2048`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `river_logreg`
- final_strategy: `river_hoeffding_tree`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.883789 |
| river_hoeffding_tree | 0.882324 |
| river_logreg | 0.884766 |
| river_nb | 0.810547 |
| windowed_histgb | 0.781738 |
| windowed_rf | 0.831055 |

- best_fixed_strategy: `river_logreg`
- best_fixed_score: `0.884766`
- adaptive_delta_vs_best_fixed: `-0.000977`
- block_delta_mean: `-0.000977`
- block_delta_ci95: `0.004463`
- block_count: `16`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 511 | stay | river_logreg | river_hoeffding_tree | -0.037760 | 0.014000 | high_uncertainty |
| 639 | stay | river_logreg | river_hoeffding_tree | -0.055990 | 0.014000 | high_uncertainty |
| 767 | stay | river_logreg | river_hoeffding_tree | -0.054688 | 0.014000 | high_uncertainty |
| 895 | stay | river_logreg | river_hoeffding_tree | -0.048177 | 0.014000 | high_uncertainty |
| 1023 | stay | river_logreg | river_hoeffding_tree | -0.032552 | 0.014000 | high_uncertainty |
| 1151 | stay | river_logreg | river_hoeffding_tree | 0.002604 | 0.014000 | high_uncertainty |
| 1279 | stay | river_logreg | river_hoeffding_tree | 0.027344 | 0.014000 | high_uncertainty |
| 1407 | stay | river_logreg | river_hoeffding_tree | 0.041667 | 0.014000 | high_uncertainty |
| 1535 | stay | river_logreg | river_hoeffding_tree | 0.045573 | 0.014000 | high_uncertainty |
| 1663 | switch | river_logreg | river_hoeffding_tree | 0.037760 | 0.014000 | switch_advantage |
| 1791 | stay | river_hoeffding_tree | windowed_rf | -0.010417 | 0.014000 | high_uncertainty |
| 1919 | stay | river_hoeffding_tree | river_logreg | -0.009115 | 0.014000 | high_uncertainty |
| 2047 | stay | river_hoeffding_tree | river_logreg | 0.000000 | 0.014000 | high_uncertainty |
