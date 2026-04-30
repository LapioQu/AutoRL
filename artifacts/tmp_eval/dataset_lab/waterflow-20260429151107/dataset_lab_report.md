# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T15:11:11.269281+00:00`
- dataset_name: `WaterFlow`
- task_type: `regression`
- target_column: `water_flow_lps`
- policy_name: `fixed_share_portfolio`
- source_row_count: `1268`
- source_rows_used: `1268`
- sample_count: `1265`
- feature_count: `3`
- next_prediction: `103.96383914203936`
- prediction_confidence: `0.9762` (high)

## Comparative Metrics

- adaptive_score: `0.949918`
- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.937528`
- delta_vs_best_fixed: `+0.012390`
- oracle_score: `0.973763`
- oracle_gain: `0.036235`
- oracle_capture_ratio: `34.19%`
- final_strategy: `lin_lr_0_01`
- switch_count: `5`

## Interpretation

- Adaptive policy `fixed_share_portfolio` finished on strategy `lin_lr_0_01` after 5 switches.
- It achieved `0.9499` against the best fixed baseline `knn_regressor` at `0.9375`.
- Oracle upper bound on this stream is `0.9738`. Available oracle gain over best fixed is `0.0362`, and the current adaptive controller captures `34.2%` of it.
- The uploaded stream looks non-stationary enough for adaptation to help: the gain over best fixed is `0.0124`.
- Multiple switches suggest regime changes or at least changing local winners across the stream.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `103.9638` based on the latest lagged context `['104.3', '104.23', '104.1']`.

## Caveats

- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "Time": "2022-05-16 22:00:00+02:00",
  "water_flow_lps": "104.1"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 1253 | 104.39 | 103.76838096990959 | {"target_lag_1": 103.78, "target_lag_2": 102.92, "target_lag_3": 102.86} |
| 1254 | 104.71 | 104.37724266826235 | {"target_lag_1": 104.39, "target_lag_2": 103.78, "target_lag_3": 102.92} |
| 1255 | 104.77 | 104.60934890244857 | {"target_lag_1": 104.71, "target_lag_2": 104.39, "target_lag_3": 103.78} |
| 1256 | 104.69 | 104.60706345434848 | {"target_lag_1": 104.77, "target_lag_2": 104.71, "target_lag_3": 104.39} |
| 1257 | 104.69 | 104.49493356183692 | {"target_lag_1": 104.69, "target_lag_2": 104.77, "target_lag_3": 104.71} |
| 1258 | 104.64 | 104.4922446419236 | {"target_lag_1": 104.69, "target_lag_2": 104.69, "target_lag_3": 104.77} |
| 1259 | 104.59 | 104.45366738911198 | {"target_lag_1": 104.64, "target_lag_2": 104.69, "target_lag_3": 104.69} |
| 1260 | 104.62 | 104.40625815822058 | {"target_lag_1": 104.59, "target_lag_2": 104.64, "target_lag_3": 104.69} |
| 1261 | 104.65 | 104.44533682040687 | {"target_lag_1": 104.62, "target_lag_2": 104.59, "target_lag_3": 104.64} |
| 1262 | 104.3 | 104.48426240300184 | {"target_lag_1": 104.65, "target_lag_2": 104.62, "target_lag_3": 104.59} |
| 1263 | 104.23 | 104.12799872935612 | {"target_lag_1": 104.3, "target_lag_2": 104.65, "target_lag_3": 104.62} |
| 1264 | 104.1 | 104.05622557308207 | {"target_lag_1": 104.23, "target_lag_2": 104.3, "target_lag_3": 104.65} |

## Visual Artifacts

- score_plot_path: `artifacts\tmp_eval\dataset_lab\waterflow-20260429151107\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\tmp_eval\dataset_lab\waterflow-20260429151107\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\tmp_eval\dataset_lab\waterflow-20260429151107\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\tmp_eval\dataset_lab\waterflow-20260429151107`
- replay_summary_json_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\waterflow-20260429151107\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\waterflow-20260429151107\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\waterflow-20260429151107\summary.md`
