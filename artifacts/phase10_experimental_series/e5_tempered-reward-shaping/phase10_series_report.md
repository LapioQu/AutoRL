# E5 - Tempered reward shaping

- mode: benchmark profile suite
- profiles: `h2_tempered_drift`
- datasets: `Airlines, Elec2, InsectsRecurring`
- n: `3`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- max_samples: `256`
- delta_mean: `-0.046875`
- delta_std: `0.025615`
- delta_ci95: `0.028986`
- effect_size_d: `-1.829983`
- paired_sign_test_p_value: `0.250000`
- wins_vs_best_fixed: `0`
- suite_summary_json_path: `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\suite_summary.json`
- suite_summary_md_path: `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\suite_summary.md`
- primary_plot_path: `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\phase10_delta_vs_best_fixed.png`
- switches_plot_path: `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\phase10_switch_count.png`

## Benchmark Protocol

- dataset_count: `3`
- profile_count: `1`
- sample_count_min: `256`
- sample_count_max: `256`
- consistent_sample_count: `True`
- interpretation_note: `Benchmark replay rows are deterministic temporal streams; inferential statistics are computed over dataset/profile result deltas and should be read as cautious phase-level evidence, not as a claim of universal superiority.`

## Policy Aggregates

| Policy | n | Delta Mean | Delta Std | Delta CI95 | Wins vs Best Fixed | Mean Switch Count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| hard_switch_lcb | 3 | -0.046875 | 0.025615 | 0.028986 | 0 | 0.000000 |

## Benchmark Results

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Delta | Switches | Report |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Airlines | h2_tempered_drift | hard_switch_lcb | accuracy | 256 | 0.761719 | 0.785156 | -0.023438 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\airlines\summary.md` |
| Elec2 | h2_tempered_drift | hard_switch_lcb | accuracy | 256 | 0.832031 | 0.906250 | -0.074219 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\elec2\summary.md` |
| InsectsRecurring | h2_tempered_drift | hard_switch_lcb | accuracy | 256 | 0.777344 | 0.820312 | -0.042969 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\insects_recurring\summary.md` |

## Artifact Coverage

| Dataset | Profile | Config | Metrics | Decisions | Plot | Report |
| --- | --- | --- | --- | --- | --- | --- |
| Airlines | h2_tempered_drift | `E:\dipproj\configs\benchmark_profiles\h2_tempered_drift.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\airlines\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\airlines\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\airlines\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\airlines\summary.md` |
| Elec2 | h2_tempered_drift | `E:\dipproj\configs\benchmark_profiles\h2_tempered_drift.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\elec2\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\elec2\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\elec2\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\elec2\summary.md` |
| InsectsRecurring | h2_tempered_drift | `E:\dipproj\configs\benchmark_profiles\h2_tempered_drift.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\insects_recurring\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\insects_recurring\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\insects_recurring\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\insects_recurring\summary.md` |
