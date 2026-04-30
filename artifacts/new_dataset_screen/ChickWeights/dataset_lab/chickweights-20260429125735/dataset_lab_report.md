# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T12:57:38.858965+00:00`
- dataset_name: `ChickWeights`
- task_type: `classification`
- target_column: `target`
- policy_name: `recent_leader_meta`
- source_row_count: `578`
- source_rows_used: `578`
- sample_count: `578`
- feature_count: `3`
- next_prediction: `264`
- prediction_confidence: `0.5000` (low)

## Comparative Metrics

- adaptive_score: `0.058824`
- best_fixed_strategy: `knn_classifier`
- best_fixed_score: `0.057093`
- delta_vs_best_fixed: `+0.001730`
- oracle_score: `0.110727`
- oracle_gain: `0.053633`
- oracle_capture_ratio: `3.23%`
- final_strategy: `knn_classifier`
- switch_count: `1`

## Interpretation

- Adaptive policy `recent_leader_meta` finished on strategy `knn_classifier` after 1 switches.
- It achieved `0.0588` against the best fixed baseline `knn_classifier` at `0.0571`.
- Oracle upper bound on this stream is `0.1107`. Available oracle gain over best fixed is `0.0536`, and the current adaptive controller captures `3.2%` of it.
- The uploaded stream looks non-stationary enough for adaptation to help: the gain over best fixed is `0.0017`.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step class from the final adaptive strategy is `264` based on the latest lagged context `['322', '237', '264']`.

## Caveats

- The stream is replayed in the original CSV row order.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is prequential accuracy over the uploaded stream.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "time": "21",
  "chick": "50",
  "diet": "4",
  "target": "264"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 566 | 290 | 103 | {"chick": 38, "diet": 3, "time": 21} |
| 567 | 272 | 128 | {"chick": 39, "diet": 3, "time": 21} |
| 568 | 321 | 130 | {"chick": 40, "diet": 3, "time": 21} |
| 569 | 204 | 153 | {"chick": 41, "diet": 4, "time": 21} |
| 570 | 281 | 174 | {"chick": 42, "diet": 4, "time": 21} |
| 571 | 200 | 188 | {"chick": 43, "diet": 4, "time": 21} |
| 572 | 196 | 141 | {"chick": 45, "diet": 4, "time": 21} |
| 573 | 238 | 156 | {"chick": 46, "diet": 4, "time": 21} |
| 574 | 205 | 157 | {"chick": 47, "diet": 4, "time": 21} |
| 575 | 322 | 170 | {"chick": 48, "diet": 4, "time": 21} |
| 576 | 237 | 166 | {"chick": 49, "diet": 4, "time": 21} |
| 577 | 264 | 175 | {"chick": 50, "diet": 4, "time": 21} |

## Visual Artifacts

- score_plot_path: `artifacts\new_dataset_screen\ChickWeights\dataset_lab\chickweights-20260429125735\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\new_dataset_screen\ChickWeights\dataset_lab\chickweights-20260429125735\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\new_dataset_screen\ChickWeights\dataset_lab\chickweights-20260429125735\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\new_dataset_screen\ChickWeights\dataset_lab\chickweights-20260429125735`
- replay_summary_json_path: `E:\dipproj\artifacts\new_dataset_screen\ChickWeights\dataset_lab\chickweights-20260429125735\auto_meta_selection\recent_leader_meta\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\new_dataset_screen\ChickWeights\dataset_lab\chickweights-20260429125735\auto_meta_selection\recent_leader_meta\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\new_dataset_screen\ChickWeights\dataset_lab\chickweights-20260429125735\auto_meta_selection\recent_leader_meta\summary.md`
