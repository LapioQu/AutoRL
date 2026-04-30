# Real-Stream Benchmark Replay

- dataset: `Airlines`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `256`
- source: MOA Airlines delay stream replayed in temporal order from the official SourceForge archive; target is whether the flight is delayed.
- source_url: `https://downloads.sourceforge.net/project/moa-datastream/Datasets/Classification/airlines.arff.zip`
- start_strategy: `river_logreg`
- final_strategy: `river_logreg`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.761719 |
| river_hoeffding_tree | 0.769531 |
| river_logreg | 0.761719 |
| river_nb | 0.785156 |
| windowed_histgb | 0.730469 |
| windowed_rf | 0.769531 |

- best_fixed_strategy: `river_nb`
- best_fixed_score: `0.785156`
- adaptive_delta_vs_best_fixed: `-0.023438`
- block_delta_mean: `-0.023438`
- block_delta_ci95: `0.032483`
- block_count: `2`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
