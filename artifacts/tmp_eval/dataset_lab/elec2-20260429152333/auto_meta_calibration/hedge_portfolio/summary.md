# Real-Stream Benchmark Replay

- dataset: `Elec2 calibration`
- score_name: `accuracy`
- policy_name: `hedge_portfolio`
- samples: `880`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `pa_classifier`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.893182 |
| knn_classifier | 0.876136 |
| pa_classifier | 0.944318 |
| sgd_lr_0_05 | 0.844318 |
| sgd_lr_0_10 | 0.860227 |
| tree_classifier | 0.826136 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.944318`
- adaptive_delta_vs_best_fixed: `-0.051136`
- block_delta_mean: `-0.058594`
- block_delta_ci95: `0.104838`
- block_count: `6`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | stay | tree_classifier | tree_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 255 | switch | tree_classifier | pa_classifier |  | 0.015000 | warmup_leader |
| 255 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 383 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 511 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 639 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 767 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
