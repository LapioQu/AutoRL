# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | noisy-reward-seed-45-20260430080725-6d24100c |
| Experiment Name | noisy_reward-seed-45 |
| Status | completed |
| Scenario | noisy_reward |
| Seed | 45 |
| Config Hash | 7095b8e03f8809aac5d42aec80e3cb2a3455cc14ded0fb5f7f8b56c7b21cea07 |
| Artifacts Path | `E:\dipproj\artifacts\phase10_experimental_series\e4_noisy-reward\seed_45\experiments\noisy-reward-seed-45-20260430080725-6d24100c` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 140 |
| Decisions | 123 |
| Switches | 0 |
| Fallback Decisions | 9 |
| Average Reward | 0.960413 |
| Success Rate | 1.000000 |
| Cumulative Reward | 134.457837 |
| Mean Window Variance | 0.002402 |
| Final Strategy | lcb_conservative |

## Plot Artifacts

- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`

## Stay/Switch Summary

| Evaluation | Action | Current | Candidate | Margin | Threshold | Reason |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | stay | lcb_conservative | adaptive_meta | - | 0.210000 | insufficient_samples |
| 1 | stay | lcb_conservative | adaptive_meta | - | 0.210000 | insufficient_samples |
| 2 | stay | lcb_conservative | adaptive_meta | - | 0.210000 | insufficient_samples |
| 3 | stay | lcb_conservative | adaptive_meta | - | 0.210000 | insufficient_samples |
| 4 | stay | lcb_conservative | adaptive_meta | - | 0.210000 | insufficient_samples |
| 5 | stay | lcb_conservative | adaptive_meta | - | 0.210000 | insufficient_samples |
| 6 | stay | lcb_conservative | adaptive_meta | - | 0.210000 | insufficient_samples |
| 7 | stay | lcb_conservative | adaptive_meta | - | 0.210000 | insufficient_samples |
| 8 | stay | lcb_conservative | adaptive_meta | - | 0.210000 | insufficient_samples |
| 9 | stay | lcb_conservative | adaptive_meta | -0.097753 | 0.210000 | no_candidate_improvement |
| 10 | stay | lcb_conservative | adaptive_meta | -0.097999 | 0.210000 | no_candidate_improvement |
| 11 | stay | lcb_conservative | adaptive_meta | -0.098000 | 0.210000 | no_candidate_improvement |
| 12 | stay | lcb_conservative | adaptive_meta | -0.098000 | 0.210000 | no_candidate_improvement |
| 13 | stay | lcb_conservative | adaptive_meta | -0.098000 | 0.210000 | no_candidate_improvement |
| 14 | stay | lcb_conservative | adaptive_meta | -0.098000 | 0.210000 | no_candidate_improvement |
| 15 | stay | lcb_conservative | adaptive_meta | -0.098000 | 0.210000 | no_candidate_improvement |
| 16 | stay | lcb_conservative | adaptive_meta | -0.098000 | 0.210000 | no_candidate_improvement |
| 17 | stay | lcb_conservative | adaptive_meta | -0.098000 | 0.210000 | no_candidate_improvement |
| 18 | stay | lcb_conservative | adaptive_meta | -0.098000 | 0.210000 | no_candidate_improvement |
| 19 | stay | lcb_conservative | adaptive_meta | -0.098000 | 0.210000 | no_candidate_improvement |

_Showing first 20 of 123 decisions._

## Config Snapshot

```yaml
schema_version: '1.0'
experiment_name: noisy_reward-seed-45
seed: 45
mode: adaptive
scenario:
  name: noisy_reward
  episodes: 140
  steps_per_episode: 55
  reward_noise_std: 0.35
  drift_episode: null
  drift_start_episode: null
  drift_end_episode: null
  fallback_patience: null
  tags:
  - noise
  - variance
  description: Stable regime with stochastic reward noise.
strategies:
- name: lcb_conservative
  parameters:
    confidence_lambda: 1.5
  enabled: true
  compute_cost: 0.12
  description: null
- name: adaptive_meta
  parameters:
    evaluation_window: 18
    temperature: 0.75
  enabled: true
  compute_cost: 0.22
  description: null
meta_controller:
  window_size: 18
  min_samples: 10
  delta: 0.05
  lambda: 1.4
  switch_cost: 0.16
  utility_weights:
    compute_cost: 0.1
    reward_mean: 1.0
    reward_variance: 0.35
    switch_cost: 0.55
artifacts_root: E:\dipproj\artifacts\phase10_experimental_series\e4_noisy-reward\seed_45
tags:
- phase1
- noisy_reward
notes: null
```
