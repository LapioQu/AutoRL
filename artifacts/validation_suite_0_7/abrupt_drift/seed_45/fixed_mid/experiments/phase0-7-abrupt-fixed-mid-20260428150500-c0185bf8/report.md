# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | phase0-7-abrupt-fixed-mid-20260428150500-c0185bf8 |
| Experiment Name | phase0-7-abrupt-fixed_mid |
| Status | completed |
| Scenario | abrupt_drift |
| Seed | 45 |
| Config Hash | 8a61e9a4442317fe7b64c43f642381d95c5178b1655cb19d52ed6b94079a6c96 |
| Artifacts Path | `artifacts\validation_suite_0_7\abrupt_drift\seed_45\fixed_mid\experiments\phase0-7-abrupt-fixed-mid-20260428150500-c0185bf8` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 80 |
| Decisions | 0 |
| Switches | 0 |
| Fallback Decisions | 0 |
| Average Reward | 0.942103 |
| Success Rate | 1.000000 |
| Cumulative Reward | 75.368228 |
| Mean Window Variance | 0.001718 |
| Final Strategy | fixed_mid |

## Plot Artifacts

- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`

## Stay/Switch Summary

| Evaluation | Action | Current | Candidate | Margin | Threshold | Reason |
| --- | --- | --- | --- | ---: | ---: | --- |

## Config Snapshot

```yaml
schema_version: '1.0'
experiment_name: phase0-7-abrupt-fixed_mid
seed: 45
mode: baseline
scenario:
  name: abrupt_drift
  episodes: 80
  steps_per_episode: 20
  reward_noise_std: 0.0
  drift_episode: 40
  drift_start_episode: null
  drift_end_episode: null
  fallback_patience: null
  tags: []
  description: Phase 0-7 validation abrupt drift scenario.
strategies:
- name: fixed_mid
  parameters:
    fixed_action_index: 1
  enabled: true
  compute_cost: 0.05
  description: null
- name: fixed_low
  parameters:
    fixed_action_index: 0
  enabled: true
  compute_cost: 0.03
  description: null
- name: fixed_high
  parameters:
    fixed_action_index: 3
  enabled: true
  compute_cost: 0.07
  description: null
- name: adaptive_meta_final
  parameters:
    reward_weight: 0.2
    success_weight: 0.2
    fit_weight: 0.45
    recency_weight: 0.2
    cost_weight: 0.08
  enabled: true
  compute_cost: 0.12
  description: null
meta_controller:
  window_size: 8
  min_samples: 5
  delta: 0.01
  lambda: 0.3
  switch_cost: 0.01
  utility_weights:
    reward_mean: 1.0
    reward_variance: 0.15
    compute_cost: 0.08
    switch_cost: 0.2
artifacts_root: artifacts\validation_suite_0_7\abrupt_drift\seed_45\fixed_mid
tags:
- phase_validation
- abrupt_drift
notes: null
```
