# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T14:47:59.681278+00:00`
- dataset_name: `pollution-8000`
- task_type: `regression`
- target_column: `pm2.5`
- policy_name: `best_fixed_guard`
- source_row_count: `43824`
- source_rows_used: `8000`
- sample_count: `7997`
- feature_count: `15`
- next_prediction: `10.556629638161475`
- prediction_confidence: `0.2000` (low)

## Comparative Metrics

- adaptive_score: `0.864799`
- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.864799`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.915589`
- oracle_gain: `0.050789`
- oracle_capture_ratio: `0.00%`
- final_strategy: `lin_lr_0_002`
- switch_count: `0`

## Interpretation

- Adaptive policy `best_fixed_guard` finished on strategy `lin_lr_0_002` after 0 switches.
- It achieved `0.8648` against the best fixed baseline `lin_lr_0_002` at `0.8648`.
- Oracle upper bound on this stream is `0.9156`. Available oracle gain over best fixed is `0.0508`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `10.5566` based on the latest lagged context `['18', '16', '16']`.

## Caveats

- The stream is replayed in the original CSV row order.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "No": "8669",
  "year": "2010",
  "month": "12",
  "day": "28",
  "hour": "4",
  "pm2.5": "16",
  "DEWP": "-20",
  "TEMP": "-5",
  "PRES": "1017",
  "cbwd": "NW",
  "Iws": "139.47",
  "Is": "0",
  "Ir": "0"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 7985 | 28.0 | 39.02914257920074 | {"DEWP": -15, "Ir": 0, "Is": 0, "Iws": 55.88, "No": 8658, "PRES": 1009, "TEMP": 4, "cbwd": "NW", "day": 27, "hour": 17, "month": 12, "target_lag_1": 31.0, "target_lag_2": 38.0, "target_lag_3": 47.0, "year": 2010} |
| 7986 | 21.0 | 31.800914519667757 | {"DEWP": -19, "Ir": 0, "Is": 0, "Iws": 64.82, "No": 8659, "PRES": 1010, "TEMP": 3, "cbwd": "NW", "day": 27, "hour": 18, "month": 12, "target_lag_1": 28.0, "target_lag_2": 31.0, "target_lag_3": 38.0, "year": 2010} |
| 7987 | 16.0 | 22.938484111312576 | {"DEWP": -21, "Ir": 0, "Is": 0, "Iws": 73.76, "No": 8660, "PRES": 1012, "TEMP": 2, "cbwd": "NW", "day": 27, "hour": 19, "month": 12, "target_lag_1": 21.0, "target_lag_2": 28.0, "target_lag_3": 31.0, "year": 2010} |
| 7988 | 20.0 | 18.77091980658652 | {"DEWP": -21, "Ir": 0, "Is": 0, "Iws": 86.72, "No": 8661, "PRES": 1013, "TEMP": 1, "cbwd": "NW", "day": 27, "hour": 20, "month": 12, "target_lag_1": 16.0, "target_lag_2": 21.0, "target_lag_3": 28.0, "year": 2010} |
| 7989 | 29.0 | 27.67127931003749 | {"DEWP": -19, "Ir": 0, "Is": 0, "Iws": 94.77, "No": 8662, "PRES": 1014, "TEMP": -1, "cbwd": "NW", "day": 27, "hour": 21, "month": 12, "target_lag_1": 20.0, "target_lag_2": 16.0, "target_lag_3": 21.0, "year": 2010} |
| 7990 | 15.0 | 37.02174095385631 | {"DEWP": -19, "Ir": 0, "Is": 0, "Iws": 101.92, "No": 8663, "PRES": 1015, "TEMP": -2, "cbwd": "NW", "day": 27, "hour": 22, "month": 12, "target_lag_1": 29.0, "target_lag_2": 20.0, "target_lag_3": 16.0, "year": 2010} |
| 7991 | 21.0 | 22.33670796932642 | {"DEWP": -19, "Ir": 0, "Is": 0, "Iws": 107.73, "No": 8664, "PRES": 1016, "TEMP": -3, "cbwd": "NW", "day": 27, "hour": 23, "month": 12, "target_lag_1": 15.0, "target_lag_2": 29.0, "target_lag_3": 20.0, "year": 2010} |
| 7992 | 16.0 | 8.572790051627592 | {"DEWP": -20, "Ir": 0, "Is": 0, "Iws": 112.65, "No": 8665, "PRES": 1016, "TEMP": -4, "cbwd": "NW", "day": 28, "hour": 0, "month": 12, "target_lag_1": 21.0, "target_lag_2": 15.0, "target_lag_3": 29.0, "year": 2010} |
| 7993 | 17.0 | 6.997760953977448 | {"DEWP": -20, "Ir": 0, "Is": 0, "Iws": 118.46, "No": 8666, "PRES": 1016, "TEMP": -5, "cbwd": "NW", "day": 28, "hour": 1, "month": 12, "target_lag_1": 16.0, "target_lag_2": 21.0, "target_lag_3": 15.0, "year": 2010} |
| 7994 | 18.0 | 8.024912025231814 | {"DEWP": -21, "Ir": 0, "Is": 0, "Iws": 123.38, "No": 8667, "PRES": 1017, "TEMP": -6, "cbwd": "NW", "day": 28, "hour": 2, "month": 12, "target_lag_1": 17.0, "target_lag_2": 16.0, "target_lag_3": 21.0, "year": 2010} |
| 7995 | 16.0 | 11.126162353743211 | {"DEWP": -20, "Ir": 0, "Is": 0, "Iws": 132.32, "No": 8668, "PRES": 1017, "TEMP": -5, "cbwd": "NW", "day": 28, "hour": 3, "month": 12, "target_lag_1": 18.0, "target_lag_2": 17.0, "target_lag_3": 16.0, "year": 2010} |
| 7996 | 16.0 | 9.936542702057146 | {"DEWP": -20, "Ir": 0, "Is": 0, "Iws": 139.47, "No": 8669, "PRES": 1017, "TEMP": -5, "cbwd": "NW", "day": 28, "hour": 4, "month": 12, "target_lag_1": 16.0, "target_lag_2": 18.0, "target_lag_3": 17.0, "year": 2010} |

## Visual Artifacts

- score_plot_path: `artifacts\dataset_lab\pollution-8000-20260429144725\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\dataset_lab\pollution-8000-20260429144725\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\dataset_lab\pollution-8000-20260429144725\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\dataset_lab\pollution-8000-20260429144725`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab\pollution-8000-20260429144725\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab\pollution-8000-20260429144725\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab\pollution-8000-20260429144725\summary.md`
