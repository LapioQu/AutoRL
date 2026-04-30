# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T12:33:21.126264+00:00`
- dataset_name: `TrumpApproval`
- task_type: `regression`
- target_column: `approval`
- policy_name: `best_fixed_guard`
- source_row_count: `1001`
- source_rows_used: `1001`
- sample_count: `1001`
- feature_count: `6`
- next_prediction: `41.766619952703245`
- prediction_confidence: `0.9954` (high)

## Comparative Metrics

- adaptive_score: `0.801432`
- best_fixed_strategy: `sgd_lr_0_05`
- best_fixed_score: `0.801432`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.856048`
- oracle_gain: `0.054615`
- oracle_capture_ratio: `0.00%`
- final_strategy: `sgd_lr_0_05`
- switch_count: `0`

## Interpretation

- Adaptive policy `best_fixed_guard` finished on strategy `sgd_lr_0_05` after 0 switches.
- It achieved `0.8014` against the best fixed baseline `sgd_lr_0_05` at `0.8014`.
- Oracle upper bound on this stream is `0.8560`. Available oracle gain over best fixed is `0.0546`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `41.7666` based on the latest lagged context `[41.891828000000004, 41.725396999999994, 41.740203]`.

## Caveats

- Для цього готового датасету використано нативний потоковий профіль без CSV-перетворення ознак.
- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "ordinal_date": "737389",
  "gallup": "43.843213",
  "ipsos": "40.570679",
  "morning_consult": "37.818749",
  "rasmussen": "40.104692",
  "you_gov": "41.636914000000004"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 989 | 41.196125 | 41.94687398682733 | {"gallup": 41.843213, "ipsos": 41.570679, "morning_consult": 37.318749, "ordinal_date": 737378, "rasmussen": 44.104692, "you_gov": 42.636914000000004} |
| 990 | 41.196125 | 41.399565673549176 | {"gallup": 41.843213, "ipsos": 41.570679, "morning_consult": 37.318749, "ordinal_date": 737379, "rasmussen": 44.104692, "you_gov": 42.636914000000004} |
| 991 | 41.196125 | 41.29556855622372 | {"gallup": 41.843213, "ipsos": 41.570679, "morning_consult": 37.318749, "ordinal_date": 737380, "rasmussen": 44.104692, "you_gov": 42.636914000000004} |
| 992 | 41.218683 | 41.480395517709496 | {"gallup": 41.843213, "ipsos": 41.570679, "morning_consult": 39.318749, "ordinal_date": 737381, "rasmussen": 44.104692, "you_gov": 41.97024733333334} |
| 993 | 41.285517999999996 | 41.04431929534993 | {"gallup": 41.843213, "ipsos": 41.570679, "morning_consult": 38.318749, "ordinal_date": 737382, "rasmussen": 42.104692, "you_gov": 45.636914000000004} |
| 994 | 41.351546 | 41.16002907166147 | {"gallup": 43.843213, "ipsos": 40.570679, "morning_consult": 36.318749, "ordinal_date": 737383, "rasmussen": 42.104692, "you_gov": 39.636914000000004} |
| 995 | 41.876382 | 41.2588231586622 | {"gallup": 43.843213, "ipsos": 40.570679, "morning_consult": 36.318749, "ordinal_date": 737384, "rasmussen": 40.104692, "you_gov": 42.636914000000004} |
| 996 | 41.891828000000004 | 41.96051492668662 | {"gallup": 43.843213, "ipsos": 40.570679, "morning_consult": 38.818749, "ordinal_date": 737385, "rasmussen": 40.104692, "you_gov": 43.636914000000004} |
| 997 | 41.891828000000004 | 41.96518141517568 | {"gallup": 43.843213, "ipsos": 40.570679, "morning_consult": 38.818749, "ordinal_date": 737386, "rasmussen": 40.104692, "you_gov": 43.636914000000004} |
| 998 | 41.891828000000004 | 41.966231361673124 | {"gallup": 43.843213, "ipsos": 40.570679, "morning_consult": 38.818749, "ordinal_date": 737387, "rasmussen": 40.104692, "you_gov": 43.636914000000004} |
| 999 | 41.725396999999994 | 41.77313989394931 | {"gallup": 43.843213, "ipsos": 40.570679, "morning_consult": 38.818749, "ordinal_date": 737388, "rasmussen": 38.104692, "you_gov": 41.636914000000004} |
| 1000 | 41.740203 | 41.887949456221094 | {"gallup": 43.843213, "ipsos": 40.570679, "morning_consult": 37.818749, "ordinal_date": 737389, "rasmussen": 40.104692, "you_gov": 41.636914000000004} |

## Visual Artifacts

- score_plot_path: `artifacts\ui_generic_fix_check\dataset_lab\trumpapproval-20260429123320\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\ui_generic_fix_check\dataset_lab\trumpapproval-20260429123320\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\ui_generic_fix_check\dataset_lab\trumpapproval-20260429123320\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\ui_generic_fix_check\dataset_lab\trumpapproval-20260429123320`
- replay_summary_json_path: `E:\dipproj\artifacts\ui_generic_fix_check\dataset_lab\trumpapproval-20260429123320\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\ui_generic_fix_check\dataset_lab\trumpapproval-20260429123320\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\ui_generic_fix_check\dataset_lab\trumpapproval-20260429123320\summary.md`
