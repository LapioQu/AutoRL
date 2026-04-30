# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T14:43:44.067340+00:00`
- dataset_name: `pollution`
- task_type: `classification`
- target_column: `pm2.5`
- policy_name: `fixed_share_portfolio`
- source_row_count: `43824`
- source_rows_used: `41757`
- sample_count: `41757`
- feature_count: `12`
- next_prediction: `12`
- prediction_confidence: `0.7500` (medium)

## Comparative Metrics

- adaptive_score: `0.036904`
- best_fixed_strategy: `knn_classifier`
- best_fixed_score: `0.042125`
- delta_vs_best_fixed: `-0.005221`
- oracle_score: `0.074287`
- oracle_gain: `0.032162`
- oracle_capture_ratio: `0.00%`
- final_strategy: `softmax_lr_0_20`
- switch_count: `144`

## Interpretation

- Adaptive policy `fixed_share_portfolio` finished on strategy `softmax_lr_0_20` after 144 switches.
- It achieved `0.0369` against the best fixed baseline `knn_classifier` at `0.0421`.
- Oracle upper bound on this stream is `0.0743`. Available oracle gain over best fixed is `0.0322`, and the current adaptive controller captures `0.0%` of it.
- The current stationary portfolio dominated the adaptive controller here; the gap is `-0.0052`.
- Multiple switches suggest regime changes or at least changing local winners across the stream.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step class from the final adaptive strategy is `12` based on the latest lagged context `['10', '8', '12']`.

## Caveats

- The stream is replayed in the original CSV row order.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is prequential accuracy over the uploaded stream.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "No": "43824",
  "year": "2014",
  "month": "12",
  "day": "31",
  "hour": "23",
  "pm2.5": "12",
  "DEWP": "-21",
  "TEMP": "-3",
  "PRES": "1034",
  "cbwd": "NW",
  "Iws": "249.85",
  "Is": "0",
  "Ir": "0"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 41745 | 17 | 12 | {"DEWP": -22, "Ir": 0, "Is": 0, "Iws": 177.44, "No": 43813, "PRES": 1033, "TEMP": 0, "cbwd": "NW", "day": 31, "hour": 12, "month": 12, "year": 2014} |
| 41746 | 11 | 17 | {"DEWP": -27, "Ir": 0, "Is": 0, "Iws": 186.38, "No": 43814, "PRES": 1032, "TEMP": 0, "cbwd": "NW", "day": 31, "hour": 13, "month": 12, "year": 2014} |
| 41747 | 9 | 11 | {"DEWP": -27, "Ir": 0, "Is": 0, "Iws": 196.21, "No": 43815, "PRES": 1032, "TEMP": 1, "cbwd": "NW", "day": 31, "hour": 14, "month": 12, "year": 2014} |
| 41748 | 11 | 9 | {"DEWP": -26, "Ir": 0, "Is": 0, "Iws": 205.15, "No": 43816, "PRES": 1032, "TEMP": 1, "cbwd": "NW", "day": 31, "hour": 15, "month": 12, "year": 2014} |
| 41749 | 8 | 11 | {"DEWP": -23, "Ir": 0, "Is": 0, "Iws": 214.09, "No": 43817, "PRES": 1032, "TEMP": 0, "cbwd": "NW", "day": 31, "hour": 16, "month": 12, "year": 2014} |
| 41750 | 9 | 8 | {"DEWP": -22, "Ir": 0, "Is": 0, "Iws": 221.24, "No": 43818, "PRES": 1033, "TEMP": -1, "cbwd": "NW", "day": 31, "hour": 17, "month": 12, "year": 2014} |
| 41751 | 10 | 9 | {"DEWP": -22, "Ir": 0, "Is": 0, "Iws": 226.16, "No": 43819, "PRES": 1033, "TEMP": -2, "cbwd": "NW", "day": 31, "hour": 18, "month": 12, "year": 2014} |
| 41752 | 8 | 10 | {"DEWP": -23, "Ir": 0, "Is": 0, "Iws": 231.97, "No": 43820, "PRES": 1034, "TEMP": -2, "cbwd": "NW", "day": 31, "hour": 19, "month": 12, "year": 2014} |
| 41753 | 10 | 8 | {"DEWP": -22, "Ir": 0, "Is": 0, "Iws": 237.78, "No": 43821, "PRES": 1034, "TEMP": -3, "cbwd": "NW", "day": 31, "hour": 20, "month": 12, "year": 2014} |
| 41754 | 10 | 10 | {"DEWP": -22, "Ir": 0, "Is": 0, "Iws": 242.7, "No": 43822, "PRES": 1034, "TEMP": -3, "cbwd": "NW", "day": 31, "hour": 21, "month": 12, "year": 2014} |
| 41755 | 8 | 10 | {"DEWP": -22, "Ir": 0, "Is": 0, "Iws": 246.72, "No": 43823, "PRES": 1034, "TEMP": -4, "cbwd": "NW", "day": 31, "hour": 22, "month": 12, "year": 2014} |
| 41756 | 12 | 8 | {"DEWP": -21, "Ir": 0, "Is": 0, "Iws": 249.85, "No": 43824, "PRES": 1034, "TEMP": -3, "cbwd": "NW", "day": 31, "hour": 23, "month": 12, "year": 2014} |

## Visual Artifacts

- score_plot_path: `artifacts\dataset_lab_jobs\pollution-20260429140746-40dc4ef7\analysis\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\dataset_lab_jobs\pollution-20260429140746-40dc4ef7\analysis\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\dataset_lab_jobs\pollution-20260429140746-40dc4ef7\analysis\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\dataset_lab_jobs\pollution-20260429140746-40dc4ef7\analysis`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab_jobs\pollution-20260429140746-40dc4ef7\analysis\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab_jobs\pollution-20260429140746-40dc4ef7\analysis\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab_jobs\pollution-20260429140746-40dc4ef7\analysis\summary.md`
