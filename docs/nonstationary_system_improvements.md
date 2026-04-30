# Nonstationary System Improvements

This note records the concrete changes that improved the nonstationary replay system.

## What Was Improved

### 1. Strategy space

The stationary portfolio is no longer limited to a few SGD learning rates.

The replay stack now supports heterogeneous stationary strategies:

- linear / logistic SGD
- passive-aggressive learners
- adaptive Hoeffding trees
- Gaussian naive Bayes for classification

This matters because the controller cannot outperform a weak or redundant portfolio.

### 2. Portfolio generation

The system now includes a balanced portfolio selector over a broader candidate bank.

Key idea:

- choose deployed strategies from a larger warmup-evaluated set;
- use late-calibration performance rather than the full early prefix;
- add diversity via disagreement so the controller receives real challengers instead of near-duplicates.

### 3. Dataset access

The benchmark stack now has external loaders for:

- `Airlines` from the official MOA SourceForge archive
- `InsectsRecurring` from the official USP DS Repository archive

This removes the previous blocker where the most chaotic recurring-drift dataset was inaccessible because the River wrapper URL was broken.

## What Actually Helped

The evidence now supports three different lessons:

- on `Elec2` and `Bikes`, controller conservatism was a major bottleneck;
- on `WaterFlow`, the major bottleneck was portfolio construction;
- on `InsectsRecurring`, a richer portfolio plus the improved hard-switch controller already produces a meaningful adaptive win.

## Best Current Result

The strongest new result is on `InsectsRecurring`:

- `hard_switch_lcb = 0.787667`
- `best_fixed = 0.782283`
- delta = `+0.005383`
- switches = `4`

This is currently the clearest evidence that the nonstationary system can be practically better than the best fixed stationary strategy on a recurring-drift benchmark.

## Design Conclusion

The controller should not be treated as the only adaptive component.

The full system should be understood as:

1. candidate strategy generator
2. portfolio selector
3. nonstationary controller

Improving only step 3 is not enough when the deployed stationary set is weak, redundant, or badly calibrated.
