# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `hedge_portfolio`
- samples: `1024`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `gaussian_nb`
- final_strategy: `pa_classifier`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.940430 |
| gaussian_nb | 0.824219 |
| pa_classifier | 0.949219 |
| softmax_lr_0_05 | 0.908203 |
| softmax_lr_0_20 | 0.938477 |
| tree_classifier | 0.846680 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.949219`
- adaptive_delta_vs_best_fixed: `-0.008789`
- block_delta_mean: `-0.008929`
- block_delta_ci95: `0.022771`
- block_count: `21`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 47 | stay | gaussian_nb | gaussian_nb | 0.000000 | 0.015000 | hedge_same_leader |
| 95 | stay | gaussian_nb | softmax_lr_0_20 | 0.000000 | 0.015000 | hedge_margin_too_small |
| 143 | stay | gaussian_nb | gaussian_nb | 0.000000 | 0.015000 | hedge_same_leader |
| 191 | switch | gaussian_nb | pa_classifier | 0.531445 | 0.015000 | hedge_weight_advantage |
| 239 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 287 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 335 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 383 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 431 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 479 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 527 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 575 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 623 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 671 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 719 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 767 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 815 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 863 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 911 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 959 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |

... truncated 1 additional decision rows in `decisions.csv`.
