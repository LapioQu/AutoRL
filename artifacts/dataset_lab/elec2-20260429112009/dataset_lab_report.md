# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T11:20:10.128297+00:00`
- dataset_name: `Elec2`
- task_type: `classification`
- target_column: `price_up`
- policy_name: `best_fixed_guard`
- source_row_count: `45312`
- source_rows_used: `1268`
- sample_count: `1268`
- feature_count: `8`
- next_prediction: `False`
- prediction_confidence: `1.0000` (high)

## Comparative Metrics

- adaptive_score: `0.952681`
- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.952681`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.981861`
- oracle_gain: `0.029180`
- oracle_capture_ratio: `0.00%`
- final_strategy: `pa_classifier`
- switch_count: `0`

## Interpretation

- Adaptive policy `best_fixed_guard` finished on strategy `pa_classifier` after 0 switches.
- It achieved `0.9527` against the best fixed baseline `pa_classifier` at `0.9527`.
- Oracle upper bound on this stream is `0.9819`. Available oracle gain over best fixed is `0.0292`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step class from the final adaptive strategy is `False` based on the latest lagged context `[False, False, False]`.

## Caveats

- Для цього готового датасету використано нативний потоковий профіль без CSV-перетворення ознак.
- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is prequential accuracy over the uploaded stream.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "date": "0.004203",
  "day": "7",
  "period": "0.404255",
  "nswprice": "0.044134",
  "nswdemand": "0.417882",
  "vicprice": "0.003467",
  "vicdemand": "0.422915",
  "transfer": "0.414912"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 1256 | False | False | {"date": 0.004203, "day": 7, "nswdemand": 0.076912, "nswprice": 0.043683, "period": 0.170213, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 1257 | False | False | {"date": 0.004203, "day": 7, "nswdemand": 0.071854, "nswprice": 0.043683, "period": 0.191489, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 1258 | False | False | {"date": 0.004203, "day": 7, "nswdemand": 0.076763, "nswprice": 0.043683, "period": 0.212766, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 1259 | False | False | {"date": 0.004203, "day": 7, "nswdemand": 0.08911, "nswprice": 0.043833, "period": 0.234043, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 1260 | False | False | {"date": 0.004203, "day": 7, "nswdemand": 0.109491, "nswprice": 0.043833, "period": 0.255319, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 1261 | False | False | {"date": 0.004203, "day": 7, "nswdemand": 0.129872, "nswprice": 0.043833, "period": 0.276596, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 1262 | False | False | {"date": 0.004203, "day": 7, "nswdemand": 0.153526, "nswprice": 0.043833, "period": 0.297872, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 1263 | False | False | {"date": 0.004203, "day": 7, "nswdemand": 0.214222, "nswprice": 0.043983, "period": 0.319149, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 1264 | False | False | {"date": 0.004203, "day": 7, "nswdemand": 0.284142, "nswprice": 0.043983, "period": 0.340426, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 1265 | False | False | {"date": 0.004203, "day": 7, "nswdemand": 0.339929, "nswprice": 0.044134, "period": 0.361702, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 1266 | False | False | {"date": 0.004203, "day": 7, "nswdemand": 0.391996, "nswprice": 0.044134, "period": 0.382979, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 1267 | False | False | {"date": 0.004203, "day": 7, "nswdemand": 0.417882, "nswprice": 0.044134, "period": 0.404255, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |

## Artifact Paths

- artifact_root: `artifacts\dataset_lab\elec2-20260429112009`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab\elec2-20260429112009\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab\elec2-20260429112009\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab\elec2-20260429112009\summary.md`
