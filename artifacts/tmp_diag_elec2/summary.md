# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- samples: `45312`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `sgd_lr_1_0`
- final_strategy: `sgd_lr_0_5`
- switch_count: `5`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.916159 |
| sgd_lr_0_1 | 0.894928 |
| sgd_lr_0_5 | 0.916005 |
| sgd_lr_1_0 | 0.915122 |

- best_fixed_strategy: `sgd_lr_0_5`
- best_fixed_score: `0.916005`
- adaptive_delta_vs_best_fixed: `0.000154`
- block_delta_mean: `0.000154`
- block_delta_ci95: `0.001199`
- block_count: `354`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 511 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.005208 | 0.018000 | no_candidate_improvement |
| 639 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.003906 | 0.018000 | no_candidate_improvement |
| 767 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.001302 | 0.018000 | no_candidate_improvement |
| 895 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.003906 | 0.018000 | no_candidate_improvement |
| 1023 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.006510 | 0.018000 | no_candidate_improvement |
| 1151 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.009115 | 0.018000 | no_candidate_improvement |
| 1279 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.010417 | 0.018000 | no_candidate_improvement |
| 1407 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.011719 | 0.018000 | no_candidate_improvement |
| 1535 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.009115 | 0.018000 | high_uncertainty |
| 1663 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.001302 | 0.018000 | no_candidate_improvement |
| 1791 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.005208 | 0.018000 | high_uncertainty |
| 1919 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.003906 | 0.018000 | high_uncertainty |
| 2047 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.001302 | 0.018000 | no_candidate_improvement |
| 2175 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.006510 | 0.018000 | no_candidate_improvement |
| 2303 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.011719 | 0.018000 | no_candidate_improvement |
| 2431 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.011719 | 0.018000 | no_candidate_improvement |
| 2559 | stay | sgd_lr_1_0 | sgd_lr_0_5 | -0.007812 | 0.018000 | no_candidate_improvement |
| 2687 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.001302 | 0.018000 | no_candidate_improvement |
| 2815 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.003906 | 0.018000 | no_candidate_improvement |
| 2943 | stay | sgd_lr_1_0 | sgd_lr_0_5 | 0.000000 | 0.018000 | no_candidate_improvement |

... truncated 331 additional decision rows in `decisions.csv`.
