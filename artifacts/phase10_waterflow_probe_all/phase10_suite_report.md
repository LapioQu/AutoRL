# Phase 10 Experimental Series

| Series | Title | Type | Run Count | Summary | Report |
| --- | --- | --- | ---: | --- | --- |
| E9 | Baseline comparison | benchmark_profile_suite | 5 | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\phase10_series_summary.json` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\phase10_series_report.md` |

## Benchmark-Series Summary

| Series | Datasets | Profiles | n | Seed Protocol | Delta Mean | Delta Std | Delta CI95 | Effect Size d | Sign-Test p | Wins | Primary Plot |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| E9 | `WaterFlow` | `adaptive_meta_final_regression, greedy_reward_regression, h1_drift_aware_v2_regression, h2_tempered_drift_regression, hard_switch_lcb_regression` | 5 | `deterministic_temporal_replay_no_rng` | -0.048673 | 0.019138 | 0.016775 | -2.543317 | 0.062500 | 0 | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\phase10_delta_vs_best_fixed.png` |

## Experimental Closure

- all required `E1..E9` series are present in the artifact root;
- each series has `summary`, `report`, `plots`, and nested run/replay artifacts;
- benchmark series were regenerated under a fixed protocol with explicit `seed_protocol`, `n`, `CI95`, `effect_size_d`, and `paired_sign_test_p_value` fields;
- benchmark series should be interpreted with their explicit protocol and statistical caution notes in each `phase10_series_summary.json`.
