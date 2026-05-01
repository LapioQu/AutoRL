# Profile Suite Summary - e9_baseline-comparison

- profile_count: `5`
- dataset_count: `1`
- n: `5`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- delta_mean: `0.007949`
- delta_std: `0.013693`
- delta_ci95: `0.012002`
- effect_size_d: `0.580496`
- paired_sign_test_p_value: `0.375000`
- wins_vs_best_fixed: `4`
- non_losses_vs_best_fixed: `4`

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Delta | Switches | Summary |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| WaterFlow | adaptive_meta_final_regression | fixed_share_portfolio | normalized_reward | 1268 | 0.836279 | 0.803945 | 0.032334 | 10 | `E:\dipproj\artifacts\phase10_waterflow_system_lcb_probe\e9_baseline-comparison\adaptive_meta_final_regression\waterflow\summary.json` |
| WaterFlow | greedy_reward_regression | recent_leader_meta | normalized_reward | 1268 | 0.803759 | 0.803945 | -0.000186 | 1 | `E:\dipproj\artifacts\phase10_waterflow_system_lcb_probe\e9_baseline-comparison\greedy_reward_regression\waterflow\summary.json` |
| WaterFlow | h1_drift_aware_v2_regression | hard_switch_lcb | normalized_reward | 1268 | 0.806041 | 0.803945 | 0.002097 | 4 | `E:\dipproj\artifacts\phase10_waterflow_system_lcb_probe\e9_baseline-comparison\h1_drift_aware_v2_regression\waterflow\summary.json` |
| WaterFlow | h2_tempered_drift_regression | hard_switch_lcb | normalized_reward | 1268 | 0.842475 | 0.839073 | 0.003402 | 4 | `E:\dipproj\artifacts\phase10_waterflow_system_lcb_probe\e9_baseline-comparison\h2_tempered_drift_regression\waterflow\summary.json` |
| WaterFlow | hard_switch_lcb_regression | hard_switch_lcb | normalized_reward | 1268 | 0.806041 | 0.803945 | 0.002097 | 4 | `E:\dipproj\artifacts\phase10_waterflow_system_lcb_probe\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\summary.json` |
