# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T12:56:51.675918+00:00`
- dataset_name: `WaterFlow`
- task_type: `regression`
- target_column: `water_flow_lps`
- policy_name: `fixed_share_portfolio`
- source_row_count: `1268`
- source_rows_used: `1268`
- sample_count: `1268`
- feature_count: `1`
- next_prediction: `103.47866152881701`
- prediction_confidence: `0.9303` (high)

## Comparative Metrics

- adaptive_score: `0.836279`
- best_fixed_strategy: `lin_lr_0_001`
- best_fixed_score: `0.803945`
- delta_vs_best_fixed: `+0.032334`
- oracle_score: `0.874010`
- oracle_gain: `0.070065`
- oracle_capture_ratio: `46.15%`
- final_strategy: `lin_lr_0_0005`
- switch_count: `10`

## Interpretation

- Adaptive policy `fixed_share_portfolio` finished on strategy `lin_lr_0_0005` after 10 switches.
- It achieved `0.8363` against the best fixed baseline `lin_lr_0_001` at `0.8039`.
- Oracle upper bound on this stream is `0.8740`. Available oracle gain over best fixed is `0.0701`, and the current adaptive controller captures `46.1%` of it.
- The uploaded stream looks non-stationary enough for adaptation to help: the gain over best fixed is `0.0323`.
- Multiple switches suggest regime changes or at least changing local winners across the stream.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `103.4787` based on the latest lagged context `[104.3, 104.23, 104.1]`.

## Caveats

- Для цього готового датасету використано нативний потоковий профіль без CSV-перетворення ознак.
- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "Time": "2022-05-16 22:00:00+02:00"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 1256 | 104.39 | 102.91649792035908 | {"Time": "2022-05-16 08:00:00+02:00"} |
| 1257 | 104.71 | 102.96288940674677 | {"Time": "2022-05-16 09:00:00+02:00"} |
| 1258 | 104.77 | 103.01666409267419 | {"Time": "2022-05-16 10:00:00+02:00"} |
| 1259 | 104.69 | 103.07042831452809 | {"Time": "2022-05-16 11:00:00+02:00"} |
| 1260 | 104.69 | 103.12041442472716 | {"Time": "2022-05-16 12:00:00+02:00"} |
| 1261 | 104.64 | 103.16905998025734 | {"Time": "2022-05-16 13:00:00+02:00"} |
| 1262 | 104.59 | 103.21511336544513 | {"Time": "2022-05-16 14:00:00+02:00"} |
| 1263 | 104.62 | 103.25872658064421 | {"Time": "2022-05-16 15:00:00+02:00"} |
| 1264 | 104.65 | 103.30226491732094 | {"Time": "2022-05-16 16:00:00+02:00"} |
| 1265 | 104.3 | 103.41771448523589 | {"Time": "2022-05-16 20:00:00+02:00"} |
| 1266 | 104.23 | 103.44925702972262 | {"Time": "2022-05-16 21:00:00+02:00"} |
| 1267 | 104.1 | 103.4783007063431 | {"Time": "2022-05-16 22:00:00+02:00"} |

## Visual Artifacts

- score_plot_path: `artifacts\ui_manual_check\dataset_lab\waterflow-20260429125651\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\ui_manual_check\dataset_lab\waterflow-20260429125651\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\ui_manual_check\dataset_lab\waterflow-20260429125651\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\ui_manual_check\dataset_lab\waterflow-20260429125651`
- replay_summary_json_path: `E:\dipproj\artifacts\ui_manual_check\dataset_lab\waterflow-20260429125651\auto_meta_selection\fixed_share_portfolio\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\ui_manual_check\dataset_lab\waterflow-20260429125651\auto_meta_selection\fixed_share_portfolio\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\ui_manual_check\dataset_lab\waterflow-20260429125651\auto_meta_selection\fixed_share_portfolio\summary.md`
