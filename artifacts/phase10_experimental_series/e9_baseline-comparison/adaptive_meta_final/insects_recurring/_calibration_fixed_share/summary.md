# Real-Stream Benchmark Replay

- dataset: `InsectsRecurring`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `2048`
- source: USP DS Repository INSECTS recurring-drift stream replayed in temporal order; target is the insect class under recurring concept drift.
- source_url: `https://sites.google.com/view/uspdsrepository`
- start_strategy: `river_logreg`
- final_strategy: `river_logreg`
- switch_count: `11`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.710938 |
| oracle | 0.898438 |
| river_hoeffding_tree | 0.490234 |
| river_logreg | 0.733887 |
| river_nb | 0.612793 |
| windowed_histgb | 0.682129 |
| windowed_rf | 0.710449 |

- best_fixed_strategy: `river_logreg`
- best_fixed_score: `0.733887`
- oracle_score: `0.898438`
- oracle_gain: `0.164551`
- oracle_capture_ratio: `0.000000`
- adaptive_delta_vs_best_fixed: `-0.022949`
- block_delta_mean: `-0.022949`
- block_delta_ci95: `0.044220`
- block_count: `16`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | river_logreg | river_nb |  | 0.010000 | fixed_share_warmup_leader |
| 127 | stay | river_nb | river_hoeffding_tree | 0.002589 | 0.010000 | fixed_share_margin_too_small |
| 255 | switch | river_nb | windowed_rf | 0.304536 | 0.010000 | fixed_share_weight_advantage |
| 383 | stay | windowed_rf | windowed_rf | 0.000000 | 0.010000 | fixed_share_same_leader |
| 511 | stay | windowed_rf | windowed_rf | 0.000000 | 0.010000 | fixed_share_same_leader |
| 639 | switch | windowed_rf | river_logreg | 0.015946 | 0.010000 | fixed_share_weight_advantage |
| 767 | switch | river_logreg | windowed_rf | 0.223982 | 0.010000 | fixed_share_weight_advantage |
| 895 | stay | windowed_rf | windowed_rf | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1023 | switch | windowed_rf | river_logreg | 0.361916 | 0.010000 | fixed_share_weight_advantage |
| 1151 | stay | river_logreg | river_logreg | 0.000000 | 0.010000 | fixed_share_same_leader |
| 1279 | switch | river_logreg | windowed_histgb | 0.071143 | 0.010000 | fixed_share_weight_advantage |
| 1407 | switch | windowed_histgb | windowed_rf | 0.033767 | 0.010000 | fixed_share_weight_advantage |
| 1535 | switch | windowed_rf | windowed_histgb | 0.090280 | 0.010000 | fixed_share_weight_advantage |
| 1663 | switch | windowed_histgb | river_logreg | 0.028263 | 0.010000 | fixed_share_weight_advantage |
| 1791 | switch | river_logreg | windowed_rf | 0.029634 | 0.010000 | fixed_share_weight_advantage |
| 1919 | stay | windowed_rf | windowed_rf | 0.000000 | 0.010000 | fixed_share_same_leader |
| 2047 | switch | windowed_rf | river_logreg | 0.105596 | 0.010000 | fixed_share_weight_advantage |
