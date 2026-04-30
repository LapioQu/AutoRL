# Environment Extension Guide

## Controlled Environment

The controlled system-validation environment lives in:
- `src/autorl/domain/environment.py`

Current built-in scenarios:
- `stationary`
- `abrupt_drift`
- `gradual_drift`
- `noisy_reward`
- `fallback`
- `reproducibility`

## Adding a New Controlled Scenario

1. Extend `ScenarioName` in `src/autorl/domain/models.py`.
2. Extend scenario validation in `ScenarioConfig`.
3. Implement regime logic in `AdaptiveLearningEnv`.
4. Add config examples in `configs/examples/`.
5. Add focused tests in `tests/test_environment.py`.

## Real-Stream Replay Datasets

Real-stream replay datasets are handled separately in:
- `src/autorl/application/benchmark_replay.py`

To add a new replay dataset:
1. Create a stream iterator or loader.
2. Build a `PredictionTrace` or `OutcomeTrace`.
3. Attach it to `BenchmarkReplayRunner`.
4. Add smoke coverage in `tests/test_benchmark_replay.py`.

This separation keeps the controlled RL-like environment extensible while preserving replay support for practical datasets.
