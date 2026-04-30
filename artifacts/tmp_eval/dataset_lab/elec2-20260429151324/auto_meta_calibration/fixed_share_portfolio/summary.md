# Real-Stream Benchmark Replay

- dataset: `Elec2 calibration`
- score_name: `accuracy`
- policy_name: `fixed_share_portfolio`
- samples: `880`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `pa_classifier`
- switch_count: `3`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.921591 |
| knn_classifier | 0.875000 |
| pa_classifier | 0.944318 |
| sgd_lr_0_05 | 0.844318 |
| sgd_lr_0_10 | 0.860227 |
| tree_classifier | 0.818182 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.944318`
- adaptive_delta_vs_best_fixed: `-0.022727`
- block_delta_mean: `-0.026042`
- block_delta_ci95: `0.041256`
- block_count: `6`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 127 | switch | tree_classifier | pa_classifier | 0.071036 | 0.015000 | fixed_share_weight_advantage |
| 255 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 383 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
| 511 | switch | pa_classifier | tree_classifier | 0.019229 | 0.015000 | fixed_share_weight_advantage |
| 639 | switch | tree_classifier | pa_classifier | 0.177354 | 0.015000 | fixed_share_weight_advantage |
| 767 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | fixed_share_same_leader |
