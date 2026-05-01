# E6 - Drift-aware selector / H1 control

- mode: benchmark profile suite
- profiles: `h1_drift_aware_v2, h1_drift_aware_v2_regression`
- datasets: `Elec2, InsectsRecurring, WaterFlow`
- n: `3`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- max_samples: `None`
- delta_mean: `-0.002128`
- delta_std: `0.003674`
- delta_ci95: `0.004157`
- effect_size_d: `-0.579347`
- paired_sign_test_p_value: `1.000000`
- wins_vs_best_fixed: `1`
- suite_summary_json_path: `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\suite_summary.json`
- suite_summary_md_path: `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\suite_summary.md`
- primary_plot_path: `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\phase10_delta_vs_best_fixed.png`
- switches_plot_path: `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\phase10_switch_count.png`

## Benchmark Protocol

- dataset_count: `3`
- profile_count: `2`
- sample_count_min: `1268`
- sample_count_max: `79986`
- consistent_sample_count: `False`
- interpretation_note: `Benchmark replay rows are deterministic temporal streams; inferential statistics are computed over dataset/profile result deltas and should be read as cautious phase-level evidence, not as a claim of universal superiority.`

## Policy Aggregates

| Policy | n | Delta Mean | Delta Std | Delta CI95 | Wins vs Best Fixed | Mean Switch Count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| hard_switch_lcb | 3 | -0.002128 | 0.003674 | 0.004157 | 1 | 14.000000 |

## Benchmark Results

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Delta | Switches | Report |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Elec2 | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 45312 | 0.872263 | 0.876832 | -0.004568 | 2 | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\elec2\summary.md` |
| InsectsRecurring | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 79986 | 0.768597 | 0.772510 | -0.003913 | 36 | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\insects_recurring\summary.md` |
| WaterFlow | h1_drift_aware_v2_regression | hard_switch_lcb | normalized_reward | 1268 | 0.806041 | 0.803945 | 0.002097 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2_regression\waterflow\summary.md` |

## Artifact Coverage

| Dataset | Profile | Config | Metrics | Decisions | Plot | Report |
| --- | --- | --- | --- | --- | --- | --- |
| Elec2 | h1_drift_aware_v2 | `E:\dipproj\configs\benchmark_profiles\h1_drift_aware_v2.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\elec2\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\elec2\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\elec2\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\elec2\summary.md` |
| InsectsRecurring | h1_drift_aware_v2 | `E:\dipproj\configs\benchmark_profiles\h1_drift_aware_v2.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\insects_recurring\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\insects_recurring\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\insects_recurring\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\insects_recurring\summary.md` |
| WaterFlow | h1_drift_aware_v2_regression | `E:\dipproj\configs\benchmark_profiles\h1_drift_aware_v2_regression.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2_regression\waterflow\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2_regression\waterflow\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2_regression\waterflow\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2_regression\waterflow\summary.md` |
