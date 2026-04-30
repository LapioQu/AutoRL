# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T11:33:03.802931+00:00`
- dataset_name: `Bikes`
- task_type: `regression`
- target_column: `bikes_in_use`
- policy_name: `fixed_share_portfolio`
- source_row_count: `182470`
- source_rows_used: `182470`
- sample_count: `182470`
- feature_count: `8`
- next_prediction: `11.773263559647042`
- prediction_confidence: `0.2510` (low)

## Comparative Metrics

- adaptive_score: `0.670058`
- best_fixed_strategy: `sgd_lr_0_0001`
- best_fixed_score: `0.669679`
- delta_vs_best_fixed: `+0.000378`
- oracle_score: `0.672902`
- oracle_gain: `0.003223`
- oracle_capture_ratio: `11.74%`
- final_strategy: `sgd_lr_0_0001`
- switch_count: `100`

## Interpretation

- Adaptive policy `fixed_share_portfolio` finished on strategy `sgd_lr_0_0001` after 100 switches.
- It achieved `0.6701` against the best fixed baseline `sgd_lr_0_0001` at `0.6697`.
- Oracle upper bound on this stream is `0.6729`. Available oracle gain over best fixed is `0.0032`, and the current adaptive controller captures `11.7%` of it.
- The uploaded stream looks non-stationary enough for adaptation to help: the gain over best fixed is `0.0004`.
- Multiple switches suggest regime changes or at least changing local winners across the stream.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `11.7733` based on the latest lagged context `[5, 11, 12]`.

## Caveats

- Для цього готового датасету використано нативний потоковий профіль без CSV-перетворення ознак.
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
  "wind": "1.95"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 182458 | 13 | 10.723568915038417 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "moment": "2016-10-05 09:42:34", "pressure": 1017.34, "station": "pomme", "temperature": 17.45, "wind": 1.95} |
| 182459 | 13 | 10.774157698470855 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "moment": "2016-10-05 09:45:06", "pressure": 1017.34, "station": "pomme", "temperature": 17.45, "wind": 1.95} |
| 182460 | 13 | 10.823621639373386 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "moment": "2016-10-05 09:46:29", "pressure": 1017.34, "station": "pomme", "temperature": 17.45, "wind": 1.95} |
| 182461 | 23 | 10.87198575073344 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "moment": "2016-10-05 09:47:50", "pressure": 1017.34, "station": "place-jeanne-darc", "temperature": 17.45, "wind": 1.95} |
| 182462 | 4 | 11.141595619680876 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "moment": "2016-10-05 09:49:38", "pressure": 1017.34, "station": "metro-canal-du-midi", "temperature": 17.45, "wind": 1.95} |
| 182463 | 12 | 10.98280139501977 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "moment": "2016-10-05 09:50:54", "pressure": 1017.34, "station": "pomme", "temperature": 17.45, "wind": 1.95} |
| 182464 | 32 | 11.005394166417041 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "moment": "2016-10-05 09:51:43", "pressure": 1017.34, "station": "place-esquirol", "temperature": 17.45, "wind": 1.95} |
| 182465 | 12 | 11.472124324325804 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "moment": "2016-10-05 09:53:00", "pressure": 1017.34, "station": "pomme", "temperature": 17.45, "wind": 1.95} |
| 182466 | 32 | 11.483837956642816 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "moment": "2016-10-05 09:53:27", "pressure": 1017.34, "station": "place-esquirol", "temperature": 17.45, "wind": 1.95} |
| 182467 | 5 | 11.939929186606161 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "moment": "2016-10-05 09:53:39", "pressure": 1017.34, "station": "metro-canal-du-midi", "temperature": 17.45, "wind": 1.95} |
| 182468 | 11 | 11.785619147484564 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "moment": "2016-10-05 09:54:04", "pressure": 1017.34, "station": "pomme", "temperature": 17.45, "wind": 1.95} |
| 182469 | 12 | 11.768131045079246 | {"clouds": 88, "description": "overcast clouds", "humidity": 84, "moment": "2016-10-05 09:57:18", "pressure": 1017.34, "station": "pomme", "temperature": 17.45, "wind": 1.95} |

## Artifact Paths

- artifact_root: `artifacts\runtime_diagnosis\bikes_auto_meta_full\dataset_lab\bikes-20260429112642`
- replay_summary_json_path: `E:\dipproj\artifacts\runtime_diagnosis\bikes_auto_meta_full\dataset_lab\bikes-20260429112642\auto_meta_selection\fixed_share_portfolio\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\runtime_diagnosis\bikes_auto_meta_full\dataset_lab\bikes-20260429112642\auto_meta_selection\fixed_share_portfolio\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\runtime_diagnosis\bikes_auto_meta_full\dataset_lab\bikes-20260429112642\auto_meta_selection\fixed_share_portfolio\summary.md`
