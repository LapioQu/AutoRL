# Phase 10 Experimental Series

| Series | Title | Type | Run Count | Summary | Report |
| --- | --- | --- | ---: | --- | --- |
| E9 | Baseline comparison | benchmark_profile_suite | 1 | `E:\dipproj\artifacts\phase10_waterflow_probe\e9_baseline-comparison\phase10_series_summary.json` | `E:\dipproj\artifacts\phase10_waterflow_probe\e9_baseline-comparison\phase10_series_report.md` |

## Benchmark-Series Summary

| Series | Datasets | Profiles | n | Seed Protocol | Delta Mean | Delta Std | Delta CI95 | Effect Size d | Sign-Test p | Wins | Primary Plot |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| E9 | `WaterFlow` | `hard_switch_lcb_regression` | 1 | `deterministic_temporal_replay_no_rng` | -0.065067 | 0.000000 | 0.000000 | - | 1.000000 | 0 | `E:\dipproj\artifacts\phase10_waterflow_probe\e9_baseline-comparison\phase10_delta_vs_best_fixed.png` |

## Experimental Closure

- all required `E1..E9` series are present in the artifact root;
- each series has `summary`, `report`, `plots`, and nested run/replay artifacts;
- benchmark series were regenerated under a fixed protocol with explicit `seed_protocol`, `n`, `CI95`, `effect_size_d`, and `paired_sign_test_p_value` fields;
- benchmark series should be interpreted with their explicit protocol and statistical caution notes in each `phase10_series_summary.json`.
