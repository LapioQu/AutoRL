# Phase 2: controlled adaptive environment

Phase 2 adds a seed-controlled RL-like environment with Gym-style `reset()` and `step()` methods, while still avoiding training orchestration and strategy execution logic from later phases.

## Implemented scope

- `AdaptiveLearningEnv` in `autorl.domain.environment`;
- typed observation and step payloads;
- scenario dynamics for `stationary`, `abrupt_drift`, `gradual_drift`, `noisy_reward`, `fallback`, and compatibility with `reproducibility`;
- seed-controlled rollouts through local `random.Random`;
- signals exposed via `info`: reward noise, success, learning progress, action quality, regime strength, and fallback trigger.

## Scenario behavior

- `stationary`: stable low regime strength;
- `abrupt_drift`: regime switches sharply at `drift_episode`;
- `gradual_drift`: regime strength interpolates between `drift_start_episode` and `drift_end_episode`;
- `noisy_reward`: same base regime plus Gaussian reward noise;
- `fallback`: low-quality regime with repeated-failure safeguard signal;
- `reproducibility`: deterministic zero-noise control scenario.

## Verification

The Phase 2 test suite verifies:

- identical seeded rollouts for the same config and action sequence;
- changed rollouts when the seed changes in noisy mode;
- reward drop for a fixed action across abrupt drift;
- monotonic regime progression in gradual drift;
- emitted reward noise in noisy mode;
- fallback safeguard activation after repeated failures.
