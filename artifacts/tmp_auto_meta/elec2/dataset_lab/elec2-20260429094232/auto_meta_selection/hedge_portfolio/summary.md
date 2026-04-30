# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `hedge_portfolio`
- samples: `336`
- source: User-uploaded CSV replayed as a temporal streaming classification task.
- source_url: `local-upload`
- start_strategy: `tree_classifier`
- final_strategy: `pa_classifier`
- switch_count: `2`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.913690 |
| gaussian_nb | 0.839286 |
| pa_classifier | 0.943452 |
| softmax_lr_0_05 | 0.898810 |
| softmax_lr_0_20 | 0.922619 |
| tree_classifier | 0.854167 |

- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.943452`
- adaptive_delta_vs_best_fixed: `-0.029762`
- block_delta_mean: `-0.029762`
- block_delta_ci95: `0.067956`
- block_count: `7`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 47 | stay | tree_classifier | tree_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 95 | switch | tree_classifier | gaussian_nb |  | 0.015000 | warmup_leader |
| 95 | stay | gaussian_nb | softmax_lr_0_20 | 0.000000 | 0.015000 | hedge_margin_too_small |
| 143 | stay | gaussian_nb | gaussian_nb | 0.000000 | 0.015000 | hedge_same_leader |
| 191 | switch | gaussian_nb | pa_classifier | 0.488389 | 0.015000 | hedge_weight_advantage |
| 239 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 287 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
| 335 | stay | pa_classifier | pa_classifier | 0.000000 | 0.015000 | hedge_same_leader |
