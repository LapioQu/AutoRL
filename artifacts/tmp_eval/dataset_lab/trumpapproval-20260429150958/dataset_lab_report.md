# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T15:10:02.000278+00:00`
- dataset_name: `TrumpApproval`
- task_type: `regression`
- target_column: `approval`
- policy_name: `recent_leader_meta`
- source_row_count: `1001`
- source_rows_used: `1001`
- sample_count: `998`
- feature_count: `8`
- next_prediction: `41.8841946`
- prediction_confidence: `0.9728` (high)

## Comparative Metrics

- adaptive_score: `0.817867`
- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.817867`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.868765`
- oracle_gain: `0.050898`
- oracle_capture_ratio: `0.00%`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Interpretation

- Adaptive policy `recent_leader_meta` finished on strategy `knn_regressor` after 0 switches.
- It achieved `0.8179` against the best fixed baseline `knn_regressor` at `0.8179`.
- Oracle upper bound on this stream is `0.8688`. Available oracle gain over best fixed is `0.0509`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `41.8842` based on the latest lagged context `['41.891828000000004', '41.725396999999994', '41.740203']`.

## Caveats

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
  "you_gov": "41.636914000000004",
  "approval": "41.740203"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 986 | 41.196125 | 41.3612436 | {"gallup": 41.843213, "ipsos": 41.570679, "morning_consult": 37.318749, "rasmussen": 44.104692, "target_lag_1": 41.151785, "target_lag_2": 40.950028, "target_lag_3": 41.10089, "you_gov": 42.636914000000004} |
| 987 | 41.196125 | 41.3505686 | {"gallup": 41.843213, "ipsos": 41.570679, "morning_consult": 37.318749, "rasmussen": 44.104692, "target_lag_1": 41.196125, "target_lag_2": 41.151785, "target_lag_3": 40.950028, "you_gov": 42.636914000000004} |
| 988 | 41.196125 | 41.3120696 | {"gallup": 41.843213, "ipsos": 41.570679, "morning_consult": 37.318749, "rasmussen": 44.104692, "target_lag_1": 41.196125, "target_lag_2": 41.196125, "target_lag_3": 41.151785, "you_gov": 42.636914000000004} |
| 989 | 41.218683 | 41.318615199999996 | {"gallup": 41.843213, "ipsos": 41.570679, "morning_consult": 39.318749, "rasmussen": 44.104692, "target_lag_1": 41.196125, "target_lag_2": 41.196125, "target_lag_3": 41.196125, "you_gov": 41.97024733333334} |
| 990 | 41.285517999999996 | 40.435122 | {"gallup": 41.843213, "ipsos": 41.570679, "morning_consult": 38.318749, "rasmussen": 42.104692, "target_lag_1": 41.218683, "target_lag_2": 41.196125, "target_lag_3": 41.196125, "you_gov": 45.636914000000004} |
| 991 | 41.351546 | 40.32385 | {"gallup": 43.843213, "ipsos": 40.570679, "morning_consult": 36.318749, "rasmussen": 42.104692, "target_lag_1": 41.285517999999996, "target_lag_2": 41.218683, "target_lag_3": 41.196125, "you_gov": 39.636914000000004} |
| 992 | 41.876382 | 41.2429256 | {"gallup": 43.843213, "ipsos": 40.570679, "morning_consult": 36.318749, "rasmussen": 40.104692, "target_lag_1": 41.351546, "target_lag_2": 41.285517999999996, "target_lag_3": 41.218683, "you_gov": 42.636914000000004} |
| 993 | 41.891828000000004 | 41.197824000000004 | {"gallup": 43.843213, "ipsos": 40.570679, "morning_consult": 38.818749, "rasmussen": 40.104692, "target_lag_1": 41.876382, "target_lag_2": 41.351546, "target_lag_3": 41.285517999999996, "you_gov": 43.636914000000004} |
| 994 | 41.891828000000004 | 41.3524356 | {"gallup": 43.843213, "ipsos": 40.570679, "morning_consult": 38.818749, "rasmussen": 40.104692, "target_lag_1": 41.891828000000004, "target_lag_2": 41.876382, "target_lag_3": 41.351546, "you_gov": 43.636914000000004} |
| 995 | 41.891828000000004 | 41.584245200000005 | {"gallup": 43.843213, "ipsos": 40.570679, "morning_consult": 38.818749, "rasmussen": 40.104692, "target_lag_1": 41.891828000000004, "target_lag_2": 41.891828000000004, "target_lag_3": 41.876382, "you_gov": 43.636914000000004} |
| 996 | 41.725396999999994 | 41.5394996 | {"gallup": 43.843213, "ipsos": 40.570679, "morning_consult": 38.818749, "rasmussen": 38.104692, "target_lag_1": 41.891828000000004, "target_lag_2": 41.891828000000004, "target_lag_3": 41.891828000000004, "you_gov": 41.636914000000004} |
| 997 | 41.740203 | 41.76527 | {"gallup": 43.843213, "ipsos": 40.570679, "morning_consult": 37.818749, "rasmussen": 40.104692, "target_lag_1": 41.725396999999994, "target_lag_2": 41.891828000000004, "target_lag_3": 41.891828000000004, "you_gov": 41.636914000000004} |

## Visual Artifacts

- score_plot_path: `artifacts\tmp_eval\dataset_lab\trumpapproval-20260429150958\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\tmp_eval\dataset_lab\trumpapproval-20260429150958\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\tmp_eval\dataset_lab\trumpapproval-20260429150958\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\tmp_eval\dataset_lab\trumpapproval-20260429150958`
- replay_summary_json_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\trumpapproval-20260429150958\auto_meta_selection\recent_leader_meta\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\trumpapproval-20260429150958\auto_meta_selection\recent_leader_meta\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\trumpapproval-20260429150958\auto_meta_selection\recent_leader_meta\summary.md`
