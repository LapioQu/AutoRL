# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T16:42:57.118130+00:00`
- dataset_name: `AirQuality_candidate`
- task_type: `regression`
- target_column: `AH`
- policy_name: `hard_switch_lcb`
- source_row_count: `9357`
- source_rows_used: `9357`
- sample_count: `9354`
- feature_count: `16`
- next_prediction: `-200.0`
- prediction_confidence: `0.6403` (medium)

## Comparative Metrics

- adaptive_score: `0.993305`
- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.986403`
- delta_vs_best_fixed: `+0.006903`
- oracle_score: `0.997380`
- oracle_gain: `0.010977`
- oracle_capture_ratio: `62.88%`
- final_strategy: `tree_regressor`
- switch_count: `1`

## Interpretation

- Adaptive policy `hard_switch_lcb` finished on strategy `tree_regressor` after 1 switches.
- It achieved `0.9933` against the best fixed baseline `knn_regressor` at `0.9864`.
- Oracle upper bound on this stream is `0.9974`. Available oracle gain over best fixed is `0.0110`, and the current adaptive controller captures `62.9%` of it.
- The uploaded stream looks non-stationary enough for adaptation to help: the gain over best fixed is `0.0069`.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `-200.0000` based on the latest lagged context `['-200.0', '0.4425158182703054', '-200.0']`.

## Caveats

- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "Date": "11/02/2005",
  "Time": "16:00:00",
  "CO(GT)": "7.1",
  "PT08.S1(CO)": "-200.0",
  "NMHC(GT)": "-200",
  "C6H6(GT)": "-200.0",
  "PT08.S2(NMHC)": "-200.0",
  "NOx(GT)": "1218.0",
  "PT08.S3(NOx)": "-200.0",
  "NO2(GT)": "339.7",
  "PT08.S4(NO2)": "-200.0",
  "PT08.S5(O3)": "-200.0",
  "T": "-200.0",
  "RH": "-200.0",
  "AH": "-200.0"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 9342 | -200.0 | -200.0 | {"C6H6(GT)": -200, "CO(GT)": 5.4, "Date": "11/02/2005", "NMHC(GT)": -200, "NOx(GT)": 746.8, "PT08.S1(CO)": -200, "PT08.S2(NMHC)": -200, "PT08.S3(NOx)": -200, "PT08.S4(NO2)": -200, "PT08.S5(O3)": -200, "RH": -200, "T": -200, "Time": "10:00:00", "target_lag_1": -200.0, "target_lag_2": -200.0, "target_lag_3": 0.4304398978358917} |
| 9343 | 0.6820181973278787 | 0.8115645254003371 | {"C6H6(GT)": 16.66098269486679, "CO(GT)": 3.8, "Date": "22/02/2005", "NMHC(GT)": -200, "NOx(GT)": 687.4, "PT08.S1(CO)": 1407.5, "PT08.S2(NMHC)": 1199.75, "PT08.S3(NOx)": 490.25, "PT08.S4(NO2)": 1523.25, "PT08.S5(O3)": 1368.75, "RH": 82.674999237061, "T": 4.0500000715256, "Time": "08:00:00", "target_lag_1": -200.0, "target_lag_2": -200.0, "target_lag_3": -200.0} |
| 9344 | -200.0 | -200.0 | {"C6H6(GT)": -200, "CO(GT)": 5.9, "Date": "11/02/2005", "NMHC(GT)": -200, "NOx(GT)": 699.5, "PT08.S1(CO)": -200, "PT08.S2(NMHC)": -200, "PT08.S3(NOx)": -200, "PT08.S4(NO2)": -200, "PT08.S5(O3)": -200, "RH": -200, "T": -200, "Time": "09:00:00", "target_lag_1": 0.6820181973278787, "target_lag_2": -200.0, "target_lag_3": -200.0} |
| 9345 | 0.5175629703363939 | 0.5751038730385867 | {"C6H6(GT)": 20.11991542874835, "CO(GT)": 3.9, "Date": "04/02/2005", "NMHC(GT)": -200, "NOx(GT)": 654.3, "PT08.S1(CO)": 1327.5, "PT08.S2(NMHC)": 1299.75, "PT08.S3(NOx)": 498.75, "PT08.S4(NO2)": 1405, "PT08.S5(O3)": 1672, "RH": 61.050000190735, "T": 4.4499999284744, "Time": "09:00:00", "target_lag_1": -200.0, "target_lag_2": 0.6820181973278787, "target_lag_3": -200.0} |
| 9346 | 0.5181882373285943 | 0.8112454457745428 | {"C6H6(GT)": 19.708043566624657, "CO(GT)": 4, "Date": "04/02/2005", "NMHC(GT)": -200, "NOx(GT)": 886.7, "PT08.S1(CO)": 1411.25, "PT08.S2(NMHC)": 1288.25, "PT08.S3(NOx)": 491.5, "PT08.S4(NO2)": 1472.25, "PT08.S5(O3)": 1637.5, "RH": 70.85000038147, "T": 2.2999999523163, "Time": "08:00:00", "target_lag_1": 0.5175629703363939, "target_lag_2": -200.0, "target_lag_3": 0.6820181973278787} |
| 9347 | 0.4490811739114067 | 0.5748718532696262 | {"C6H6(GT)": 29.094718616706597, "CO(GT)": 5.6, "Date": "03/02/2005", "NMHC(GT)": -200, "NOx(GT)": 974.6, "PT08.S1(CO)": 1543.5, "PT08.S2(NMHC)": 1529.5, "PT08.S3(NOx)": 415.75, "PT08.S4(NO2)": 1706, "PT08.S5(O3)": 2030.25, "RH": 62.150000572205, "T": 2.1249999701977, "Time": "09:00:00", "target_lag_1": 0.5181882373285943, "target_lag_2": 0.5175629703363939, "target_lag_3": -200.0} |
| 9348 | 0.4345365371524944 | 0.5650213144534559 | {"C6H6(GT)": 11.270728575099753, "CO(GT)": 4.1, "Date": "05/02/2005", "NMHC(GT)": -200, "NOx(GT)": 758.9, "PT08.S1(CO)": 1165, "PT08.S2(NMHC)": 1024, "PT08.S3(NOx)": 646, "PT08.S4(NO2)": 1133.5, "PT08.S5(O3)": 1364.75, "RH": 52.674999237061, "T": 4.0500000119209, "Time": "09:00:00", "target_lag_1": 0.4490811739114067, "target_lag_2": 0.5181882373285943, "target_lag_3": 0.5175629703363939} |
| 9349 | -200.0 | -200.0 | {"C6H6(GT)": -200, "CO(GT)": 6.1, "Date": "11/02/2005", "NMHC(GT)": -200, "NOx(GT)": 1053.7, "PT08.S1(CO)": -200, "PT08.S2(NMHC)": -200, "PT08.S3(NOx)": -200, "PT08.S4(NO2)": -200, "PT08.S5(O3)": -200, "RH": -200, "T": -200, "Time": "15:00:00", "target_lag_1": 0.4345365371524944, "target_lag_2": 0.4490811739114067, "target_lag_3": 0.5181882373285943} |
| 9350 | 0.4499045038711265 | 0.5743666698183884 | {"C6H6(GT)": 20.735408792744465, "CO(GT)": 4.9, "Date": "03/02/2005", "NMHC(GT)": -200, "NOx(GT)": 947.3, "PT08.S1(CO)": 1428.75, "PT08.S2(NMHC)": 1316.75, "PT08.S3(NOx)": 494.75, "PT08.S4(NO2)": 1424.75, "PT08.S5(O3)": 1915.5, "RH": 50.77499961853, "T": 5.0999999642372, "Time": "10:00:00", "target_lag_1": -200.0, "target_lag_2": 0.4345365371524944, "target_lag_3": 0.4490811739114067} |
| 9351 | -200.0 | -200.0 | {"C6H6(GT)": -200, "CO(GT)": 6.6, "Date": "11/02/2005", "NMHC(GT)": -200, "NOx(GT)": 1226.7, "PT08.S1(CO)": -200, "PT08.S2(NMHC)": -200, "PT08.S3(NOx)": -200, "PT08.S4(NO2)": -200, "PT08.S5(O3)": -200, "RH": -200, "T": -200, "Time": "17:00:00", "target_lag_1": 0.4499045038711265, "target_lag_2": -200.0, "target_lag_3": 0.4345365371524944} |
| 9352 | 0.4425158182703054 | 0.5639339413092812 | {"C6H6(GT)": 15.47632606744206, "CO(GT)": 3.5, "Date": "03/02/2005", "NMHC(GT)": -200, "NOx(GT)": 790, "PT08.S1(CO)": 1312, "PT08.S2(NMHC)": 1163.5, "PT08.S3(NOx)": 569.5, "PT08.S4(NO2)": 1229.5, "PT08.S5(O3)": 1761, "RH": 39.699999809265, "T": 8.5250000953674, "Time": "11:00:00", "target_lag_1": -200.0, "target_lag_2": 0.4499045038711265, "target_lag_3": -200.0} |
| 9353 | -200.0 | -200.0 | {"C6H6(GT)": -200, "CO(GT)": 7.1, "Date": "11/02/2005", "NMHC(GT)": -200, "NOx(GT)": 1218, "PT08.S1(CO)": -200, "PT08.S2(NMHC)": -200, "PT08.S3(NOx)": -200, "PT08.S4(NO2)": -200, "PT08.S5(O3)": -200, "RH": -200, "T": -200, "Time": "16:00:00", "target_lag_1": 0.4425158182703054, "target_lag_2": -200.0, "target_lag_3": 0.4499045038711265} |

## Visual Artifacts

- score_plot_path: `artifacts\dataset_lab_jobs\airquality-candidate-20260429164205-f5e89f7c\analysis\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\dataset_lab_jobs\airquality-candidate-20260429164205-f5e89f7c\analysis\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\dataset_lab_jobs\airquality-candidate-20260429164205-f5e89f7c\analysis\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\dataset_lab_jobs\airquality-candidate-20260429164205-f5e89f7c\analysis`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab_jobs\airquality-candidate-20260429164205-f5e89f7c\analysis\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab_jobs\airquality-candidate-20260429164205-f5e89f7c\analysis\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab_jobs\airquality-candidate-20260429164205-f5e89f7c\analysis\summary.md`
