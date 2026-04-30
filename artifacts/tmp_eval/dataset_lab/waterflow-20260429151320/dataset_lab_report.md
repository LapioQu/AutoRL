# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T15:13:23.774482+00:00`
- dataset_name: `WaterFlow`
- task_type: `regression`
- target_column: `water_flow_lps`
- policy_name: `recent_leader_meta`
- source_row_count: `1268`
- source_rows_used: `1268`
- sample_count: `1265`
- feature_count: `3`
- next_prediction: `102.66799999999999`
- prediction_confidence: `0.9762` (high)

## Comparative Metrics

- adaptive_score: `0.937470`
- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.937470`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.973752`
- oracle_gain: `0.036282`
- oracle_capture_ratio: `0.00%`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Interpretation

- Adaptive policy `recent_leader_meta` finished on strategy `knn_regressor` after 0 switches.
- It achieved `0.9375` against the best fixed baseline `knn_regressor` at `0.9375`.
- Oracle upper bound on this stream is `0.9738`. Available oracle gain over best fixed is `0.0363`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `102.6680` based on the latest lagged context `['104.3', '104.23', '104.1']`.

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
| 1253 | 104.39 | 103.156 | {"target_lag_1": 103.78, "target_lag_2": 102.92, "target_lag_3": 102.86} |
| 1254 | 104.71 | 103.542 | {"target_lag_1": 104.39, "target_lag_2": 103.78, "target_lag_3": 102.92} |
| 1255 | 104.77 | 102.952 | {"target_lag_1": 104.71, "target_lag_2": 104.39, "target_lag_3": 103.78} |
| 1256 | 104.69 | 102.696 | {"target_lag_1": 104.77, "target_lag_2": 104.71, "target_lag_3": 104.39} |
| 1257 | 104.69 | 103.01 | {"target_lag_1": 104.69, "target_lag_2": 104.77, "target_lag_3": 104.71} |
| 1258 | 104.64 | 103.45 | {"target_lag_1": 104.69, "target_lag_2": 104.69, "target_lag_3": 104.77} |
| 1259 | 104.59 | 103.776 | {"target_lag_1": 104.64, "target_lag_2": 104.69, "target_lag_3": 104.69} |
| 1260 | 104.62 | 103.756 | {"target_lag_1": 104.59, "target_lag_2": 104.64, "target_lag_3": 104.69} |
| 1261 | 104.65 | 103.742 | {"target_lag_1": 104.62, "target_lag_2": 104.59, "target_lag_3": 104.64} |
| 1262 | 104.3 | 104.638 | {"target_lag_1": 104.65, "target_lag_2": 104.62, "target_lag_3": 104.59} |
| 1263 | 104.23 | 102.906 | {"target_lag_1": 104.3, "target_lag_2": 104.65, "target_lag_3": 104.62} |
| 1264 | 104.1 | 102.58200000000001 | {"target_lag_1": 104.23, "target_lag_2": 104.3, "target_lag_3": 104.65} |

## Visual Artifacts

- score_plot_path: `artifacts\tmp_eval\dataset_lab\waterflow-20260429151320\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\tmp_eval\dataset_lab\waterflow-20260429151320\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\tmp_eval\dataset_lab\waterflow-20260429151320\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\tmp_eval\dataset_lab\waterflow-20260429151320`
- replay_summary_json_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\waterflow-20260429151320\auto_meta_selection\recent_leader_meta\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\waterflow-20260429151320\auto_meta_selection\recent_leader_meta\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\waterflow-20260429151320\auto_meta_selection\recent_leader_meta\summary.md`
