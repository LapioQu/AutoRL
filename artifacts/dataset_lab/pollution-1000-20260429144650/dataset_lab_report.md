# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T14:46:55.492860+00:00`
- dataset_name: `pollution-1000`
- task_type: `regression`
- target_column: `pm2.5`
- policy_name: `recent_leader_meta`
- source_row_count: `43824`
- source_rows_used: `1000`
- sample_count: `997`
- feature_count: `15`
- next_prediction: `19.6`
- prediction_confidence: `0.2023` (low)

## Comparative Metrics

- adaptive_score: `0.844537`
- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.844537`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.915990`
- oracle_gain: `0.071453`
- oracle_capture_ratio: `0.00%`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Interpretation

- Adaptive policy `recent_leader_meta` finished on strategy `knn_regressor` after 0 switches.
- It achieved `0.8445` against the best fixed baseline `knn_regressor` at `0.8445`.
- Oracle upper bound on this stream is `0.9160`. Available oracle gain over best fixed is `0.0715`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `19.6000` based on the latest lagged context `['39', '25', '17']`.

## Caveats

- The stream is replayed in the original CSV row order.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "No": "1092",
  "year": "2010",
  "month": "2",
  "day": "15",
  "hour": "11",
  "pm2.5": "17",
  "DEWP": "-23",
  "TEMP": "-4",
  "PRES": "1037",
  "cbwd": "NW",
  "Iws": "15.2",
  "Is": "0",
  "Ir": "0"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 985 | 45.0 | 43.4 | {"DEWP": -21, "Ir": 0, "Is": 0, "Iws": 4.02, "No": 1081, "PRES": 1036, "TEMP": -7, "cbwd": "NE", "day": 15, "hour": 0, "month": 2, "target_lag_1": 46.0, "target_lag_2": 67.0, "target_lag_3": 51.0, "year": 2010} |
| 986 | 27.0 | 22.2 | {"DEWP": -22, "Ir": 0, "Is": 0, "Iws": 8.04, "No": 1082, "PRES": 1037, "TEMP": -7, "cbwd": "NE", "day": 15, "hour": 1, "month": 2, "target_lag_1": 45.0, "target_lag_2": 46.0, "target_lag_3": 67.0, "year": 2010} |
| 987 | 24.0 | 24.2 | {"DEWP": -22, "Ir": 0, "Is": 0, "Iws": 12.96, "No": 1083, "PRES": 1036, "TEMP": -7, "cbwd": "NE", "day": 15, "hour": 2, "month": 2, "target_lag_1": 27.0, "target_lag_2": 45.0, "target_lag_3": 46.0, "year": 2010} |
| 988 | 18.0 | 20.2 | {"DEWP": -22, "Ir": 0, "Is": 0, "Iws": 0.89, "No": 1084, "PRES": 1037, "TEMP": -8, "cbwd": "cv", "day": 15, "hour": 3, "month": 2, "target_lag_1": 24.0, "target_lag_2": 27.0, "target_lag_3": 45.0, "year": 2010} |
| 989 | 15.0 | 18.4 | {"DEWP": -22, "Ir": 0, "Is": 0, "Iws": 1.78, "No": 1085, "PRES": 1036, "TEMP": -8, "cbwd": "cv", "day": 15, "hour": 4, "month": 2, "target_lag_1": 18.0, "target_lag_2": 24.0, "target_lag_3": 27.0, "year": 2010} |
| 990 | 17.0 | 14.0 | {"DEWP": -22, "Ir": 0, "Is": 0, "Iws": 3.13, "No": 1086, "PRES": 1036, "TEMP": -9, "cbwd": "NE", "day": 15, "hour": 5, "month": 2, "target_lag_1": 15.0, "target_lag_2": 18.0, "target_lag_3": 24.0, "year": 2010} |
| 991 | 11.0 | 12.6 | {"DEWP": -22, "Ir": 0, "Is": 0, "Iws": 7.15, "No": 1087, "PRES": 1036, "TEMP": -9, "cbwd": "NE", "day": 15, "hour": 6, "month": 2, "target_lag_1": 17.0, "target_lag_2": 15.0, "target_lag_3": 18.0, "year": 2010} |
| 992 | 16.0 | 25.2 | {"DEWP": -22, "Ir": 0, "Is": 0, "Iws": 4.02, "No": 1088, "PRES": 1037, "TEMP": -10, "cbwd": "NW", "day": 15, "hour": 7, "month": 2, "target_lag_1": 11.0, "target_lag_2": 17.0, "target_lag_3": 15.0, "year": 2010} |
| 993 | 16.0 | 12.8 | {"DEWP": -21, "Ir": 0, "Is": 0, "Iws": 7.15, "No": 1089, "PRES": 1037, "TEMP": -9, "cbwd": "NW", "day": 15, "hour": 8, "month": 2, "target_lag_1": 16.0, "target_lag_2": 11.0, "target_lag_3": 17.0, "year": 2010} |
| 994 | 39.0 | 16.6 | {"DEWP": -22, "Ir": 0, "Is": 0, "Iws": 10.28, "No": 1090, "PRES": 1038, "TEMP": -6, "cbwd": "NW", "day": 15, "hour": 9, "month": 2, "target_lag_1": 16.0, "target_lag_2": 16.0, "target_lag_3": 11.0, "year": 2010} |
| 995 | 25.0 | 25.2 | {"DEWP": -23, "Ir": 0, "Is": 0, "Iws": 12.07, "No": 1091, "PRES": 1038, "TEMP": -5, "cbwd": "NW", "day": 15, "hour": 10, "month": 2, "target_lag_1": 39.0, "target_lag_2": 16.0, "target_lag_3": 16.0, "year": 2010} |
| 996 | 17.0 | 24.0 | {"DEWP": -23, "Ir": 0, "Is": 0, "Iws": 15.2, "No": 1092, "PRES": 1037, "TEMP": -4, "cbwd": "NW", "day": 15, "hour": 11, "month": 2, "target_lag_1": 25.0, "target_lag_2": 39.0, "target_lag_3": 16.0, "year": 2010} |

## Visual Artifacts

- score_plot_path: `artifacts\dataset_lab\pollution-1000-20260429144650\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\dataset_lab\pollution-1000-20260429144650\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\dataset_lab\pollution-1000-20260429144650\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\dataset_lab\pollution-1000-20260429144650`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab\pollution-1000-20260429144650\auto_meta_selection\recent_leader_meta\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab\pollution-1000-20260429144650\auto_meta_selection\recent_leader_meta\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab\pollution-1000-20260429144650\auto_meta_selection\recent_leader_meta\summary.md`
