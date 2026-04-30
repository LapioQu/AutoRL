# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T12:21:14.798745+00:00`
- dataset_name: `Elec2`
- task_type: `classification`
- target_column: `price_up`
- policy_name: `recent_leader_meta`
- source_row_count: `45312`
- source_rows_used: `5000`
- sample_count: `5000`
- feature_count: `8`
- next_prediction: `False`
- prediction_confidence: `1.0000` (high)

## Comparative Metrics

- adaptive_score: `0.947400`
- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.952200`
- delta_vs_best_fixed: `-0.004800`
- oracle_score: `0.984200`
- oracle_gain: `0.032000`
- oracle_capture_ratio: `0.00%`
- final_strategy: `pa_classifier`
- switch_count: `2`

## Interpretation

- Adaptive policy `recent_leader_meta` finished on strategy `pa_classifier` after 2 switches.
- It achieved `0.9474` against the best fixed baseline `pa_classifier` at `0.9522`.
- Oracle upper bound on this stream is `0.9842`. Available oracle gain over best fixed is `0.0320`, and the current adaptive controller captures `0.0%` of it.
- The current stationary portfolio dominated the adaptive controller here; the gap is `-0.0048`.
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
  "date": "0.013805",
  "day": "1",
  "period": "0.148936",
  "nswprice": "0.045034",
  "nswdemand": "0.15055",
  "vicprice": "0.003467",
  "vicdemand": "0.422915",
  "transfer": "0.414912"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 4988 | False | False | {"date": 0.01376, "day": 7, "nswdemand": 0.426807, "nswprice": 0.045785, "period": 0.93617, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 4989 | False | False | {"date": 0.01376, "day": 7, "nswdemand": 0.412675, "nswprice": 0.045755, "period": 0.957447, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 4990 | False | False | {"date": 0.01376, "day": 7, "nswdemand": 0.415799, "nswprice": 0.045034, "period": 0.978723, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 4991 | False | False | {"date": 0.01376, "day": 7, "nswdemand": 0.38679, "nswprice": 0.045034, "period": 1.0, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 4992 | False | False | {"date": 0.013805, "day": 1, "nswdemand": 0.366111, "nswprice": 0.041131, "period": 0.0, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 4993 | False | False | {"date": 0.013805, "day": 1, "nswdemand": 0.330854, "nswprice": 0.041191, "period": 0.021277, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 4994 | False | False | {"date": 0.013805, "day": 1, "nswdemand": 0.320738, "nswprice": 0.041972, "period": 0.042553, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 4995 | False | False | {"date": 0.013805, "day": 1, "nswdemand": 0.274918, "nswprice": 0.045034, "period": 0.06383, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 4996 | False | False | {"date": 0.013805, "day": 1, "nswdemand": 0.232966, "nswprice": 0.043413, "period": 0.085106, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 4997 | False | False | {"date": 0.013805, "day": 1, "nswdemand": 0.198155, "nswprice": 0.045755, "period": 0.106383, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 4998 | False | False | {"date": 0.013805, "day": 1, "nswdemand": 0.177031, "nswprice": 0.041131, "period": 0.12766, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 4999 | False | False | {"date": 0.013805, "day": 1, "nswdemand": 0.15055, "nswprice": 0.045034, "period": 0.148936, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |

## Visual Artifacts

- score_plot_path: `artifacts\debug_elec2_5k\dataset_lab\elec2-20260429122112\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\debug_elec2_5k\dataset_lab\elec2-20260429122112\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\debug_elec2_5k\dataset_lab\elec2-20260429122112\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\debug_elec2_5k\dataset_lab\elec2-20260429122112`
- replay_summary_json_path: `E:\dipproj\artifacts\debug_elec2_5k\dataset_lab\elec2-20260429122112\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\debug_elec2_5k\dataset_lab\elec2-20260429122112\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\debug_elec2_5k\dataset_lab\elec2-20260429122112\summary.md`
