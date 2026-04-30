# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T14:47:08.785287+00:00`
- dataset_name: `pollution-detail`
- task_type: `regression`
- target_column: `pm2.5`
- policy_name: `fixed_share_portfolio`
- source_row_count: `43824`
- source_rows_used: `4000`
- sample_count: `3997`
- feature_count: `15`
- next_prediction: `177.6897225737224`
- prediction_confidence: `0.2000` (low)

## Comparative Metrics

- adaptive_score: `0.839117`
- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.838480`
- delta_vs_best_fixed: `+0.000637`
- oracle_score: `0.904514`
- oracle_gain: `0.066034`
- oracle_capture_ratio: `0.96%`
- final_strategy: `lin_lr_0_002`
- switch_count: `21`

## Interpretation

- Adaptive policy `fixed_share_portfolio` finished on strategy `lin_lr_0_002` after 21 switches.
- It achieved `0.8391` against the best fixed baseline `lin_lr_0_002` at `0.8385`.
- Oracle upper bound on this stream is `0.9045`. Available oracle gain over best fixed is `0.0660`, and the current adaptive controller captures `1.0%` of it.
- The uploaded stream looks non-stationary enough for adaptation to help: the gain over best fixed is `0.0006`.
- Multiple switches suggest regime changes or at least changing local winners across the stream.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `177.6897` based on the latest lagged context `['159', '174', '189']`.

## Caveats

- The stream is replayed in the original CSV row order.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "No": "4291",
  "year": "2010",
  "month": "6",
  "day": "28",
  "hour": "18",
  "pm2.5": "189",
  "DEWP": "19",
  "TEMP": "30",
  "PRES": "1001",
  "cbwd": "SE",
  "Iws": "25.47",
  "Is": "0",
  "Ir": "0"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 3985 | 112.0 | 128.6944954921016 | {"DEWP": 20, "Ir": 0, "Is": 0, "Iws": 8.05, "No": 4280, "PRES": 1002, "TEMP": 23, "cbwd": "NW", "day": 28, "hour": 7, "month": 6, "target_lag_1": 124.0, "target_lag_2": 118.0, "target_lag_3": 134.0, "year": 2010} |
| 3986 | 101.0 | 115.58148680378473 | {"DEWP": 19, "Ir": 0, "Is": 0, "Iws": 9.84, "No": 4281, "PRES": 1002, "TEMP": 25, "cbwd": "NW", "day": 28, "hour": 8, "month": 6, "target_lag_1": 112.0, "target_lag_2": 124.0, "target_lag_3": 118.0, "year": 2010} |
| 3987 | 131.0 | 106.7051070393205 | {"DEWP": 19, "Ir": 0, "Is": 0, "Iws": 0.89, "No": 4282, "PRES": 1002, "TEMP": 26, "cbwd": "cv", "day": 28, "hour": 9, "month": 6, "target_lag_1": 101.0, "target_lag_2": 112.0, "target_lag_3": 124.0, "year": 2010} |
| 3988 | 137.0 | 130.43746484148824 | {"DEWP": 18, "Ir": 0, "Is": 0, "Iws": 1.78, "No": 4283, "PRES": 1002, "TEMP": 27, "cbwd": "cv", "day": 28, "hour": 10, "month": 6, "target_lag_1": 131.0, "target_lag_2": 101.0, "target_lag_3": 112.0, "year": 2010} |
| 3989 | 166.0 | 133.02476070199327 | {"DEWP": 19, "Ir": 0, "Is": 0, "Iws": 3.57, "No": 4284, "PRES": 1002, "TEMP": 29, "cbwd": "cv", "day": 28, "hour": 11, "month": 6, "target_lag_1": 137.0, "target_lag_2": 131.0, "target_lag_3": 101.0, "year": 2010} |
| 3990 | 152.0 | 155.3501046060009 | {"DEWP": 18, "Ir": 0, "Is": 0, "Iws": 3.13, "No": 4285, "PRES": 1002, "TEMP": 30, "cbwd": "SE", "day": 28, "hour": 12, "month": 6, "target_lag_1": 166.0, "target_lag_2": 137.0, "target_lag_3": 131.0, "year": 2010} |
| 3991 | 153.0 | 142.48111076500177 | {"DEWP": 18, "Ir": 0, "Is": 0, "Iws": 6.26, "No": 4286, "PRES": 1001, "TEMP": 30, "cbwd": "SE", "day": 28, "hour": 13, "month": 6, "target_lag_1": 152.0, "target_lag_2": 166.0, "target_lag_3": 137.0, "year": 2010} |
| 3992 | 164.0 | 143.82711159929346 | {"DEWP": 18, "Ir": 0, "Is": 0, "Iws": 10.28, "No": 4287, "PRES": 1001, "TEMP": 31, "cbwd": "SE", "day": 28, "hour": 14, "month": 6, "target_lag_1": 153.0, "target_lag_2": 152.0, "target_lag_3": 166.0, "year": 2010} |
| 3993 | 174.0 | 154.1201984584742 | {"DEWP": 19, "Ir": 0, "Is": 0, "Iws": 14.3, "No": 4288, "PRES": 1001, "TEMP": 32, "cbwd": "SE", "day": 28, "hour": 15, "month": 6, "target_lag_1": 164.0, "target_lag_2": 153.0, "target_lag_3": 152.0, "year": 2010} |
| 3994 | 159.0 | 162.88648489529498 | {"DEWP": 19, "Ir": 0, "Is": 0, "Iws": 18.32, "No": 4289, "PRES": 1001, "TEMP": 31, "cbwd": "SE", "day": 28, "hour": 16, "month": 6, "target_lag_1": 174.0, "target_lag_2": 164.0, "target_lag_3": 153.0, "year": 2010} |
| 3995 | 174.0 | 148.85594232621543 | {"DEWP": 18, "Ir": 0, "Is": 0, "Iws": 22.34, "No": 4290, "PRES": 1001, "TEMP": 31, "cbwd": "SE", "day": 28, "hour": 17, "month": 6, "target_lag_1": 159.0, "target_lag_2": 174.0, "target_lag_3": 164.0, "year": 2010} |
| 3996 | 189.0 | 164.70839897517646 | {"DEWP": 19, "Ir": 0, "Is": 0, "Iws": 25.47, "No": 4291, "PRES": 1001, "TEMP": 30, "cbwd": "SE", "day": 28, "hour": 18, "month": 6, "target_lag_1": 174.0, "target_lag_2": 159.0, "target_lag_3": 174.0, "year": 2010} |

## Visual Artifacts

- score_plot_path: `artifacts\dataset_lab\pollution-detail-20260429144650\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\dataset_lab\pollution-detail-20260429144650\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\dataset_lab\pollution-detail-20260429144650\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\dataset_lab\pollution-detail-20260429144650`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab\pollution-detail-20260429144650\auto_meta_selection\fixed_share_portfolio\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab\pollution-detail-20260429144650\auto_meta_selection\fixed_share_portfolio\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab\pollution-detail-20260429144650\auto_meta_selection\fixed_share_portfolio\summary.md`
