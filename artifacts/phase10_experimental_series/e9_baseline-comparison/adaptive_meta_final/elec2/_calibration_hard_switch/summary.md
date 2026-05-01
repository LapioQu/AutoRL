# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `2048`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `river_logreg`
- final_strategy: `windowed_rf`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.867188 |
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
- adaptive_delta_vs_best_fixed: `-0.020020`
- block_delta_mean: `-0.020020`
- block_delta_ci95: `0.039015`
- block_count: `16`

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
