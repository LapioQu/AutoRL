# Real-Stream Benchmark Replay

- dataset: `Bikes calibration`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `40142`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `lin_lr_0_0001`
- final_strategy: `tree_regressor`
- switch_count: `12`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.683690 |
| lin_lr_0_0001 | 0.679432 |
| lin_lr_0_0005 | 0.679727 |
| lin_lr_0_001 | 0.680266 |
| lin_lr_0_002 | 0.680713 |
| tree_regressor | 0.695042 |

- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.695042`
- adaptive_delta_vs_best_fixed: `-0.011351`
- block_delta_mean: `-0.011355`
- block_delta_ci95: `0.005683`
- block_count: `627`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 191 | stay | lin_lr_0_0001 | lin_lr_0_002 | 0.004714 | 0.003000 | high_uncertainty |
| 255 | stay | lin_lr_0_0001 | tree_regressor | 0.062367 | 0.003000 | high_uncertainty |
| 319 | stay | lin_lr_0_0001 | tree_regressor | 0.092915 | 0.003000 | high_uncertainty |
| 383 | stay | lin_lr_0_0001 | tree_regressor | 0.047171 | 0.003000 | high_uncertainty |
| 447 | stay | lin_lr_0_0001 | tree_regressor | 0.007605 | 0.003000 | high_uncertainty |
| 511 | stay | lin_lr_0_0001 | tree_regressor | 0.041594 | 0.003000 | high_uncertainty |
| 575 | stay | lin_lr_0_0001 | tree_regressor | 0.052087 | 0.003000 | high_uncertainty |
| 639 | stay | lin_lr_0_0001 | lin_lr_0_001 | 0.005943 | 0.003000 | high_uncertainty |
| 703 | stay | lin_lr_0_0001 | lin_lr_0_001 | 0.008394 | 0.003000 | high_uncertainty |
| 767 | stay | lin_lr_0_0001 | lin_lr_0_001 | 0.004100 | 0.003000 | high_uncertainty |
| 831 | stay | lin_lr_0_0001 | lin_lr_0_0005 | 0.002219 | 0.003000 | high_uncertainty |
| 895 | stay | lin_lr_0_0001 | lin_lr_0_0005 | 0.002011 | 0.003000 | high_uncertainty |
| 959 | stay | lin_lr_0_0001 | lin_lr_0_0005 | 0.001010 | 0.003000 | high_uncertainty |
| 1023 | stay | lin_lr_0_0001 | lin_lr_0_002 | 0.002490 | 0.003000 | high_uncertainty |
| 1087 | stay | lin_lr_0_0001 | lin_lr_0_002 | 0.008815 | 0.003000 | high_uncertainty |
| 1151 | stay | lin_lr_0_0001 | lin_lr_0_002 | 0.006678 | 0.003000 | high_uncertainty |
| 1215 | stay | lin_lr_0_0001 | lin_lr_0_0005 | 0.001557 | 0.003000 | high_uncertainty |
| 1279 | stay | lin_lr_0_0001 | lin_lr_0_0005 | -0.000335 | 0.003000 | high_uncertainty |
| 1343 | stay | lin_lr_0_0001 | lin_lr_0_0005 | -0.000879 | 0.003000 | high_uncertainty |
| 1407 | switch | lin_lr_0_0001 | lin_lr_0_002 | 0.003710 | 0.003000 | switch_advantage |

... truncated 605 additional decision rows in `decisions.csv`.
