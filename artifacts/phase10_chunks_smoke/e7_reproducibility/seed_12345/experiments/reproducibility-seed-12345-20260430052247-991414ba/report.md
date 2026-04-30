# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | reproducibility-seed-12345-20260430052247-991414ba |
| Experiment Name | reproducibility-seed-12345 |
| Status | completed |
| Scenario | reproducibility |
| Seed | 12345 |
| Config Hash | da4d9136d82ad8cb52f3321aa7d6e1db00a29e26870fb19181cfc93d84d5db2e |
| Artifacts Path | `E:\dipproj\artifacts\phase10_chunks_smoke\e7_reproducibility\seed_12345\experiments\reproducibility-seed-12345-20260430052247-991414ba` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 80 |
| Decisions | 69 |
| Switches | 0 |
| Fallback Decisions | 5 |
| Average Reward | 0.987972 |
| Success Rate | 1.000000 |
| Cumulative Reward | 79.037749 |
| Mean Window Variance | 0.000027 |
| Final Strategy | fixed |

## Plot Artifacts

- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`

## Stay/Switch Summary

| Evaluation | Action | Current | Candidate | Margin | Threshold | Reason |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | stay | fixed | adaptive_meta | - | 0.100000 | insufficient_samples |
| 1 | stay | fixed | adaptive_meta | - | 0.100000 | insufficient_samples |
| 2 | stay | fixed | adaptive_meta | - | 0.100000 | insufficient_samples |
| 3 | stay | fixed | adaptive_meta | - | 0.100000 | insufficient_samples |
| 4 | stay | fixed | adaptive_meta | - | 0.100000 | insufficient_samples |
| 5 | stay | fixed | adaptive_meta | -0.053929 | 0.100000 | no_candidate_improvement |
| 6 | stay | fixed | adaptive_meta | -0.053028 | 0.100000 | no_candidate_improvement |
| 7 | stay | fixed | adaptive_meta | -0.053001 | 0.100000 | no_candidate_improvement |
| 8 | stay | fixed | adaptive_meta | -0.053000 | 0.100000 | no_candidate_improvement |
| 9 | stay | fixed | adaptive_meta | -0.053000 | 0.100000 | no_candidate_improvement |
| 10 | stay | fixed | adaptive_meta | -0.053000 | 0.100000 | no_candidate_improvement |
| 11 | stay | fixed | adaptive_meta | -0.053000 | 0.100000 | no_candidate_improvement |
| 12 | stay | fixed | adaptive_meta | -0.053000 | 0.100000 | no_candidate_improvement |
| 13 | stay | fixed | adaptive_meta | -0.053000 | 0.100000 | no_candidate_improvement |
| 14 | stay | fixed | adaptive_meta | -0.053000 | 0.100000 | no_candidate_improvement |
| 15 | stay | fixed | adaptive_meta | -0.053000 | 0.100000 | no_candidate_improvement |
| 16 | stay | fixed | adaptive_meta | -0.053000 | 0.100000 | no_candidate_improvement |
| 17 | stay | fixed | adaptive_meta | -0.053000 | 0.100000 | no_candidate_improvement |
| 18 | stay | fixed | adaptive_meta | -0.053000 | 0.100000 | no_candidate_improvement |
| 19 | stay | fixed | adaptive_meta | -0.053000 | 0.100000 | no_candidate_improvement |

_Showing first 20 of 69 decisions._

## Config Snapshot

```yaml
schema_version: '1.0'
experiment_name: reproducibility-seed-12345
seed: 12345
mode: adaptive
scenario:
  name: reproducibility
  episodes: 80
  steps_per_episode: 30
  reward_noise_std: 0.0
  drift_episode: null
  drift_start_episode: null
  drift_end_episode: null
  fallback_patience: null
  tags:
  - reproducibility
  - control
  description: Canonical seed-locked control configuration.
strategies:
- name: fixed
  parameters:
    exploration_rate: 0.05
  enabled: true
  compute_cost: 0.05
  description: null
- name: adaptive_meta
  parameters:
    evaluation_window: 12
    temperature: 0.85
  enabled: true
  compute_cost: 0.18
  description: null
meta_controller:
  window_size: 12
  min_samples: 6
  delta: 0.02
  lambda: 1.0
  switch_cost: 0.08
  utility_weights:
    compute_cost: 0.1
    reward_mean: 1.0
    reward_variance: 0.15
    switch_cost: 0.5
artifacts_root: E:\dipproj\artifacts\phase10_chunks_smoke\e7_reproducibility\seed_12345
tags:
- phase1
- reproducibility
notes: JSON example used for deterministic reload checks.
```
