# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T13:19:16.286640+00:00`
- dataset_name: `pollution`
- task_type: `regression`
- target_column: `pm2.5`
- policy_name: `fixed_share_portfolio`
- source_row_count: `43824`
- source_rows_used: `2000`
- sample_count: `1997`
- feature_count: `15`
- next_prediction: `133.34291935569945`
- prediction_confidence: `0.2000` (low)

## Comparative Metrics

- adaptive_score: `0.842885`
- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.837381`
- delta_vs_best_fixed: `+0.005504`
- oracle_score: `0.913213`
- oracle_gain: `0.075832`
- oracle_capture_ratio: `7.26%`
- final_strategy: `lin_lr_0_002`
- switch_count: `14`

## Interpretation

- Adaptive policy `fixed_share_portfolio` finished on strategy `lin_lr_0_002` after 14 switches.
- It achieved `0.8429` against the best fixed baseline `lin_lr_0_002` at `0.8374`.
- Oracle upper bound on this stream is `0.9132`. Available oracle gain over best fixed is `0.0758`, and the current adaptive controller captures `7.3%` of it.
- The uploaded stream looks non-stationary enough for adaptation to help: the gain over best fixed is `0.0055`.
- Multiple switches suggest regime changes or at least changing local winners across the stream.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `133.3429` based on the latest lagged context `['132', '142', '147']`.

## Caveats

- The stream is replayed in the original CSV row order.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "No": "2095",
  "year": "2010",
  "month": "3",
  "day": "29",
  "hour": "6",
  "pm2.5": "147",
  "DEWP": "-4",
  "TEMP": "3",
  "PRES": "1025",
  "cbwd": "cv",
  "Iws": "1.78",
  "Is": "0",
  "Ir": "0"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 1985 | 48.0 | 60.02603122265654 | {"DEWP": -8, "Ir": 0, "Is": 0, "Iws": 25.93, "No": 2084, "PRES": 1023, "TEMP": 10, "cbwd": "SE", "day": 28, "hour": 19, "month": 3, "target_lag_1": 46.0, "target_lag_2": 57.0, "target_lag_3": 63.0, "year": 2010} |
| 1986 | 60.0 | 53.646875577111345 | {"DEWP": -9, "Ir": 0, "Is": 0, "Iws": 30.85, "No": 2085, "PRES": 1024, "TEMP": 12, "cbwd": "SE", "day": 28, "hour": 20, "month": 3, "target_lag_1": 48.0, "target_lag_2": 46.0, "target_lag_3": 57.0, "year": 2010} |
| 1987 | 57.0 | 65.33791919571746 | {"DEWP": -8, "Ir": 0, "Is": 0, "Iws": 32.64, "No": 2086, "PRES": 1024, "TEMP": 9, "cbwd": "SE", "day": 28, "hour": 21, "month": 3, "target_lag_1": 60.0, "target_lag_2": 48.0, "target_lag_3": 46.0, "year": 2010} |
| 1988 | 72.0 | 61.40478990858262 | {"DEWP": -8, "Ir": 0, "Is": 0, "Iws": 34.43, "No": 2087, "PRES": 1025, "TEMP": 8, "cbwd": "SE", "day": 28, "hour": 22, "month": 3, "target_lag_1": 57.0, "target_lag_2": 60.0, "target_lag_3": 48.0, "year": 2010} |
| 1989 | 82.0 | 74.60832997248934 | {"DEWP": -7, "Ir": 0, "Is": 0, "Iws": 35.32, "No": 2088, "PRES": 1025, "TEMP": 7, "cbwd": "SE", "day": 28, "hour": 23, "month": 3, "target_lag_1": 72.0, "target_lag_2": 57.0, "target_lag_3": 60.0, "year": 2010} |
| 1990 | 92.0 | 78.35356445793882 | {"DEWP": -4, "Ir": 0, "Is": 0, "Iws": 37.11, "No": 2089, "PRES": 1025, "TEMP": 6, "cbwd": "SE", "day": 29, "hour": 0, "month": 3, "target_lag_1": 82.0, "target_lag_2": 72.0, "target_lag_3": 57.0, "year": 2010} |
| 1991 | 100.0 | 79.98340674016885 | {"DEWP": -6, "Ir": 0, "Is": 0, "Iws": 38.9, "No": 2090, "PRES": 1025, "TEMP": 6, "cbwd": "SE", "day": 29, "hour": 1, "month": 3, "target_lag_1": 92.0, "target_lag_2": 82.0, "target_lag_3": 72.0, "year": 2010} |
| 1992 | 117.0 | 86.35141937329661 | {"DEWP": -6, "Ir": 0, "Is": 0, "Iws": 40.69, "No": 2091, "PRES": 1025, "TEMP": 5, "cbwd": "SE", "day": 29, "hour": 2, "month": 3, "target_lag_1": 100.0, "target_lag_2": 92.0, "target_lag_3": 82.0, "year": 2010} |
| 1993 | 129.0 | 101.55137537280416 | {"DEWP": -5, "Ir": 0, "Is": 0, "Iws": 42.48, "No": 2092, "PRES": 1024, "TEMP": 5, "cbwd": "SE", "day": 29, "hour": 3, "month": 3, "target_lag_1": 117.0, "target_lag_2": 100.0, "target_lag_3": 92.0, "year": 2010} |
| 1994 | 132.0 | 113.31306730756958 | {"DEWP": -4, "Ir": 0, "Is": 0, "Iws": 43.37, "No": 2093, "PRES": 1024, "TEMP": 3, "cbwd": "SE", "day": 29, "hour": 4, "month": 3, "target_lag_1": 129.0, "target_lag_2": 117.0, "target_lag_3": 100.0, "year": 2010} |
| 1995 | 142.0 | 126.41039455998006 | {"DEWP": -4, "Ir": 0, "Is": 0, "Iws": 0.89, "No": 2094, "PRES": 1024, "TEMP": 2, "cbwd": "cv", "day": 29, "hour": 5, "month": 3, "target_lag_1": 132.0, "target_lag_2": 129.0, "target_lag_3": 117.0, "year": 2010} |
| 1996 | 147.0 | 130.26959818177963 | {"DEWP": -4, "Ir": 0, "Is": 0, "Iws": 1.78, "No": 2095, "PRES": 1025, "TEMP": 3, "cbwd": "cv", "day": 29, "hour": 6, "month": 3, "target_lag_1": 142.0, "target_lag_2": 132.0, "target_lag_3": 129.0, "year": 2010} |

## Visual Artifacts

- score_plot_path: `artifacts\dataset_lab\pollution-20260429131907\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\dataset_lab\pollution-20260429131907\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\dataset_lab\pollution-20260429131907\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\dataset_lab\pollution-20260429131907`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab\pollution-20260429131907\auto_meta_selection\fixed_share_portfolio\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab\pollution-20260429131907\auto_meta_selection\fixed_share_portfolio\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab\pollution-20260429131907\auto_meta_selection\fixed_share_portfolio\summary.md`
