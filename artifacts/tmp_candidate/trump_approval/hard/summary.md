# Real-Stream Benchmark Replay

- dataset: `trump_approval`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `512`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `sgd_lr_0_01`
- final_strategy: `sgd_lr_0_05`
- switch_count: `1`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.692012 |
| sgd_lr_0_001 | 0.564354 |
| sgd_lr_0_01 | 0.659141 |
| sgd_lr_0_05 | 0.726360 |

- best_fixed_strategy: `sgd_lr_0_05`
- best_fixed_score: `0.726360`
- adaptive_delta_vs_best_fixed: `-0.034348`
- block_delta_mean: `-0.034348`
- block_delta_ci95: `0.027080`
- block_count: `16`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 95 | stay | sgd_lr_0_01 | sgd_lr_0_05 | -0.003918 | 0.010000 | high_uncertainty |
| 127 | stay | sgd_lr_0_01 | sgd_lr_0_05 | 0.053801 | 0.010000 | high_uncertainty |
| 159 | stay | sgd_lr_0_01 | sgd_lr_0_05 | 0.057511 | 0.010000 | high_uncertainty |
| 191 | stay | sgd_lr_0_01 | sgd_lr_0_05 | 0.032956 | 0.010000 | high_uncertainty |
| 223 | stay | sgd_lr_0_01 | sgd_lr_0_05 | 0.055490 | 0.010000 | high_uncertainty |
| 255 | stay | sgd_lr_0_01 | sgd_lr_0_05 | 0.071740 | 0.010000 | high_uncertainty |
| 287 | stay | sgd_lr_0_01 | sgd_lr_0_05 | 0.096162 | 0.010000 | high_uncertainty |
| 319 | switch | sgd_lr_0_01 | sgd_lr_0_05 | 0.112697 | 0.010000 | switch_advantage |
| 351 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.063805 | 0.010000 | high_uncertainty |
| 383 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.067087 | 0.010000 | high_uncertainty |
| 415 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.140978 | 0.010000 | high_uncertainty |
| 447 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.134044 | 0.010000 | high_uncertainty |
| 479 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.075917 | 0.010000 | high_uncertainty |
| 511 | stay | sgd_lr_0_05 | sgd_lr_0_01 | -0.054888 | 0.010000 | no_candidate_improvement |
