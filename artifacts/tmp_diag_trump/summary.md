# Real-Stream Benchmark Replay

- dataset: `TrumpApproval`
- score_name: `normalized_reward`
- samples: `1001`
- source: Real approval-rating regression stream replayed in temporal order; used as a compact regression case where one fixed learner may dominate.
- source_url: `https://riverml.xyz/`
- start_strategy: `sgd_lr_0_01`
- final_strategy: `sgd_lr_0_05`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.783516 |
| sgd_lr_0_001 | 0.645687 |
| sgd_lr_0_01 | 0.733956 |
| sgd_lr_0_05 | 0.801432 |

- best_fixed_strategy: `sgd_lr_0_05`
- best_fixed_score: `0.801432`
- adaptive_delta_vs_best_fixed: `-0.017916`
- block_delta_mean: `-0.018079`
- block_delta_ci95: `0.015584`
- block_count: `31`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 95 | stay | sgd_lr_0_01 | sgd_lr_0_05 | -0.005302 | 0.010000 | high_uncertainty |
| 127 | stay | sgd_lr_0_01 | sgd_lr_0_05 | 0.052889 | 0.010000 | high_uncertainty |
| 159 | stay | sgd_lr_0_01 | sgd_lr_0_05 | 0.057147 | 0.010000 | high_uncertainty |
| 191 | stay | sgd_lr_0_01 | sgd_lr_0_05 | 0.033235 | 0.010000 | high_uncertainty |
| 223 | stay | sgd_lr_0_01 | sgd_lr_0_05 | 0.057169 | 0.010000 | high_uncertainty |
| 255 | stay | sgd_lr_0_01 | sgd_lr_0_05 | 0.074265 | 0.010000 | high_uncertainty |
| 287 | stay | sgd_lr_0_01 | sgd_lr_0_05 | 0.099450 | 0.010000 | high_uncertainty |
| 319 | switch | sgd_lr_0_01 | sgd_lr_0_05 | 0.116438 | 0.010000 | switch_advantage |
| 351 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.065923 | 0.010000 | high_uncertainty |
| 383 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.069392 | 0.010000 | high_uncertainty |
| 415 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.146654 | 0.010000 | high_uncertainty |
| 447 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.140201 | 0.010000 | high_uncertainty |
| 479 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.079789 | 0.010000 | high_uncertainty |
| 511 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.057884 | 0.010000 | no_candidate_improvement |
| 543 | stay | sgd_lr_0_05 | sgd_lr_0_001 | -0.040778 | 0.010000 | no_candidate_improvement |
| 575 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.081772 | 0.010000 | high_uncertainty |
| 607 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.094405 | 0.010000 | no_candidate_improvement |
| 639 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.101177 | 0.010000 | high_uncertainty |
| 671 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.091718 | 0.010000 | high_uncertainty |
| 703 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.066914 | 0.010000 | high_uncertainty |

... truncated 9 additional decision rows in `decisions.csv`.
