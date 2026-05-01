# Real-Stream Benchmark Replay

- dataset: `InsectsRecurring`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `2048`
- source: USP DS Repository INSECTS recurring-drift stream replayed in temporal order; target is the insect class under recurring concept drift.
- source_url: `https://sites.google.com/view/uspdsrepository`
- start_strategy: `river_logreg`
- final_strategy: `windowed_rf`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.699707 |
| river_hoeffding_tree | 0.502441 |
| river_logreg | 0.733887 |
| river_nb | 0.612793 |
| windowed_histgb | 0.682129 |
| windowed_rf | 0.710449 |

- best_fixed_strategy: `river_logreg`
- best_fixed_score: `0.733887`
- adaptive_delta_vs_best_fixed: `-0.034180`
- block_delta_mean: `-0.034180`
- block_delta_ci95: `0.048778`
- block_count: `16`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 511 | stay | river_logreg | windowed_rf | 0.011719 | 0.014000 | no_candidate_improvement |
| 639 | stay | river_logreg | windowed_rf | 0.007812 | 0.014000 | no_candidate_improvement |
| 767 | stay | river_logreg | windowed_rf | 0.018229 | 0.014000 | high_uncertainty |
| 895 | switch | river_logreg | windowed_rf | 0.028646 | 0.014000 | switch_advantage |
| 1023 | stay | windowed_rf | river_logreg | 0.024740 | 0.014000 | high_uncertainty |
| 1151 | stay | windowed_rf | river_logreg | 0.130208 | 0.014000 | high_uncertainty |
| 1279 | stay | windowed_rf | river_logreg | 0.177083 | 0.014000 | high_uncertainty |
| 1407 | stay | windowed_rf | river_logreg | 0.127604 | 0.014000 | high_uncertainty |
| 1535 | stay | windowed_rf | river_logreg | 0.039062 | 0.014000 | high_uncertainty |
| 1663 | stay | windowed_rf | river_logreg | 0.007812 | 0.014000 | high_uncertainty |
| 1791 | stay | windowed_rf | river_logreg | 0.001302 | 0.014000 | high_uncertainty |
| 1919 | stay | windowed_rf | river_logreg | -0.018229 | 0.014000 | high_uncertainty |
| 2047 | stay | windowed_rf | river_logreg | -0.018229 | 0.014000 | high_uncertainty |
