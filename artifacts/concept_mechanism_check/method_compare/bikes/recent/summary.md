# Real-Stream Benchmark Replay

- dataset: `Bikes`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `40000`
- source: Real Toulouse bike-availability stream replayed in temporal order; evaluation uses the first 40,000 samples for a reproducible CPU-bound benchmark.
- source_url: `https://maxhalford.github.io/files/datasets/toulouse_bikes.zip`
- start_strategy: `sgd_lr_0_0005`
- final_strategy: `sgd_lr_0_0001`
- switch_count: `87`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.677979 |
| sgd_lr_0_0001 | 0.676251 |
| sgd_lr_0_0005 | 0.575938 |
| sgd_lr_0_001 | 0.574939 |

- best_fixed_strategy: `sgd_lr_0_0001`
- best_fixed_score: `0.676251`
- adaptive_delta_vs_best_fixed: `0.001728`
- block_delta_mean: `0.001731`
- block_delta_ci95: `0.001003`
- block_count: `312`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 255 | switch | sgd_lr_0_0005 | sgd_lr_0_0001 |  | 0.000500 | recent_leader_warmup |
| 383 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.000500 | recent_leader_same |
| 511 | stay | sgd_lr_0_0001 | sgd_lr_0_0001 | 0.000000 | 0.000500 | recent_leader_same |
| 639 | switch | sgd_lr_0_0001 | sgd_lr_0_001 | 0.010153 | 0.000500 | recent_leader_advantage |
| 767 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.000819 | 0.000500 | recent_leader_advantage |
| 895 | stay | sgd_lr_0_0005 | sgd_lr_0_0005 | 0.000000 | 0.000500 | recent_leader_same |
| 1023 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.002859 | 0.000500 | recent_leader_advantage |
| 1151 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.000500 | recent_leader_same |
| 1279 | switch | sgd_lr_0_001 | sgd_lr_0_0001 | 0.002094 | 0.000500 | recent_leader_advantage |
| 1407 | switch | sgd_lr_0_0001 | sgd_lr_0_001 | 0.004467 | 0.000500 | recent_leader_advantage |
| 1535 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.000500 | recent_leader_same |
| 1663 | stay | sgd_lr_0_001 | sgd_lr_0_0005 | 0.000275 | 0.000500 | recent_leader_margin_too_small |
| 1791 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.000500 | recent_leader_same |
| 1919 | switch | sgd_lr_0_001 | sgd_lr_0_0005 | 0.009622 | 0.000500 | recent_leader_advantage |
| 2047 | stay | sgd_lr_0_0005 | sgd_lr_0_001 | 0.000173 | 0.000500 | recent_leader_margin_too_small |
| 2175 | switch | sgd_lr_0_0005 | sgd_lr_0_001 | 0.004183 | 0.000500 | recent_leader_advantage |
| 2303 | stay | sgd_lr_0_001 | sgd_lr_0_0001 | 0.002122 | 0.000500 | recent_leader_incumbent_floor |
| 2431 | stay | sgd_lr_0_001 | sgd_lr_0_001 | 0.000000 | 0.000500 | recent_leader_same |
| 2559 | stay | sgd_lr_0_001 | sgd_lr_0_0001 | 0.009166 | 0.000500 | recent_leader_incumbent_floor |
| 2687 | stay | sgd_lr_0_001 | sgd_lr_0_0001 | 0.013192 | 0.000500 | recent_leader_incumbent_floor |

... truncated 291 additional decision rows in `decisions.csv`.
