# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `45312`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `river_logreg`
- final_strategy: `river_logreg`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.876390 |
| river_hoeffding_tree | 0.830045 |
| river_logreg | 0.876832 |
| river_nb | 0.728725 |
| windowed_histgb | 0.787076 |
| windowed_rf | 0.801774 |

- best_fixed_strategy: `river_logreg`
- best_fixed_score: `0.876832`
- adaptive_delta_vs_best_fixed: `-0.000441`
- block_delta_mean: `-0.000441`
- block_delta_ci95: `0.000660`
- block_count: `354`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 511 | stay | river_logreg | river_hoeffding_tree | -0.020833 | 0.014000 | high_uncertainty |
| 639 | stay | river_logreg | river_hoeffding_tree | -0.042969 | 0.014000 | high_uncertainty |
| 767 | stay | river_logreg | river_hoeffding_tree | -0.048177 | 0.014000 | high_uncertainty |
| 895 | stay | river_logreg | river_hoeffding_tree | -0.046875 | 0.014000 | high_uncertainty |
| 1023 | stay | river_logreg | river_hoeffding_tree | -0.033854 | 0.014000 | high_uncertainty |
| 1151 | stay | river_logreg | river_hoeffding_tree | -0.003906 | 0.014000 | high_uncertainty |
| 1279 | stay | river_logreg | river_hoeffding_tree | 0.015625 | 0.014000 | high_uncertainty |
| 1407 | stay | river_logreg | river_hoeffding_tree | 0.026042 | 0.014000 | high_uncertainty |
| 1535 | stay | river_logreg | river_hoeffding_tree | 0.035156 | 0.014000 | high_uncertainty |
| 1663 | switch | river_logreg | river_hoeffding_tree | 0.033854 | 0.014000 | switch_advantage |
| 1791 | stay | river_hoeffding_tree | windowed_rf | -0.015625 | 0.014000 | high_uncertainty |
| 1919 | stay | river_hoeffding_tree | river_logreg | -0.014323 | 0.014000 | high_uncertainty |
| 2047 | stay | river_hoeffding_tree | river_logreg | 0.013021 | 0.014000 | high_uncertainty |
| 2175 | stay | river_hoeffding_tree | river_nb | 0.044271 | 0.014000 | high_uncertainty |
| 2303 | switch | river_hoeffding_tree | river_logreg | 0.048177 | 0.014000 | switch_advantage |
| 2431 | stay | river_logreg | windowed_histgb | -0.033854 | 0.014000 | high_uncertainty |
| 2559 | stay | river_logreg | windowed_histgb | -0.035156 | 0.014000 | high_uncertainty |
| 2687 | stay | river_logreg | windowed_rf | -0.006510 | 0.014000 | high_uncertainty |
| 2815 | stay | river_logreg | windowed_rf | -0.023438 | 0.014000 | high_uncertainty |
| 2943 | stay | river_logreg | windowed_rf | -0.055990 | 0.014000 | high_uncertainty |

... truncated 331 additional decision rows in `decisions.csv`.
