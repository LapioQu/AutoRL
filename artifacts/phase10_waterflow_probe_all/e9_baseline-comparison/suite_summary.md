# Profile Suite Summary - e9_baseline-comparison

- profile_count: `5`
- dataset_count: `1`
- n: `5`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- delta_mean: `-0.048673`
- delta_std: `0.019138`
- delta_ci95: `0.016775`
- effect_size_d: `-2.543317`
- paired_sign_test_p_value: `0.062500`
- wins_vs_best_fixed: `0`
- non_losses_vs_best_fixed: `0`

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Delta | Switches | Summary |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| WaterFlow | adaptive_meta_final_regression | fixed_share_portfolio | normalized_reward | 1268 | 0.834057 | 0.854192 | -0.020135 | 6 | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\adaptive_meta_final_regression\waterflow\summary.json` |
| WaterFlow | greedy_reward_regression | recent_leader_meta | normalized_reward | 1268 | 0.814857 | 0.854192 | -0.039335 | 2 | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\greedy_reward_regression\waterflow\summary.json` |
| WaterFlow | h1_drift_aware_v2_regression | hard_switch_lcb | normalized_reward | 1268 | 0.789125 | 0.854192 | -0.065067 | 1 | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\h1_drift_aware_v2_regression\waterflow\summary.json` |
| WaterFlow | h2_tempered_drift_regression | hard_switch_lcb | normalized_reward | 1268 | 0.824297 | 0.878059 | -0.053762 | 1 | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\h2_tempered_drift_regression\waterflow\summary.json` |
| WaterFlow | hard_switch_lcb_regression | hard_switch_lcb | normalized_reward | 1268 | 0.789125 | 0.854192 | -0.065067 | 1 | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\summary.json` |
