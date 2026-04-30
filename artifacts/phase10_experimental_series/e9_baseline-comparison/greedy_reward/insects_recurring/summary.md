# Real-Stream Benchmark Replay

- dataset: `InsectsRecurring`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `256`
- source: USP DS Repository INSECTS recurring-drift stream replayed in temporal order; target is the insect class under recurring concept drift.
- source_url: `https://sites.google.com/view/uspdsrepository`
- start_strategy: `river_logreg`
- final_strategy: `windowed_histgb`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.761719 |
| river_hoeffding_tree | 0.679688 |
| river_logreg | 0.777344 |
| river_nb | 0.796875 |
| windowed_histgb | 0.820312 |
| windowed_rf | 0.820312 |

- best_fixed_strategy: `windowed_rf`
- best_fixed_score: `0.820312`
- adaptive_delta_vs_best_fixed: `-0.058594`
- block_delta_mean: `-0.058594`
- block_delta_ci95: `0.081207`
- block_count: `2`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | river_logreg | windowed_rf |  | 0.000000 | recent_leader_warmup |
| 255 | switch | windowed_rf | windowed_histgb | 0.031250 | 0.000000 | recent_leader_advantage |
