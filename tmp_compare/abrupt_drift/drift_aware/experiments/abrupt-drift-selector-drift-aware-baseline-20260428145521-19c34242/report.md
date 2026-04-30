# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | abrupt-drift-selector-drift-aware-baseline-20260428145521-19c34242 |
| Experiment Name | abrupt-drift-selector-drift_aware-baseline |
| Status | completed |
| Scenario | abrupt_drift |
| Seed | 52 |
| Config Hash | ec9f4013faec9cd0405f450fafa97648b3b98746d51d62dd6a068f29d9207feb |
| Artifacts Path | `tmp_compare\abrupt_drift\drift_aware\experiments\abrupt-drift-selector-drift-aware-baseline-20260428145521-19c34242` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 60 |
| Decisions | 0 |
| Switches | 0 |
| Fallback Decisions | 0 |
| Average Reward | 0.910369 |
| Success Rate | 1.000000 |
| Cumulative Reward | 54.622166 |
| Mean Window Variance | 0.000081 |
| Final Strategy | drift_aware |

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
experiment_name: abrupt-drift-selector-drift_aware-baseline
seed: 52
mode: baseline
scenario:
  name: abrupt_drift
  episodes: 60
  steps_per_episode: 20
  reward_noise_std: 0.0
  drift_episode: 30
  drift_start_episode: null
  drift_end_episode: null
  fallback_patience: null
  tags:
  - drift
  - abrupt
  description: Reward regime changes sharply at one episode boundary.
strategies:
- name: drift_aware
  parameters:
    detector_window: 15
    trigger_zscore: 2.5
  enabled: true
  compute_cost: 0.18
  description: null
meta_controller:
  window_size: 8
  min_samples: 5
  delta: 0.01
  lambda: 0.3
  switch_cost: 0.01
  utility_weights:
    reward_mean: 1.0
    reward_variance: 0.25
    compute_cost: 0.15
    switch_cost: 0.6
artifacts_root: tmp_compare\abrupt_drift\drift_aware
tags:
- phase1
- abrupt_drift
notes: null
```
