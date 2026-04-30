# Real-Stream Benchmark Replay

- dataset: `Airlines`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `100000`
- source: MOA Airlines delay stream replayed in temporal order from the official SourceForge archive; target is whether the flight is delayed.
- source_url: `https://downloads.sourceforge.net/project/moa-datastream/Datasets/Classification/airlines.arff.zip`
- start_strategy: `gaussian_nb`
- final_strategy: `pa_classifier`
- switch_count: `7`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.641670 |
| gaussian_nb | 0.642170 |
| logistic_lr_0_1 | 0.634190 |
| pa_classifier | 0.592190 |

- best_fixed_strategy: `gaussian_nb`
- best_fixed_score: `0.642170`
- adaptive_delta_vs_best_fixed: `-0.000500`
- block_delta_mean: `-0.000411`
- block_delta_ci95: `0.002951`
- block_count: `390`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 511 | stay | gaussian_nb | logistic_lr_0_1 | -0.001953 | 0.006000 | high_uncertainty |
| 767 | stay | gaussian_nb | logistic_lr_0_1 | 0.007812 | 0.006000 | high_uncertainty |
| 1023 | stay | gaussian_nb | logistic_lr_0_1 | 0.000000 | 0.006000 | high_uncertainty |
| 1279 | stay | gaussian_nb | logistic_lr_0_1 | -0.003906 | 0.006000 | high_uncertainty |
| 1535 | stay | gaussian_nb | logistic_lr_0_1 | -0.011719 | 0.006000 | high_uncertainty |
| 1791 | stay | gaussian_nb | logistic_lr_0_1 | -0.009766 | 0.006000 | high_uncertainty |
| 2047 | stay | gaussian_nb | logistic_lr_0_1 | 0.000000 | 0.006000 | no_candidate_improvement |
| 2303 | stay | gaussian_nb | logistic_lr_0_1 | -0.013672 | 0.006000 | high_uncertainty |
| 2559 | stay | gaussian_nb | logistic_lr_0_1 | -0.011719 | 0.006000 | high_uncertainty |
| 2815 | switch | gaussian_nb | logistic_lr_0_1 | 0.011719 | 0.006000 | switch_advantage |
| 3071 | stay | logistic_lr_0_1 | gaussian_nb | 0.025391 | 0.006000 | high_uncertainty |
| 3327 | stay | logistic_lr_0_1 | gaussian_nb | 0.017578 | 0.006000 | high_uncertainty |
| 3583 | stay | logistic_lr_0_1 | gaussian_nb | 0.000000 | 0.006000 | high_uncertainty |
| 3839 | stay | logistic_lr_0_1 | gaussian_nb | 0.015625 | 0.006000 | high_uncertainty |
| 4095 | stay | logistic_lr_0_1 | gaussian_nb | 0.015625 | 0.006000 | high_uncertainty |
| 4351 | stay | logistic_lr_0_1 | gaussian_nb | 0.039062 | 0.006000 | high_uncertainty |
| 4607 | stay | logistic_lr_0_1 | gaussian_nb | 0.033203 | 0.006000 | high_uncertainty |
| 4863 | stay | logistic_lr_0_1 | gaussian_nb | 0.035156 | 0.006000 | high_uncertainty |
| 5119 | stay | logistic_lr_0_1 | pa_classifier | 0.011719 | 0.006000 | high_uncertainty |
| 5375 | stay | logistic_lr_0_1 | pa_classifier | -0.033203 | 0.006000 | high_uncertainty |

... truncated 369 additional decision rows in `decisions.csv`.
