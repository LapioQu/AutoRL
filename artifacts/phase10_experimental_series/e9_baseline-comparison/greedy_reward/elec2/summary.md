# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `256`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `river_logreg`
- final_strategy: `windowed_rf`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.867188 |
| river_hoeffding_tree | 0.812500 |
| river_logreg | 0.832031 |
| river_nb | 0.812500 |
| windowed_histgb | 0.804688 |
| windowed_rf | 0.906250 |

- best_fixed_strategy: `windowed_rf`
- best_fixed_score: `0.906250`
- adaptive_delta_vs_best_fixed: `-0.039062`
- block_delta_mean: `-0.039062`
- block_delta_ci95: `0.054138`
- block_count: `2`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | river_logreg | windowed_rf |  | 0.000000 | recent_leader_warmup |
| 255 | stay | windowed_rf | windowed_rf | 0.000000 | 0.000000 | recent_leader_same |
