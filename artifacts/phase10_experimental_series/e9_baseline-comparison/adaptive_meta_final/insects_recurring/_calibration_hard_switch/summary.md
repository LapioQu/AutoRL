# Real-Stream Benchmark Replay

- dataset: `InsectsRecurring`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `128`
- source: USP DS Repository INSECTS recurring-drift stream replayed in temporal order; target is the insect class under recurring concept drift.
- source_url: `https://sites.google.com/view/uspdsrepository`
- start_strategy: `river_logreg`
- final_strategy: `river_logreg`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.742188 |
| river_hoeffding_tree | 0.757812 |
| river_logreg | 0.742188 |
| river_nb | 0.851562 |
| windowed_histgb | 0.828125 |
| windowed_rf | 0.859375 |

- best_fixed_strategy: `windowed_rf`
- best_fixed_score: `0.859375`
- adaptive_delta_vs_best_fixed: `-0.117188`
- block_delta_mean: `-0.117188`
- block_delta_ci95: `0.000000`
- block_count: `1`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
