# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T15:09:46.555802+00:00`
- dataset_name: `Bikes`
- task_type: `regression`
- target_column: `bikes_in_use`
- policy_name: `fixed_share_portfolio`
- source_row_count: `4000`
- source_rows_used: `4000`
- sample_count: `3997`
- feature_count: `10`
- next_prediction: `1.7255346356144574`
- prediction_confidence: `0.2566` (low)

## Comparative Metrics

- adaptive_score: `0.728013`
- best_fixed_strategy: `lin_lr_0_001`
- best_fixed_score: `0.690565`
- delta_vs_best_fixed: `+0.037448`
- oracle_score: `0.788706`
- oracle_gain: `0.098141`
- oracle_capture_ratio: `38.16%`
- final_strategy: `lin_lr_0_002`
- switch_count: `18`

## Interpretation

- Adaptive policy `fixed_share_portfolio` finished on strategy `lin_lr_0_002` after 18 switches.
- It achieved `0.7280` against the best fixed baseline `lin_lr_0_001` at `0.6906`.
- Oracle upper bound on this stream is `0.7887`. Available oracle gain over best fixed is `0.0981`, and the current adaptive controller captures `38.2%` of it.
- The uploaded stream looks non-stationary enough for adaptation to help: the gain over best fixed is `0.0374`.
- Multiple switches suggest regime changes or at least changing local winners across the stream.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `1.7255` based on the latest lagged context `['7', '1', '1']`.

## Caveats

- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "moment": "2016-04-03 07:14:49",
  "station": "place-esquirol",
  "clouds": "0",
  "description": "clear sky",
  "humidity": "87",
  "pressure": "1009.0",
  "temperature": "10.28",
  "wind": "3.6",
  "bikes_in_use": "1"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 3985 | 1.0 | 1.4574691827687618 | {"clouds": 0, "description": "clear sky", "humidity": 87, "pressure": 1009, "station": "pomme", "target_lag_1": 7.0, "target_lag_2": 0.0, "target_lag_3": 0.0, "temperature": 10.28, "wind": 3.6} |
| 3986 | 0.0 | 1.9305599572398928 | {"clouds": 0, "description": "clear sky", "humidity": 87, "pressure": 1009, "station": "place-esquirol", "target_lag_1": 1.0, "target_lag_2": 7.0, "target_lag_3": 0.0, "temperature": 10.28, "wind": 3.6} |
| 3987 | 0.0 | 1.741244289896569 | {"clouds": 0, "description": "clear sky", "humidity": 87, "pressure": 1009, "station": "place-jeanne-darc", "target_lag_1": 0.0, "target_lag_2": 1.0, "target_lag_3": 7.0, "temperature": 10.28, "wind": 3.6} |
| 3988 | 0.0 | 1.6474262737458338 | {"clouds": 0, "description": "clear sky", "humidity": 87, "pressure": 1009, "station": "place-des-carmes", "target_lag_1": 0.0, "target_lag_2": 0.0, "target_lag_3": 1.0, "temperature": 10.28, "wind": 3.6} |
| 3989 | 7.0 | 1.553864199283879 | {"clouds": 0, "description": "clear sky", "humidity": 87, "pressure": 1009, "station": "metro-canal-du-midi", "target_lag_1": 0.0, "target_lag_2": 0.0, "target_lag_3": 0.0, "temperature": 10.28, "wind": 3.6} |
| 3990 | 1.0 | 1.4575074122653422 | {"clouds": 0, "description": "clear sky", "humidity": 87, "pressure": 1009, "station": "pomme", "target_lag_1": 7.0, "target_lag_2": 0.0, "target_lag_3": 0.0, "temperature": 10.28, "wind": 3.6} |
| 3991 | 0.0 | 1.9263005419453114 | {"clouds": 0, "description": "clear sky", "humidity": 87, "pressure": 1009, "station": "place-esquirol", "target_lag_1": 1.0, "target_lag_2": 7.0, "target_lag_3": 0.0, "temperature": 10.28, "wind": 3.6} |
| 3992 | 0.0 | 1.7374493303350693 | {"clouds": 0, "description": "clear sky", "humidity": 87, "pressure": 1009, "station": "place-jeanne-darc", "target_lag_1": 0.0, "target_lag_2": 1.0, "target_lag_3": 7.0, "temperature": 10.28, "wind": 3.6} |
| 3993 | 0.0 | 1.64880623570558 | {"clouds": 0, "description": "clear sky", "humidity": 87, "pressure": 1009, "station": "place-des-carmes", "target_lag_1": 0.0, "target_lag_2": 0.0, "target_lag_3": 1.0, "temperature": 10.28, "wind": 3.6} |
| 3994 | 7.0 | 1.5560607401633926 | {"clouds": 0, "description": "clear sky", "humidity": 87, "pressure": 1009, "station": "metro-canal-du-midi", "target_lag_1": 0.0, "target_lag_2": 0.0, "target_lag_3": 0.0, "temperature": 10.28, "wind": 3.6} |
| 3995 | 1.0 | 1.4577751437293616 | {"clouds": 0, "description": "clear sky", "humidity": 87, "pressure": 1009, "station": "pomme", "target_lag_1": 7.0, "target_lag_2": 0.0, "target_lag_3": 0.0, "temperature": 10.28, "wind": 3.6} |
| 3996 | 1.0 | 1.9222674709211154 | {"clouds": 0, "description": "clear sky", "humidity": 87, "pressure": 1009, "station": "place-esquirol", "target_lag_1": 1.0, "target_lag_2": 7.0, "target_lag_3": 0.0, "temperature": 10.28, "wind": 3.6} |

## Visual Artifacts

- score_plot_path: `artifacts\tmp_eval\dataset_lab\bikes-20260429150932\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\tmp_eval\dataset_lab\bikes-20260429150932\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\tmp_eval\dataset_lab\bikes-20260429150932\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\tmp_eval\dataset_lab\bikes-20260429150932`
- replay_summary_json_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\bikes-20260429150932\auto_meta_selection\fixed_share_portfolio\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\bikes-20260429150932\auto_meta_selection\fixed_share_portfolio\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\tmp_eval\dataset_lab\bikes-20260429150932\auto_meta_selection\fixed_share_portfolio\summary.md`
