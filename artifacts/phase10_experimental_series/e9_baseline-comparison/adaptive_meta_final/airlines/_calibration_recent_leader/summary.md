# Real-Stream Benchmark Replay

- dataset: `Airlines`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `128`
- source: MOA Airlines delay stream replayed in temporal order from the official SourceForge archive; target is whether the flight is delayed.
- source_url: `https://downloads.sourceforge.net/project/moa-datastream/Datasets/Classification/airlines.arff.zip`
- start_strategy: `river_logreg`
- final_strategy: `river_logreg`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.726562 |
| river_hoeffding_tree | 0.734375 |
| river_logreg | 0.726562 |
| river_nb | 0.773438 |
| windowed_histgb | 0.718750 |
| windowed_rf | 0.734375 |

- best_fixed_strategy: `river_nb`
- best_fixed_score: `0.773438`
- adaptive_delta_vs_best_fixed: `-0.046875`
- block_delta_mean: `-0.046875`
- block_delta_ci95: `0.000000`
- block_count: `1`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
