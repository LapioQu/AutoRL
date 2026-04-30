# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | stationary-seed-43-20260430043001-4dcceb41 |
| Experiment Name | stationary-seed-43 |
| Status | completed |
| Scenario | stationary |
| Seed | 43 |
| Config Hash | 0334c46ebfc83f113bb42488f6c5cee5f0edee29bf2f392e27ded27c60812c12 |
| Artifacts Path | `E:\dipproj\artifacts\phase10_experimental_series\e1_stationary-control\seed_43\experiments\stationary-seed-43-20260430043001-4dcceb41` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 120 |
| Decisions | 101 |
| Switches | 0 |
| Fallback Decisions | 9 |
| Average Reward | 0.988865 |
| Success Rate | 1.000000 |
| Cumulative Reward | 118.663852 |
| Mean Window Variance | 0.000006 |
| Final Strategy | fixed |

## Plot Artifacts

- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`

## Stay/Switch Summary

| Evaluation | Action | Current | Candidate | Margin | Threshold | Reason |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | stay | fixed | adaptive_meta | - | 0.200000 | insufficient_samples |
| 1 | stay | fixed | adaptive_meta | - | 0.200000 | insufficient_samples |
| 2 | stay | fixed | adaptive_meta | - | 0.200000 | insufficient_samples |
| 3 | stay | fixed | adaptive_meta | - | 0.200000 | insufficient_samples |
| 4 | stay | fixed | adaptive_meta | - | 0.200000 | insufficient_samples |
| 5 | stay | fixed | adaptive_meta | - | 0.200000 | insufficient_samples |
| 6 | stay | fixed | adaptive_meta | - | 0.200000 | insufficient_samples |
| 7 | stay | fixed | adaptive_meta | - | 0.200000 | insufficient_samples |
| 8 | stay | fixed | adaptive_meta | - | 0.200000 | insufficient_samples |
| 9 | stay | fixed | adaptive_meta | -0.095253 | 0.200000 | no_candidate_improvement |
| 10 | stay | fixed | adaptive_meta | -0.095000 | 0.200000 | no_candidate_improvement |
| 11 | stay | fixed | adaptive_meta | -0.095000 | 0.200000 | no_candidate_improvement |
| 12 | stay | fixed | adaptive_meta | -0.095000 | 0.200000 | no_candidate_improvement |
| 13 | stay | fixed | adaptive_meta | -0.095000 | 0.200000 | no_candidate_improvement |
| 14 | stay | fixed | adaptive_meta | -0.095000 | 0.200000 | no_candidate_improvement |
| 15 | stay | fixed | adaptive_meta | -0.095000 | 0.200000 | no_candidate_improvement |
| 16 | stay | fixed | adaptive_meta | -0.095000 | 0.200000 | no_candidate_improvement |
| 17 | stay | fixed | adaptive_meta | -0.095000 | 0.200000 | no_candidate_improvement |
| 18 | stay | fixed | adaptive_meta | -0.095000 | 0.200000 | no_candidate_improvement |
| 19 | stay | fixed | adaptive_meta | -0.095000 | 0.200000 | no_candidate_improvement |

_Showing first 20 of 101 decisions._

## Config Snapshot

```yaml
schema_version: '1.0'
experiment_name: stationary-seed-43
seed: 43
mode: adaptive
scenario:
  name: stationary
  episodes: 120
  steps_per_episode: 50
  reward_noise_std: 0.0
  drift_episode: null
  drift_start_episode: null
  drift_end_episode: null
  fallback_patience: null
  tags:
  - control
  - stable
  description: Stable reward regime without drift.
strategies:
- name: fixed
  parameters:
    exploration_rate: 0.1
  enabled: true
  compute_cost: 0.05
  description: null
- name: adaptive_meta
  parameters:
    evaluation_window: 20
    temperature: 0.8
  enabled: true
  compute_cost: 0.25
  description: null
meta_controller:
  window_size: 20
  min_samples: 10
  delta: 0.05
  lambda: 1.0
  switch_cost: 0.15
  utility_weights:
    compute_cost: 0.1
    reward_mean: 1.0
    reward_variance: 0.2
    switch_cost: 0.5
artifacts_root: E:\dipproj\artifacts\phase10_experimental_series\e1_stationary-control\seed_43
tags:
- phase1
- stationary
notes: Phase 1 baseline example.
```
