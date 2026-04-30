# Real-Stream Benchmark Replay

- dataset: `Airlines`
- score_name: `accuracy`
- policy_name: `recent_leader_meta`
- samples: `100000`
- source: MOA Airlines delay stream replayed in temporal order from the official SourceForge archive; target is whether the flight is delayed.
- source_url: `https://downloads.sourceforge.net/project/moa-datastream/Datasets/Classification/airlines.arff.zip`
- start_strategy: `logistic_lr_0_01`
- final_strategy: `logistic_lr_0_01`
- switch_count: `6`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.646010 |
| gaussian_nb | 0.642170 |
| logistic_lr_0_01 | 0.646200 |
| pa_classifier | 0.592190 |

- best_fixed_strategy: `logistic_lr_0_01`
- best_fixed_score: `0.646200`
- adaptive_delta_vs_best_fixed: `-0.000190`
- block_delta_mean: `-0.000190`
- block_delta_ci95: `0.000469`
- block_count: `390`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 511 | stay | logistic_lr_0_01 | logistic_lr_0_01 | 0.000000 | 0.002000 | recent_leader_warmup_same |
| 767 | stay | logistic_lr_0_01 | logistic_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 1023 | stay | logistic_lr_0_01 | logistic_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 1279 | stay | logistic_lr_0_01 | logistic_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 1535 | switch | logistic_lr_0_01 | gaussian_nb | 0.002604 | 0.002000 | recent_leader_advantage |
| 1791 | stay | gaussian_nb | gaussian_nb | 0.000000 | 0.002000 | recent_leader_cooldown |
| 2047 | stay | gaussian_nb | gaussian_nb | 0.000000 | 0.002000 | recent_leader_same |
| 2303 | stay | gaussian_nb | gaussian_nb | 0.000000 | 0.002000 | recent_leader_same |
| 2559 | stay | gaussian_nb | gaussian_nb | 0.000000 | 0.002000 | recent_leader_same |
| 2815 | stay | gaussian_nb | logistic_lr_0_01 | 0.001302 | 0.002000 | recent_leader_margin_too_small |
| 3071 | stay | gaussian_nb | logistic_lr_0_01 | 0.001302 | 0.002000 | recent_leader_margin_too_small |
| 3327 | switch | gaussian_nb | logistic_lr_0_01 | 0.024740 | 0.002000 | recent_leader_advantage |
| 3583 | stay | logistic_lr_0_01 | logistic_lr_0_01 | 0.000000 | 0.002000 | recent_leader_cooldown |
| 3839 | stay | logistic_lr_0_01 | logistic_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 4095 | stay | logistic_lr_0_01 | logistic_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 4351 | stay | logistic_lr_0_01 | logistic_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |
| 4607 | stay | logistic_lr_0_01 | gaussian_nb | 0.010417 | 0.002000 | recent_leader_incumbent_floor |
| 4863 | stay | logistic_lr_0_01 | gaussian_nb | 0.009115 | 0.002000 | recent_leader_incumbent_floor |
| 5119 | stay | logistic_lr_0_01 | pa_classifier | 0.003906 | 0.002000 | recent_leader_incumbent_floor |
| 5375 | stay | logistic_lr_0_01 | logistic_lr_0_01 | 0.000000 | 0.002000 | recent_leader_same |

... truncated 369 additional decision rows in `decisions.csv`.
