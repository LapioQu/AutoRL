# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T11:12:05.991071+00:00`
- dataset_name: `Bikes`
- task_type: `regression`
- target_column: `bikes_in_use`
- policy_name: `best_fixed_guard`
- source_row_count: `182470`
- source_rows_used: `512`
- sample_count: `512`
- feature_count: `8`
- next_prediction: `6.514284880465447`
- prediction_confidence: `0.9891` (high)

## Comparative Metrics

- adaptive_score: `0.657233`
- best_fixed_strategy: `sgd_lr_0_0001`
- best_fixed_score: `0.657233`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.663471`
- oracle_gain: `0.006237`
- oracle_capture_ratio: `0.00%`
- final_strategy: `sgd_lr_0_0001`
- switch_count: `0`

## Interpretation

- Adaptive policy `best_fixed_guard` finished on strategy `sgd_lr_0_0001` after 0 switches.
- It achieved `0.6572` against the best fixed baseline `sgd_lr_0_0001` at `0.6572`.
- Oracle upper bound on this stream is `0.6635`. Available oracle gain over best fixed is `0.0062`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `6.5143` based on the latest lagged context `[2, 16, 3]`.

## Caveats

- Для цього готового датасету використано нативний потоковий профіль без CSV-перетворення ознак.
- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "moment": "2016-04-01 09:22:28",
  "station": "place-esquirol",
  "clouds": "90",
  "description": "overcast clouds",
  "humidity": "87",
  "pressure": "1018.0",
  "temperature": "6.49",
  "wind": "4.6"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 500 | 14 | 6.571422845546726 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 09:16:03", "pressure": 1018.0, "station": "place-jeanne-darc", "temperature": 6.49, "wind": 4.6} |
| 501 | 6 | 6.7248625003216596 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 09:17:10", "pressure": 1018.0, "station": "pomme", "temperature": 6.49, "wind": 4.6} |
| 502 | 3 | 6.709473747404349 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 09:17:11", "pressure": 1018.0, "station": "place-esquirol", "temperature": 6.49, "wind": 4.6} |
| 503 | 6 | 6.63231350028229 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 09:17:16", "pressure": 1018.0, "station": "place-des-carmes", "temperature": 6.49, "wind": 4.6} |
| 504 | 6 | 6.618858223411169 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 09:17:41", "pressure": 1018.0, "station": "pomme", "temperature": 6.49, "wind": 4.6} |
| 505 | 2 | 6.605687408558529 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 09:18:13", "pressure": 1018.0, "station": "place-esquirol", "temperature": 6.49, "wind": 4.6} |
| 506 | 2 | 6.510038392186192 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 09:19:16", "pressure": 1018.0, "station": "place-esquirol", "temperature": 6.49, "wind": 4.6} |
| 507 | 1 | 6.416392737139827 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 09:19:40", "pressure": 1018.0, "station": "place-esquirol", "temperature": 6.49, "wind": 4.6} |
| 508 | 15 | 6.304025149311192 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 09:20:47", "pressure": 1018.0, "station": "place-jeanne-darc", "temperature": 6.49, "wind": 4.6} |
| 509 | 2 | 6.483524662244488 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 09:21:35", "pressure": 1018.0, "station": "place-esquirol", "temperature": 6.49, "wind": 4.6} |
| 510 | 16 | 6.390479711168797 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 09:22:26", "pressure": 1018.0, "station": "place-jeanne-darc", "temperature": 6.49, "wind": 4.6} |
| 511 | 3 | 6.588810621107239 | {"clouds": 90, "description": "overcast clouds", "humidity": 87, "moment": "2016-04-01 09:22:28", "pressure": 1018.0, "station": "place-esquirol", "temperature": 6.49, "wind": 4.6} |

## Artifact Paths

- artifact_root: `artifacts\rows_indicator_check\dataset_lab\bikes-20260429111205`
- replay_summary_json_path: `E:\dipproj\artifacts\rows_indicator_check\dataset_lab\bikes-20260429111205\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\rows_indicator_check\dataset_lab\bikes-20260429111205\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\rows_indicator_check\dataset_lab\bikes-20260429111205\summary.md`
