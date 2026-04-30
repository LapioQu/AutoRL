# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | phase0-7-gradual-fixed-high-20260428150821-62e42b58 |
| Experiment Name | phase0-7-gradual-fixed_high |
| Status | completed |
| Scenario | gradual_drift |
| Seed | 44 |
| Config Hash | 70c50be8a923451076c7993a7207e50fc42bf7d224878915a4b9732d6a2770cd |
| Artifacts Path | `artifacts\validation_suite_0_7\gradual_drift\seed_44\fixed_high\experiments\phase0-7-gradual-fixed-high-20260428150821-62e42b58` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 90 |
| Decisions | 0 |
| Switches | 0 |
| Fallback Decisions | 0 |
| Average Reward | 0.718474 |
| Success Rate | 0.522222 |
| Cumulative Reward | 64.662616 |
| Mean Window Variance | 0.000571 |
| Final Strategy | fixed_high |

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
experiment_name: phase0-7-gradual-fixed_high
seed: 44
mode: baseline
scenario:
  name: gradual_drift
  episodes: 90
  steps_per_episode: 20
  reward_noise_std: 0.0
  drift_episode: null
  drift_start_episode: 25
  drift_end_episode: 65
  fallback_patience: null
  tags: []
  description: Phase 0-7 validation gradual drift scenario.
strategies:
- name: fixed_high
  parameters:
    fixed_action_index: 3
  enabled: true
  compute_cost: 0.07
  description: null
- name: fixed_low
  parameters:
    fixed_action_index: 0
  enabled: true
  compute_cost: 0.03
  description: null
- name: fixed_mid
  parameters:
    fixed_action_index: 1
  enabled: true
  compute_cost: 0.05
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
artifacts_root: artifacts\validation_suite_0_7\gradual_drift\seed_44\fixed_high
tags:
- phase_validation
- gradual_drift
notes: null
```
