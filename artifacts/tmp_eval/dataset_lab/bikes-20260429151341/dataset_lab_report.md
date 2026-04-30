# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T15:27:43.926947+00:00`
- dataset_name: `Bikes`
- task_type: `regression`
- target_column: `bikes_in_use`
- policy_name: `fixed_share_portfolio`
- source_row_count: `182470`
- source_rows_used: `182470`
- sample_count: `182467`
- feature_count: `10`
- next_prediction: `10.88890731202557`
- prediction_confidence: `0.7470` (medium)

## Comparative Metrics

- adaptive_score: `0.702174`
- best_fixed_strategy: `lin_lr_0_002`
- best_fixed_score: `0.674377`
- delta_vs_best_fixed: `+0.027797`
- oracle_score: `0.774606`
- oracle_gain: `0.100229`
- oracle_capture_ratio: `27.73%`
- final_strategy: `lin_lr_0_0001`
- switch_count: `1085`

## Interpretation

- Adaptive policy `fixed_share_portfolio` finished on strategy `lin_lr_0_0001` after 1085 switches.
- It achieved `0.7022` against the best fixed baseline `lin_lr_0_002` at `0.6744`.
- Oracle upper bound on this stream is `0.7746`. Available oracle gain over best fixed is `0.1002`, and the current adaptive controller captures `27.7%` of it.
- The uploaded stream looks non-stationary enough for adaptation to help: the gain over best fixed is `0.0278`.
- Multiple switches suggest regime changes or at least changing local winners across the stream.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `10.8889` based on the latest lagged context `['5', '11', '12']`.

## Caveats

- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "moment": "2016-10-05 09:57:18",
  "station": "pomme",
  "clouds": "88",
  "description": "overcast clouds",
  "humidity": "84",
  "pressure": "1017.34",
  "temperature": "17.45",
  "wind": "1.95",
  "bikes_in_use": "12"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 182455 | 13.0 | 10.308129803937751 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "pressure": 1017.34, "station": "pomme", "target_lag_1": 31.0, "target_lag_2": 4.0, "target_lag_3": 12.0, "temperature": 17.45, "wind": 1.95} |
| 182456 | 13.0 | 12.04376197520352 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "pressure": 1017.34, "station": "pomme", "target_lag_1": 13.0, "target_lag_2": 31.0, "target_lag_3": 4.0, "temperature": 17.45, "wind": 1.95} |
| 182457 | 13.0 | 12.83936780963527 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "pressure": 1017.34, "station": "pomme", "target_lag_1": 13.0, "target_lag_2": 13.0, "target_lag_3": 31.0, "temperature": 17.45, "wind": 1.95} |
| 182458 | 23.0 | 11.167737664149076 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "pressure": 1017.34, "station": "place-jeanne-darc", "target_lag_1": 13.0, "target_lag_2": 13.0, "target_lag_3": 13.0, "temperature": 17.45, "wind": 1.95} |
| 182459 | 4.0 | 11.51942756502527 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "pressure": 1017.34, "station": "metro-canal-du-midi", "target_lag_1": 23.0, "target_lag_2": 13.0, "target_lag_3": 13.0, "temperature": 17.45, "wind": 1.95} |
| 182460 | 12.0 | 12.132297739395202 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "pressure": 1017.34, "station": "pomme", "target_lag_1": 4.0, "target_lag_2": 23.0, "target_lag_3": 13.0, "temperature": 17.45, "wind": 1.95} |
| 182461 | 32.0 | 11.306295309164673 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "pressure": 1017.34, "station": "place-esquirol", "target_lag_1": 12.0, "target_lag_2": 4.0, "target_lag_3": 23.0, "temperature": 17.45, "wind": 1.95} |
| 182462 | 12.0 | 10.94265603458809 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "pressure": 1017.34, "station": "pomme", "target_lag_1": 32.0, "target_lag_2": 12.0, "target_lag_3": 4.0, "temperature": 17.45, "wind": 1.95} |
| 182463 | 32.0 | 13.43588687208813 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "pressure": 1017.34, "station": "place-esquirol", "target_lag_1": 12.0, "target_lag_2": 32.0, "target_lag_3": 12.0, "temperature": 17.45, "wind": 1.95} |
| 182464 | 5.0 | 13.984945153858 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "pressure": 1017.34, "station": "metro-canal-du-midi", "target_lag_1": 32.0, "target_lag_2": 12.0, "target_lag_3": 32.0, "temperature": 17.45, "wind": 1.95} |
| 182465 | 11.0 | 13.586710027524305 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "pressure": 1017.34, "station": "pomme", "target_lag_1": 5.0, "target_lag_2": 32.0, "target_lag_3": 12.0, "temperature": 17.45, "wind": 1.95} |
| 182466 | 12.0 | 12.833511987332626 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "pressure": 1017.34, "station": "pomme", "target_lag_1": 11.0, "target_lag_2": 5.0, "target_lag_3": 32.0, "temperature": 17.45, "wind": 1.95} |

## Visual Artifacts

- score_plot_path: `artifacts\tmp_eval\dataset_lab\bikes-20260429151341\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\tmp_eval\dataset_lab\bikes-20260429151341\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\tmp_eval\dataset_lab\bikes-20260429151341\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\tmp_eval\dataset_lab\bikes-20260429151341`
- replay_summary_json_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\bikes-20260429151341\auto_meta_selection\fixed_share_portfolio\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\bikes-20260429151341\auto_meta_selection\fixed_share_portfolio\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\bikes-20260429151341\auto_meta_selection\fixed_share_portfolio\summary.md`
