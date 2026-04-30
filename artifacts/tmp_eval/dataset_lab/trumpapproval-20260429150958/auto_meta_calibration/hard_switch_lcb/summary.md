# Real-Stream Benchmark Replay

- dataset: `TrumpApproval calibration`
- score_name: `normalized_reward`
- policy_name: `hard_switch_lcb`
- samples: `256`
- source: User-uploaded CSV replayed as a temporal streaming regression task.
- source_url: `local-upload`
- start_strategy: `knn_regressor`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.763769 |
| knn_regressor | 0.763769 |
| lin_lr_0_0001 | 0.440208 |
| lin_lr_0_0005 | 0.422779 |
| lin_lr_0_001 | 0.390199 |
| tree_regressor | 0.536387 |

- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.763769`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `4`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 191 | stay | knn_regressor | tree_regressor | -0.256105 | 0.003000 | high_uncertainty |
| 255 | stay | knn_regressor | lin_lr_0_0001 | -0.172484 | 0.003000 | high_uncertainty |
