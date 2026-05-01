# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `fixed_share_portfolio`
- samples: `317`
- source: Real pipeline water-flow stream replayed in temporal order; evaluation includes anomalous low-flow segments and a pumping-induced peak.
- source_url: ``
- start_strategy: `pa_regressor`
- final_strategy: `lin_lr_0_001`
- switch_count: `4`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.634216 |
| oracle | 0.704637 |
| lin_lr_0_0005 | 0.493435 |
| lin_lr_0_001 | 0.510585 |
| pa_regressor | 0.630479 |

- best_fixed_strategy: `pa_regressor`
- best_fixed_score: `0.630479`
- oracle_score: `0.704637`
- oracle_gain: `0.074159`
- oracle_capture_ratio: `0.050400`
- adaptive_delta_vs_best_fixed: `0.003738`
- block_delta_mean: `0.002044`
- block_delta_ci95: `0.044924`
- block_count: `13`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 23 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 47 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 71 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 95 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 119 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 143 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 167 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 191 | switch | pa_regressor | lin_lr_0_0005 | 0.278886 | 0.010000 | fixed_share_weight_advantage |
| 215 | switch | lin_lr_0_0005 | lin_lr_0_001 | 0.227930 | 0.010000 | fixed_share_weight_advantage |
| 239 | switch | lin_lr_0_001 | pa_regressor | 0.441048 | 0.010000 | fixed_share_weight_advantage |
| 263 | stay | pa_regressor | pa_regressor | 0.000000 | 0.010000 | fixed_share_same_leader |
| 287 | switch | pa_regressor | lin_lr_0_001 | 0.182724 | 0.010000 | fixed_share_weight_advantage |
| 311 | stay | lin_lr_0_001 | lin_lr_0_001 | 0.000000 | 0.010000 | fixed_share_same_leader |
