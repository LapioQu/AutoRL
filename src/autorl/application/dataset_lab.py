"""User-facing dataset upload and next-prediction workflow."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
from datetime import UTC, datetime
import hashlib
import io
import json
from pathlib import Path
import re
from statistics import fmean
from threading import Lock, Thread
import time
from typing import Any, Iterable
from uuid import uuid4

from autorl.application.benchmark_replay import (
    BenchmarkReplayRunner,
    OutcomeTrace,
    ReplayBenchmarkResult,
    ReplayStrategySpec,
    _subset_outcome_trace,
    _build_binary_classifier_model,
    _build_multiclass_classifier_model,
    _build_regressor_model,
    _default_feature_transform,
    _resolve_regression_scale,
)
from autorl.domain import MetaControllerConfig
from autorl.application.reporting import PngCanvas
from river import datasets


@dataclass(frozen=True, slots=True)
class BuiltinDatasetOption:
    """One curated dataset available directly inside Forecast Studio."""

    dataset_id: str
    label: str
    description: str
    task_type: str
    target_column: str
    order_column: str | None
    source_label: str


@dataclass(frozen=True, slots=True)
class BuiltinDatasetPayload:
    """Materialized built-in dataset rendered as CSV text."""

    dataset_id: str
    label: str
    description: str
    csv_text: str
    row_count: int
    task_type: str
    target_column: str
    order_column: str | None
    source_label: str


@dataclass(frozen=True, slots=True)
class ManualRowInterpretation:
    """Schema-aligned manual rows ready to append to a CSV stream."""

    normalized_rows_csv: str
    preview_rows: tuple[dict[str, Any], ...]
    appended_row_count: int
    blank_target_row_count: int
    notes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class _ReplayPreset:
    """Dataset-specific replay tuning reused from the benchmark layer."""

    strategy_specs: tuple[ReplayStrategySpec, ...]
    evaluation_interval: int
    start_strategy: str | None = None
    balance_warmup_samples: int | None = None
    balance_block_size: int | None = None
    balance_max_strategies: int | None = None
    recent_leader_lookback_blocks: int = 3
    recent_leader_margin: float = 0.001
    recent_leader_warmup_blocks: int = 2
    recent_leader_cooldown_blocks: int = 1
    recent_leader_incumbent_floor: float = 0.001
    hard_window_size: int = 4
    hard_min_samples: int = 2
    hard_delta: float = 0.001
    hard_lambda_value: float = 0.0
    hard_switch_cost: float = 0.0
    use_target_lags: bool = True
    calibration_fraction: float = 0.25
    calibration_min_samples: int = 96
    calibration_min_blocks: int = 4


@dataclass(frozen=True, slots=True)
class DatasetLabResult:
    """One uploaded-dataset adaptive replay result."""

    dataset_name: str
    task_type: str
    target_column: str
    source_row_count: int
    source_rows_used: int
    sample_count: int
    feature_count: int
    score_name: str
    policy_name: str
    adaptive_score: float
    best_fixed_strategy: str
    best_fixed_score: float
    delta_vs_best_fixed: float
    oracle_score: float
    oracle_gain: float
    oracle_capture_ratio: float
    prediction_mode: str
    final_strategy: str
    switch_count: int
    next_prediction: str
    prediction_confidence: float
    confidence_label: str
    next_prediction_by_strategy: dict[str, str]
    forecast_row_preview: dict[str, Any]
    artifact_root: str
    input_manifest_path: str
    summary_json_path: str
    report_md_path: str
    decision_csv_path: str
    score_plot_path: str
    portfolio_plot_path: str
    switch_plot_path: str
    preview_rows: tuple[dict[str, Any], ...]
    interpretation: tuple[str, ...]
    caveats: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DatasetLabJobStatus:
    """Persisted background analysis job status."""

    job_id: str
    dataset_name: str
    source_kind: str
    status: str
    phase: str
    progress: float
    created_at_utc: str
    updated_at_utc: str
    artifacts_root: str
    artifact_root: str
    summary_json_path: str
    report_md_path: str
    error_message: str | None = None
    source_row_count: int = 0
    source_rows_used: int = 0
    sample_count: int = 0
    adaptive_score: float | None = None
    best_fixed_score: float | None = None
    delta_vs_best_fixed: float | None = None
    oracle_capture_ratio: float | None = None
    switch_count: int = 0
    final_strategy: str = ""
    policy_name: str = ""
    telemetry_path: str = ""
    sample_index: int = 0
    total_samples: int = 0
    evaluation_index: int = 0
    active_strategy: str = ""
    candidate_strategy: str = ""
    adaptive_score_so_far: float | None = None
    best_fixed_score_so_far: float | None = None
    delta_so_far: float | None = None
    oracle_capture_so_far: float | None = None
    background_running: bool = False


@dataclass(frozen=True, slots=True)
class _PreparedDataset:
    dataset_name: str
    task_type: str
    target_column: str
    source_row_count: int
    source_rows_used: int
    feature_count: int
    sample_count: int
    examples: tuple[tuple[dict[str, Any], Any], ...]
    next_features: dict[str, Any]
    raw_target_tail: tuple[Any, ...]
    prediction_mode: str
    forecast_row_preview: dict[str, Any]


class DatasetLabService:
    """Analyze uploaded CSV data as a temporal stream with adaptive strategy selection."""

    def __init__(self, *, default_artifacts_root: str | Path = "artifacts") -> None:
        self._default_artifacts_root = Path(default_artifacts_root)
        self._runner = BenchmarkReplayRunner()
        self._builtin_cache: dict[tuple[str, int], BuiltinDatasetPayload] = {}
        self._builtin_count_cache: dict[str, int] = {}

    def analyze_csv(
        self,
        *,
        dataset_name: str,
        csv_text: str,
        target_column: str,
        task_type: str = "auto",
        order_column: str | None = None,
        lag_count: int = 3,
        policy_name: str = "recent_leader_meta",
        dataset_profile: str | None = None,
        artifacts_root: str | Path | None = None,
        max_rows: int = 4000,
        artifact_root_override: str | Path | None = None,
        progress_callback: Any | None = None,
    ) -> DatasetLabResult:
        """Run adaptive streaming analysis on one uploaded CSV dataset."""
        if not csv_text.strip():
            raise ValueError("dataset text is empty")
        if lag_count <= 0:
            raise ValueError("lag_count must be positive")

        _emit_progress(progress_callback, phase="preparing_dataset", progress=0.08, dataset_name=dataset_name)
        preset_hint = _resolve_replay_preset(
            dataset_profile=dataset_profile,
            task_type=task_type if task_type != "auto" else "",
        )
        prepared = self._prepare_dataset(
            dataset_name=dataset_name,
            csv_text=csv_text,
            target_column=target_column,
            requested_task_type=task_type,
            order_column=order_column,
            lag_count=lag_count,
            max_rows=max_rows,
            use_target_lags=preset_hint.use_target_lags if preset_hint is not None else None,
        )
        _emit_progress(
            progress_callback,
            phase="dataset_prepared",
            progress=0.2,
            dataset_name=prepared.dataset_name,
            source_row_count=prepared.source_row_count,
            source_rows_used=prepared.source_rows_used,
            sample_count=prepared.sample_count,
        )
        artifact_root = Path(artifact_root_override) if artifact_root_override is not None else self._artifact_root(artifacts_root, prepared.dataset_name)
        artifact_root.mkdir(parents=True, exist_ok=True)
        input_manifest_path = artifact_root / "input_manifest.json"
        input_manifest_payload = {
            "dataset_name": prepared.dataset_name,
            "task_type": prepared.task_type,
            "target_column": prepared.target_column,
            "source_row_count": prepared.source_row_count,
            "source_rows_used": prepared.source_rows_used,
            "sample_count": prepared.sample_count,
            "feature_count": prepared.feature_count,
            "input_sha256": hashlib.sha256(csv_text.encode("utf-8")).hexdigest(),
            "raw_input_persisted": False,
            "column_names": sorted({*prepared.next_features.keys(), prepared.target_column}),
        }
        input_manifest_path.write_text(json.dumps(input_manifest_payload, ensure_ascii=True, indent=2), encoding="utf-8")
        preset = _resolve_replay_preset(dataset_profile=dataset_profile, task_type=prepared.task_type)

        _emit_progress(progress_callback, phase="building_strategy_trace", progress=0.35, dataset_name=prepared.dataset_name)
        if prepared.task_type == "classification":
            strategy_specs = preset.strategy_specs if preset is not None else _classification_strategies()
            trace, predictions_by_strategy, next_prediction_by_strategy = _build_classification_trace_bundle(
                dataset_name=prepared.dataset_name,
                samples=prepared.examples,
                next_features=prepared.next_features,
                strategies=strategy_specs,
                progress_callback=progress_callback,
            )
        else:
            strategy_specs = preset.strategy_specs if preset is not None else _regression_strategies()
            trace, predictions_by_strategy, next_prediction_by_strategy = _build_regression_trace_bundle(
                dataset_name=prepared.dataset_name,
                samples=prepared.examples,
                next_features=prepared.next_features,
                strategies=strategy_specs,
                progress_callback=progress_callback,
            )

        if _can_balance_portfolio(trace=trace, preset=preset):
            selected_names = self._runner._select_balanced_portfolio(
                trace=trace,
                warmup_samples=min(preset.balance_warmup_samples, len(next(iter(trace.rewards_by_strategy.values()), ()))),
                block_size=preset.balance_block_size,
                max_strategies=preset.balance_max_strategies,
            )
            trace = _subset_outcome_trace(trace, selected_names)
            predictions_by_strategy = {name: predictions_by_strategy[name] for name in selected_names if name in predictions_by_strategy}
            next_prediction_by_strategy = {name: next_prediction_by_strategy[name] for name in selected_names if name in next_prediction_by_strategy}
            strategy_specs = tuple(spec for spec in strategy_specs if spec.name in selected_names)

        start_strategy = _resolve_start_strategy(trace=trace, strategy_specs=strategy_specs, preset=preset)
        _emit_progress(progress_callback, phase="running_adaptive_replay", progress=0.6, dataset_name=prepared.dataset_name)
        replay_result = self._run_policy(
            trace=trace,
            policy_name=policy_name,
            output_root=artifact_root,
            start_strategy=start_strategy,
            preset=preset,
            progress_callback=progress_callback,
        )

        adaptive_next_prediction = next_prediction_by_strategy.get(replay_result.final_strategy)
        if adaptive_next_prediction is None:
            adaptive_next_prediction = next_prediction_by_strategy.get(replay_result.best_fixed_strategy, "n/a")
        prediction_confidence = _prediction_confidence(
            task_type=prepared.task_type,
            next_prediction=adaptive_next_prediction,
            next_prediction_by_strategy=next_prediction_by_strategy,
        )
        confidence_label = _confidence_label(prediction_confidence)
        oracle_score, oracle_gain, oracle_capture_ratio = _oracle_summary(
            trace=trace,
            adaptive_score=replay_result.adaptive_score,
            best_fixed_score=replay_result.best_fixed_score,
        )

        preview_rows = _build_preview_rows(
            samples=prepared.examples,
            predictions_by_strategy=predictions_by_strategy,
            final_strategy=replay_result.final_strategy,
            limit=12,
        )
        interpretation = _build_interpretation(
            result=replay_result,
            oracle_score=oracle_score,
            oracle_gain=oracle_gain,
            oracle_capture_ratio=oracle_capture_ratio,
            task_type=prepared.task_type,
            prediction_mode=prepared.prediction_mode,
            next_prediction=adaptive_next_prediction,
            raw_target_tail=prepared.raw_target_tail,
        )
        caveats = _build_caveats(
            task_type=prepared.task_type,
            order_column=order_column,
            lag_count=lag_count,
        )
        _emit_progress(progress_callback, phase="building_report", progress=0.86, dataset_name=prepared.dataset_name)

        created_at_utc = datetime.now(tz=UTC).isoformat()
        lab_summary_path = artifact_root / "dataset_lab_summary.json"
        plot_paths = self._build_visual_artifacts(
            artifact_root=artifact_root,
            fixed_scores=replay_result.fixed_scores,
            adaptive_score=replay_result.adaptive_score,
            best_fixed_score=replay_result.best_fixed_score,
            oracle_score=oracle_score,
            next_prediction_by_strategy={name: str(value) for name, value in next_prediction_by_strategy.items()},
            decision_csv_path=Path(replay_result.decision_csv_path),
        )
        payload = {
            "created_at_utc": created_at_utc,
            "dataset_name": prepared.dataset_name,
            "task_type": prepared.task_type,
            "target_column": prepared.target_column,
            "source_row_count": prepared.source_row_count,
            "source_rows_used": prepared.source_rows_used,
            "sample_count": prepared.sample_count,
            "feature_count": prepared.feature_count,
            "score_name": replay_result.score_name,
            "policy_name": replay_result.policy_name,
            "adaptive_score": replay_result.adaptive_score,
            "best_fixed_strategy": replay_result.best_fixed_strategy,
            "best_fixed_score": replay_result.best_fixed_score,
            "delta_vs_best_fixed": replay_result.delta_vs_best_fixed,
            "oracle_score": oracle_score,
            "oracle_gain": oracle_gain,
            "oracle_capture_ratio": oracle_capture_ratio,
            "prediction_mode": prepared.prediction_mode,
            "final_strategy": replay_result.final_strategy,
            "switch_count": replay_result.switch_count,
            "next_prediction": str(adaptive_next_prediction),
            "prediction_confidence": prediction_confidence,
            "confidence_label": confidence_label,
            "next_prediction_by_strategy": {name: str(value) for name, value in next_prediction_by_strategy.items()},
            "interpretation": list(interpretation),
            "caveats": list(caveats),
            "artifact_root": str(artifact_root),
            "input_manifest_path": str(input_manifest_path),
            "raw_input_persisted": False,
            "replay_summary_json_path": replay_result.summary_json_path,
            "decision_csv_path": replay_result.decision_csv_path,
            "report_md_path": replay_result.report_md_path,
            "score_plot_path": str(plot_paths["score_plot_path"]),
            "portfolio_plot_path": str(plot_paths["portfolio_plot_path"]),
            "switch_plot_path": str(plot_paths["switch_plot_path"]),
        }
        lab_summary_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        detailed_report_path = artifact_root / "dataset_lab_report.md"
        detailed_report_path.write_text(_build_dataset_lab_report(payload), encoding="utf-8")
        payload["dataset_lab_report_md_path"] = str(detailed_report_path)
        lab_summary_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        self._append_history_entry(artifacts_root=artifacts_root, entry=_build_history_entry(payload))

        return DatasetLabResult(
            dataset_name=prepared.dataset_name,
            task_type=prepared.task_type,
            target_column=prepared.target_column,
            source_row_count=prepared.source_row_count,
            source_rows_used=prepared.source_rows_used,
            sample_count=prepared.sample_count,
            feature_count=prepared.feature_count,
            score_name=replay_result.score_name,
            policy_name=replay_result.policy_name,
            adaptive_score=replay_result.adaptive_score,
            best_fixed_strategy=replay_result.best_fixed_strategy,
            best_fixed_score=replay_result.best_fixed_score,
            delta_vs_best_fixed=replay_result.delta_vs_best_fixed,
            oracle_score=oracle_score,
            oracle_gain=oracle_gain,
            oracle_capture_ratio=oracle_capture_ratio,
            prediction_mode=prepared.prediction_mode,
            final_strategy=replay_result.final_strategy,
            switch_count=replay_result.switch_count,
            next_prediction=str(adaptive_next_prediction),
            prediction_confidence=prediction_confidence,
            confidence_label=confidence_label,
            next_prediction_by_strategy={name: str(value) for name, value in next_prediction_by_strategy.items()},
            forecast_row_preview=prepared.forecast_row_preview,
            artifact_root=str(artifact_root),
            input_manifest_path=str(input_manifest_path),
            summary_json_path=str(lab_summary_path),
            report_md_path=str(detailed_report_path),
            decision_csv_path=replay_result.decision_csv_path,
            score_plot_path=str(plot_paths["score_plot_path"]),
            portfolio_plot_path=str(plot_paths["portfolio_plot_path"]),
            switch_plot_path=str(plot_paths["switch_plot_path"]),
            preview_rows=preview_rows,
            interpretation=interpretation,
            caveats=caveats,
        )

    def analyze_builtin_dataset(
        self,
        *,
        dataset_id: str,
        row_count: int,
        policy_name: str = "recent_leader_meta",
        artifacts_root: str | Path | None = None,
        artifact_root_override: str | Path | None = None,
        progress_callback: Any | None = None,
    ) -> DatasetLabResult:
        """Analyze one curated built-in dataset without degrading native feature types through CSV parsing."""
        option = next((item for item in _builtin_dataset_options() if item.dataset_id == dataset_id), None)
        if option is None:
            raise ValueError(f"unknown built-in dataset: {dataset_id!r}")
        if row_count <= 0:
            raise ValueError("row_count must be positive")
        builtin_payload = self.load_builtin_dataset_csv(dataset_id, max_rows=row_count)
        return self.analyze_csv(
            dataset_name=builtin_payload.label,
            csv_text=builtin_payload.csv_text,
            target_column=builtin_payload.target_column,
            task_type=builtin_payload.task_type,
            order_column=builtin_payload.order_column,
            lag_count=3,
            policy_name=policy_name,
            artifacts_root=artifacts_root,
            max_rows=row_count,
            artifact_root_override=artifact_root_override,
            progress_callback=progress_callback,
        )
        _emit_progress(progress_callback, phase="loading_builtin_dataset", progress=0.08, dataset_name=option.label)
        total_builtin_rows = self.builtin_dataset_row_count(dataset_id)

        preset = _resolve_replay_preset(dataset_profile=dataset_id, task_type=option.task_type)
        stream_rows = _load_builtin_dataset_rows(dataset_id=dataset_id, max_rows=row_count)
        if len(stream_rows) < 5:
            raise ValueError("built-in dataset slice is too short for replay")

        examples = tuple((dict(features), target) for features, target in stream_rows)
        next_features = dict(stream_rows[-1][0])
        raw_target_tail = tuple(target for _, target in stream_rows[-3:])
        _emit_progress(
            progress_callback,
            phase="dataset_prepared",
            progress=0.2,
            dataset_name=option.label,
            source_row_count=total_builtin_rows,
            source_rows_used=len(stream_rows),
            sample_count=len(examples),
        )
        artifact_root = Path(artifact_root_override) if artifact_root_override is not None else self._artifact_root(artifacts_root, option.label)
        artifact_root.mkdir(parents=True, exist_ok=True)

        strategy_specs = preset.strategy_specs if preset is not None else (
            _classification_strategies() if option.task_type == "classification" else _regression_strategies()
        )
        _emit_progress(progress_callback, phase="building_strategy_trace", progress=0.35, dataset_name=option.label)
        if option.task_type == "classification":
            trace, predictions_by_strategy, next_prediction_by_strategy = _build_classification_trace_bundle(
                dataset_name=option.label,
                samples=examples,
                next_features=next_features,
                strategies=strategy_specs,
                progress_callback=progress_callback,
            )
        else:
            trace, predictions_by_strategy, next_prediction_by_strategy = _build_regression_trace_bundle(
                dataset_name=option.label,
                samples=examples,
                next_features=next_features,
                strategies=strategy_specs,
                progress_callback=progress_callback,
            )

        if _can_balance_portfolio(trace=trace, preset=preset):
            selected_names = self._runner._select_balanced_portfolio(
                trace=trace,
                warmup_samples=min(preset.balance_warmup_samples, len(next(iter(trace.rewards_by_strategy.values()), ()))),
                block_size=preset.balance_block_size,
                max_strategies=preset.balance_max_strategies,
            )
            trace = _subset_outcome_trace(trace, selected_names)
            predictions_by_strategy = {name: predictions_by_strategy[name] for name in selected_names if name in predictions_by_strategy}
            next_prediction_by_strategy = {name: next_prediction_by_strategy[name] for name in selected_names if name in next_prediction_by_strategy}
            strategy_specs = tuple(spec for spec in strategy_specs if spec.name in selected_names)

        start_strategy = _resolve_start_strategy(trace=trace, strategy_specs=tuple(strategy_specs), preset=preset)
        _emit_progress(progress_callback, phase="running_adaptive_replay", progress=0.6, dataset_name=option.label)
        replay_result = self._run_policy(
            trace=trace,
            policy_name=policy_name,
            output_root=artifact_root,
            start_strategy=start_strategy,
            preset=preset,
            progress_callback=progress_callback,
        )

        adaptive_next_prediction = next_prediction_by_strategy.get(replay_result.final_strategy)
        if adaptive_next_prediction is None:
            adaptive_next_prediction = next_prediction_by_strategy.get(replay_result.best_fixed_strategy, "n/a")
        prediction_confidence = _prediction_confidence(
            task_type=option.task_type,
            next_prediction=adaptive_next_prediction,
            next_prediction_by_strategy=next_prediction_by_strategy,
        )
        confidence_label = _confidence_label(prediction_confidence)
        oracle_score, oracle_gain, oracle_capture_ratio = _oracle_summary(
            trace=trace,
            adaptive_score=replay_result.adaptive_score,
            best_fixed_score=replay_result.best_fixed_score,
        )

        preview_rows = _build_preview_rows(
            samples=examples,
            predictions_by_strategy=predictions_by_strategy,
            final_strategy=replay_result.final_strategy,
            limit=12,
        )
        interpretation = _build_interpretation(
            result=replay_result,
            oracle_score=oracle_score,
            oracle_gain=oracle_gain,
            oracle_capture_ratio=oracle_capture_ratio,
            task_type=option.task_type,
            prediction_mode="next_step",
            next_prediction=adaptive_next_prediction,
            raw_target_tail=raw_target_tail,
        )
        caveats = (
            "Для цього готового датасету використано нативний потоковий профіль без CSV-перетворення ознак.",
        ) + _build_caveats(task_type=option.task_type, order_column=option.order_column, lag_count=3)
        _emit_progress(progress_callback, phase="building_report", progress=0.86, dataset_name=option.label)

        created_at_utc = datetime.now(tz=UTC).isoformat()
        lab_summary_path = artifact_root / "dataset_lab_summary.json"
        plot_paths = self._build_visual_artifacts(
            artifact_root=artifact_root,
            fixed_scores=replay_result.fixed_scores,
            adaptive_score=replay_result.adaptive_score,
            best_fixed_score=replay_result.best_fixed_score,
            oracle_score=oracle_score,
            next_prediction_by_strategy={name: str(value) for name, value in next_prediction_by_strategy.items()},
            decision_csv_path=Path(replay_result.decision_csv_path),
        )
        payload = {
            "created_at_utc": created_at_utc,
            "dataset_name": option.label,
            "task_type": option.task_type,
            "target_column": option.target_column,
            "source_row_count": total_builtin_rows,
            "source_rows_used": len(stream_rows),
            "sample_count": len(examples),
            "feature_count": len(examples[0][0]),
            "score_name": replay_result.score_name,
            "policy_name": replay_result.policy_name,
            "adaptive_score": replay_result.adaptive_score,
            "best_fixed_strategy": replay_result.best_fixed_strategy,
            "best_fixed_score": replay_result.best_fixed_score,
            "delta_vs_best_fixed": replay_result.delta_vs_best_fixed,
            "oracle_score": oracle_score,
            "oracle_gain": oracle_gain,
            "oracle_capture_ratio": oracle_capture_ratio,
            "prediction_mode": "next_step",
            "final_strategy": replay_result.final_strategy,
            "switch_count": replay_result.switch_count,
            "next_prediction": str(adaptive_next_prediction),
            "prediction_confidence": prediction_confidence,
            "confidence_label": confidence_label,
            "next_prediction_by_strategy": {name: str(value) for name, value in next_prediction_by_strategy.items()},
            "forecast_row_preview": {key: _serialize_csv_value(value) for key, value in next_features.items()},
            "preview_rows": list(preview_rows),
            "interpretation": list(interpretation),
            "caveats": list(caveats),
            "artifact_root": str(artifact_root),
            "replay_summary_json_path": replay_result.summary_json_path,
            "decision_csv_path": replay_result.decision_csv_path,
            "report_md_path": replay_result.report_md_path,
            "score_plot_path": str(plot_paths["score_plot_path"]),
            "portfolio_plot_path": str(plot_paths["portfolio_plot_path"]),
            "switch_plot_path": str(plot_paths["switch_plot_path"]),
        }
        lab_summary_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        detailed_report_path = artifact_root / "dataset_lab_report.md"
        detailed_report_path.write_text(_build_dataset_lab_report(payload), encoding="utf-8")
        payload["dataset_lab_report_md_path"] = str(detailed_report_path)
        lab_summary_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        self._append_history_entry(artifacts_root=artifacts_root, entry=_build_history_entry(payload))

        return DatasetLabResult(
            dataset_name=option.label,
            task_type=option.task_type,
            target_column=option.target_column,
            source_row_count=total_builtin_rows,
            source_rows_used=len(stream_rows),
            sample_count=len(examples),
            feature_count=len(examples[0][0]),
            score_name=replay_result.score_name,
            policy_name=replay_result.policy_name,
            adaptive_score=replay_result.adaptive_score,
            best_fixed_strategy=replay_result.best_fixed_strategy,
            best_fixed_score=replay_result.best_fixed_score,
            delta_vs_best_fixed=replay_result.delta_vs_best_fixed,
            oracle_score=oracle_score,
            oracle_gain=oracle_gain,
            oracle_capture_ratio=oracle_capture_ratio,
            prediction_mode="next_step",
            final_strategy=replay_result.final_strategy,
            switch_count=replay_result.switch_count,
            next_prediction=str(adaptive_next_prediction),
            prediction_confidence=prediction_confidence,
            confidence_label=confidence_label,
            next_prediction_by_strategy={name: str(value) for name, value in next_prediction_by_strategy.items()},
            forecast_row_preview={key: _serialize_csv_value(value) for key, value in next_features.items()},
            artifact_root=str(artifact_root),
            input_manifest_path="builtin-native-stream",
            summary_json_path=str(lab_summary_path),
            report_md_path=str(detailed_report_path),
            decision_csv_path=replay_result.decision_csv_path,
            score_plot_path=str(plot_paths["score_plot_path"]),
            portfolio_plot_path=str(plot_paths["portfolio_plot_path"]),
            switch_plot_path=str(plot_paths["switch_plot_path"]),
            preview_rows=preview_rows,
            interpretation=interpretation,
            caveats=caveats,
        )

    def peek_csv_schema(self, csv_text: str) -> dict[str, Any]:
        """Inspect CSV headers and approximate row count without running replay."""
        reader = csv.DictReader(io.StringIO(csv_text))
        if reader.fieldnames is None:
            raise ValueError("CSV must include a header row")
        row_count = sum(1 for row in reader if any((value or "").strip() for value in row.values()))
        return {"columns": list(reader.fieldnames), "row_count": row_count}

    def available_policy_names(self) -> tuple[str, ...]:
        """Return supported adaptive policies for uploaded datasets."""
        return ("auto_meta", "recent_leader_meta", "hard_switch_lcb", "fixed_share_portfolio")

    def available_builtin_datasets(self) -> tuple[BuiltinDatasetOption, ...]:
        """Return curated built-in streaming datasets for one-click evaluation."""
        return _builtin_dataset_options()

    def builtin_dataset_row_count(self, dataset_id: str) -> int:
        """Return the full available row count for one built-in dataset."""
        normalized = dataset_id.strip().lower()
        cached = self._builtin_count_cache.get(normalized)
        if cached is not None:
            return cached
        row_count = _count_builtin_dataset_rows(dataset_id=normalized)
        self._builtin_count_cache[normalized] = row_count
        return row_count

    def list_dataset_lab_analyses(
        self,
        *,
        artifacts_root: str | Path | None = None,
        limit: int = 20,
    ) -> tuple[dict[str, Any], ...]:
        """Return the most recent persisted dataset-lab analyses."""
        if limit <= 0:
            return ()
        history_path = self._history_index_path(artifacts_root)
        if not history_path.exists():
            return ()
        try:
            payload = json.loads(history_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return ()
        if not isinstance(payload, list):
            return ()
        rows = [row for row in payload if isinstance(row, dict)]
        rows.sort(key=lambda row: str(row.get("created_at_utc", "")), reverse=True)
        return tuple(rows[:limit])

    def load_result_from_summary(self, summary_json_path: str | Path) -> DatasetLabResult:
        """Load one persisted dataset-lab result back into a typed object."""
        payload = json.loads(Path(summary_json_path).read_text(encoding="utf-8"))
        return DatasetLabResult(
            dataset_name=str(payload.get("dataset_name", "")),
            task_type=str(payload.get("task_type", "")),
            target_column=str(payload.get("target_column", "")),
            source_row_count=int(payload.get("source_row_count", 0)),
            source_rows_used=int(payload.get("source_rows_used", 0)),
            sample_count=int(payload.get("sample_count", 0)),
            feature_count=int(payload.get("feature_count", 0)),
            score_name=str(payload.get("score_name", "")),
            policy_name=str(payload.get("policy_name", "")),
            adaptive_score=float(payload.get("adaptive_score", 0.0)),
            best_fixed_strategy=str(payload.get("best_fixed_strategy", "")),
            best_fixed_score=float(payload.get("best_fixed_score", 0.0)),
            delta_vs_best_fixed=float(payload.get("delta_vs_best_fixed", 0.0)),
            oracle_score=float(payload.get("oracle_score", 0.0)),
            oracle_gain=float(payload.get("oracle_gain", 0.0)),
            oracle_capture_ratio=float(payload.get("oracle_capture_ratio", 0.0)),
            prediction_mode=str(payload.get("prediction_mode", "")),
            final_strategy=str(payload.get("final_strategy", "")),
            switch_count=int(payload.get("switch_count", 0)),
            next_prediction=str(payload.get("next_prediction", "")),
            prediction_confidence=float(payload.get("prediction_confidence", 0.0)),
            confidence_label=str(payload.get("confidence_label", "")),
            next_prediction_by_strategy={str(key): str(value) for key, value in dict(payload.get("next_prediction_by_strategy", {})).items()},
            forecast_row_preview={},
            artifact_root=str(payload.get("artifact_root", "")),
            input_manifest_path=str(payload.get("input_manifest_path", "")),
            summary_json_path=str(summary_json_path),
            report_md_path=str(payload.get("dataset_lab_report_md_path", payload.get("report_md_path", ""))),
            decision_csv_path=str(payload.get("decision_csv_path", "")),
            score_plot_path=str(payload.get("score_plot_path", "")),
            portfolio_plot_path=str(payload.get("portfolio_plot_path", "")),
            switch_plot_path=str(payload.get("switch_plot_path", "")),
            preview_rows=(),
            interpretation=tuple(str(item) for item in list(payload.get("interpretation", []))),
            caveats=tuple(str(item) for item in list(payload.get("caveats", []))),
        )

    def load_builtin_dataset_csv(self, dataset_id: str, *, max_rows: int = 512) -> BuiltinDatasetPayload:
        """Materialize one curated built-in dataset as CSV text."""
        if max_rows <= 0:
            raise ValueError("max_rows must be positive")
        normalized = dataset_id.strip().lower()
        cache_key = (normalized, max_rows)
        cached = self._builtin_cache.get(cache_key)
        if cached is not None:
            return cached

        option = next((item for item in _builtin_dataset_options() if item.dataset_id == normalized), None)
        if option is None:
            raise ValueError(f"unknown built-in dataset: {dataset_id!r}")

        csv_text, row_count = _load_builtin_dataset_csv(option=option, max_rows=max_rows)
        payload = BuiltinDatasetPayload(
            dataset_id=option.dataset_id,
            label=option.label,
            description=option.description,
            csv_text=csv_text,
            row_count=row_count,
            task_type=option.task_type,
            target_column=option.target_column,
            order_column=option.order_column,
            source_label=option.source_label,
        )
        self._builtin_cache[cache_key] = payload
        return payload

    def interpret_manual_rows(
        self,
        *,
        base_csv_text: str,
        manual_text: str,
        target_column: str,
    ) -> ManualRowInterpretation:
        """Convert manual free-text rows into the active CSV schema."""
        schema = self.peek_csv_schema(base_csv_text)
        columns = tuple(schema["columns"])
        if target_column not in columns:
            raise ValueError(f"target column not found: {target_column!r}")
        rows = _parse_manual_rows(
            columns=columns,
            manual_text=manual_text,
            target_column=target_column,
        )
        csv_rows_text = _rows_to_csv_fragment(columns=columns, rows=rows)
        blank_target_row_count = sum(1 for row in rows if str(row.get(target_column, "")).strip() == "")
        notes = [
            "Each interpreted row is aligned to the current CSV schema and can be appended directly to the active stream.",
        ]
        if blank_target_row_count:
            notes.append("Rows with a blank target will be treated as forecast rows: the system will predict that missing target.")
        if any(any(str(row.get(column, "")).strip() == "" for column in columns if column != target_column) for row in rows):
            notes.append("Missing feature fields were left blank; the replay will reuse the latest available context where possible.")
        return ManualRowInterpretation(
            normalized_rows_csv=csv_rows_text,
            preview_rows=tuple(rows),
            appended_row_count=len(rows),
            blank_target_row_count=blank_target_row_count,
            notes=tuple(notes),
        )

    def append_manual_rows(self, *, base_csv_text: str, normalized_rows_csv: str) -> str:
        """Append normalized row fragments to a CSV document."""
        if not normalized_rows_csv.strip():
            return base_csv_text
        base = base_csv_text.rstrip("\r\n")
        extra = normalized_rows_csv.strip("\r\n")
        return f"{base}\n{extra}\n"

    def _artifact_root(self, artifacts_root: str | Path | None, dataset_name: str) -> Path:
        root = Path(artifacts_root or self._default_artifacts_root)
        slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in dataset_name).strip("-") or "dataset"
        timestamp = datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S")
        target = root / "dataset_lab" / f"{slug}-{timestamp}"
        target.mkdir(parents=True, exist_ok=True)
        return target

    def _build_visual_artifacts(
        self,
        *,
        artifact_root: Path,
        fixed_scores: dict[str, float],
        adaptive_score: float,
        best_fixed_score: float,
        oracle_score: float,
        next_prediction_by_strategy: dict[str, str],
        decision_csv_path: Path,
    ) -> dict[str, Path]:
        score_plot_path = artifact_root / "dataset_lab_scores.png"
        portfolio_plot_path = artifact_root / "dataset_lab_portfolio.png"
        switch_plot_path = artifact_root / "dataset_lab_switches.png"
        score_plot_path.write_bytes(_build_vertical_bar_plot(
            title="Adaptive vs Fixed vs Oracle",
            labels=("Adaptive", "Best fixed", "Oracle"),
            values=(adaptive_score, best_fixed_score, oracle_score),
            highlight_index=0,
        ))
        ordered_fixed_scores = sorted(fixed_scores.items(), key=lambda item: item[1], reverse=True)[:8]
        portfolio_plot_path.write_bytes(_build_vertical_bar_plot(
            title="Fixed portfolio scores",
            labels=tuple(name for name, _ in ordered_fixed_scores),
            values=tuple(score for _, score in ordered_fixed_scores),
            highlight_index=0 if ordered_fixed_scores else None,
        ))
        switch_plot_path.write_bytes(_build_switch_timeline_plot(decision_csv_path))
        return {
            "score_plot_path": score_plot_path,
            "portfolio_plot_path": portfolio_plot_path,
            "switch_plot_path": switch_plot_path,
        }

    def _history_index_path(self, artifacts_root: str | Path | None) -> Path:
        root = Path(artifacts_root or self._default_artifacts_root)
        history_root = root / "dataset_lab"
        history_root.mkdir(parents=True, exist_ok=True)
        return history_root / "history.json"

    def _append_history_entry(self, *, artifacts_root: str | Path | None, entry: dict[str, Any]) -> None:
        history_path = self._history_index_path(artifacts_root)
        if history_path.exists():
            try:
                payload = json.loads(history_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                payload = []
        else:
            payload = []
        if not isinstance(payload, list):
            payload = []
        payload = [row for row in payload if not (isinstance(row, dict) and row.get("summary_json_path") == entry.get("summary_json_path"))]
        payload.append(entry)
        payload.sort(key=lambda row: str(row.get("created_at_utc", "")), reverse=True)
        history_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")

    def _prepare_dataset(
        self,
        *,
        dataset_name: str,
        csv_text: str,
        target_column: str,
        requested_task_type: str,
        order_column: str | None,
        lag_count: int,
        max_rows: int,
        use_target_lags: bool | None,
    ) -> _PreparedDataset:
        reader = csv.DictReader(io.StringIO(csv_text))
        if reader.fieldnames is None:
            raise ValueError("CSV must include a header row")
        if target_column not in reader.fieldnames:
            raise ValueError(f"target column not found: {target_column!r}")
        rows = [dict(row) for row in reader if any((value or "").strip() for value in row.values())]
        if order_column:
            if order_column not in reader.fieldnames:
                raise ValueError(f"order column not found: {order_column!r}")
            rows.sort(key=lambda row: _sortable_value(row.get(order_column)))
        observed_rows, pending_rows = _split_observed_and_pending_rows(rows=rows, target_column=target_column)
        if max_rows > 0:
            observed_rows = observed_rows[:max_rows]
        min_history = (lag_count + 4) if use_target_lags else 5
        if len(observed_rows) <= min_history:
            raise ValueError("dataset is too short for streaming replay after lag generation")

        raw_targets = [row[target_column] for row in observed_rows]
        task_type = _resolve_task_type(raw_targets, requested_task_type)
        if use_target_lags is None:
            use_target_lags = task_type != "classification"
        encoded_targets = [_coerce_target_value(value, task_type) for value in raw_targets]

        examples: list[tuple[dict[str, Any], Any]] = []
        start_index = lag_count if use_target_lags else 0
        for row_index in range(start_index, len(observed_rows)):
            base_features = {
                key: _coerce_feature_value(value)
                for key, value in observed_rows[row_index].items()
                if key not in {target_column, order_column}
            }
            if use_target_lags:
                for lag_offset in range(1, lag_count + 1):
                    base_features[f"target_lag_{lag_offset}"] = encoded_targets[row_index - lag_offset]
            examples.append((base_features, encoded_targets[row_index]))

        next_source_row = pending_rows[0] if pending_rows else observed_rows[-1]
        next_features = {
            key: _coerce_feature_value(value)
            for key, value in next_source_row.items()
            if key not in {target_column, order_column}
        }
        if use_target_lags:
            for lag_offset in range(1, lag_count + 1):
                next_features[f"target_lag_{lag_offset}"] = encoded_targets[-lag_offset]

        return _PreparedDataset(
            dataset_name=dataset_name,
            task_type=task_type,
            target_column=target_column,
            source_row_count=len(rows),
            source_rows_used=len(observed_rows) + len(pending_rows),
            feature_count=len(examples[0][0]),
            sample_count=len(examples),
            examples=tuple(examples),
            next_features=next_features,
            raw_target_tail=tuple(raw_targets[-lag_count:]),
            prediction_mode="manual_row" if pending_rows else "next_step",
            forecast_row_preview={key: next_source_row.get(key) for key in reader.fieldnames},
        )

    def _run_policy(
        self,
        *,
        trace: OutcomeTrace,
        policy_name: str,
        output_root: Path,
        start_strategy: str,
        preset: _ReplayPreset | None = None,
        progress_callback: Any | None = None,
    ) -> ReplayBenchmarkResult:
        sample_count = len(next(iter(trace.rewards_by_strategy.values())))
        evaluation_interval = preset.evaluation_interval if preset is not None else max(8, min(48, sample_count // 12 or 8))

        normalized = policy_name.strip().lower()
        if normalized == "auto_meta":
            return self._run_auto_policy(
                trace=trace,
                output_root=output_root,
                start_strategy=start_strategy,
                preset=preset,
                evaluation_interval=evaluation_interval,
                progress_callback=progress_callback,
            )
        if normalized == "recent_leader_meta":
            return self._runner.run_outcome_trace_with_recent_leader(
                trace=trace,
                output_root=output_root,
                evaluation_interval=evaluation_interval,
                start_strategy=start_strategy,
                lookback_blocks=preset.recent_leader_lookback_blocks if preset is not None else 3,
                margin=preset.recent_leader_margin if preset is not None else (0.001 if trace.score_name != "accuracy" else 0.0),
                warmup_blocks=preset.recent_leader_warmup_blocks if preset is not None else (2 if sample_count >= evaluation_interval * 3 else 1),
                cooldown_blocks=preset.recent_leader_cooldown_blocks if preset is not None else 1,
                incumbent_floor=preset.recent_leader_incumbent_floor if preset is not None else (0.001 if trace.score_name != "accuracy" else 0.0),
                progress_callback=progress_callback,
            )

        if normalized == "fixed_share_portfolio":
            warmup_samples = min(max(evaluation_interval * 2, 32), len(next(iter(trace.rewards_by_strategy.values()))))
            return self._runner.run_outcome_trace_with_fixed_share(
                trace=trace,
                output_root=output_root,
                evaluation_interval=evaluation_interval,
                start_strategy=start_strategy,
                eta=0.45 if trace.score_name != "accuracy" else 0.35,
                share_alpha=0.03 if trace.score_name != "accuracy" else 0.02,
                switch_threshold=0.01 if trace.score_name != "accuracy" else 0.015,
                warmup_samples=warmup_samples,
                progress_callback=progress_callback,
            )

        return self._runner.run_outcome_trace(
            trace=trace,
            output_root=output_root,
            meta_config=MetaControllerConfig(
                window_size=preset.hard_window_size if preset is not None else 4,
                min_samples=preset.hard_min_samples if preset is not None else 2,
                delta=preset.hard_delta if preset is not None else (0.001 if trace.score_name != "accuracy" else 0.0),
                lambda_value=preset.hard_lambda_value if preset is not None else 0.0,
                switch_cost=preset.hard_switch_cost if preset is not None else 0.0,
                utility_weights={
                    "reward_mean": 1.0,
                    "reward_variance": 0.0,
                    "compute_cost": 0.0,
                    "switch_cost": 0.0,
                },
            ),
            evaluation_interval=evaluation_interval,
            start_strategy=start_strategy,
            progress_callback=progress_callback,
        )

    def _run_auto_policy(
        self,
        *,
        trace: OutcomeTrace,
        output_root: Path,
        start_strategy: str,
        preset: _ReplayPreset | None,
        evaluation_interval: int,
        progress_callback: Any | None = None,
    ) -> ReplayBenchmarkResult:
        """Select one controller family from a calibration prefix, then run it on the full stream."""
        calibration_trace = _build_calibration_trace(
            trace=trace,
            evaluation_interval=evaluation_interval,
            preset=preset,
        )
        ranked_candidates = _rank_auto_meta_candidates(
            calibration_trace=calibration_trace,
            candidates=_auto_meta_candidate_names(),
            run_candidate=lambda candidate_name, candidate_trace: self._run_candidate_policy(
                trace=candidate_trace,
                policy_name=candidate_name,
                output_root=output_root / "auto_meta_calibration" / candidate_name,
                start_strategy=start_strategy,
                preset=preset,
                evaluation_interval=evaluation_interval,
            ),
        )
        selected_candidate_name = ranked_candidates[0]
        selected_result = self._run_candidate_policy(
            trace=trace,
            policy_name=selected_candidate_name,
            output_root=output_root / "auto_meta_selection" / selected_candidate_name,
            start_strategy=start_strategy,
            preset=preset,
            evaluation_interval=evaluation_interval,
            progress_callback=progress_callback,
        )
        if selected_result.delta_vs_best_fixed >= 0.0:
            return selected_result
        return self._build_best_fixed_guard_result(trace=trace, output_root=output_root)

    def _run_candidate_policy(
        self,
        *,
        trace: OutcomeTrace,
        policy_name: str,
        output_root: Path,
        start_strategy: str,
        preset: _ReplayPreset | None,
        evaluation_interval: int,
        progress_callback: Any | None = None,
    ) -> ReplayBenchmarkResult:
        normalized = policy_name.strip().lower()
        if normalized == "recent_leader_meta":
            return self._runner.run_outcome_trace_with_recent_leader(
                trace=trace,
                output_root=output_root,
                evaluation_interval=evaluation_interval,
                start_strategy=start_strategy,
                lookback_blocks=preset.recent_leader_lookback_blocks if preset is not None else 3,
                margin=preset.recent_leader_margin if preset is not None else (0.001 if trace.score_name != "accuracy" else 0.0),
                warmup_blocks=preset.recent_leader_warmup_blocks if preset is not None else 2,
                cooldown_blocks=preset.recent_leader_cooldown_blocks if preset is not None else 1,
                incumbent_floor=preset.recent_leader_incumbent_floor if preset is not None else (0.001 if trace.score_name != "accuracy" else 0.0),
                progress_callback=progress_callback,
            )

        if normalized == "hedge_portfolio":
            warmup_samples = min(max(evaluation_interval * 2, 32), len(next(iter(trace.rewards_by_strategy.values()))))
            return self._runner.run_outcome_trace_with_hedge(
                trace=trace,
                output_root=output_root,
                evaluation_interval=evaluation_interval,
                start_strategy=start_strategy,
                eta=0.45 if trace.score_name != "accuracy" else 0.35,
                switch_threshold=0.01 if trace.score_name != "accuracy" else 0.015,
                warmup_samples=warmup_samples,
                progress_callback=progress_callback,
            )

        if normalized == "fixed_share_portfolio":
            warmup_samples = min(max(evaluation_interval * 2, 32), len(next(iter(trace.rewards_by_strategy.values()))))
            return self._runner.run_outcome_trace_with_fixed_share(
                trace=trace,
                output_root=output_root,
                evaluation_interval=evaluation_interval,
                start_strategy=start_strategy,
                eta=0.45 if trace.score_name != "accuracy" else 0.35,
                share_alpha=0.03 if trace.score_name != "accuracy" else 0.02,
                switch_threshold=0.01 if trace.score_name != "accuracy" else 0.015,
                warmup_samples=warmup_samples,
                progress_callback=progress_callback,
            )

        return self._runner.run_outcome_trace(
            trace=trace,
            output_root=output_root,
            meta_config=MetaControllerConfig(
                window_size=preset.hard_window_size if preset is not None else 4,
                min_samples=preset.hard_min_samples if preset is not None else 2,
                delta=preset.hard_delta if preset is not None else (0.001 if trace.score_name != "accuracy" else 0.0),
                lambda_value=preset.hard_lambda_value if preset is not None else 0.0,
                switch_cost=preset.hard_switch_cost if preset is not None else 0.0,
                utility_weights={
                    "reward_mean": 1.0,
                    "reward_variance": 0.0,
                    "compute_cost": 0.0,
                    "switch_cost": 0.0,
                },
            ),
            evaluation_interval=evaluation_interval,
            start_strategy=start_strategy,
            progress_callback=progress_callback,
        )

    def _build_best_fixed_guard_result(self, *, trace: OutcomeTrace, output_root: Path) -> ReplayBenchmarkResult:
        """Return a no-loss fallback that follows the strongest stationary strategy for the observed history."""
        fixed_scores = {name: fmean(rewards) for name, rewards in trace.rewards_by_strategy.items()}
        best_fixed_strategy, best_fixed_score = max(
            fixed_scores.items(),
            key=lambda item: (item[1], item[0]),
        )
        result = ReplayBenchmarkResult(
            dataset_name=trace.dataset_name,
            score_name=trace.score_name,
            policy_name="best_fixed_guard",
            sample_count=len(next(iter(trace.rewards_by_strategy.values()))),
            evaluation_interval=max(1, len(next(iter(trace.rewards_by_strategy.values()))) // 4),
            window_size=max(1, len(next(iter(trace.rewards_by_strategy.values()))) // 4),
            start_strategy=best_fixed_strategy,
            final_strategy=best_fixed_strategy,
            switch_count=0,
            adaptive_score=best_fixed_score,
            best_fixed_strategy=best_fixed_strategy,
            best_fixed_score=best_fixed_score,
            delta_vs_best_fixed=0.0,
            fixed_scores=fixed_scores,
            block_delta_mean=0.0,
            block_delta_std=0.0,
            block_delta_ci95=0.0,
            block_count=0,
            decision_csv_path="",
            summary_json_path="",
            report_md_path="",
        )
        return self._runner._persist_result(
            result=result,
            trace=trace,
            decisions=[],
            output_root=output_root,
        )


@dataclass(slots=True)
class _BackgroundDatasetLabState:
    job_id: str
    artifacts_root: str
    thread: Thread
    status_path: Path
    last_result: DatasetLabResult | None = None
    error_message: str | None = None


class DatasetLabJobService:
    """Background execution and persisted monitoring for dataset-lab analyses."""

    def __init__(self, *, default_artifacts_root: str | Path = "artifacts") -> None:
        self._default_artifacts_root = Path(default_artifacts_root)
        self._dataset_lab = DatasetLabService(default_artifacts_root=self._default_artifacts_root)
        self._jobs: dict[str, _BackgroundDatasetLabState] = {}
        self._lock = Lock()

    def start_csv_job(
        self,
        *,
        dataset_name: str,
        csv_text: str,
        target_column: str,
        task_type: str = "auto",
        order_column: str | None = None,
        lag_count: int = 3,
        policy_name: str = "auto_meta",
        dataset_profile: str | None = None,
        artifacts_root: str | Path | None = None,
        max_rows: int = 0,
    ) -> DatasetLabJobStatus:
        job_id = _build_dataset_job_id(dataset_name)
        job_root = self._job_root(artifacts_root, job_id)
        status_path = job_root / "status.json"
        payload = self._base_status_payload(
            job_id=job_id,
            dataset_name=dataset_name,
            source_kind="csv",
            artifacts_root=artifacts_root,
            artifact_root=job_root / "analysis",
        )
        self._write_status(status_path, payload)
        thread = Thread(
            target=self._run_csv_job,
            kwargs={
                "job_id": job_id,
                "status_path": status_path,
                "dataset_name": dataset_name,
                "csv_text": csv_text,
                "target_column": target_column,
                "task_type": task_type,
                "order_column": order_column,
                "lag_count": lag_count,
                "policy_name": policy_name,
                "dataset_profile": dataset_profile,
                "artifacts_root": artifacts_root,
                "max_rows": max_rows,
                "artifact_root_override": job_root / "analysis",
            },
            daemon=True,
            name=f"dataset-lab-csv-{job_id}",
        )
        with self._lock:
            self._jobs[job_id] = _BackgroundDatasetLabState(
                job_id=job_id,
                artifacts_root=str(Path(artifacts_root or self._default_artifacts_root)),
                thread=thread,
                status_path=status_path,
            )
        thread.start()
        return DatasetLabJobStatus(**{**asdict(self._status_from_payload(payload)), "background_running": True})

    def start_builtin_job(
        self,
        *,
        dataset_id: str,
        dataset_name: str,
        row_count: int,
        policy_name: str = "auto_meta",
        artifacts_root: str | Path | None = None,
    ) -> DatasetLabJobStatus:
        builtin_payload = self._dataset_lab.load_builtin_dataset_csv(dataset_id, max_rows=row_count)
        return self.start_csv_job(
            dataset_name=dataset_name,
            csv_text=builtin_payload.csv_text,
            target_column=builtin_payload.target_column,
            task_type=builtin_payload.task_type,
            order_column=builtin_payload.order_column,
            lag_count=3,
            policy_name=policy_name,
            artifacts_root=artifacts_root,
            max_rows=row_count,
        )
        job_id = _build_dataset_job_id(dataset_name)
        job_root = self._job_root(artifacts_root, job_id)
        status_path = job_root / "status.json"
        payload = self._base_status_payload(
            job_id=job_id,
            dataset_name=dataset_name,
            source_kind="builtin",
            artifacts_root=artifacts_root,
            artifact_root=job_root / "analysis",
        )
        self._write_status(status_path, payload)
        thread = Thread(
            target=self._run_builtin_job,
            kwargs={
                "job_id": job_id,
                "status_path": status_path,
                "dataset_id": dataset_id,
                "dataset_name": dataset_name,
                "row_count": row_count,
                "policy_name": policy_name,
                "artifacts_root": artifacts_root,
                "artifact_root_override": job_root / "analysis",
            },
            daemon=True,
            name=f"dataset-lab-builtin-{job_id}",
        )
        with self._lock:
            self._jobs[job_id] = _BackgroundDatasetLabState(
                job_id=job_id,
                artifacts_root=str(Path(artifacts_root or self._default_artifacts_root)),
                thread=thread,
                status_path=status_path,
            )
        thread.start()
        return DatasetLabJobStatus(**{**asdict(self._status_from_payload(payload)), "background_running": True})

    def list_jobs(
        self,
        *,
        artifacts_root: str | Path | None = None,
        limit: int = 20,
    ) -> tuple[DatasetLabJobStatus, ...]:
        job_root = self._jobs_root(artifacts_root)
        rows: list[DatasetLabJobStatus] = []
        for status_path in job_root.glob("*/status.json"):
            try:
                payload = json.loads(status_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            rows.append(self._status_from_payload(payload))
        rows.sort(key=lambda item: item.created_at_utc, reverse=True)
        return tuple(rows[:limit])

    def get_job_status(self, job_id: str, *, artifacts_root: str | Path | None = None) -> DatasetLabJobStatus:
        status_path = self._job_root(artifacts_root, job_id) / "status.json"
        payload = json.loads(status_path.read_text(encoding="utf-8"))
        status = self._status_from_payload(payload)
        with self._lock:
            state = self._jobs.get(job_id)
            if state is not None:
                return DatasetLabJobStatus(**{**asdict(status), "background_running": state.thread.is_alive()})
        return status

    def load_completed_result(self, job_id: str, *, artifacts_root: str | Path | None = None) -> DatasetLabResult:
        status = self.get_job_status(job_id, artifacts_root=artifacts_root)
        if not status.summary_json_path:
            raise FileNotFoundError(f"summary not available for job: {job_id}")
        return self._dataset_lab.load_result_from_summary(status.summary_json_path)

    def _run_csv_job(self, **kwargs: Any) -> None:
        self._run_job(
            job_id=str(kwargs["job_id"]),
            status_path=Path(kwargs["status_path"]),
            runner=lambda callback: self._dataset_lab.analyze_csv(
                dataset_name=str(kwargs["dataset_name"]),
                csv_text=str(kwargs["csv_text"]),
                target_column=str(kwargs["target_column"]),
                task_type=str(kwargs["task_type"]),
                order_column=kwargs["order_column"],
                lag_count=int(kwargs["lag_count"]),
                policy_name=str(kwargs["policy_name"]),
                dataset_profile=kwargs["dataset_profile"],
                artifacts_root=kwargs["artifacts_root"],
                max_rows=int(kwargs["max_rows"]),
                artifact_root_override=kwargs["artifact_root_override"],
                progress_callback=callback,
            ),
        )

    def _run_builtin_job(self, **kwargs: Any) -> None:
        self._run_job(
            job_id=str(kwargs["job_id"]),
            status_path=Path(kwargs["status_path"]),
            runner=lambda callback: self._dataset_lab.analyze_builtin_dataset(
                dataset_id=str(kwargs["dataset_id"]),
                row_count=int(kwargs["row_count"]),
                policy_name=str(kwargs["policy_name"]),
                artifacts_root=kwargs["artifacts_root"],
                artifact_root_override=kwargs["artifact_root_override"],
                progress_callback=callback,
            ),
        )

    def _run_job(self, *, job_id: str, status_path: Path, runner: Any) -> None:
        try:
            self._update_status(status_path, status="running", phase="starting", progress=0.02)
            telemetry_path = Path(json.loads(status_path.read_text(encoding="utf-8")).get("telemetry_path", ""))
            result = runner(lambda **payload: self._handle_progress_update(status_path=status_path, telemetry_path=telemetry_path, **payload))
            self._update_status(
                status_path,
                status="completed",
                phase="completed",
                progress=1.0,
                summary_json_path=result.summary_json_path,
                report_md_path=result.report_md_path,
                artifact_root=result.artifact_root,
                policy_name=result.policy_name,
                source_row_count=result.source_row_count,
                source_rows_used=result.source_rows_used,
                sample_count=result.sample_count,
                adaptive_score=result.adaptive_score,
                best_fixed_score=result.best_fixed_score,
                delta_vs_best_fixed=result.delta_vs_best_fixed,
                oracle_capture_ratio=result.oracle_capture_ratio,
                switch_count=result.switch_count,
                final_strategy=result.final_strategy,
                error_message=None,
            )
            with self._lock:
                if job_id in self._jobs:
                    self._jobs[job_id].last_result = result
        except Exception as exc:
            self._update_status(status_path, status="failed", phase="failed", progress=1.0, error_message=str(exc))
            with self._lock:
                if job_id in self._jobs:
                    self._jobs[job_id].error_message = str(exc)

    def load_telemetry(
        self,
        job_id: str,
        *,
        artifacts_root: str | Path | None = None,
        limit: int = 300,
    ) -> tuple[dict[str, Any], ...]:
        status = self.get_job_status(job_id, artifacts_root=artifacts_root)
        telemetry_path = Path(status.telemetry_path)
        if not telemetry_path.exists():
            return ()
        rows: list[dict[str, Any]] = []
        for line in telemetry_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return tuple(rows[-limit:])

    def _jobs_root(self, artifacts_root: str | Path | None) -> Path:
        root = Path(artifacts_root or self._default_artifacts_root) / "dataset_lab_jobs"
        root.mkdir(parents=True, exist_ok=True)
        return root

    def _job_root(self, artifacts_root: str | Path | None, job_id: str) -> Path:
        root = self._jobs_root(artifacts_root) / job_id
        root.mkdir(parents=True, exist_ok=True)
        return root

    def _base_status_payload(
        self,
        *,
        job_id: str,
        dataset_name: str,
        source_kind: str,
        artifacts_root: str | Path | None,
        artifact_root: Path,
    ) -> dict[str, Any]:
        timestamp = datetime.now(tz=UTC).isoformat()
        return {
            "job_id": job_id,
            "dataset_name": dataset_name,
            "source_kind": source_kind,
            "status": "queued",
            "phase": "queued",
            "progress": 0.0,
            "created_at_utc": timestamp,
            "updated_at_utc": timestamp,
            "artifacts_root": str(Path(artifacts_root or self._default_artifacts_root)),
            "artifact_root": str(artifact_root),
            "summary_json_path": "",
            "report_md_path": "",
            "telemetry_path": str(Path(artifact_root).parent / "telemetry.jsonl"),
            "error_message": None,
            "source_row_count": 0,
            "source_rows_used": 0,
            "sample_count": 0,
            "adaptive_score": None,
            "best_fixed_score": None,
            "delta_vs_best_fixed": None,
            "oracle_capture_ratio": None,
            "switch_count": 0,
            "final_strategy": "",
            "policy_name": "",
            "sample_index": 0,
            "total_samples": 0,
            "evaluation_index": 0,
            "active_strategy": "",
            "candidate_strategy": "",
            "adaptive_score_so_far": None,
            "best_fixed_score_so_far": None,
            "delta_so_far": None,
            "oracle_capture_so_far": None,
        }

    def _update_status(self, status_path: Path, **updates: Any) -> None:
        payload = json.loads(status_path.read_text(encoding="utf-8"))
        payload.update(updates)
        payload["updated_at_utc"] = datetime.now(tz=UTC).isoformat()
        self._write_status(status_path, payload)

    def _handle_progress_update(self, *, status_path: Path, telemetry_path: Path, **payload: Any) -> None:
        self._update_status(status_path, status="running", **payload)
        if payload.get("phase") == "adaptive_replay_running":
            telemetry_path.parent.mkdir(parents=True, exist_ok=True)
            with telemetry_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps({"updated_at_utc": datetime.now(tz=UTC).isoformat(), **payload}, ensure_ascii=True) + "\n")

    def _write_status(self, status_path: Path, payload: dict[str, Any]) -> None:
        status_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = status_path.with_suffix(".tmp")
        temp_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        for _ in range(10):
            try:
                temp_path.replace(status_path)
                return
            except PermissionError:
                time.sleep(0.01)
        status_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")

    def _status_from_payload(self, payload: dict[str, Any]) -> DatasetLabJobStatus:
        return DatasetLabJobStatus(
            job_id=str(payload.get("job_id", "")),
            dataset_name=str(payload.get("dataset_name", "")),
            source_kind=str(payload.get("source_kind", "")),
            status=str(payload.get("status", "")),
            phase=str(payload.get("phase", "")),
            progress=float(payload.get("progress", 0.0)),
            created_at_utc=str(payload.get("created_at_utc", "")),
            updated_at_utc=str(payload.get("updated_at_utc", "")),
            artifacts_root=str(payload.get("artifacts_root", "")),
            artifact_root=str(payload.get("artifact_root", "")),
            summary_json_path=str(payload.get("summary_json_path", "")),
            report_md_path=str(payload.get("report_md_path", "")),
            error_message=str(payload["error_message"]) if payload.get("error_message") is not None else None,
            source_row_count=int(payload.get("source_row_count", 0)),
            source_rows_used=int(payload.get("source_rows_used", 0)),
            sample_count=int(payload.get("sample_count", 0)),
            adaptive_score=float(payload["adaptive_score"]) if payload.get("adaptive_score") is not None else None,
            best_fixed_score=float(payload["best_fixed_score"]) if payload.get("best_fixed_score") is not None else None,
            delta_vs_best_fixed=float(payload["delta_vs_best_fixed"]) if payload.get("delta_vs_best_fixed") is not None else None,
            oracle_capture_ratio=float(payload["oracle_capture_ratio"]) if payload.get("oracle_capture_ratio") is not None else None,
            switch_count=int(payload.get("switch_count", 0)),
            final_strategy=str(payload.get("final_strategy", "")),
            policy_name=str(payload.get("policy_name", "")),
            telemetry_path=str(payload.get("telemetry_path", "")),
            sample_index=int(payload.get("sample_index", 0)),
            total_samples=int(payload.get("total_samples", 0)),
            evaluation_index=int(payload.get("evaluation_index", 0)),
            active_strategy=str(payload.get("active_strategy", "")),
            candidate_strategy=str(payload.get("candidate_strategy", "")),
            adaptive_score_so_far=float(payload["adaptive_score_so_far"]) if payload.get("adaptive_score_so_far") is not None else None,
            best_fixed_score_so_far=float(payload["best_fixed_score_so_far"]) if payload.get("best_fixed_score_so_far") is not None else None,
            delta_so_far=float(payload["delta_so_far"]) if payload.get("delta_so_far") is not None else None,
            oracle_capture_so_far=float(payload["oracle_capture_so_far"]) if payload.get("oracle_capture_so_far") is not None else None,
            background_running=False,
        )
    def _run_auto_policy(
        self,
        *,
        trace: OutcomeTrace,
        output_root: Path,
        start_strategy: str,
        preset: _ReplayPreset | None,
        evaluation_interval: int,
        progress_callback: Any | None = None,
    ) -> ReplayBenchmarkResult:
        """Automatically select one controller family from a calibration prefix."""
        calibration_trace = _build_calibration_trace(
            trace=trace,
            evaluation_interval=evaluation_interval,
            preset=preset,
        )
        ranked_candidates = _rank_auto_meta_candidates(
            calibration_trace=calibration_trace,
            candidates=_auto_meta_candidate_names(),
            run_candidate=lambda candidate_name, candidate_trace: self._run_candidate_policy(
                trace=candidate_trace,
                policy_name=candidate_name,
                output_root=output_root / "auto_meta_calibration" / candidate_name,
                start_strategy=start_strategy,
                preset=preset,
                evaluation_interval=evaluation_interval,
            ),
        )
        best_candidate = self._run_candidate_policy(
            trace=trace,
            policy_name=ranked_candidates[0],
            output_root=output_root / "auto_meta_selection" / ranked_candidates[0],
            start_strategy=start_strategy,
            preset=preset,
            evaluation_interval=evaluation_interval,
            progress_callback=progress_callback,
        )
        if best_candidate.delta_vs_best_fixed >= 0.0:
            return best_candidate
        return self._build_best_fixed_guard_result(trace=trace, output_root=output_root)

    def _run_candidate_policy(
        self,
        *,
        trace: OutcomeTrace,
        policy_name: str,
        output_root: Path,
        start_strategy: str,
        preset: _ReplayPreset | None,
        evaluation_interval: int,
    ) -> ReplayBenchmarkResult:
        normalized = policy_name.strip().lower()
        if normalized == "recent_leader_meta":
            return self._runner.run_outcome_trace_with_recent_leader(
                trace=trace,
                output_root=output_root,
                evaluation_interval=evaluation_interval,
                start_strategy=start_strategy,
                lookback_blocks=preset.recent_leader_lookback_blocks if preset is not None else 3,
                margin=preset.recent_leader_margin if preset is not None else (0.001 if trace.score_name != "accuracy" else 0.0),
                warmup_blocks=preset.recent_leader_warmup_blocks if preset is not None else 2,
                cooldown_blocks=preset.recent_leader_cooldown_blocks if preset is not None else 1,
                incumbent_floor=preset.recent_leader_incumbent_floor if preset is not None else (0.001 if trace.score_name != "accuracy" else 0.0),
            )

        if normalized == "hedge_portfolio":
            warmup_samples = min(max(evaluation_interval * 2, 32), len(next(iter(trace.rewards_by_strategy.values()))))
            return self._runner.run_outcome_trace_with_hedge(
                trace=trace,
                output_root=output_root,
                evaluation_interval=evaluation_interval,
                start_strategy=start_strategy,
                eta=0.45 if trace.score_name != "accuracy" else 0.35,
                switch_threshold=0.01 if trace.score_name != "accuracy" else 0.015,
                warmup_samples=warmup_samples,
            )

        if normalized == "fixed_share_portfolio":
            warmup_samples = min(max(evaluation_interval * 2, 32), len(next(iter(trace.rewards_by_strategy.values()))))
            return self._runner.run_outcome_trace_with_fixed_share(
                trace=trace,
                output_root=output_root,
                evaluation_interval=evaluation_interval,
                start_strategy=start_strategy,
                eta=0.45 if trace.score_name != "accuracy" else 0.35,
                share_alpha=0.03 if trace.score_name != "accuracy" else 0.02,
                switch_threshold=0.01 if trace.score_name != "accuracy" else 0.015,
                warmup_samples=warmup_samples,
            )

        return self._runner.run_outcome_trace(
            trace=trace,
            output_root=output_root,
            meta_config=MetaControllerConfig(
                window_size=preset.hard_window_size if preset is not None else 4,
                min_samples=preset.hard_min_samples if preset is not None else 2,
                delta=preset.hard_delta if preset is not None else (0.001 if trace.score_name != "accuracy" else 0.0),
                lambda_value=preset.hard_lambda_value if preset is not None else 0.0,
                switch_cost=preset.hard_switch_cost if preset is not None else 0.0,
                utility_weights={
                    "reward_mean": 1.0,
                    "reward_variance": 0.0,
                    "compute_cost": 0.0,
                    "switch_cost": 0.0,
                },
            ),
            evaluation_interval=evaluation_interval,
            start_strategy=start_strategy,
        )

    def _build_best_fixed_guard_result(self, *, trace: OutcomeTrace, output_root: Path) -> ReplayBenchmarkResult:
        """Return a no-loss fallback that follows the strongest stationary strategy for the observed history."""
        fixed_scores = {name: fmean(rewards) for name, rewards in trace.rewards_by_strategy.items()}
        best_fixed_strategy, best_fixed_score = max(
            fixed_scores.items(),
            key=lambda item: (item[1], item[0]),
        )
        result = ReplayBenchmarkResult(
            dataset_name=trace.dataset_name,
            score_name=trace.score_name,
            policy_name="best_fixed_guard",
            sample_count=len(next(iter(trace.rewards_by_strategy.values()))),
            evaluation_interval=max(1, len(next(iter(trace.rewards_by_strategy.values()))) // 4),
            window_size=max(1, len(next(iter(trace.rewards_by_strategy.values()))) // 4),
            start_strategy=best_fixed_strategy,
            final_strategy=best_fixed_strategy,
            switch_count=0,
            adaptive_score=best_fixed_score,
            best_fixed_strategy=best_fixed_strategy,
            best_fixed_score=best_fixed_score,
            delta_vs_best_fixed=0.0,
            fixed_scores=fixed_scores,
            block_delta_mean=0.0,
            block_delta_std=0.0,
            block_delta_ci95=0.0,
            block_count=0,
            decision_csv_path="",
            summary_json_path="",
            report_md_path="",
        )
        return self._runner._persist_result(
            result=result,
            trace=trace,
            decisions=[],
            output_root=output_root,
        )


def _classification_strategies() -> tuple[ReplayStrategySpec, ...]:
    return (
        ReplayStrategySpec("sgd_lr_0_005", 0.005, "Online SGD classifier lr=0.005"),
        ReplayStrategySpec("sgd_lr_0_01", 0.01, "Online SGD classifier lr=0.01"),
        ReplayStrategySpec("sgd_lr_0_05", 0.05, "Online SGD classifier lr=0.05"),
        ReplayStrategySpec("sgd_lr_0_10", 0.10, "Online SGD classifier lr=0.10"),
        ReplayStrategySpec("sgd_lr_0_20", 0.20, "Online SGD classifier lr=0.20"),
        ReplayStrategySpec("pa_classifier", 0.0, "Passive-aggressive classifier", model_kind="pa_classifier"),
        ReplayStrategySpec("gaussian_nb", 0.0, "Gaussian naive Bayes", model_kind="gaussian_nb"),
        ReplayStrategySpec("tree_classifier", 0.0, "Hoeffding adaptive tree classifier", model_kind="hoeffding_tree_classifier"),
        ReplayStrategySpec("knn_classifier", 0.0, "KNN classifier", model_kind="knn_classifier"),
    )


def _regression_strategies() -> tuple[ReplayStrategySpec, ...]:
    return (
        ReplayStrategySpec("lin_lr_0_0001", 0.0001, "Online linear regression with SGD lr=0.0001"),
        ReplayStrategySpec("lin_lr_0_0005", 0.0005, "Online linear regression with SGD lr=0.0005"),
        ReplayStrategySpec("lin_lr_0_001", 0.001, "Online linear regression with SGD lr=0.001"),
        ReplayStrategySpec("lin_lr_0_002", 0.002, "Online linear regression with SGD lr=0.002"),
        ReplayStrategySpec("lin_lr_0_005", 0.005, "Online linear regression with SGD lr=0.005"),
        ReplayStrategySpec("lin_lr_0_01", 0.01, "Online linear regression with SGD lr=0.01"),
        ReplayStrategySpec("pa_regressor", 0.0, "Passive-aggressive regressor", model_kind="pa_regressor"),
        ReplayStrategySpec("tree_regressor", 0.0, "Hoeffding adaptive tree regressor", model_kind="hoeffding_tree_regressor"),
        ReplayStrategySpec("knn_regressor", 0.0, "KNN regressor", model_kind="knn_regressor"),
    )


def _build_classification_trace_bundle(
    *,
    dataset_name: str,
    samples: Iterable[tuple[dict[str, Any], Any]],
    next_features: dict[str, Any],
    strategies: Iterable[ReplayStrategySpec],
    progress_callback: Any | None = None,
) -> tuple[OutcomeTrace, dict[str, tuple[Any, ...]], dict[str, Any]]:
    strategy_specs = tuple(strategies)
    sample_rows = tuple(samples)
    distinct_targets = tuple(dict.fromkeys(target for _, target in sample_rows))
    is_binary = len(distinct_targets) <= 2
    if not is_binary:
        strategy_specs = tuple(spec for spec in strategy_specs if spec.model_kind != "pa_classifier")
    binary_label_map: dict[Any, bool] | None = None
    binary_inverse_map: dict[bool, Any] | None = None
    if is_binary:
        first_label = distinct_targets[0]
        second_label = distinct_targets[1] if len(distinct_targets) > 1 else distinct_targets[0]
        binary_label_map = {first_label: False, second_label: True}
        binary_inverse_map = {False: first_label, True: second_label}
        models = {spec.name: _build_binary_classifier_model(spec) for spec in strategy_specs}
    else:
        models = {spec.name: _build_multiclass_classifier_model(spec) for spec in strategy_specs}
    predictions_by_strategy: dict[str, list[Any]] = {spec.name: [] for spec in strategy_specs}
    rewards_by_strategy: dict[str, list[float]] = {spec.name: [] for spec in strategy_specs}
    successes_by_strategy: dict[str, list[bool]] = {spec.name: [] for spec in strategy_specs}
    labels_seen: list[Any] = []

    sample_count = len(sample_rows)
    progress_step = max(1, sample_count // 48) if sample_count else 1
    for row_index, (features, target) in enumerate(sample_rows):
        numeric_features = _default_feature_transform(features)
        for spec in strategy_specs:
            model = models[spec.name]
            prediction = model.predict_one(numeric_features)
            if is_binary:
                label_target = binary_label_map[target]
                if prediction is None:
                    prediction_label = labels_seen[-1] if labels_seen else target
                else:
                    prediction_label = binary_inverse_map[bool(prediction)]
                prediction = prediction_label
            else:
                label_target = target
                if prediction is None:
                    prediction = labels_seen[-1] if labels_seen else target
            predictions_by_strategy[spec.name].append(prediction)
            success = prediction == target
            rewards_by_strategy[spec.name].append(1.0 if success else 0.0)
            successes_by_strategy[spec.name].append(success)
            model.learn_one(numeric_features, label_target)
        labels_seen.append(target)
        if progress_callback is not None and (((row_index + 1) % progress_step == 0) or (row_index + 1 == sample_count)):
            _emit_progress(
                progress_callback,
                phase="building_strategy_trace",
                progress=0.35 + (0.23 * ((row_index + 1) / max(1, sample_count))),
                sample_index=row_index + 1,
                total_samples=sample_count,
            )

    next_numeric_features = _default_feature_transform(next_features)
    if is_binary:
        fallback_label = labels_seen[-1] if labels_seen else distinct_targets[0]
        next_prediction_by_strategy = {}
        for spec in strategy_specs:
            raw_prediction = models[spec.name].predict_one(next_numeric_features)
            if raw_prediction is None:
                next_prediction_by_strategy[spec.name] = fallback_label
            else:
                next_prediction_by_strategy[spec.name] = binary_inverse_map[bool(raw_prediction)]
    else:
        next_prediction_by_strategy = {
            spec.name: _classification_value(models[spec.name].predict_one(next_numeric_features), labels_seen[-1])
            for spec in strategy_specs
        }

    return (
        OutcomeTrace(
            dataset_name=dataset_name,
            score_name="accuracy",
            rewards_by_strategy={name: tuple(values) for name, values in rewards_by_strategy.items()},
            successes_by_strategy={name: tuple(values) for name, values in successes_by_strategy.items()},
            source_description="User-uploaded CSV replayed as a temporal streaming classification task.",
            source_url="local-upload",
        ),
        {name: tuple(values) for name, values in predictions_by_strategy.items()},
        next_prediction_by_strategy,
    )


def _build_regression_trace_bundle(
    *,
    dataset_name: str,
    samples: Iterable[tuple[dict[str, Any], Any]],
    next_features: dict[str, Any],
    strategies: Iterable[ReplayStrategySpec],
    progress_callback: Any | None = None,
) -> tuple[OutcomeTrace, dict[str, tuple[float, ...]], dict[str, float]]:
    strategy_specs = tuple(strategies)
    sample_rows = tuple(samples)
    targets = [float(target) for _, target in sample_rows]
    scale = _resolve_regression_scale(targets)
    models = {spec.name: _build_regressor_model(spec) for spec in strategy_specs}
    predictions_by_strategy: dict[str, list[float]] = {spec.name: [] for spec in strategy_specs}
    rewards_by_strategy: dict[str, list[float]] = {spec.name: [] for spec in strategy_specs}
    successes_by_strategy: dict[str, list[bool]] = {spec.name: [] for spec in strategy_specs}

    sample_count = len(sample_rows)
    progress_step = max(1, sample_count // 48) if sample_count else 1
    for row_index, (features, target) in enumerate(sample_rows):
        numeric_features = _default_feature_transform(features)
        history_mean = fmean(targets[:row_index]) if row_index > 0 else float(target)
        for spec in strategy_specs:
            model = models[spec.name]
            prediction = model.predict_one(numeric_features)
            numeric_prediction = history_mean if prediction is None else float(prediction)
            predictions_by_strategy[spec.name].append(numeric_prediction)
            error = abs(numeric_prediction - float(target))
            rewards_by_strategy[spec.name].append(1.0 / (1.0 + (error / scale)))
            successes_by_strategy[spec.name].append(error <= scale)
            model.learn_one(numeric_features, float(target))
        if progress_callback is not None and (((row_index + 1) % progress_step == 0) or (row_index + 1 == sample_count)):
            _emit_progress(
                progress_callback,
                phase="building_strategy_trace",
                progress=0.35 + (0.23 * ((row_index + 1) / max(1, sample_count))),
                sample_index=row_index + 1,
                total_samples=sample_count,
            )

    next_numeric_features = _default_feature_transform(next_features)
    next_prediction_by_strategy = {
        spec.name: float(models[spec.name].predict_one(next_numeric_features) or targets[-1])
        for spec in strategy_specs
    }

    return (
        OutcomeTrace(
            dataset_name=dataset_name,
            score_name="normalized_reward",
            rewards_by_strategy={name: tuple(values) for name, values in rewards_by_strategy.items()},
            successes_by_strategy={name: tuple(values) for name, values in successes_by_strategy.items()},
            source_description="User-uploaded CSV replayed as a temporal streaming regression task.",
            source_url="local-upload",
        ),
        {name: tuple(values) for name, values in predictions_by_strategy.items()},
        next_prediction_by_strategy,
    )


def _build_preview_rows(
    *,
    samples: Iterable[tuple[dict[str, Any], Any]],
    predictions_by_strategy: dict[str, tuple[Any, ...]],
    final_strategy: str,
    limit: int,
) -> tuple[dict[str, Any], ...]:
    sample_rows = tuple(samples)
    predictions = predictions_by_strategy.get(final_strategy, ())
    preview: list[dict[str, Any]] = []
    start_index = max(0, len(sample_rows) - limit)
    for index in range(start_index, len(sample_rows)):
        features, target = sample_rows[index]
        preview.append(
            {
                "row_index": index,
                "actual_target": target,
                "adaptive_prediction": predictions[index] if index < len(predictions) else None,
                "feature_snapshot": json.dumps(features, ensure_ascii=True, sort_keys=True, default=str),
            }
        )
    return tuple(preview)


def _build_interpretation(
    *,
    result: ReplayBenchmarkResult,
    oracle_score: float,
    oracle_gain: float,
    oracle_capture_ratio: float,
    task_type: str,
    prediction_mode: str,
    next_prediction: Any,
    raw_target_tail: tuple[Any, ...],
) -> tuple[str, ...]:
    delta = result.delta_vs_best_fixed
    lines = [
        (
            f"Adaptive policy `{result.policy_name}` finished on strategy `{result.final_strategy}` "
            f"after {result.switch_count} switches."
        ),
        (
            f"It achieved `{result.adaptive_score:.4f}` against the best fixed baseline "
            f"`{result.best_fixed_strategy}` at `{result.best_fixed_score:.4f}`."
        ),
        (
            f"Oracle upper bound on this stream is `{oracle_score:.4f}`. "
            f"Available oracle gain over best fixed is `{oracle_gain:.4f}`, and the current adaptive controller "
            f"captures `{oracle_capture_ratio * 100.0:.1f}%` of it."
        ),
    ]
    if delta > 0.0:
        lines.append(
            f"The uploaded stream looks non-stationary enough for adaptation to help: the gain over best fixed is `{delta:.4f}`."
        )
    elif delta == 0.0:
        lines.append("Adaptive and best fixed finished effectively tied on this stream.")
    else:
        lines.append(
            f"The current stationary portfolio dominated the adaptive controller here; the gap is `{delta:.4f}`."
        )
    if result.switch_count >= 3:
        lines.append("Multiple switches suggest regime changes or at least changing local winners across the stream.")
    elif result.switch_count == 0:
        lines.append("No strategy changes were needed; the stream behaved close to one dominant regime.")
    if prediction_mode == "manual_row":
        lines.append("The forecast target comes from a manually appended row with a missing target value.")
    else:
        lines.append("The forecast target is the next step after the last fully observed row in the stream.")
    if task_type == "regression":
        lines.append(
            f"Next-step forecast from the final adaptive strategy is `{float(next_prediction):.4f}` based on the latest lagged context `{list(raw_target_tail)}`."
        )
    else:
        lines.append(
            f"Next-step class from the final adaptive strategy is `{next_prediction}` based on the latest lagged context `{list(raw_target_tail)}`."
        )
    return tuple(lines)


def _build_caveats(*, task_type: str, order_column: str | None, lag_count: int) -> tuple[str, ...]:
    caveats = [
        f"The stream is replayed in {'the selected order column' if order_column else 'the original CSV row order'}.",
        f"Automatic lag generation uses the previous `{lag_count}` observed target values.",
    ]
    if task_type == "regression":
        caveats.append("The quality score is a bounded normalized reward, not raw MAE or RMSE.")
    else:
        caveats.append("The quality score is prequential accuracy over the uploaded stream.")
    caveats.append("If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.")
    return tuple(caveats)


def _resolve_task_type(raw_targets: list[str], requested_task_type: str) -> str:
    normalized = requested_task_type.strip().lower()
    if normalized in {"classification", "regression"}:
        return normalized
    numeric_values: list[float] = []
    for value in raw_targets:
        try:
            numeric_values.append(float(value))
        except (TypeError, ValueError):
            return "classification"
    unique_count = len({round(value, 10) for value in numeric_values})
    return "classification" if unique_count <= max(10, len(numeric_values) // 20 or 2) else "regression"


def _coerce_target_value(value: str, task_type: str) -> Any:
    if task_type == "regression":
        return float(value)
    stripped = (value or "").strip()
    if stripped.lower() in {"true", "false"}:
        return stripped.lower() == "true"
    try:
        numeric = float(stripped)
    except ValueError:
        return stripped
    if numeric.is_integer():
        return int(numeric)
    return numeric


def _coerce_feature_value(value: Any) -> Any:
    if value is None:
        return None
    stripped = str(value).strip()
    if stripped == "":
        return None
    if stripped.lower() in {"true", "false"}:
        return stripped.lower() == "true"
    try:
        numeric = float(stripped)
    except ValueError:
        return stripped
    if numeric.is_integer():
        return int(numeric)
    return numeric


def _sortable_value(value: Any) -> Any:
    if value is None:
        return ""
    stripped = str(value).strip()
    try:
        return float(stripped)
    except ValueError:
        return stripped


def _classification_value(prediction: Any, fallback: Any) -> Any:
    return fallback if prediction is None else prediction


def _prediction_confidence(*, task_type: str, next_prediction: Any, next_prediction_by_strategy: dict[str, Any]) -> float:
    values = list(next_prediction_by_strategy.values())
    if not values:
        return 0.0
    if task_type == "classification":
        return sum(1 for value in values if value == next_prediction) / len(values)
    numeric_values = [float(value) for value in values]
    if len(numeric_values) == 1:
        return 1.0
    mean_value = fmean(numeric_values)
    spread = max(numeric_values) - min(numeric_values)
    scale = max(1.0, abs(mean_value))
    return max(0.0, min(1.0, 1.0 / (1.0 + (spread / scale))))


def _confidence_label(score: float) -> str:
    if score >= 0.8:
        return "high"
    if score >= 0.55:
        return "medium"
    return "low"


def _oracle_summary(*, trace: OutcomeTrace, adaptive_score: float, best_fixed_score: float) -> tuple[float, float, float]:
    reward_rows = tuple(trace.rewards_by_strategy.values())
    if not reward_rows:
        return best_fixed_score, 0.0, 1.0

    sample_count = len(reward_rows[0])
    oracle_rewards = [max(rewards[index] for rewards in reward_rows) for index in range(sample_count)]
    oracle_score = fmean(oracle_rewards) if oracle_rewards else best_fixed_score
    oracle_gain = oracle_score - best_fixed_score
    adaptive_gain = adaptive_score - best_fixed_score
    if oracle_gain <= 1e-12:
        oracle_capture_ratio = 1.0 if adaptive_gain >= -1e-12 else 0.0
    else:
        oracle_capture_ratio = max(0.0, min(1.0, adaptive_gain / oracle_gain))
    return oracle_score, oracle_gain, oracle_capture_ratio


def _auto_meta_candidate_names() -> tuple[str, ...]:
    return ("recent_leader_meta", "hard_switch_lcb", "hedge_portfolio", "fixed_share_portfolio")


def _rank_auto_meta_candidates(
    *,
    calibration_trace: OutcomeTrace,
    candidates: Iterable[str],
    run_candidate: Any,
) -> tuple[str, ...]:
    """Rank controller families using only a calibration prefix of the stream."""
    scored: list[tuple[tuple[float, float, float, float, float, str], str]] = []
    for candidate_name in candidates:
        candidate_result = run_candidate(candidate_name, calibration_trace)
        _, _, capture = _oracle_summary(
            trace=calibration_trace,
            adaptive_score=candidate_result.adaptive_score,
            best_fixed_score=candidate_result.best_fixed_score,
        )
        sort_key = (
            1.0 if candidate_result.delta_vs_best_fixed >= 0.0 else 0.0,
            capture,
            candidate_result.delta_vs_best_fixed,
            candidate_result.adaptive_score,
            -float(candidate_result.switch_count),
            candidate_name,
        )
        scored.append((sort_key, candidate_name))
    scored.sort(reverse=True)
    return tuple(candidate_name for _, candidate_name in scored)


def _calibration_prefix_trace(*, trace: OutcomeTrace, evaluation_interval: int) -> OutcomeTrace:
    """Take an aligned warmup prefix for automatic controller-family selection."""
    sample_count = len(next(iter(trace.rewards_by_strategy.values()), ()))
    if sample_count <= evaluation_interval * 3:
        return trace

    calibration_samples = min(sample_count - evaluation_interval, max(evaluation_interval * 4, sample_count // 3))
    calibration_samples = max(evaluation_interval * 2, (calibration_samples // evaluation_interval) * evaluation_interval)
    calibration_samples = min(calibration_samples, sample_count)
    return OutcomeTrace(
        dataset_name=trace.dataset_name,
        score_name=trace.score_name,
        rewards_by_strategy={name: rewards[:calibration_samples] for name, rewards in trace.rewards_by_strategy.items()},
        successes_by_strategy={name: successes[:calibration_samples] for name, successes in trace.successes_by_strategy.items()},
        source_description=trace.source_description,
        source_url=trace.source_url,
    )


def _suggest_start_strategy(*, trace: OutcomeTrace, strategy_specs: tuple[ReplayStrategySpec, ...]) -> str:
    """Choose a safer incumbent from the first slice of rewards instead of hard-coding the first registry entry."""
    if not strategy_specs:
        raise ValueError("strategy_specs must not be empty")
    sample_count = len(next(iter(trace.rewards_by_strategy.values()), ()))
    if sample_count <= 0:
        return strategy_specs[0].name

    warmup_size = max(8, min(48, sample_count // 10 or 8))
    scored = []
    for spec in strategy_specs:
        rewards = trace.rewards_by_strategy.get(spec.name, ())
        if not rewards:
            continue
        score = fmean(rewards[:warmup_size])
        scored.append((score, spec.name))
    if not scored:
        return strategy_specs[0].name
    scored.sort(reverse=True)
    return scored[0][1]


def _resolve_start_strategy(
    *,
    trace: OutcomeTrace,
    strategy_specs: tuple[ReplayStrategySpec, ...],
    preset: _ReplayPreset | None,
) -> str:
    available_names = {spec.name for spec in strategy_specs}
    if preset is not None and preset.start_strategy in available_names:
        return str(preset.start_strategy)
    return _suggest_start_strategy(trace=trace, strategy_specs=strategy_specs)


def _build_calibration_trace(
    *,
    trace: OutcomeTrace,
    evaluation_interval: int,
    preset: _ReplayPreset | None,
) -> OutcomeTrace:
    sample_count = len(next(iter(trace.rewards_by_strategy.values())))
    calibration_fraction = preset.calibration_fraction if preset is not None else 0.22
    calibration_min_samples = preset.calibration_min_samples if preset is not None else 128
    calibration_min_blocks = preset.calibration_min_blocks if preset is not None else 4
    target_samples = max(
        calibration_min_samples,
        evaluation_interval * calibration_min_blocks,
        int(sample_count * calibration_fraction),
    )
    prefix_samples = min(sample_count, max(evaluation_interval, target_samples))
    if prefix_samples >= sample_count:
        prefix_samples = max(min(evaluation_interval, sample_count), sample_count - evaluation_interval)
    if prefix_samples <= 0:
        prefix_samples = sample_count
    return OutcomeTrace(
        dataset_name=f"{trace.dataset_name} calibration",
        score_name=trace.score_name,
        rewards_by_strategy={name: values[:prefix_samples] for name, values in trace.rewards_by_strategy.items()},
        successes_by_strategy={name: values[:prefix_samples] for name, values in trace.successes_by_strategy.items()},
        source_description=trace.source_description,
        source_url=trace.source_url,
    )


def _can_balance_portfolio(*, trace: OutcomeTrace, preset: _ReplayPreset | None) -> bool:
    if preset is None:
        return False
    if not preset.balance_warmup_samples or not preset.balance_block_size or not preset.balance_max_strategies:
        return False
    sample_count = len(next(iter(trace.rewards_by_strategy.values()), ()))
    return sample_count >= max(8, preset.balance_block_size * 2)


def _default_replay_preset(task_type: str) -> _ReplayPreset | None:
    normalized = task_type.strip().lower()
    if normalized == "classification":
        return _ReplayPreset(
            strategy_specs=_classification_strategies(),
            evaluation_interval=128,
            balance_warmup_samples=768,
            balance_block_size=128,
            balance_max_strategies=5,
            recent_leader_lookback_blocks=2,
            recent_leader_margin=0.01,
            recent_leader_warmup_blocks=3,
            recent_leader_cooldown_blocks=2,
            recent_leader_incumbent_floor=0.001,
            hard_window_size=128,
            hard_min_samples=2,
            hard_delta=0.0,
            hard_lambda_value=0.0,
            hard_switch_cost=0.002,
            use_target_lags=False,
            calibration_fraction=0.22,
            calibration_min_samples=192,
            calibration_min_blocks=4,
        )
    if normalized == "regression":
        return _ReplayPreset(
            strategy_specs=_regression_strategies(),
            evaluation_interval=64,
            balance_warmup_samples=512,
            balance_block_size=64,
            balance_max_strategies=5,
            recent_leader_lookback_blocks=2,
            recent_leader_margin=0.001,
            recent_leader_warmup_blocks=2,
            recent_leader_cooldown_blocks=1,
            recent_leader_incumbent_floor=0.001,
            hard_window_size=128,
            hard_min_samples=2,
            hard_delta=0.001,
            hard_lambda_value=0.0,
            hard_switch_cost=0.002,
            use_target_lags=True,
            calibration_fraction=0.22,
            calibration_min_samples=128,
            calibration_min_blocks=4,
        )
    return None


def _resolve_replay_preset(*, dataset_profile: str | None, task_type: str) -> _ReplayPreset | None:
    task_normalized = task_type.strip().lower()
    return _default_replay_preset(task_normalized)


def _builtin_dataset_options() -> tuple[BuiltinDatasetOption, ...]:
    return (
        BuiltinDatasetOption(
            dataset_id="waterflow",
            label="WaterFlow",
            description="Forecast hourly water flow under anomalies and pumping shifts.",
            task_type="regression",
            target_column="water_flow_lps",
            order_column="Time",
            source_label="River WaterFlow benchmark",
        ),
        BuiltinDatasetOption(
            dataset_id="bikes",
            label="Bikes",
            description="Forecast station bike demand from weather and station context.",
            task_type="regression",
            target_column="bikes_in_use",
            order_column="moment",
            source_label="River Bikes benchmark",
        ),
        BuiltinDatasetOption(
            dataset_id="elec2",
            label="Elec2",
            description="Classify electricity price direction on a non-stationary market stream.",
            task_type="classification",
            target_column="price_up",
            order_column="date",
            source_label="River Elec2 benchmark",
        ),
        BuiltinDatasetOption(
            dataset_id="trump_approval",
            label="TrumpApproval",
            description="Forecast approval rating changes from polling signals over time.",
            task_type="regression",
            target_column="approval",
            order_column="ordinal_date",
            source_label="River TrumpApproval benchmark",
        ),
    )


def _load_builtin_dataset_csv(*, option: BuiltinDatasetOption, max_rows: int) -> tuple[str, int]:
    dataset_factory = _builtin_dataset_factory(option.dataset_id)
    if dataset_factory is None:
        raise ValueError(f"no loader registered for built-in dataset {option.dataset_id!r}")

    stream = dataset_factory()
    rows: list[dict[str, Any]] = []
    for row_index, (features, target) in enumerate(stream, start=1):
        row = {key: _serialize_csv_value(value) for key, value in features.items()}
        if option.order_column and option.order_column not in row:
            row[option.order_column] = _serialize_csv_value(row_index)
        row[option.target_column] = _serialize_csv_value(target)
        rows.append(row)
        if row_index >= max_rows:
            break

    if not rows:
        raise ValueError(f"built-in dataset {option.label} returned no rows")

    fieldnames = list(rows[0].keys())
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue(), len(rows)


def _load_builtin_dataset_rows(*, dataset_id: str, max_rows: int) -> tuple[tuple[dict[str, Any], Any], ...]:
    dataset_factory = _builtin_dataset_factory(dataset_id)
    if dataset_factory is None:
        raise ValueError(f"no loader registered for built-in dataset {dataset_id!r}")
    rows: list[tuple[dict[str, Any], Any]] = []
    for row_index, (features, target) in enumerate(dataset_factory(), start=1):
        rows.append((dict(features), target))
        if row_index >= max_rows:
            break
    return tuple(rows)


def _builtin_dataset_factory(dataset_id: str):
    return {
        "waterflow": datasets.WaterFlow,
        "bikes": datasets.Bikes,
        "elec2": datasets.Elec2,
        "trump_approval": datasets.TrumpApproval,
    }.get(dataset_id)


def _count_builtin_dataset_rows(*, dataset_id: str) -> int:
    dataset_factory = _builtin_dataset_factory(dataset_id)
    if dataset_factory is None:
        raise ValueError(f"no loader registered for built-in dataset {dataset_id!r}")
    row_count = 0
    for row_count, _ in enumerate(dataset_factory(), start=1):
        pass
    if row_count <= 0:
        raise ValueError(f"built-in dataset {dataset_id!r} returned no rows")
    return row_count


def _serialize_csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _emit_progress(callback: Any | None, *, phase: str, progress: float, **extra: Any) -> None:
    if callback is None:
        return
    callback(phase=phase, progress=max(0.0, min(1.0, progress)), **extra)


def _build_dataset_job_id(dataset_name: str) -> str:
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in dataset_name).strip("-") or "dataset"
    return f"{slug}-{datetime.now(tz=UTC).strftime('%Y%m%d%H%M%S')}-{uuid4().hex[:8]}"


def _build_vertical_bar_plot(
    *,
    title: str,
    labels: tuple[str, ...],
    values: tuple[float, ...],
    highlight_index: int | None,
) -> bytes:
    canvas = PngCanvas(960, 420, background=(255, 255, 255))
    canvas.fill_rect(0, 0, 959, 55, (22, 50, 71))
    chart_left = 90
    chart_right = 900
    chart_top = 90
    chart_bottom = 340
    canvas.draw_line(chart_left, chart_bottom, chart_right, chart_bottom, (148, 163, 184), thickness=2)
    canvas.draw_line(chart_left, chart_top, chart_left, chart_bottom, (148, 163, 184), thickness=2)
    if not values:
        return canvas.to_png_bytes()
    minimum = min(min(values), 0.0)
    maximum = max(values)
    span = max(maximum - minimum, 1e-6)
    bar_width = max(24, (chart_right - chart_left) // max(1, len(values) * 2))
    gap = max(14, (chart_right - chart_left - (bar_width * len(values))) // max(1, len(values) + 1))
    for index, value in enumerate(values):
        x0 = chart_left + gap + index * (bar_width + gap)
        x1 = x0 + bar_width
        normalized = (value - minimum) / span
        y1 = chart_bottom - 1
        y0 = chart_bottom - int(normalized * (chart_bottom - chart_top))
        color = (15, 118, 110) if highlight_index == index else (31, 119, 180)
        canvas.fill_rect(x0, y0, x1, y1, color)
    return canvas.to_png_bytes()


def _build_switch_timeline_plot(decision_csv_path: Path) -> bytes:
    canvas = PngCanvas(960, 300, background=(255, 255, 255))
    canvas.fill_rect(0, 0, 959, 55, (22, 50, 71))
    chart_left = 70
    chart_right = 920
    chart_mid = 180
    canvas.draw_line(chart_left, chart_mid, chart_right, chart_mid, (148, 163, 184), thickness=2)
    if not decision_csv_path.exists():
        return canvas.to_png_bytes()
    with decision_csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return canvas.to_png_bytes()
    max_eval = max(int(row.get("evaluation_index", 0) or 0) for row in rows) or 1
    for row in rows:
        eval_index = int(row.get("evaluation_index", 0) or 0)
        switched = str(row.get("switched", "")).strip().lower() in {"1", "true", "yes"}
        x_coord = chart_left + int((eval_index / max_eval) * (chart_right - chart_left))
        color = (180, 83, 9) if switched else (148, 163, 184)
        radius = 6 if switched else 3
        canvas.fill_rect(x_coord - radius, chart_mid - radius, x_coord + radius, chart_mid + radius, color)
    return canvas.to_png_bytes()


def _build_history_entry(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "created_at_utc": payload.get("created_at_utc", ""),
        "dataset_name": payload.get("dataset_name", ""),
        "task_type": payload.get("task_type", ""),
        "policy_name": payload.get("policy_name", ""),
        "source_row_count": payload.get("source_row_count", 0),
        "source_rows_used": payload.get("source_rows_used", 0),
        "sample_count": payload.get("sample_count", 0),
        "adaptive_score": payload.get("adaptive_score", 0.0),
        "best_fixed_score": payload.get("best_fixed_score", 0.0),
        "delta_vs_best_fixed": payload.get("delta_vs_best_fixed", 0.0),
        "oracle_capture_ratio": payload.get("oracle_capture_ratio", 0.0),
        "switch_count": payload.get("switch_count", 0),
        "summary_json_path": payload.get("artifact_root", "") and str(Path(payload["artifact_root"]) / "dataset_lab_summary.json"),
        "report_md_path": payload.get("dataset_lab_report_md_path", payload.get("report_md_path", "")),
        "artifact_root": payload.get("artifact_root", ""),
        "score_plot_path": payload.get("score_plot_path", ""),
        "portfolio_plot_path": payload.get("portfolio_plot_path", ""),
        "switch_plot_path": payload.get("switch_plot_path", ""),
    }


def _build_dataset_lab_report(payload: dict[str, Any]) -> str:
    interpretation = payload.get("interpretation", [])
    caveats = payload.get("caveats", [])
    lines = [
        "# Dataset Lab Report",
        "",
        "## Summary",
        "",
        f"- created_at_utc: `{payload.get('created_at_utc', '')}`",
        f"- dataset_name: `{payload.get('dataset_name', '')}`",
        f"- task_type: `{payload.get('task_type', '')}`",
        f"- target_column: `{payload.get('target_column', '')}`",
        f"- policy_name: `{payload.get('policy_name', '')}`",
        f"- source_row_count: `{payload.get('source_row_count', 0)}`",
        f"- source_rows_used: `{payload.get('source_rows_used', 0)}`",
        f"- sample_count: `{payload.get('sample_count', 0)}`",
        f"- feature_count: `{payload.get('feature_count', 0)}`",
        f"- next_prediction: `{payload.get('next_prediction', '')}`",
        f"- prediction_confidence: `{payload.get('prediction_confidence', 0.0):.4f}` ({payload.get('confidence_label', '')})",
        "",
        "## Comparative Metrics",
        "",
        f"- adaptive_score: `{payload.get('adaptive_score', 0.0):.6f}`",
        f"- best_fixed_strategy: `{payload.get('best_fixed_strategy', '')}`",
        f"- best_fixed_score: `{payload.get('best_fixed_score', 0.0):.6f}`",
        f"- delta_vs_best_fixed: `{payload.get('delta_vs_best_fixed', 0.0):+.6f}`",
        f"- oracle_score: `{payload.get('oracle_score', 0.0):.6f}`",
        f"- oracle_gain: `{payload.get('oracle_gain', 0.0):.6f}`",
        f"- oracle_capture_ratio: `{payload.get('oracle_capture_ratio', 0.0) * 100.0:.2f}%`",
        f"- final_strategy: `{payload.get('final_strategy', '')}`",
        f"- switch_count: `{payload.get('switch_count', 0)}`",
        "",
        "## Interpretation",
        "",
    ]
    for line in interpretation:
        lines.append(f"- {line}")
    lines.extend(["", "## Caveats", ""])
    for line in caveats:
        lines.append(f"- {line}")
    lines.extend(
        [
            "",
            "## Privacy Note",
            "",
            "- Persisted reports intentionally exclude raw preview rows and full forecast-row payloads.",
            "- Raw uploaded trajectories are not copied into the human-readable report layer.",
            "",
            "## Visual Artifacts",
            "",
            f"- score_plot_path: `{payload.get('score_plot_path', '')}`",
            f"- portfolio_plot_path: `{payload.get('portfolio_plot_path', '')}`",
            f"- switch_plot_path: `{payload.get('switch_plot_path', '')}`",
            "",
            "## Artifact Paths",
            "",
            f"- artifact_root: `{payload.get('artifact_root', '')}`",
            f"- input_manifest_path: `{payload.get('input_manifest_path', '')}`",
            f"- replay_summary_json_path: `{payload.get('replay_summary_json_path', '')}`",
            f"- decision_csv_path: `{payload.get('decision_csv_path', '')}`",
            f"- replay_report_md_path: `{payload.get('report_md_path', '')}`",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def _split_observed_and_pending_rows(*, rows: list[dict[str, Any]], target_column: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    target_values = [str(row.get(target_column, "") or "").strip() for row in rows]
    last_observed_index = -1
    for index, value in enumerate(target_values):
        if not _is_missing_target_value(value):
            last_observed_index = index

    observed_rows: list[dict[str, Any]] = []
    pending_rows: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        target_value = target_values[index]
        if index > last_observed_index:
            if _is_missing_target_value(target_value):
                pending_rows.append(row)
            else:
                raise ValueError("rows with empty target values must appear only at the end of the dataset")
            continue
        if _is_missing_target_value(target_value):
            continue
        observed_rows.append(row)
    if len(pending_rows) > 1:
        raise ValueError("only one trailing row with an empty target is supported for direct next-step prediction")
    return observed_rows, pending_rows


def _is_missing_target_value(value: str) -> bool:
    return value.strip().lower() in {"", "na", "nan", "null", "none"}


def _parse_manual_rows(*, columns: tuple[str, ...], manual_text: str, target_column: str) -> tuple[dict[str, Any], ...]:
    stripped = manual_text.strip()
    if not stripped:
        raise ValueError("manual row text is empty")
    parsed = _parse_manual_rows_from_json(columns=columns, manual_text=stripped)
    if parsed:
        return parsed
    parsed = _parse_manual_rows_from_key_value(columns=columns, manual_text=stripped)
    if parsed:
        return parsed
    return _parse_manual_rows_from_positional_csv(columns=columns, manual_text=stripped, target_column=target_column)


def _parse_manual_rows_from_json(*, columns: tuple[str, ...], manual_text: str) -> tuple[dict[str, Any], ...]:
    try:
        payload = json.loads(manual_text)
    except json.JSONDecodeError:
        return ()
    items = payload if isinstance(payload, list) else [payload]
    rows: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("JSON manual rows must be one object or a list of objects")
        row = {column: _serialize_csv_value(item.get(column, "")) for column in columns}
        rows.append(row)
    return tuple(rows)


def _parse_manual_rows_from_key_value(*, columns: tuple[str, ...], manual_text: str) -> tuple[dict[str, Any], ...]:
    lines = [line.strip() for line in manual_text.splitlines() if line.strip()]
    if not lines or not all(("=" in line or ":" in line) for line in lines):
        return ()

    rows: list[dict[str, Any]] = []
    for line in lines:
        tokens = [token.strip() for token in re.split(r"[;,]\s*", line) if token.strip()]
        row = {column: "" for column in columns}
        parsed_pairs = 0
        for token in tokens:
            if "=" in token:
                key, value = token.split("=", 1)
            elif ":" in token:
                key, value = token.split(":", 1)
            else:
                continue
            normalized_key = key.strip()
            if normalized_key not in row:
                raise ValueError(f"manual row column not found in current schema: {normalized_key!r}")
            row[normalized_key] = value.strip()
            parsed_pairs += 1
        if parsed_pairs == 0:
            raise ValueError("manual row key-value input could not be interpreted")
        rows.append(row)
    return tuple(rows)


def _parse_manual_rows_from_positional_csv(
    *,
    columns: tuple[str, ...],
    manual_text: str,
    target_column: str,
) -> tuple[dict[str, Any], ...]:
    reader = csv.reader(io.StringIO(manual_text))
    rows: list[dict[str, Any]] = []
    for values in reader:
        if not any((value or "").strip() for value in values):
            continue
        cleaned = [value.strip() for value in values]
        if len(cleaned) == len(columns):
            rows.append({column: cleaned[index] for index, column in enumerate(columns)})
            continue
        if len(cleaned) == len(columns) - 1:
            row: dict[str, Any] = {}
            value_index = 0
            for column in columns:
                if column == target_column:
                    row[column] = ""
                else:
                    row[column] = cleaned[value_index]
                    value_index += 1
            rows.append(row)
            continue
        raise ValueError(
            f"manual positional row has {len(cleaned)} values, but the active schema expects {len(columns)} values "
            f"(or {len(columns) - 1} when omitting the target column)"
        )
    if not rows:
        raise ValueError("manual row text did not contain any usable row")
    return tuple(rows)


def _rows_to_csv_fragment(*, columns: tuple[str, ...], rows: Iterable[dict[str, Any]]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(columns), extrasaction="ignore", lineterminator="\n")
    for row in rows:
        writer.writerow({column: _serialize_csv_value(row.get(column, "")) for column in columns})
    return buffer.getvalue()
