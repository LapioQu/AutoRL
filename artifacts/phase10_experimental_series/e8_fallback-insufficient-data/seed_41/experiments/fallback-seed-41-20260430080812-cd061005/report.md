# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | fallback-seed-41-20260430080812-cd061005 |
| Experiment Name | fallback-seed-41 |
| Status | completed |
| Scenario | fallback |
| Seed | 41 |
| Config Hash | 5d097b446bee8ddc6404601679f17b61f959746e5c318d35a2be129f319f5963 |
| Artifacts Path | `E:\dipproj\artifacts\phase10_experimental_series\e8_fallback-insufficient-data\seed_41\experiments\fallback-seed-41-20260430080812-cd061005` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 100 |
| Decisions | 85 |
| Switches | 0 |
| Fallback Decisions | 7 |
| Average Reward | 1.138057 |
| Success Rate | 1.000000 |
| Cumulative Reward | 113.805650 |
| Mean Window Variance | 0.000031 |
| Final Strategy | fixed |

## Plot Artifacts

- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`

## Stay/Switch Summary

| Evaluation | Action | Current | Candidate | Margin | Threshold | Reason |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | stay | fixed | drift_aware | - | 0.130000 | insufficient_samples |
| 1 | stay | fixed | drift_aware | - | 0.130000 | insufficient_samples |
| 2 | stay | fixed | drift_aware | - | 0.130000 | insufficient_samples |
| 3 | stay | fixed | drift_aware | - | 0.130000 | insufficient_samples |
| 4 | stay | fixed | drift_aware | - | 0.130000 | insufficient_samples |
| 5 | stay | fixed | drift_aware | - | 0.130000 | insufficient_samples |
| 6 | stay | fixed | drift_aware | - | 0.130000 | insufficient_samples |
| 7 | stay | fixed | drift_aware | -0.060000 | 0.130000 | no_candidate_improvement |
| 8 | stay | fixed | drift_aware | -0.060000 | 0.130000 | no_candidate_improvement |
| 9 | stay | fixed | drift_aware | -0.060000 | 0.130000 | no_candidate_improvement |
| 10 | stay | fixed | drift_aware | -0.060000 | 0.130000 | no_candidate_improvement |
| 11 | stay | fixed | drift_aware | -0.060000 | 0.130000 | no_candidate_improvement |
| 12 | stay | fixed | drift_aware | -0.060000 | 0.130000 | no_candidate_improvement |
| 13 | stay | fixed | drift_aware | -0.060000 | 0.130000 | no_candidate_improvement |
| 14 | stay | fixed | drift_aware | -0.060000 | 0.130000 | no_candidate_improvement |
| 15 | stay | fixed | drift_aware | -0.060000 | 0.130000 | no_candidate_improvement |
| 16 | stay | fixed | drift_aware | -0.060000 | 0.130000 | no_candidate_improvement |
| 17 | stay | fixed | drift_aware | -0.060000 | 0.130000 | no_candidate_improvement |
| 18 | stay | fixed | drift_aware | -0.060000 | 0.130000 | no_candidate_improvement |
| 19 | stay | fixed | drift_aware | -0.060000 | 0.130000 | no_candidate_improvement |

_Showing first 20 of 85 decisions._

## Config Snapshot

```yaml
schema_version: '1.0'
experiment_name: fallback-seed-41
seed: 41
mode: adaptive
scenario:
  name: fallback
  episodes: 100
  steps_per_episode: 40
  reward_noise_std: 0.0
  drift_episode: null
  drift_start_episode: null
  drift_end_episode: null
  fallback_patience: 5
  tags:
  - fallback
  - safety
  description: Scenario reserved for insufficient-data and safe-stay pathways.
strategies:
- name: fixed
  parameters:
    exploration_rate: 0.05
  enabled: true
  compute_cost: 0.05
  description: null
- name: drift_aware
  parameters:
    detector_window: 12
  enabled: true
  compute_cost: 0.15
  description: null
meta_controller:
  window_size: 16
  min_samples: 8
  delta: 0.03
  lambda: 1.0
  switch_cost: 0.1
  utility_weights:
    compute_cost: 0.1
    reward_mean: 1.0
    reward_variance: 0.2
    switch_cost: 0.5
artifacts_root: E:\dipproj\artifacts\phase10_experimental_series\e8_fallback-insufficient-data\seed_41
tags:
- phase1
- fallback
notes: null
```
