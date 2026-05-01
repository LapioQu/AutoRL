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
| adaptive | 0.872263 |
| river_hoeffding_tree | 0.830067 |
| river_logreg | 0.876832 |
| river_nb | 0.728725 |
| windowed_histgb | 0.787076 |
| windowed_rf | 0.801774 |

- best_fixed_strategy: `river_logreg`
- best_fixed_score: `0.876832`
- adaptive_delta_vs_best_fixed: `-0.004568`
- block_delta_mean: `-0.004568`
- block_delta_ci95: `0.002461`
- block_count: `354`

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
| 2175 | stay | river_hoeffding_tree | river_nb | 0.016927 | 0.014000 | high_uncertainty |
| 2303 | stay | river_hoeffding_tree | river_logreg | 0.018229 | 0.014000 | high_uncertainty |
| 2431 | stay | river_hoeffding_tree | river_logreg | 0.037760 | 0.014000 | high_uncertainty |
| 2559 | stay | river_hoeffding_tree | river_logreg | 0.046875 | 0.014000 | high_uncertainty |
| 2687 | stay | river_hoeffding_tree | river_logreg | 0.039062 | 0.014000 | high_uncertainty |
| 2815 | stay | river_hoeffding_tree | river_logreg | 0.032552 | 0.014000 | high_uncertainty |
| 2943 | stay | river_hoeffding_tree | river_logreg | 0.026042 | 0.014000 | high_uncertainty |

... truncated 331 additional decision rows in `decisions.csv`.
