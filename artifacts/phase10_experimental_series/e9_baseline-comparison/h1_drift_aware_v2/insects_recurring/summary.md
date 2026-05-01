# Real-Stream Benchmark Replay

- dataset: `InsectsRecurring`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `79986`
- source: USP DS Repository INSECTS recurring-drift stream replayed in temporal order; target is the insect class under recurring concept drift.
- source_url: `https://sites.google.com/view/uspdsrepository`
- start_strategy: `river_logreg`
- final_strategy: `river_logreg`
- switch_count: `36`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.768597 |
| river_hoeffding_tree | 0.600218 |
| river_logreg | 0.772510 |
| river_nb | 0.487035 |
| windowed_histgb | 0.765434 |
| windowed_rf | 0.766697 |

- best_fixed_strategy: `river_logreg`
- best_fixed_score: `0.772510`
- adaptive_delta_vs_best_fixed: `-0.003913`
- block_delta_mean: `-0.003919`
- block_delta_ci95: `0.004555`
- block_count: `624`

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
| 2175 | stay | windowed_rf | river_logreg | 0.007812 | 0.014000 | high_uncertainty |
| 2303 | stay | windowed_rf | river_logreg | 0.045573 | 0.014000 | high_uncertainty |
| 2431 | switch | windowed_rf | river_logreg | 0.058594 | 0.014000 | switch_advantage |
| 2559 | stay | river_logreg | windowed_histgb | -0.023438 | 0.014000 | high_uncertainty |
| 2687 | stay | river_logreg | windowed_rf | -0.003906 | 0.014000 | high_uncertainty |
| 2815 | stay | river_logreg | windowed_rf | 0.009115 | 0.014000 | high_uncertainty |
| 2943 | stay | river_logreg | windowed_rf | 0.006510 | 0.014000 | high_uncertainty |

... truncated 601 additional decision rows in `decisions.csv`.
