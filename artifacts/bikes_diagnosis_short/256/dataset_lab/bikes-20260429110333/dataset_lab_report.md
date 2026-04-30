# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T11:03:33.596920+00:00`
- dataset_name: `Bikes`
- task_type: `regression`
- target_column: `bikes_in_use`
- policy_name: `best_fixed_guard`
- sample_count: `256`
- feature_count: `8`
- next_prediction: `3.19297098237233`
- prediction_confidence: `0.9529` (high)

## Comparative Metrics

- adaptive_score: `0.642812`
- best_fixed_strategy: `sgd_lr_0_0001`
- best_fixed_score: `0.642812`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.649414`
- oracle_gain: `0.006601`
- oracle_capture_ratio: `0.00%`
- final_strategy: `sgd_lr_0_0001`
- switch_count: `0`

## Interpretation

- Adaptive policy `best_fixed_guard` finished on strategy `sgd_lr_0_0001` after 0 switches.
- It achieved `0.6428` against the best fixed baseline `sgd_lr_0_0001` at `0.6428`.
- Oracle upper bound on this stream is `0.6494`. Available oracle gain over best fixed is `0.0066`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `3.1930` based on the latest lagged context `[2, 4, 3]`.

## Caveats

- Для цього готового датасету використано нативний потоковий профіль без CSV-перетворення ознак.
- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "moment": "2016-04-01 05:44:56",
  "station": "pomme",
  "clouds": "90",
  "description": "overcast clouds",
  "humidity": "87",
  "pressure": "1018.0",
  "temperature": "6.35",
  "wind": "5.1"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 244 | 3 | 3.1046093881683534 | {"clouds": 90, "description": "light rain", "humidity": 87, "moment": "2016-04-01 05:28:39", "pressure": 1018.0, "station": "metro-canal-du-midi", "temperature": 6.38, "wind": 5.7} |
| 245 | 0 | 3.101832429677632 | {"clouds": 90, "description": "light rain", "humidity": 87, "moment": "2016-04-01 05:29:01", "pressure": 1018.0, "station": "place-des-carmes", "temperature": 6.38, "wind": 5.7} |
| 246 | 12 | 3.0407079625013607 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 05:29:33", "pressure": 1018.0, "station": "place-jeanne-darc", "temperature": 6.35, "wind": 5.1} |
| 247 | 1 | 3.233865311339277 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 05:30:30", "pressure": 1018.0, "station": "pomme", "temperature": 6.35, "wind": 5.1} |
| 248 | 4 | 3.184998697120979 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 05:34:10", "pressure": 1018.0, "station": "metro-canal-du-midi", "temperature": 6.35, "wind": 5.1} |
| 249 | 0 | 3.201992548432914 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 05:36:37", "pressure": 1018.0, "station": "place-esquirol", "temperature": 6.35, "wind": 5.1} |
| 250 | 0 | 3.1324176411695035 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 05:39:05", "pressure": 1018.0, "station": "place-des-carmes", "temperature": 6.35, "wind": 5.1} |
| 251 | 12 | 3.0644613302130654 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 05:39:37", "pressure": 1018.0, "station": "place-jeanne-darc", "temperature": 6.35, "wind": 5.1} |
| 252 | 1 | 3.2561179296412086 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 05:40:34", "pressure": 1018.0, "station": "pomme", "temperature": 6.35, "wind": 5.1} |
| 253 | 2 | 3.207085384005198 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 05:41:30", "pressure": 1018.0, "station": "pomme", "temperature": 6.35, "wind": 5.1} |
| 254 | 4 | 3.1806485340605177 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 05:44:12", "pressure": 1018.0, "station": "metro-canal-du-midi", "temperature": 6.35, "wind": 5.1} |
| 255 | 3 | 3.1977099169188516 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 05:44:56", "pressure": 1018.0, "station": "pomme", "temperature": 6.35, "wind": 5.1} |

## Artifact Paths

- artifact_root: `artifacts\bikes_diagnosis_short\256\dataset_lab\bikes-20260429110333`
- replay_summary_json_path: `E:\dipproj\artifacts\bikes_diagnosis_short\256\dataset_lab\bikes-20260429110333\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\bikes_diagnosis_short\256\dataset_lab\bikes-20260429110333\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\bikes_diagnosis_short\256\dataset_lab\bikes-20260429110333\summary.md`
