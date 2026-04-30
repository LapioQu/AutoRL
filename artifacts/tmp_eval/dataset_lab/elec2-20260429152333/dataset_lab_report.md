# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T15:23:44.383031+00:00`
- dataset_name: `Elec2`
- task_type: `classification`
- target_column: `price_up`
- policy_name: `best_fixed_guard`
- source_row_count: `4000`
- source_rows_used: `4000`
- sample_count: `4000`
- feature_count: `7`
- next_prediction: `False`
- prediction_confidence: `1.0000` (high)

## Comparative Metrics

- adaptive_score: `0.948250`
- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.948250`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.986000`
- oracle_gain: `0.037750`
- oracle_capture_ratio: `0.00%`
- final_strategy: `pa_classifier`
- switch_count: `0`

## Interpretation

- Adaptive policy `best_fixed_guard` finished on strategy `pa_classifier` after 0 switches.
- It achieved `0.9483` against the best fixed baseline `pa_classifier` at `0.9483`.
- Oracle upper bound on this stream is `0.9860`. Available oracle gain over best fixed is `0.0377`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step class from the final adaptive strategy is `False` based on the latest lagged context `['false', 'false', 'false']`.

## Caveats

- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is prequential accuracy over the uploaded stream.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "date": "0.009823",
  "day": "1",
  "period": "0.319149",
  "nswprice": "0.041732",
  "nswdemand": "0.595507",
  "vicprice": "0.003467",
  "vicdemand": "0.422915",
  "transfer": "0.414912",
  "price_up": "false"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 3988 | False | False | {"day": 1, "nswdemand": 0.237876, "nswprice": 0.041281, "period": 0.085106, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 3989 | False | False | {"day": 1, "nswdemand": 0.211098, "nswprice": 0.040681, "period": 0.106383, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 3990 | False | False | {"day": 1, "nswdemand": 0.184766, "nswprice": 0.040591, "period": 0.12766, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 3991 | False | False | {"day": 1, "nswdemand": 0.162452, "nswprice": 0.040591, "period": 0.148936, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 3992 | False | False | {"day": 1, "nswdemand": 0.150104, "nswprice": 0.041582, "period": 0.170213, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 3993 | False | False | {"day": 1, "nswdemand": 0.158733, "nswprice": 0.044824, "period": 0.191489, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 3994 | False | False | {"day": 1, "nswdemand": 0.190866, "nswprice": 0.041281, "period": 0.212766, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 3995 | False | False | {"day": 1, "nswdemand": 0.251711, "nswprice": 0.044824, "period": 0.234043, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 3996 | False | False | {"day": 1, "nswdemand": 0.359268, "nswprice": 0.041732, "period": 0.255319, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 3997 | False | False | {"day": 1, "nswdemand": 0.486314, "nswprice": 0.043683, "period": 0.276596, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 3998 | False | False | {"day": 1, "nswdemand": 0.522464, "nswprice": 0.044824, "period": 0.297872, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |
| 3999 | False | False | {"day": 1, "nswdemand": 0.595507, "nswprice": 0.041732, "period": 0.319149, "transfer": 0.414912, "vicdemand": 0.422915, "vicprice": 0.003467} |

## Visual Artifacts

- score_plot_path: `artifacts\tmp_eval\dataset_lab\elec2-20260429152333\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\tmp_eval\dataset_lab\elec2-20260429152333\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\tmp_eval\dataset_lab\elec2-20260429152333\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\tmp_eval\dataset_lab\elec2-20260429152333`
- replay_summary_json_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\elec2-20260429152333\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\elec2-20260429152333\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\elec2-20260429152333\summary.md`
