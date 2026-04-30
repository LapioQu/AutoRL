# Real-Stream Validation on Elec2

This document records the first real-stream replay validation run for the AutoRL metacontroller on a non-stationary dataset outside the synthetic phase 0-7 environment.

## Dataset

- dataset: `Elec2`
- task: binary classification
- stream order: temporal replay
- source description: New South Wales electricity market, where prices are affected by demand and supply and are set every five minutes
- artifact bundle: `artifacts/real_stream_validation/elec2`

The replay bundle in this repository was generated with:

```bash
python -m autorl benchmark-elec2 --artifacts-root artifacts/real_stream_validation/elec2
```

## Stationary Strategy Registry

The current real-stream replay uses three stationary online learners:

- `sgd_lr_0_1`: logistic regression with fixed SGD learning rate `0.1`
- `sgd_lr_0_5`: logistic regression with fixed SGD learning rate `0.5`
- `sgd_lr_1_0`: logistic regression with fixed SGD learning rate `1.0`

These are intentionally stationary baselines: their update rule and learning-rate policy do not change over time.

## Adaptive Replay Setup

- start strategy: `sgd_lr_1_0`
- evaluation interval: `128` samples
- window size: `256`
- min samples per decision: `3`
- utility weights:
  - reward mean: `1.0`
  - reward variance: `0.0`
  - compute cost: `0.0`
  - switch cost: `0.0`
- metacontroller parameters:
  - `delta = 0.002`
  - `switch_cost = 0.016`
  - `lambda = 0.0`

This setup keeps the replay focused on one question: whether the metacontroller can improve over fixed stationary strategies by switching between them when recent stream behavior changes.

## Observed Result

The generated artifact summary is:

- adaptive accuracy: `0.916159`
- best fixed strategy: `sgd_lr_0_5`
- best fixed accuracy: `0.916005`
- adaptive delta vs best fixed: `+0.000154`
- block delta CI95: `0.001199`
- switch count: `5`
- final strategy: `sgd_lr_0_5`

See:

- [summary.md](/E:/dipproj/artifacts/real_stream_validation/elec2/summary.md:1)
- [summary.json](/E:/dipproj/artifacts/real_stream_validation/elec2/summary.json:1)
- [decisions.csv](/E:/dipproj/artifacts/real_stream_validation/elec2/decisions.csv:1)

## Interpretation

- This is a real streaming replay, not a synthetic drift simulator.
- The adaptive system did not just execute; it made real `Stay/Switch` decisions and finished slightly above the best stationary baseline in aggregate accuracy.
- The gain is small, and the blockwise CI95 is larger than the mean delta, so this run alone should not be treated as a strong statistical win.
- The practical significance of this run is not the effect size by itself, but the fact that switching was both triggered and non-destructive on a real non-stationary stream.

## What This Does Prove

- the current metacontroller can be exercised on a real temporal stream;
- strategy switching can occur on real replay data, not only in the synthetic environment;
- in this Elec2 replay, the adaptive controller is slightly better than the best stationary baseline among the tested fixed strategies.

## What This Does Not Yet Prove

- it does not prove full T3 benchmark coverage;
- it does not yet cover additional real datasets such as gas-sensor drift, airlines, or regression streams;
- it does not replace the final phase 10 benchmark series with broader candidate registries, repeated seeds, and final reporting.
