# E5 - Tempered reward shaping

- mode: benchmark profile suite
- profiles: `h2_tempered_drift, h2_tempered_drift_regression`
- datasets: `Elec2, InsectsRecurring, WaterFlow`
- n: `3`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- max_samples: `None`
- delta_mean: `-0.006355`
- delta_std: `0.010455`
- delta_ci95: `0.011831`
- oracle_gain_mean: `0.097982`
- oracle_gain_ci95: `0.055056`
- oracle_capture_mean: `0.019250`
- oracle_capture_ci95: `0.037731`
- effect_size_d: `-0.607818`
- paired_sign_test_p_value: `1.000000`
- wins_vs_best_fixed: `1`
- suite_summary_json_path: `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\suite_summary.json`
- suite_summary_md_path: `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\suite_summary.md`
- primary_plot_path: `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\phase10_delta_vs_best_fixed.png`
- switches_plot_path: `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\phase10_switch_count.png`

## Benchmark Protocol

- dataset_count: `3`
- profile_count: `2`
- sample_count_min: `1268`
- sample_count_max: `79986`
- consistent_sample_count: `False`
- interpretation_note: `Benchmark replay rows are deterministic temporal streams; inferential statistics are computed over dataset/profile result deltas and should be read as cautious phase-level evidence, not as a claim of universal superiority.`

## Policy Aggregates

| Policy | n | Delta Mean | Delta Std | Delta CI95 | Oracle Gain Mean | Capture Mean | Capture CI95 | Wins vs Best Fixed | Mean Switch Count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| hard_switch_lcb | 3 | -0.006355 | 0.010455 | 0.011831 | 0.097982 | 0.019250 | 0.037731 | 1 | 15.000000 |

## Benchmark Results

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Oracle | Delta | Capture | Switches | Report |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Elec2 | h2_tempered_drift | hard_switch_lcb | accuracy | 45312 | 0.859441 | 0.876832 | 0.959393 | -0.017391 | 0.000000 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\elec2\summary.md` |
| InsectsRecurring | h2_tempered_drift | hard_switch_lcb | accuracy | 79986 | 0.767434 | 0.772510 | 0.924987 | -0.005076 | 0.000000 | 37 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\insects_recurring\summary.md` |
| WaterFlow | h2_tempered_drift_regression | hard_switch_lcb | normalized_reward | 1268 | 0.842475 | 0.839073 | 0.897982 | 0.003402 | 0.057751 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift_regression\waterflow\summary.md` |

## Artifact Coverage

| Dataset | Profile | Config | Metrics | Decisions | Plot | Report |
| --- | --- | --- | --- | --- | --- | --- |
| Elec2 | h2_tempered_drift | `E:\dipproj\configs\benchmark_profiles\h2_tempered_drift.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\elec2\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\elec2\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\elec2\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\elec2\summary.md` |
| InsectsRecurring | h2_tempered_drift | `E:\dipproj\configs\benchmark_profiles\h2_tempered_drift.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\insects_recurring\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\insects_recurring\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\insects_recurring\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\insects_recurring\summary.md` |
| WaterFlow | h2_tempered_drift_regression | `E:\dipproj\configs\benchmark_profiles\h2_tempered_drift_regression.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift_regression\waterflow\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift_regression\waterflow\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift_regression\waterflow\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift_regression\waterflow\summary.md` |
