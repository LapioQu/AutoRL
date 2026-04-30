# Real-Stream Benchmark Replay

- dataset: `Airlines`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `128`
- source: MOA Airlines delay stream replayed in temporal order from the official SourceForge archive; target is whether the flight is delayed.
- source_url: `https://downloads.sourceforge.net/project/moa-datastream/Datasets/Classification/airlines.arff.zip`
- start_strategy: `river_logreg`
- final_strategy: `river_hoeffding_tree`
- switch_count: `2`

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
| 127 | switch | river_logreg | river_nb |  | 0.010000 | fixed_share_warmup_leader |
| 127 | switch | river_nb | river_hoeffding_tree | 0.065038 | 0.010000 | fixed_share_weight_advantage |
