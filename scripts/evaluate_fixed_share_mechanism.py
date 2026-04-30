"""Reproduce the verified Fixed-Share mechanism comparison on key streams."""

from __future__ import annotations

import json
from pathlib import Path

from river import datasets

from autorl.application.benchmark_replay import (
    BenchmarkReplayRunner,
    ReplayStrategySpec,
    build_river_binary_prediction_trace,
    build_river_multiclass_prediction_trace,
    build_river_regression_outcome_trace,
    _default_feature_transform,
    _iter_insects_stream,
    _prediction_trace_to_outcome_trace,
    _subset_outcome_trace,
)


def _elec2_fixed_share(runner: BenchmarkReplayRunner, output_root: Path):
    trace = build_river_binary_prediction_trace(
        dataset_name="Elec2",
        stream=datasets.Elec2(),
        strategies=(
            ReplayStrategySpec("sgd_lr_0_1", 0.1, ""),
            ReplayStrategySpec("sgd_lr_0_5", 0.5, ""),
            ReplayStrategySpec("sgd_lr_1_0", 1.0, ""),
        ),
        source_description="Elec2",
        source_url=getattr(datasets.Elec2(), "url", ""),
    )
    return runner.run_outcome_trace_with_fixed_share(
        trace=_prediction_trace_to_outcome_trace(trace),
        output_root=output_root,
        evaluation_interval=128,
        start_strategy="sgd_lr_1_0",
        eta=0.35,
        share_alpha=0.02,
        switch_threshold=0.01,
        warmup_samples=128,
    )


def _bikes_fixed_share(runner: BenchmarkReplayRunner, output_root: Path):
    trace = build_river_regression_outcome_trace(
        dataset_name="Bikes",
        stream=datasets.Bikes(),
        strategies=(
            ReplayStrategySpec("sgd_lr_0_0001", 0.0001, ""),
            ReplayStrategySpec("sgd_lr_0_0005", 0.0005, ""),
            ReplayStrategySpec("sgd_lr_0_001", 0.001, ""),
        ),
        source_description="Bikes",
        source_url=getattr(datasets.Bikes(), "url", ""),
        feature_transform=_default_feature_transform,
        max_samples=40_000,
    )
    return runner.run_outcome_trace_with_fixed_share(
        trace=trace,
        output_root=output_root,
        evaluation_interval=128,
        start_strategy="sgd_lr_0_0005",
        eta=0.45,
        share_alpha=0.02,
        switch_threshold=0.01,
        warmup_samples=128,
    )


def _waterflow_fixed_share(runner: BenchmarkReplayRunner, output_root: Path):
    candidate_trace = build_river_regression_outcome_trace(
        dataset_name="WaterFlow",
        stream=datasets.WaterFlow(),
        strategies=(
            ReplayStrategySpec("lin_lr_0_0005", 0.0005, ""),
            ReplayStrategySpec("lin_lr_0_001", 0.001, ""),
            ReplayStrategySpec("lin_lr_0_002", 0.002, ""),
            ReplayStrategySpec("pa_regressor", 0.0, "", model_kind="pa_regressor"),
            ReplayStrategySpec("tree_regressor", 0.0, "", model_kind="hoeffding_tree_regressor"),
        ),
        source_description="WaterFlow",
        source_url=getattr(datasets.WaterFlow(), "url", ""),
        feature_transform=_default_feature_transform,
        max_samples=None,
    )
    selected = runner._select_balanced_portfolio(
        trace=candidate_trace,
        warmup_samples=240,
        block_size=24,
        max_strategies=3,
    )
    trace = _subset_outcome_trace(candidate_trace, selected)
    return runner.run_outcome_trace_with_fixed_share(
        trace=trace,
        output_root=output_root,
        evaluation_interval=24,
        start_strategy=selected[0],
        eta=0.45,
        share_alpha=0.03,
        switch_threshold=0.01,
        warmup_samples=48,
    )


def _insects_fixed_share(runner: BenchmarkReplayRunner, output_root: Path):
    prediction_trace = build_river_multiclass_prediction_trace(
        dataset_name="InsectsRecurring",
        stream=_iter_insects_stream(variant="incremental-reoccurring_balanced", max_samples=60_000),
        strategies=(
            ReplayStrategySpec("softmax_lr_0_01", 0.01, ""),
            ReplayStrategySpec("softmax_lr_0_1", 0.1, ""),
            ReplayStrategySpec("pa_classifier", 0.0, "", model_kind="pa_classifier"),
            ReplayStrategySpec("tree_classifier", 0.0, "", model_kind="hoeffding_tree_classifier"),
        ),
        source_description="InsectsRecurring",
        source_url="https://sites.google.com/view/uspdsrepository",
    )
    candidate_trace = _prediction_trace_to_outcome_trace(prediction_trace)
    selected = runner._select_balanced_portfolio(
        trace=candidate_trace,
        warmup_samples=12_000,
        block_size=256,
        max_strategies=3,
    )
    trace = _subset_outcome_trace(candidate_trace, selected)
    return runner.run_outcome_trace_with_fixed_share(
        trace=trace,
        output_root=output_root,
        evaluation_interval=256,
        start_strategy=selected[0],
        eta=0.4,
        share_alpha=0.02,
        switch_threshold=0.01,
        warmup_samples=512,
    )


def main() -> None:
    runner = BenchmarkReplayRunner()
    root = Path("artifacts/concept_mechanism_check").resolve()
    root.mkdir(parents=True, exist_ok=True)
    compare_root = root / "method_compare"
    fixed_root = root / "fixed_share"
    fixed_root.mkdir(parents=True, exist_ok=True)

    fixed_share_results = {
        "elec2": _elec2_fixed_share(runner, fixed_root / "elec2"),
        "bikes": _bikes_fixed_share(runner, fixed_root / "bikes"),
        "waterflow": _waterflow_fixed_share(runner, fixed_root / "waterflow"),
        "insects_recurring": _insects_fixed_share(runner, fixed_root / "insects_recurring"),
    }

    comparisons: list[dict[str, object]] = []
    for dataset_name in ("waterflow", "insects_recurring", "bikes", "elec2"):
        hard = runner.run_named_benchmark(dataset_name, output_root=compare_root / dataset_name / "hard")
        recent = runner.run_named_benchmark_with_recent_leader(dataset_name, output_root=compare_root / dataset_name / "recent")
        hedge = runner.run_named_benchmark_with_hedge(dataset_name, output_root=compare_root / dataset_name / "hedge")
        fixed = fixed_share_results[dataset_name]

        for mode, result in (
            ("hard", hard),
            ("recent", recent),
            ("hedge", hedge),
            ("fixed_share", fixed),
        ):
            comparisons.append(
                {
                    "dataset": dataset_name,
                    "mode": mode,
                    "adaptive_score": result.adaptive_score,
                    "best_fixed_score": result.best_fixed_score,
                    "delta_vs_best_fixed": result.delta_vs_best_fixed,
                    "switch_count": result.switch_count,
                    "summary_json_path": result.summary_json_path,
                }
            )

    output_path = root / "mechanism_comparison.json"
    output_path.write_text(json.dumps(comparisons, ensure_ascii=True, indent=2), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
