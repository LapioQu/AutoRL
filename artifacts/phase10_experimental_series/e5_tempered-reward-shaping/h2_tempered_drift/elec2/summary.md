# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `45312`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `river_logreg`
- final_strategy: `river_logreg`
- switch_count: `4`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.859441 |
| oracle | 0.959393 |
| river_hoeffding_tree | 0.833929 |
| river_logreg | 0.876832 |
| river_nb | 0.728725 |
| windowed_histgb | 0.787076 |
| windowed_rf | 0.801774 |

- best_fixed_strategy: `river_logreg`
- best_fixed_score: `0.876832`
- oracle_score: `0.959393`
- oracle_gain: `0.082561`
- oracle_capture_ratio: `0.000000`
- adaptive_delta_vs_best_fixed: `-0.017391`
- block_delta_mean: `-0.017391`
- block_delta_ci95: `0.006047`
- block_count: `354`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 511 | stay | river_logreg | river_hoeffding_tree | -0.057292 | 0.014000 | high_uncertainty |
| 639 | stay | river_logreg | river_hoeffding_tree | -0.044271 | 0.014000 | high_uncertainty |
| 767 | stay | river_logreg | river_hoeffding_tree | -0.015625 | 0.014000 | no_candidate_improvement |
| 895 | stay | river_logreg | river_hoeffding_tree | -0.016927 | 0.014000 | high_uncertainty |
| 1023 | stay | river_logreg | river_hoeffding_tree | -0.029948 | 0.014000 | no_candidate_improvement |
| 1151 | stay | river_logreg | river_hoeffding_tree | -0.013021 | 0.014000 | high_uncertainty |
| 1279 | stay | river_logreg | river_hoeffding_tree | 0.020833 | 0.014000 | high_uncertainty |
| 1407 | stay | river_logreg | river_hoeffding_tree | 0.037760 | 0.014000 | high_uncertainty |
| 1535 | stay | river_logreg | river_hoeffding_tree | 0.039062 | 0.014000 | high_uncertainty |
| 1663 | switch | river_logreg | windowed_rf | 0.031250 | 0.014000 | switch_advantage |
| 1791 | stay | windowed_rf | river_hoeffding_tree | 0.005208 | 0.014000 | high_uncertainty |
| 1919 | stay | windowed_rf | river_hoeffding_tree | 0.031250 | 0.014000 | high_uncertainty |
| 2047 | stay | windowed_rf | river_hoeffding_tree | 0.088542 | 0.014000 | high_uncertainty |
| 2175 | stay | windowed_rf | river_hoeffding_tree | 0.132812 | 0.014000 | high_uncertainty |
| 2303 | stay | windowed_rf | river_hoeffding_tree | 0.110677 | 0.014000 | high_uncertainty |
| 2431 | stay | windowed_rf | river_logreg | 0.076823 | 0.014000 | high_uncertainty |
| 2559 | stay | windowed_rf | river_logreg | 0.036458 | 0.014000 | high_uncertainty |
| 2687 | stay | windowed_rf | river_hoeffding_tree | 0.028646 | 0.014000 | high_uncertainty |
| 2815 | stay | windowed_rf | river_logreg | 0.023438 | 0.014000 | high_uncertainty |
| 2943 | stay | windowed_rf | river_logreg | 0.055990 | 0.014000 | high_uncertainty |

... truncated 331 additional decision rows in `decisions.csv`.
