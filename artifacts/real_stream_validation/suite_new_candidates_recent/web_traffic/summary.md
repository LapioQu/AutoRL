# Real-Stream Benchmark Replay

- dataset: `WebTraffic`
- score_name: `normalized_multioutput_reward`
- policy_name: `recent_leader_meta`
- samples: `42803`
- source: Real South African web-traffic stream replayed in temporal order; target includes sessionsA and sessionsB under anomalous events and missing captures.
- source_url: `https://maxhalford.github.io/files/datasets/web-traffic.csv.zip`
- start_strategy: `sgd_lr_5e-11`
- final_strategy: `sgd_lr_1e-10`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.650297 |
| sgd_lr_1e-10 | 0.650297 |
| sgd_lr_1e-11 | 0.650297 |
| sgd_lr_5e-11 | 0.650297 |

- best_fixed_strategy: `sgd_lr_1e-10`
- best_fixed_score: `0.650297`
- adaptive_delta_vs_best_fixed: `-0.000000`
- block_delta_mean: `-0.000000`
- block_delta_ci95: `0.000000`
- block_count: `445`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 191 | switch | sgd_lr_5e-11 | sgd_lr_1e-10 |  | 0.000500 | recent_leader_warmup |
| 287 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 383 | stay | sgd_lr_1e-10 | sgd_lr_1e-11 | 0.000000 | 0.000500 | recent_leader_margin_too_small |
| 479 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 575 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 671 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 767 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 863 | stay | sgd_lr_1e-10 | sgd_lr_1e-11 | 0.000000 | 0.000500 | recent_leader_margin_too_small |
| 959 | stay | sgd_lr_1e-10 | sgd_lr_1e-11 | 0.000000 | 0.000500 | recent_leader_margin_too_small |
| 1055 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 1151 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 1247 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 1343 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 1439 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 1535 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 1631 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 1727 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 1823 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 1919 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |
| 2015 | stay | sgd_lr_1e-10 | sgd_lr_1e-10 | 0.000000 | 0.000500 | recent_leader_same |

... truncated 424 additional decision rows in `decisions.csv`.
