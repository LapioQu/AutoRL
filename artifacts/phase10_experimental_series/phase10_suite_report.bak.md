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

| Series | Datasets | Profiles | n | Seed Protocol | Delta Mean | Delta Std | Delta CI95 | Effect Size d | Sign-Test p | Wins | Primary Plot |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| E5 | `Airlines, Elec2, InsectsRecurring` | `h2_tempered_drift` | 3 | `deterministic_temporal_replay_no_rng` | -0.046875 | 0.025615 | 0.028986 | -1.829983 | 0.250000 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\phase10_delta_vs_best_fixed.png` |
| E6 | `Airlines, Elec2, InsectsRecurring` | `h1_drift_aware_v2` | 3 | `deterministic_temporal_replay_no_rng` | -0.046875 | 0.025615 | 0.028986 | -1.829983 | 0.250000 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\phase10_delta_vs_best_fixed.png` |
| E9 | `Airlines, Elec2, InsectsRecurring` | `adaptive_meta_final, greedy_reward, h1_drift_aware_v2, h2_tempered_drift, hard_switch_lcb` | 15 | `deterministic_temporal_replay_no_rng` | -0.045573 | 0.020652 | 0.010452 | -2.206670 | 0.000061 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\phase10_delta_vs_best_fixed.png` |

## Experimental Closure

- all required `E1..E9` series are present in the artifact root;
- each series has `summary`, `report`, `plots`, and nested run/replay artifacts;
- benchmark series were regenerated under a fixed protocol with explicit `seed_protocol`, `n`, `CI95`, `effect_size_d`, and `paired_sign_test_p_value` fields;
- benchmark series should be interpreted with their explicit protocol and statistical caution notes in each `phase10_series_summary.json`.
