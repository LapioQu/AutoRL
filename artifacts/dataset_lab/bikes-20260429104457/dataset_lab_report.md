# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T10:44:57.979423+00:00`
- dataset_name: `Bikes`
- task_type: `regression`
- target_column: `bikes_in_use`
- policy_name: `best_fixed_guard`
- sample_count: `1268`
- feature_count: `8`
- next_prediction: `6.668797926705095`
- prediction_confidence: `0.8952` (high)

## Comparative Metrics

- adaptive_score: `0.670508`
- best_fixed_strategy: `sgd_lr_0_0005`
- best_fixed_score: `0.670508`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.684821`
- oracle_gain: `0.014314`
- oracle_capture_ratio: `0.00%`
- final_strategy: `sgd_lr_0_0005`
- switch_count: `0`

## Interpretation

- Adaptive policy `best_fixed_guard` finished on strategy `sgd_lr_0_0005` after 0 switches.
- It achieved `0.6705` against the best fixed baseline `sgd_lr_0_0005` at `0.6705`.
- Oracle upper bound on this stream is `0.6848`. Available oracle gain over best fixed is `0.0143`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `6.6688` based on the latest lagged context `[2, 4, 3]`.

## Caveats

- Для цього готового датасету використано нативний потоковий профіль без CSV-перетворення ознак.
- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "moment": "2016-04-01 17:14:18",
  "station": "place-esquirol",
  "clouds": "75",
  "description": "broken clouds",
  "humidity": "57",
  "pressure": "1018.0",
  "temperature": "10.39",
  "wind": "5.7"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 1256 | 1 | 7.712748272715237 | {"clouds": 75, "description": "broken clouds", "humidity": 57, "moment": "2016-04-01 17:06:22", "pressure": 1018.0, "station": "place-des-carmes", "temperature": 10.88, "wind": 5.7} |
| 1257 | 12 | 7.423757375778981 | {"clouds": 75, "description": "broken clouds", "humidity": 57, "moment": "2016-04-01 17:06:46", "pressure": 1018.0, "station": "pomme", "temperature": 10.88, "wind": 5.7} |
| 1258 | 6 | 7.62098686492569 | {"clouds": 75, "description": "broken clouds", "humidity": 57, "moment": "2016-04-01 17:06:53", "pressure": 1018.0, "station": "metro-canal-du-midi", "temperature": 10.88, "wind": 5.7} |
| 1259 | 9 | 7.5519232130866065 | {"clouds": 75, "description": "broken clouds", "humidity": 57, "moment": "2016-04-01 17:07:13", "pressure": 1018.0, "station": "place-jeanne-darc", "temperature": 10.88, "wind": 5.7} |
| 1260 | 2 | 7.614207838122657 | {"clouds": 75, "description": "broken clouds", "humidity": 57, "moment": "2016-04-01 17:07:42", "pressure": 1018.0, "station": "place-des-carmes", "temperature": 10.88, "wind": 5.7} |
| 1261 | 4 | 7.375540179476499 | {"clouds": 75, "description": "broken clouds", "humidity": 57, "moment": "2016-04-01 17:08:10", "pressure": 1018.0, "station": "place-esquirol", "temperature": 10.88, "wind": 5.7} |
| 1262 | 3 | 7.232929736991255 | {"clouds": 75, "description": "broken clouds", "humidity": 57, "moment": "2016-04-01 17:08:50", "pressure": 1018.0, "station": "place-esquirol", "temperature": 10.88, "wind": 5.7} |
| 1263 | 4 | 7.054630730070572 | {"clouds": 75, "description": "broken clouds", "humidity": 57, "moment": "2016-04-01 17:09:28", "pressure": 1018.0, "station": "place-esquirol", "temperature": 10.88, "wind": 5.7} |
| 1264 | 12 | 6.926812105092153 | {"clouds": 75, "description": "broken clouds", "humidity": 57, "moment": "2016-04-01 17:09:51", "pressure": 1018.0, "station": "pomme", "temperature": 10.88, "wind": 5.7} |
| 1265 | 2 | 7.141597585440481 | {"clouds": 75, "description": "broken clouds", "humidity": 57, "moment": "2016-04-01 17:11:06", "pressure": 1018.0, "station": "place-des-carmes", "temperature": 10.88, "wind": 5.7} |
| 1266 | 4 | 6.937829604369832 | {"clouds": 75, "description": "broken clouds", "humidity": 57, "moment": "2016-04-01 17:12:18", "pressure": 1018.0, "station": "place-des-carmes", "temperature": 10.39, "wind": 5.7} |
| 1267 | 3 | 6.820815682328522 | {"clouds": 75, "description": "broken clouds", "humidity": 57, "moment": "2016-04-01 17:14:18", "pressure": 1018.0, "station": "place-esquirol", "temperature": 10.39, "wind": 5.7} |

## Artifact Paths

- artifact_root: `artifacts\dataset_lab\bikes-20260429104457`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab\bikes-20260429104457\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab\bikes-20260429104457\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab\bikes-20260429104457\summary.md`
