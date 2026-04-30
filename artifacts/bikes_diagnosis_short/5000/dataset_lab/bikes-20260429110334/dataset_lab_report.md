# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T11:03:35.563505+00:00`
- dataset_name: `Bikes`
- task_type: `regression`
- target_column: `bikes_in_use`
- policy_name: `best_fixed_guard`
- sample_count: `5000`
- feature_count: `8`
- next_prediction: `4.452498282833337`
- prediction_confidence: `0.9314` (high)

## Comparative Metrics

- adaptive_score: `0.701981`
- best_fixed_strategy: `sgd_lr_0_001`
- best_fixed_score: `0.701981`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.717545`
- oracle_gain: `0.015564`
- oracle_capture_ratio: `0.00%`
- final_strategy: `sgd_lr_0_001`
- switch_count: `0`

## Interpretation

- Adaptive policy `best_fixed_guard` finished on strategy `sgd_lr_0_001` after 0 switches.
- It achieved `0.7020` against the best fixed baseline `sgd_lr_0_001` at `0.7020`.
- Oracle upper bound on this stream is `0.7175`. Available oracle gain over best fixed is `0.0156`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `4.4525` based on the latest lagged context `[1, 4, 2]`.

## Caveats

- Для цього готового датасету використано нативний потоковий профіль без CSV-перетворення ознак.
- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "moment": "2016-04-03 22:39:57",
  "station": "place-des-carmes",
  "clouds": "0",
  "description": "clear sky",
  "humidity": "67",
  "pressure": "1007.0",
  "temperature": "12.88",
  "wind": "5.7"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 4988 | 2 | 5.408567479589527 | {"clouds": 0, "description": "clear sky", "humidity": 67, "moment": "2016-04-03 22:25:14", "pressure": 1006.0, "station": "place-des-carmes", "temperature": 12.91, "wind": 5.1} |
| 4989 | 4 | 5.2700745500863695 | {"clouds": 0, "description": "clear sky", "humidity": 67, "moment": "2016-04-03 22:25:29", "pressure": 1006.0, "station": "metro-canal-du-midi", "temperature": 12.91, "wind": 5.1} |
| 4990 | 5 | 5.218413953149354 | {"clouds": 0, "description": "clear sky", "humidity": 67, "moment": "2016-04-03 22:27:16", "pressure": 1006.0, "station": "place-esquirol", "temperature": 12.91, "wind": 5.1} |
| 4991 | 4 | 5.209435597830526 | {"clouds": 0, "description": "clear sky", "humidity": 67, "moment": "2016-04-03 22:31:05", "pressure": 1006.0, "station": "place-esquirol", "temperature": 12.91, "wind": 5.1} |
| 4992 | 13 | 5.160273411315433 | {"clouds": 0, "description": "clear sky", "humidity": 67, "moment": "2016-04-03 22:31:44", "pressure": 1006.0, "station": "pomme", "temperature": 12.91, "wind": 5.1} |
| 4993 | 0 | 5.2382206628603765 | {"clouds": 0, "description": "clear sky", "humidity": 67, "moment": "2016-04-03 22:33:18", "pressure": 1007.0, "station": "place-jeanne-darc", "temperature": 12.88, "wind": 5.7} |
| 4994 | 1 | 5.029692619297136 | {"clouds": 0, "description": "clear sky", "humidity": 67, "moment": "2016-04-03 22:34:20", "pressure": 1007.0, "station": "place-des-carmes", "temperature": 12.88, "wind": 5.7} |
| 4995 | 2 | 4.869315112518337 | {"clouds": 0, "description": "clear sky", "humidity": 67, "moment": "2016-04-03 22:34:22", "pressure": 1007.0, "station": "place-des-carmes", "temperature": 12.88, "wind": 5.7} |
| 4996 | 4 | 4.755140382441063 | {"clouds": 0, "description": "clear sky", "humidity": 67, "moment": "2016-04-03 22:35:34", "pressure": 1007.0, "station": "metro-canal-du-midi", "temperature": 12.88, "wind": 5.7} |
| 4997 | 1 | 4.72504896498324 | {"clouds": 0, "description": "clear sky", "humidity": 67, "moment": "2016-04-03 22:39:18", "pressure": 1007.0, "station": "place-jeanne-darc", "temperature": 12.88, "wind": 5.7} |
| 4998 | 4 | 4.576952029284193 | {"clouds": 0, "description": "clear sky", "humidity": 67, "moment": "2016-04-03 22:39:43", "pressure": 1007.0, "station": "place-esquirol", "temperature": 12.88, "wind": 5.7} |
| 4999 | 2 | 4.553980099906747 | {"clouds": 0, "description": "clear sky", "humidity": 67, "moment": "2016-04-03 22:39:57", "pressure": 1007.0, "station": "place-des-carmes", "temperature": 12.88, "wind": 5.7} |

## Artifact Paths

- artifact_root: `artifacts\bikes_diagnosis_short\5000\dataset_lab\bikes-20260429110334`
- replay_summary_json_path: `E:\dipproj\artifacts\bikes_diagnosis_short\5000\dataset_lab\bikes-20260429110334\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\bikes_diagnosis_short\5000\dataset_lab\bikes-20260429110334\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\bikes_diagnosis_short\5000\dataset_lab\bikes-20260429110334\summary.md`
