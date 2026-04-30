# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | phase0-7-gradual-adaptive-20260428150827-ead5131e |
| Experiment Name | phase0-7-gradual-adaptive |
| Status | completed |
| Scenario | gradual_drift |
| Seed | 45 |
| Config Hash | bc865be5313bde66c71bbec63bad489ff851b52a571ddc6194058a69bbc0be09 |
| Artifacts Path | `artifacts\validation_suite_0_7\gradual_drift\seed_45\adaptive\experiments\phase0-7-gradual-adaptive-20260428150827-ead5131e` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 90 |
| Decisions | 83 |
| Switches | 2 |
| Fallback Decisions | 26 |
| Average Reward | 1.043192 |
| Success Rate | 1.000000 |
| Cumulative Reward | 93.887295 |
| Mean Window Variance | 0.001498 |
| Final Strategy | fixed_high |

## Plot Artifacts

- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`

## Stay/Switch Summary

| Evaluation | Action | Current | Candidate | Margin | Threshold | Reason |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | stay | fixed_low | fixed_mid | - | 0.020000 | insufficient_samples |
| 1 | stay | fixed_low | fixed_mid | - | 0.020000 | insufficient_samples |
| 2 | stay | fixed_low | fixed_mid | - | 0.020000 | insufficient_samples |
| 3 | stay | fixed_low | fixed_mid | - | 0.020000 | insufficient_samples |
| 4 | switch | fixed_low | fixed_mid | 0.058966 | 0.020000 | switch_advantage |
| 5 | stay | fixed_mid | adaptive_meta_final | -0.007826 | 0.020000 | no_candidate_improvement |
| 6 | stay | fixed_mid | adaptive_meta_final | -0.007619 | 0.020000 | no_candidate_improvement |
| 7 | stay | fixed_mid | adaptive_meta_final | -0.007602 | 0.020000 | no_candidate_improvement |
| 8 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 9 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 10 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 11 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 12 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 13 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 14 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 15 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 16 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 17 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 18 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 19 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |

_Showing first 20 of 83 decisions._

## Config Snapshot

```yaml
schema_version: '1.0'
experiment_name: phase0-7-gradual-adaptive
seed: 45
mode: adaptive
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
artifacts_root: artifacts\validation_suite_0_7\gradual_drift\seed_45\adaptive
tags:
- phase_validation
- gradual_drift
notes: null
```
