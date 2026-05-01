# Profile Suite Summary - e5_tempered-reward-shaping

- profile_count: `2`
- dataset_count: `3`
- n: `3`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- delta_mean: `-0.000318`
- delta_std: `0.003659`
- delta_ci95: `0.004141`
- effect_size_d: `-0.086773`
- paired_sign_test_p_value: `1.000000`
- wins_vs_best_fixed: `1`
- non_losses_vs_best_fixed: `1`

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Delta | Switches | Summary |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Elec2 | h2_tempered_drift | hard_switch_lcb | accuracy | 45312 | 0.876390 | 0.876832 | -0.000441 | 2 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\elec2\summary.json` |
| InsectsRecurring | h2_tempered_drift | hard_switch_lcb | accuracy | 79986 | 0.768597 | 0.772510 | -0.003913 | 36 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\insects_recurring\summary.json` |
| WaterFlow | h2_tempered_drift_regression | hard_switch_lcb | normalized_reward | 1268 | 0.842475 | 0.839073 | 0.003402 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift_regression\waterflow\summary.json` |
