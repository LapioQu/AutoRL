# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `128`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `river_logreg`
- final_strategy: `river_logreg`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.835938 |
| river_hoeffding_tree | 0.906250 |
| river_logreg | 0.835938 |
| river_nb | 0.906250 |
| windowed_histgb | 0.796875 |
| windowed_rf | 0.914062 |

- best_fixed_strategy: `windowed_rf`
- best_fixed_score: `0.914062`
- adaptive_delta_vs_best_fixed: `-0.078125`
- block_delta_mean: `-0.078125`
- block_delta_ci95: `0.000000`
- block_count: `1`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
