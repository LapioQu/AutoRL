# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `hedge_portfolio`
- samples: `45312`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `sgd_lr_1_0`
- final_strategy: `sgd_lr_1_0`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.915078 |
| sgd_lr_0_1 | 0.894928 |
| sgd_lr_0_5 | 0.916005 |
| sgd_lr_1_0 | 0.915122 |

- best_fixed_strategy: `sgd_lr_0_5`
- best_fixed_score: `0.916005`
- adaptive_delta_vs_best_fixed: `-0.000927`
- block_delta_mean: `-0.000927`
- block_delta_ci95: `0.001417`
- block_count: `354`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | sgd_lr_1_0 | sgd_lr_0_5 |  | 0.015000 | warmup_leader |
| 127 | stay | sgd_lr_0_5 | sgd_lr_0_5 | 0.000000 | 0.015000 | hedge_same_leader |
| 255 | switch | sgd_lr_0_5 | sgd_lr_1_0 | 0.172704 | 0.015000 | hedge_weight_advantage |
| 383 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 511 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 639 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 767 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 895 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 1023 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 1151 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 1279 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 1407 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 1535 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 1663 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 1791 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 1919 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 2047 | stay | sgd_lr_1_0 | sgd_lr_1_0 | 0.000000 | 0.015000 | hedge_same_leader |
| 2175 | stay | sgd_lr_1_0 | sgd_lr_0_1 | nan | 0.015000 | hedge_margin_too_small |
| 2303 | stay | sgd_lr_1_0 | sgd_lr_0_1 | nan | 0.015000 | hedge_margin_too_small |
| 2431 | stay | sgd_lr_1_0 | sgd_lr_0_1 | nan | 0.015000 | hedge_margin_too_small |

... truncated 335 additional decision rows in `decisions.csv`.
