# Real-Stream Benchmark Replay

- dataset: `WaterFlow`
- score_name: `normalized_reward`
- policy_name: `recent_leader_meta`
- samples: `317`
- source: Real pipeline water-flow stream replayed in temporal order; evaluation includes anomalous low-flow segments and a pumping-induced peak.
- source_url: ``
- start_strategy: `pa_regressor`
- final_strategy: `pa_regressor`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.630479 |
| oracle | 0.704637 |
| lin_lr_0_0005 | 0.493435 |
| lin_lr_0_001 | 0.510585 |
| pa_regressor | 0.630479 |

- best_fixed_strategy: `pa_regressor`
- best_fixed_score: `0.630479`
- oracle_score: `0.704637`
- oracle_gain: `0.074159`
- oracle_capture_ratio: `0.000000`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `13`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 47 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_warmup_same |
| 71 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 95 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 119 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 143 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 167 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 191 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 215 | stay | pa_regressor | lin_lr_0_001 | 0.006125 | 0.002000 | recent_leader_incumbent_floor |
| 239 | stay | pa_regressor | lin_lr_0_001 | 0.016934 | 0.002000 | recent_leader_incumbent_floor |
| 263 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 287 | stay | pa_regressor | pa_regressor | 0.000000 | 0.002000 | recent_leader_same |
| 311 | stay | pa_regressor | lin_lr_0_001 | 0.044228 | 0.002000 | recent_leader_incumbent_floor |
