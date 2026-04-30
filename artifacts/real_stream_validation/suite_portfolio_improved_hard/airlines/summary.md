# Real-Stream Benchmark Replay

- dataset: `Airlines`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `100000`
- source: MOA Airlines delay stream replayed in temporal order from the official SourceForge archive; target is whether the flight is delayed.
- source_url: `https://downloads.sourceforge.net/project/moa-datastream/Datasets/Classification/airlines.arff.zip`
- start_strategy: `logistic_lr_0_01`
- final_strategy: `logistic_lr_0_01`
- switch_count: `16`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.644870 |
| gaussian_nb | 0.642170 |
| logistic_lr_0_01 | 0.646200 |
| pa_classifier | 0.592190 |

- best_fixed_strategy: `logistic_lr_0_01`
- best_fixed_score: `0.646200`
- adaptive_delta_vs_best_fixed: `-0.001330`
- block_delta_mean: `-0.001332`
- block_delta_ci95: `0.002271`
- block_count: `390`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 511 | stay | logistic_lr_0_01 | gaussian_nb | -0.001953 | 0.006000 | high_uncertainty |
| 767 | stay | logistic_lr_0_01 | gaussian_nb | -0.007812 | 0.006000 | high_uncertainty |
| 1023 | stay | logistic_lr_0_01 | gaussian_nb | -0.005859 | 0.006000 | high_uncertainty |
| 1279 | stay | logistic_lr_0_01 | gaussian_nb | -0.003906 | 0.006000 | high_uncertainty |
| 1535 | stay | logistic_lr_0_01 | gaussian_nb | 0.007812 | 0.006000 | high_uncertainty |
| 1791 | stay | logistic_lr_0_01 | gaussian_nb | 0.011719 | 0.006000 | high_uncertainty |
| 2047 | stay | logistic_lr_0_01 | gaussian_nb | -0.001953 | 0.006000 | high_uncertainty |
| 2303 | stay | logistic_lr_0_01 | gaussian_nb | 0.001953 | 0.006000 | high_uncertainty |
| 2559 | stay | logistic_lr_0_01 | gaussian_nb | 0.005859 | 0.006000 | no_candidate_improvement |
| 2815 | stay | logistic_lr_0_01 | gaussian_nb | -0.009766 | 0.006000 | no_candidate_improvement |
| 3071 | stay | logistic_lr_0_01 | gaussian_nb | 0.000000 | 0.006000 | high_uncertainty |
| 3327 | stay | logistic_lr_0_01 | gaussian_nb | -0.029297 | 0.006000 | high_uncertainty |
| 3583 | stay | logistic_lr_0_01 | gaussian_nb | -0.027344 | 0.006000 | high_uncertainty |
| 3839 | stay | logistic_lr_0_01 | gaussian_nb | -0.005859 | 0.006000 | high_uncertainty |
| 4095 | stay | logistic_lr_0_01 | gaussian_nb | -0.011719 | 0.006000 | high_uncertainty |
| 4351 | stay | logistic_lr_0_01 | gaussian_nb | 0.005859 | 0.006000 | high_uncertainty |
| 4607 | stay | logistic_lr_0_01 | gaussian_nb | 0.011719 | 0.006000 | high_uncertainty |
| 4863 | stay | logistic_lr_0_01 | gaussian_nb | 0.011719 | 0.006000 | high_uncertainty |
| 5119 | stay | logistic_lr_0_01 | pa_classifier | 0.013672 | 0.006000 | high_uncertainty |
| 5375 | stay | logistic_lr_0_01 | pa_classifier | 0.003906 | 0.006000 | high_uncertainty |

... truncated 369 additional decision rows in `decisions.csv`.
