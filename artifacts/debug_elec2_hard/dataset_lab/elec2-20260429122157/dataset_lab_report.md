# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T12:22:24.817483+00:00`
- dataset_name: `Elec2`
- task_type: `classification`
- target_column: `price_up`
- policy_name: `hard_switch_lcb`
- source_row_count: `45312`
- source_rows_used: `45312`
- sample_count: `45312`
- feature_count: `8`
- next_prediction: `False`
- prediction_confidence: `1.0000` (high)

## Comparative Metrics

- adaptive_score: `0.866062`
- best_fixed_strategy: `pa_classifier`
- best_fixed_score: `0.922714`
- delta_vs_best_fixed: `-0.056652`
- oracle_score: `0.979365`
- oracle_gain: `0.056652`
- oracle_capture_ratio: `0.00%`
- final_strategy: `softmax_lr_0_20`
- switch_count: `19`

## Interpretation

- Adaptive policy `hard_switch_lcb` finished on strategy `softmax_lr_0_20` after 19 switches.
- It achieved `0.8661` against the best fixed baseline `pa_classifier` at `0.9227`.
- Oracle upper bound on this stream is `0.9794`. Available oracle gain over best fixed is `0.0567`, and the current adaptive controller captures `0.0%` of it.
- The current stationary portfolio dominated the adaptive controller here; the gap is `-0.0567`.
- Multiple switches suggest regime changes or at least changing local winners across the stream.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step class from the final adaptive strategy is `False` based on the latest lagged context `[False, True, False]`.

## Caveats

- Для цього готового датасету використано нативний потоковий профіль без CSV-перетворення ознак.
- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is prequential accuracy over the uploaded stream.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "date": "0.9158",
  "day": "7",
  "period": "1.0",
  "nswprice": "0.050679",
  "nswdemand": "0.288753",
  "vicprice": "0.003542",
  "vicdemand": "0.355256",
  "transfer": "0.23114"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 45300 | False | False | {"date": 0.9158, "day": 7, "nswdemand": 0.335168, "nswprice": 0.053441, "period": 0.765957, "transfer": 0.415789, "vicdemand": 0.304247, "vicprice": 0.00366} |
| 45301 | False | False | {"date": 0.9158, "day": 7, "nswdemand": 0.336061, "nswprice": 0.051249, "period": 0.787234, "transfer": 0.424123, "vicdemand": 0.294925, "vicprice": 0.00349} |
| 45302 | False | False | {"date": 0.9158, "day": 7, "nswdemand": 0.350193, "nswprice": 0.055062, "period": 0.808511, "transfer": 0.365351, "vicdemand": 0.295961, "vicprice": 0.003772} |
| 45303 | True | False | {"date": 0.9158, "day": 7, "nswdemand": 0.353913, "nswprice": 0.06542, "period": 0.829787, "transfer": 0.319737, "vicdemand": 0.319524, "vicprice": 0.004508} |
| 45304 | False | False | {"date": 0.9158, "day": 7, "nswdemand": 0.340077, "nswprice": 0.055902, "period": 0.851064, "transfer": 0.375, "vicdemand": 0.313568, "vicprice": 0.003857} |
| 45305 | False | False | {"date": 0.9158, "day": 7, "nswdemand": 0.322821, "nswprice": 0.050648, "period": 0.87234, "transfer": 0.325877, "vicdemand": 0.305541, "vicprice": 0.003488} |
| 45306 | False | False | {"date": 0.9158, "day": 7, "nswdemand": 0.340226, "nswprice": 0.058875, "period": 0.893617, "transfer": 0.351754, "vicdemand": 0.276541, "vicprice": 0.004049} |
| 45307 | False | False | {"date": 0.9158, "day": 7, "nswdemand": 0.340672, "nswprice": 0.044224, "period": 0.914894, "transfer": 0.405263, "vicdemand": 0.255049, "vicprice": 0.003033} |
| 45308 | False | False | {"date": 0.9158, "day": 7, "nswdemand": 0.355549, "nswprice": 0.044884, "period": 0.93617, "transfer": 0.420614, "vicdemand": 0.241326, "vicprice": 0.003072} |
| 45309 | False | False | {"date": 0.9158, "day": 7, "nswdemand": 0.34097, "nswprice": 0.043593, "period": 0.957447, "transfer": 0.362281, "vicdemand": 0.247799, "vicprice": 0.002983} |
| 45310 | True | True | {"date": 0.9158, "day": 7, "nswdemand": 0.329366, "nswprice": 0.066651, "period": 0.978723, "transfer": 0.206579, "vicdemand": 0.345417, "vicprice": 0.00463} |
| 45311 | False | False | {"date": 0.9158, "day": 7, "nswdemand": 0.288753, "nswprice": 0.050679, "period": 1.0, "transfer": 0.23114, "vicdemand": 0.355256, "vicprice": 0.003542} |

## Visual Artifacts

- score_plot_path: `artifacts\debug_elec2_hard\dataset_lab\elec2-20260429122157\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\debug_elec2_hard\dataset_lab\elec2-20260429122157\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\debug_elec2_hard\dataset_lab\elec2-20260429122157\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\debug_elec2_hard\dataset_lab\elec2-20260429122157`
- replay_summary_json_path: `E:\dipproj\artifacts\debug_elec2_hard\dataset_lab\elec2-20260429122157\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\debug_elec2_hard\dataset_lab\elec2-20260429122157\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\debug_elec2_hard\dataset_lab\elec2-20260429122157\summary.md`
