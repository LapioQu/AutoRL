# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | gradual-drift-seed-44-20260430080518-f8041a2a |
| Experiment Name | gradual_drift-seed-44 |
| Status | completed |
| Scenario | gradual_drift |
| Seed | 44 |
| Config Hash | bacbeb69ada942bde971b8821ba5fa298c1d5531b292893c702732af796d21dc |
| Artifacts Path | `E:\dipproj\artifacts\phase10_experimental_series\e3_gradual-drift\seed_44\experiments\gradual-drift-seed-44-20260430080518-f8041a2a` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 160 |
| Decisions | 137 |
| Switches | 0 |
| Fallback Decisions | 11 |
| Average Reward | 0.777333 |
| Success Rate | 0.687500 |
| Cumulative Reward | 124.373265 |
| Mean Window Variance | 0.000822 |
| Final Strategy | tempered_reward |

## Plot Artifacts

- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`

## Stay/Switch Summary

| Evaluation | Action | Current | Candidate | Margin | Threshold | Reason |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | stay | tempered_reward | adaptive_meta | - | 0.220000 | insufficient_samples |
| 1 | stay | tempered_reward | adaptive_meta | - | 0.220000 | insufficient_samples |
| 2 | stay | tempered_reward | adaptive_meta | - | 0.220000 | insufficient_samples |
| 3 | stay | tempered_reward | adaptive_meta | - | 0.220000 | insufficient_samples |
| 4 | stay | tempered_reward | adaptive_meta | - | 0.220000 | insufficient_samples |
| 5 | stay | tempered_reward | adaptive_meta | - | 0.220000 | insufficient_samples |
| 6 | stay | tempered_reward | adaptive_meta | - | 0.220000 | insufficient_samples |
| 7 | stay | tempered_reward | adaptive_meta | - | 0.220000 | insufficient_samples |
| 8 | stay | tempered_reward | adaptive_meta | - | 0.220000 | insufficient_samples |
| 9 | stay | tempered_reward | adaptive_meta | - | 0.220000 | insufficient_samples |
| 10 | stay | tempered_reward | adaptive_meta | - | 0.220000 | insufficient_samples |
| 11 | stay | tempered_reward | adaptive_meta | 0.091922 | 0.220000 | no_candidate_improvement |
| 12 | stay | tempered_reward | adaptive_meta | 0.092315 | 0.220000 | no_candidate_improvement |
| 13 | stay | tempered_reward | adaptive_meta | 0.092187 | 0.220000 | no_candidate_improvement |
| 14 | stay | tempered_reward | adaptive_meta | 0.092157 | 0.220000 | no_candidate_improvement |
| 15 | stay | tempered_reward | adaptive_meta | 0.092147 | 0.220000 | no_candidate_improvement |
| 16 | stay | tempered_reward | adaptive_meta | 0.092177 | 0.220000 | no_candidate_improvement |
| 17 | stay | tempered_reward | adaptive_meta | 0.092069 | 0.220000 | no_candidate_improvement |
| 18 | stay | tempered_reward | adaptive_meta | 0.091647 | 0.220000 | no_candidate_improvement |
| 19 | stay | tempered_reward | adaptive_meta | 0.090571 | 0.220000 | no_candidate_improvement |

_Showing first 20 of 137 decisions._

## Config Snapshot

```yaml
schema_version: '1.0'
experiment_name: gradual_drift-seed-44
seed: 44
mode: adaptive
scenario:
  name: gradual_drift
  episodes: 160
  steps_per_episode: 60
  reward_noise_std: 0.0
  drift_episode: null
  drift_start_episode: 50
  drift_end_episode: 110
  fallback_patience: null
  tags:
  - drift
  - gradual
  description: Reward regime shifts gradually over a wide interval.
strategies:
- name: tempered_reward
  parameters:
    decay: 0.98
    temperature: 0.7
  enabled: true
  compute_cost: 0.1
  description: null
- name: adaptive_meta
  parameters:
    evaluation_window: 24
    temperature: 0.9
  enabled: true
  compute_cost: 0.22
  description: null
meta_controller:
  window_size: 24
  min_samples: 12
  delta: 0.04
  lambda: 1.1
  switch_cost: 0.18
  utility_weights:
    compute_cost: 0.15
    reward_mean: 1.0
    reward_variance: 0.2
    switch_cost: 0.5
artifacts_root: E:\dipproj\artifacts\phase10_experimental_series\e3_gradual-drift\seed_44
tags:
- phase1
- gradual_drift
notes: null
```
