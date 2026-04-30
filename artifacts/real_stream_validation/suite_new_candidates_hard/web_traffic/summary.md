# Real-Stream Benchmark Replay

- dataset: `WebTraffic`
- score_name: `normalized_multioutput_reward`
- policy_name: `hard_switch_lcb`
- samples: `42803`
- source: Real South African web-traffic stream replayed in temporal order; target includes sessionsA and sessionsB under anomalous events and missing captures.
- source_url: `https://maxhalford.github.io/files/datasets/web-traffic.csv.zip`
- start_strategy: `sgd_lr_5e-11`
- final_strategy: `sgd_lr_5e-11`
- switch_count: `0`

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
| 383 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | high_uncertainty |
| 479 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | no_candidate_improvement |
| 575 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | high_uncertainty |
| 671 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | high_uncertainty |
| 767 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | no_candidate_improvement |
| 863 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | high_uncertainty |
| 959 | stay | sgd_lr_5e-11 | sgd_lr_1e-11 | 0.000000 | 0.005000 | no_candidate_improvement |
| 1055 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | high_uncertainty |
| 1151 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | high_uncertainty |
| 1247 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | no_candidate_improvement |
| 1343 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | high_uncertainty |
| 1439 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | no_candidate_improvement |
| 1535 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | high_uncertainty |
| 1631 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | high_uncertainty |
| 1727 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | high_uncertainty |
| 1823 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | high_uncertainty |
| 1919 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | no_candidate_improvement |
| 2015 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | high_uncertainty |
| 2111 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | high_uncertainty |
| 2207 | stay | sgd_lr_5e-11 | sgd_lr_1e-10 | 0.000000 | 0.005000 | high_uncertainty |

... truncated 422 additional decision rows in `decisions.csv`.
