# Phase 10 Experimental Series

| Series | Title | Type | Run Count | Summary | Report |
| --- | --- | --- | ---: | --- | --- |
| E1 | Stationary control | seeded_experiment_suite | 5 | `E:\dipproj\artifacts\phase10_experimental_series\e1_stationary-control\phase10_series_summary.json` | `E:\dipproj\artifacts\phase10_experimental_series\e1_stationary-control\phase10_series_report.md` |
| E2 | Abrupt drift | seeded_experiment_suite | 5 | `E:\dipproj\artifacts\phase10_experimental_series\e2_abrupt-drift\phase10_series_summary.json` | `E:\dipproj\artifacts\phase10_experimental_series\e2_abrupt-drift\phase10_series_report.md` |
| E3 | Gradual drift | seeded_experiment_suite | 5 | `E:\dipproj\artifacts\phase10_experimental_series\e3_gradual-drift\phase10_series_summary.json` | `E:\dipproj\artifacts\phase10_experimental_series\e3_gradual-drift\phase10_series_report.md` |
| E4 | Noisy reward | seeded_experiment_suite | 5 | `E:\dipproj\artifacts\phase10_experimental_series\e4_noisy-reward\phase10_series_summary.json` | `E:\dipproj\artifacts\phase10_experimental_series\e4_noisy-reward\phase10_series_report.md` |
| E5 | Tempered reward shaping | benchmark_profile_suite | 3 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\phase10_series_summary.json` | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\phase10_series_report.md` |
| E6 | Drift-aware selector / H1 control | benchmark_profile_suite | 3 | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\phase10_series_summary.json` | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\phase10_series_report.md` |
| E7 | Reproducibility | seeded_experiment_suite | 5 | `E:\dipproj\artifacts\phase10_experimental_series\e7_reproducibility\phase10_series_summary.json` | `E:\dipproj\artifacts\phase10_experimental_series\e7_reproducibility\phase10_series_report.md` |
| E8 | Fallback insufficient data | seeded_experiment_suite | 5 | `E:\dipproj\artifacts\phase10_experimental_series\e8_fallback-insufficient-data\phase10_series_summary.json` | `E:\dipproj\artifacts\phase10_experimental_series\e8_fallback-insufficient-data\phase10_series_report.md` |
| E9 | Baseline comparison | benchmark_profile_suite | 15 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\phase10_series_summary.json` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\phase10_series_report.md` |

## Controlled-Series Summary

| Series | n | Seeds | Reward Mean | Reward Std | Reward CI95 | Primary Plot | Switch Plot |
| --- | ---: | --- | ---: | ---: | ---: | --- | --- |
| E1 | 5 | `41, 42, 43, 44, 45` | 0.989074 | 0.000181 | 0.000159 | `E:\dipproj\artifacts\phase10_experimental_series\e1_stationary-control\phase10_reward_mean.png` | `E:\dipproj\artifacts\phase10_experimental_series\e1_stationary-control\phase10_switch_count.png` |
| E2 | 5 | `41, 42, 43, 44, 45` | 0.973795 | 0.000078 | 0.000069 | `E:\dipproj\artifacts\phase10_experimental_series\e2_abrupt-drift\phase10_reward_mean.png` | `E:\dipproj\artifacts\phase10_experimental_series\e2_abrupt-drift\phase10_switch_count.png` |
| E3 | 5 | `41, 42, 43, 44, 45` | 0.776206 | 0.000895 | 0.000785 | `E:\dipproj\artifacts\phase10_experimental_series\e3_gradual-drift\phase10_reward_mean.png` | `E:\dipproj\artifacts\phase10_experimental_series\e3_gradual-drift\phase10_switch_count.png` |
| E4 | 5 | `41, 42, 43, 44, 45` | 0.860163 | 0.228056 | 0.199900 | `E:\dipproj\artifacts\phase10_experimental_series\e4_noisy-reward\phase10_reward_mean.png` | `E:\dipproj\artifacts\phase10_experimental_series\e4_noisy-reward\phase10_switch_count.png` |
| E7 | 5 | `12345, 12345, 12345, 12345, 12345` | 0.987972 | 0.000000 | 0.000000 | `E:\dipproj\artifacts\phase10_experimental_series\e7_reproducibility\phase10_reward_mean.png` | `E:\dipproj\artifacts\phase10_experimental_series\e7_reproducibility\phase10_switch_count.png` |
| E8 | 5 | `41, 42, 43, 44, 45` | 1.137804 | 0.000241 | 0.000211 | `E:\dipproj\artifacts\phase10_experimental_series\e8_fallback-insufficient-data\phase10_reward_mean.png` | `E:\dipproj\artifacts\phase10_experimental_series\e8_fallback-insufficient-data\phase10_switch_count.png` |

## Benchmark-Series Summary

| Series | Datasets | Profiles | n | Seed Protocol | Delta Mean | Delta Std | Delta CI95 | Oracle Gain Mean | Capture Mean | Effect Size d | Sign-Test p | Wins | Primary Plot |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| E5 | `Elec2, InsectsRecurring, WaterFlow` | `h2_tempered_drift, h2_tempered_drift_regression` | 3 | `deterministic_temporal_replay_no_rng` | -0.006355 | 0.010455 | 0.011831 | 0.097982 | 0.019250 | -0.607818 | 1.000000 | 1 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\phase10_delta_vs_best_fixed.png` |
| E6 | `Elec2, InsectsRecurring, WaterFlow` | `h1_drift_aware_v2, h1_drift_aware_v2_regression` | 3 | `deterministic_temporal_replay_no_rng` | -0.006790 | 0.009856 | 0.011153 | 0.101701 | 0.009975 | -0.688908 | 1.000000 | 1 | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\phase10_delta_vs_best_fixed.png` |
| E9 | `Elec2, InsectsRecurring, WaterFlow` | `adaptive_meta_final, adaptive_meta_final_regression, greedy_reward, greedy_reward_regression, h1_drift_aware_v2, h1_drift_aware_v2_regression, h2_tempered_drift, h2_tempered_drift_regression, hard_switch_lcb, hard_switch_lcb_regression` | 15 | `deterministic_temporal_replay_no_rng` | -0.002249 | 0.011917 | 0.006031 | 0.100957 | 0.038606 | -0.188746 | 0.118469 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\phase10_delta_vs_best_fixed.png` |

## Experimental Closure

- all required `E1..E9` series are present in the artifact root;
- each series has `summary`, `report`, `plots`, and nested run/replay artifacts;
- benchmark series were regenerated under a fixed protocol with explicit `seed_protocol`, `n`, `CI95`, `effect_size_d`, `paired_sign_test_p_value`, and oracle-capture fields;
- benchmark series should be interpreted with their explicit protocol, best-fixed deltas, and oracle-gain / capture notes in each `phase10_series_summary.json`.
