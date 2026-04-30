# Real-Stream Benchmark Replay

- dataset: `Airlines`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `100000`
- source: MOA Airlines delay stream replayed in temporal order from the official SourceForge archive; target is whether the flight is delayed.
- source_url: `https://downloads.sourceforge.net/project/moa-datastream/Datasets/Classification/airlines.arff.zip`
- start_strategy: `tree_classifier`
- final_strategy: `tree_classifier`
- switch_count: `8`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.646960 |
| logistic_lr_0_1 | 0.634190 |
| pa_classifier | 0.592190 |
| tree_classifier | 0.647060 |

- best_fixed_strategy: `tree_classifier`
- best_fixed_score: `0.647060`
- adaptive_delta_vs_best_fixed: `-0.000100`
- block_delta_mean: `-0.000100`
- block_delta_ci95: `0.001127`
- block_count: `390`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 511 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_warmup_same |
| 767 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 1023 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 1279 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 1535 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 1791 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 2047 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 2303 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 2559 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 2815 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 3071 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 3327 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 3583 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 3839 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 4095 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 4351 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 4607 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 4863 | stay | tree_classifier | tree_classifier | 0.000000 | 0.002000 | recent_leader_same |
| 5119 | stay | tree_classifier | pa_classifier | 0.011719 | 0.002000 | recent_leader_incumbent_floor |
| 5375 | stay | tree_classifier | logistic_lr_0_1 | 0.023438 | 0.002000 | recent_leader_incumbent_floor |

... truncated 369 additional decision rows in `decisions.csv`.
