# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T16:26:08.246637+00:00`
- dataset_name: `DailyDelhiClimateTrain`
- task_type: `regression`
- target_column: `meanpressure`
- policy_name: `hard_switch_lcb`
- source_row_count: `1462`
- source_rows_used: `1462`
- sample_count: `1459`
- feature_count: `6`
- next_prediction: `1015.8619047619047`
- prediction_confidence: `0.8921` (high)

## Comparative Metrics

- adaptive_score: `0.980527`
- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.980527`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.984870`
- oracle_gain: `0.004343`
- oracle_capture_ratio: `0.00%`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Interpretation

- Adaptive policy `hard_switch_lcb` finished on strategy `knn_regressor` after 0 switches.
- It achieved `0.9805` against the best fixed baseline `knn_regressor` at `0.9805`.
- Oracle upper bound on this stream is `0.9849`. Available oracle gain over best fixed is `0.0043`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `1015.8619` based on the latest lagged context `['1017.9047619047619', '1016.1', '1016.0']`.

## Caveats

- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "date": "2017-01-01",
  "meantemp": "10.0",
  "humidity": "100.0",
  "wind_speed": "0.0",
  "meanpressure": "1016.0"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 1447 | 1015.6190476190476 | 1011.915 | {"humidity": 54.3, "meantemp": 18.05, "target_lag_1": 1015.2, "target_lag_2": 1017.4285714285714, "target_lag_3": 1018.0833333333334, "wind_speed": 19.40476190476191} |
| 1448 | 1016.1428571428571 | 1017.8218979266347 | {"humidity": 57.857142857142854, "meantemp": 17.285714285714285, "target_lag_1": 1015.6190476190476, "target_lag_2": 1015.2, "target_lag_3": 1017.4285714285714, "wind_speed": 6.1809523809523785} |
| 1449 | 1014.25 | 1016.7554071075124 | {"humidity": 74.7, "meantemp": 15.55, "target_lag_1": 1016.1428571428571, "target_lag_2": 1015.6190476190476, "target_lag_3": 1015.2, "wind_speed": 1.205} |
| 1450 | 1011.3181818181819 | 1015.350641025641 | {"humidity": 78.63636363636364, "meantemp": 17.318181818181817, "target_lag_1": 1014.25, "target_lag_2": 1016.1428571428571, "target_lag_3": 1015.6190476190476, "wind_speed": 5.236363636363636} |
| 1451 | 1014.35 | 1013.1636363636363 | {"humidity": 94.3, "meantemp": 14, "target_lag_1": 1011.3181818181819, "target_lag_2": 1014.25, "target_lag_3": 1016.1428571428571, "wind_speed": 9.084999999999999} |
| 1452 | 1016.952380952381 | 1015.6197767145136 | {"humidity": 74.85714285714286, "meantemp": 17.142857142857142, "target_lag_1": 1014.35, "target_lag_2": 1011.3181818181819, "target_lag_3": 1014.25, "wind_speed": 8.784210526315787} |
| 1453 | 1017.2 | 1017.0918546365915 | {"humidity": 67.55, "meantemp": 16.85, "target_lag_1": 1016.952380952381, "target_lag_2": 1014.35, "target_lag_3": 1011.3181818181819, "wind_speed": 8.335} |
| 1454 | 1015.5652173913044 | 1015.8625602175603 | {"humidity": 68.04347826086956, "meantemp": 17.217391304347824, "target_lag_1": 1017.2, "target_lag_2": 1016.952380952381, "target_lag_3": 1014.35, "wind_speed": 3.547826086956522} |
| 1455 | 1016.9047619047619 | 1014.2336363636364 | {"humidity": 87.85714285714286, "meantemp": 15.238095238095237, "target_lag_1": 1015.5652173913044, "target_lag_2": 1017.2, "target_lag_3": 1016.952380952381, "wind_speed": 6} |
| 1456 | 1017.9047619047619 | 1013.8145887445887 | {"humidity": 89.66666666666667, "meantemp": 14.095238095238095, "target_lag_1": 1016.9047619047619, "target_lag_2": 1015.5652173913044, "target_lag_3": 1017.2, "wind_speed": 6.266666666666667} |
| 1457 | 1016.1 | 1014.8955411255412 | {"humidity": 87, "meantemp": 15.052631578947368, "target_lag_1": 1017.9047619047619, "target_lag_2": 1016.9047619047619, "target_lag_3": 1015.5652173913044, "wind_speed": 7.325} |
| 1458 | 1016.0 | 1015.4619047619047 | {"humidity": 100, "meantemp": 10, "target_lag_1": 1016.1, "target_lag_2": 1017.9047619047619, "target_lag_3": 1016.9047619047619, "wind_speed": 0} |

## Visual Artifacts

- score_plot_path: `artifacts\dataset_lab_jobs\dailydelhiclimatetrain-20260429162602-861bded5\analysis\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\dataset_lab_jobs\dailydelhiclimatetrain-20260429162602-861bded5\analysis\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\dataset_lab_jobs\dailydelhiclimatetrain-20260429162602-861bded5\analysis\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\dataset_lab_jobs\dailydelhiclimatetrain-20260429162602-861bded5\analysis`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab_jobs\dailydelhiclimatetrain-20260429162602-861bded5\analysis\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab_jobs\dailydelhiclimatetrain-20260429162602-861bded5\analysis\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab_jobs\dailydelhiclimatetrain-20260429162602-861bded5\analysis\summary.md`
