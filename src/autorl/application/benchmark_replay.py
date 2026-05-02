"""Replay validation on real streaming datasets."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import csv
from datetime import datetime
import json
from math import exp, sqrt
from pathlib import Path
from statistics import fmean, pstdev
from typing import Any, Callable, Iterable, Iterator, Mapping
import io
import re
import urllib.request
import zipfile
import yaml

from river import datasets, linear_model, naive_bayes, neighbors, optim, preprocessing, tree
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor, RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer

from autorl.domain import Evaluator, MetaController, MetaControllerConfig, MetricsCollector


@dataclass(frozen=True, slots=True)
class ReplayStrategySpec:
    """One stationary strategy candidate used during benchmark replay."""

    name: str
    learning_rate: float
    description: str
    model_kind: str = "linear_sgd"


@dataclass(frozen=True, slots=True)
class PredictionTrace:
    """Precomputed classification trace for replay without re-running model updates."""

    dataset_name: str
    targets: tuple[bool, ...]
    predictions_by_strategy: dict[str, tuple[bool, ...]]
    source_description: str
    source_url: str


@dataclass(frozen=True, slots=True)
class OutcomeTrace:
    """Precomputed per-sample rewards for generic replay across tasks."""

    dataset_name: str
    score_name: str
    rewards_by_strategy: dict[str, tuple[float, ...]]
    successes_by_strategy: dict[str, tuple[bool, ...]]
    source_description: str
    source_url: str


@dataclass(frozen=True, slots=True)
class ReplayDecisionRecord:
    """Serializable replay decision row."""

    sample_index: int
    evaluation_index: int
    current_strategy: str
    candidate_strategy: str | None
    action: str
    switched: bool
    reason_code: str
    decision_margin: float | None
    decision_threshold: float
    reason: str


@dataclass(frozen=True, slots=True)
class ReplayBenchmarkResult:
    """Benchmark replay summary plus artifact paths."""

    dataset_name: str
    score_name: str
    policy_name: str
    sample_count: int
    evaluation_interval: int
    window_size: int
    start_strategy: str
    final_strategy: str
    switch_count: int
    adaptive_score: float
    best_fixed_strategy: str
    best_fixed_score: float
    delta_vs_best_fixed: float
    fixed_scores: dict[str, float]
    block_delta_mean: float
    block_delta_std: float
    block_delta_ci95: float
    block_count: int
    decision_csv_path: str
    summary_json_path: str
    report_md_path: str
    oracle_score: float = 0.0
    oracle_gain: float = 0.0
    oracle_capture_ratio: float = 0.0

    @property
    def adaptive_accuracy(self) -> float:
        """Compatibility alias for the first Elec2-only benchmark implementation."""
        return self.adaptive_score

    @property
    def best_fixed_accuracy(self) -> float:
        """Compatibility alias for the first Elec2-only benchmark implementation."""
        return self.best_fixed_score

    @property
    def fixed_accuracies(self) -> dict[str, float]:
        """Compatibility alias for the first Elec2-only benchmark implementation."""
        return self.fixed_scores


@dataclass(frozen=True, slots=True)
class ReplaySuiteResult:
    """Multi-dataset benchmark replay summary."""

    results: tuple[ReplayBenchmarkResult, ...]
    summary_json_path: str
    report_md_path: str


@dataclass(frozen=True, slots=True)
class BenchmarkProfile:
    """One H1/H2 benchmark replay profile loaded from YAML."""

    profile_name: str
    task_type: str
    controller_policy: str
    candidate_models: tuple[str, ...]
    notes: str


class _WindowedSklearnClassifier:
    """Sliding-window wrapper for non-incremental sklearn classifiers."""

    def __init__(self, estimator: object, *, window_size: int = 256, refit_interval: int = 16) -> None:
        self._estimator = estimator
        self._window_size = window_size
        self._refit_interval = max(1, refit_interval)
        self._vectorizer = DictVectorizer(sparse=False)
        self._features: list[dict[str, float]] = []
        self._targets: list[object] = []
        self._is_fitted = False
        self._samples_since_refit = 0

    def predict_one(self, features: Mapping[str, float]) -> object | None:
        if not self._is_fitted:
            return None
        matrix = self._vectorizer.transform([dict(features)])
        return self._estimator.predict(matrix)[0]

    def learn_one(self, features: Mapping[str, float], target: object) -> None:
        self._features.append(dict(features))
        self._targets.append(target)
        self._samples_since_refit += 1
        if len(self._features) > self._window_size:
            self._features.pop(0)
            self._targets.pop(0)
        if len(set(self._targets)) < 2:
            return
        if self._is_fitted and self._samples_since_refit < self._refit_interval:
            return
        matrix = self._vectorizer.fit_transform(self._features)
        self._estimator.fit(matrix, self._targets)
        self._is_fitted = True
        self._samples_since_refit = 0


class _WindowedSklearnRegressor:
    """Sliding-window wrapper for non-incremental sklearn regressors."""

    def __init__(self, estimator: object, *, window_size: int = 256, refit_interval: int = 16) -> None:
        self._estimator = estimator
        self._window_size = window_size
        self._refit_interval = max(1, refit_interval)
        self._vectorizer = DictVectorizer(sparse=False)
        self._features: list[dict[str, float]] = []
        self._targets: list[float] = []
        self._is_fitted = False
        self._samples_since_refit = 0

    def predict_one(self, features: Mapping[str, float]) -> float | None:
        if not self._is_fitted:
            return None
        matrix = self._vectorizer.transform([dict(features)])
        return float(self._estimator.predict(matrix)[0])

    def learn_one(self, features: Mapping[str, float], target: float) -> None:
        self._features.append(dict(features))
        self._targets.append(float(target))
        self._samples_since_refit += 1
        if len(self._features) > self._window_size:
            self._features.pop(0)
            self._targets.pop(0)
        if len(self._targets) < 4:
            return
        if self._is_fitted and self._samples_since_refit < self._refit_interval:
            return
        matrix = self._vectorizer.fit_transform(self._features)
        self._estimator.fit(matrix, self._targets)
        self._is_fitted = True
        self._samples_since_refit = 0


def build_candidate_model_registry(task_type: str) -> tuple[ReplayStrategySpec, ...]:
    """Return the benchmark replay candidate registry required by T3."""
    normalized = task_type.strip().lower()
    if normalized == "classification":
        return (
            ReplayStrategySpec("river_logreg", 0.05, "River logistic regression candidate", model_kind="linear_sgd"),
            ReplayStrategySpec("river_nb", 0.0, "River Gaussian naive Bayes candidate", model_kind="gaussian_nb"),
            ReplayStrategySpec(
                "river_hoeffding_tree",
                0.0,
                "River adaptive Hoeffding tree candidate",
                model_kind="hoeffding_tree_classifier",
            ),
            ReplayStrategySpec("windowed_rf", 0.0, "Sliding-window random forest candidate", model_kind="windowed_rf_classifier"),
            ReplayStrategySpec(
                "windowed_histgb",
                0.0,
                "Sliding-window histogram gradient boosting candidate",
                model_kind="windowed_histgb_classifier",
            ),
        )
    if normalized == "regression":
        return (
            ReplayStrategySpec("river_linreg", 0.001, "River linear regression candidate", model_kind="linear_sgd"),
            ReplayStrategySpec("river_pa", 0.0, "River passive-aggressive regression candidate", model_kind="pa_regressor"),
            ReplayStrategySpec(
                "river_hoeffding_tree",
                0.0,
                "River adaptive Hoeffding tree regression candidate",
                model_kind="hoeffding_tree_regressor",
            ),
            ReplayStrategySpec("windowed_rf", 0.0, "Sliding-window random forest regressor", model_kind="windowed_rf_regressor"),
            ReplayStrategySpec(
                "windowed_histgb",
                0.0,
                "Sliding-window histogram gradient boosting regressor",
                model_kind="windowed_histgb_regressor",
            ),
        )
    raise ValueError(f"unsupported benchmark registry task_type: {task_type!r}")


def _emit_replay_progress(
    progress_callback: Any | None,
    *,
    trace: OutcomeTrace,
    sample_index: int,
    sample_count: int,
    evaluation_index: int,
    active_strategy: str,
    candidate_strategy: str,
    switch_count: int,
    adaptive_rewards: list[float],
) -> None:
    if progress_callback is None or not adaptive_rewards:
        return
    prefix_rewards = {
        name: trace.rewards_by_strategy[name][: sample_index + 1]
        for name in trace.rewards_by_strategy
    }
    best_fixed_score_so_far = max(fmean(rewards) for rewards in prefix_rewards.values())
    adaptive_score_so_far = fmean(adaptive_rewards)
    oracle_score_so_far = sum(max(rewards[offset] for rewards in trace.rewards_by_strategy.values()) for offset in range(sample_index + 1)) / (sample_index + 1)
    oracle_gain_so_far = oracle_score_so_far - best_fixed_score_so_far
    delta_so_far = adaptive_score_so_far - best_fixed_score_so_far
    oracle_capture_so_far = 0.0 if oracle_gain_so_far <= 1e-12 else max(0.0, delta_so_far / oracle_gain_so_far)
    progress_callback(
        phase="adaptive_replay_running",
        progress=0.6 + (0.32 * ((sample_index + 1) / max(1, sample_count))),
        sample_index=sample_index + 1,
        total_samples=sample_count,
        evaluation_index=evaluation_index,
        active_strategy=active_strategy,
        candidate_strategy=candidate_strategy,
        switch_count=switch_count,
        adaptive_score_so_far=adaptive_score_so_far,
        best_fixed_score_so_far=best_fixed_score_so_far,
        delta_so_far=delta_so_far,
        oracle_capture_so_far=oracle_capture_so_far,
    )


def build_river_binary_prediction_trace(
    *,
    dataset_name: str,
    stream: Iterable[tuple[Mapping[str, object], bool]],
    strategies: Iterable[ReplayStrategySpec],
    source_description: str,
    source_url: str,
) -> PredictionTrace:
    """Replay one binary streaming dataset through a stationary strategy registry."""
    strategy_specs = tuple(strategies)
    models = {spec.name: _build_binary_classifier_model(spec) for spec in strategy_specs}

    targets: list[bool] = []
    predictions_by_strategy = {spec.name: [] for spec in strategy_specs}

    for features, target in stream:
        numeric_features = _default_feature_transform(features)
        label = bool(target)
        targets.append(label)
        for spec in strategy_specs:
            model = models[spec.name]
            prediction = model.predict_one(numeric_features)
            predictions_by_strategy[spec.name].append(False if prediction is None else bool(prediction))
            model.learn_one(numeric_features, label)

    return PredictionTrace(
        dataset_name=dataset_name,
        targets=tuple(targets),
        predictions_by_strategy={name: tuple(values) for name, values in predictions_by_strategy.items()},
        source_description=source_description,
        source_url=source_url,
    )


def build_river_multiclass_prediction_trace(
    *,
    dataset_name: str,
    stream: Iterable[tuple[Mapping[str, object], object]],
    strategies: Iterable[ReplayStrategySpec],
    source_description: str,
    source_url: str,
) -> PredictionTrace:
    """Replay one multi-class streaming dataset through stationary softmax learners."""
    strategy_specs = tuple(strategies)
    models = {spec.name: _build_multiclass_classifier_model(spec) for spec in strategy_specs}

    targets: list[bool | int | str] = []
    predictions_by_strategy = {spec.name: [] for spec in strategy_specs}

    for features, target in stream:
        numeric_features = _default_feature_transform(features)
        targets.append(target)
        for spec in strategy_specs:
            model = models[spec.name]
            prediction = model.predict_one(numeric_features)
            predictions_by_strategy[spec.name].append(target if prediction is None else prediction)
            model.learn_one(numeric_features, target)

    return PredictionTrace(
        dataset_name=dataset_name,
        targets=tuple(targets),
        predictions_by_strategy={name: tuple(values) for name, values in predictions_by_strategy.items()},
        source_description=source_description,
        source_url=source_url,
    )


def build_river_regression_outcome_trace(
    *,
    dataset_name: str,
    stream: Iterable[tuple[Mapping[str, object], float | int]],
    strategies: Iterable[ReplayStrategySpec],
    source_description: str,
    source_url: str,
    feature_transform: Callable[[Mapping[str, object]], dict[str, float]] | None = None,
    max_samples: int | None = None,
) -> OutcomeTrace:
    """Replay one regression stream and convert losses into bounded rewards."""
    strategy_specs = tuple(strategies)
    models = {spec.name: _build_regressor_model(spec) for spec in strategy_specs}

    transform = feature_transform or _default_feature_transform
    targets: list[float] = []
    predictions_by_strategy: dict[str, list[float]] = {spec.name: [] for spec in strategy_specs}

    for sample_index, (features, target) in enumerate(stream, start=1):
        numeric_features = transform(features)
        label = float(target)
        targets.append(label)
        for spec in strategy_specs:
            model = models[spec.name]
            prediction = model.predict_one(numeric_features)
            predictions_by_strategy[spec.name].append(0.0 if prediction is None else float(prediction))
            model.learn_one(numeric_features, label)
        if max_samples is not None and sample_index >= max_samples:
            break

    scale = pstdev(targets) if len(targets) > 1 else 1.0
    if scale <= 1e-9:
        scale = max(1.0, abs(fmean(targets)) if targets else 1.0)

    rewards_by_strategy: dict[str, tuple[float, ...]] = {}
    successes_by_strategy: dict[str, tuple[bool, ...]] = {}
    for name, predictions in predictions_by_strategy.items():
        rewards: list[float] = []
        successes: list[bool] = []
        for prediction, target in zip(predictions, targets):
            error = abs(prediction - target)
            rewards.append(1.0 / (1.0 + (error / scale)))
            successes.append(error <= scale)
        rewards_by_strategy[name] = tuple(rewards)
        successes_by_strategy[name] = tuple(successes)

    return OutcomeTrace(
        dataset_name=dataset_name,
        score_name="normalized_reward",
        rewards_by_strategy=rewards_by_strategy,
        successes_by_strategy=successes_by_strategy,
        source_description=source_description,
        source_url=source_url,
    )


def build_river_multioutput_regression_outcome_trace(
    *,
    dataset_name: str,
    stream: Iterable[tuple[Mapping[str, object], Mapping[str, float | int]]],
    strategies: Iterable[ReplayStrategySpec],
    source_description: str,
    source_url: str,
    feature_transform: Callable[[Mapping[str, object]], dict[str, float]] | None = None,
    max_samples: int | None = None,
) -> OutcomeTrace:
    """Replay one multi-output regression stream and convert losses into bounded rewards."""
    strategy_specs = tuple(strategies)
    transform = feature_transform or _default_feature_transform

    targets_by_output: dict[str, list[float]] = {}
    predictions_by_strategy_by_output: dict[str, dict[str, list[float]]] = {
        spec.name: {} for spec in strategy_specs
    }
    models_by_strategy_and_output: dict[str, dict[str, object]] = {spec.name: {} for spec in strategy_specs}
    sample_count = 0

    for sample_index, (features, target_mapping) in enumerate(stream, start=1):
        if any(target is None for target in target_mapping.values()):
            continue
        numeric_features = transform(features)
        for output_name, target in target_mapping.items():
            label = float(target)
            targets_by_output.setdefault(output_name, []).append(label)
            for spec in strategy_specs:
                models_for_spec = models_by_strategy_and_output[spec.name]
                if output_name not in models_for_spec:
                    models_for_spec[output_name] = _build_regressor_model(spec)
                    predictions_by_strategy_by_output[spec.name][output_name] = []
                model = models_for_spec[output_name]
                prediction = model.predict_one(numeric_features)
                predictions_by_strategy_by_output[spec.name][output_name].append(0.0 if prediction is None else float(prediction))
                model.learn_one(numeric_features, label)
        sample_count += 1
        if max_samples is not None and sample_index >= max_samples:
            break

    scales_by_output = {
        output_name: _resolve_regression_scale(targets)
        for output_name, targets in targets_by_output.items()
    }
    output_names = tuple(sorted(targets_by_output))

    rewards_by_strategy: dict[str, tuple[float, ...]] = {}
    successes_by_strategy: dict[str, tuple[bool, ...]] = {}
    for spec in strategy_specs:
        rewards: list[float] = []
        successes: list[bool] = []
        for index in range(sample_count):
            reward_components: list[float] = []
            success_components: list[bool] = []
            for output_name in output_names:
                target = targets_by_output[output_name][index]
                prediction = predictions_by_strategy_by_output[spec.name][output_name][index]
                scale = scales_by_output[output_name]
                error = abs(prediction - target)
                reward_components.append(1.0 / (1.0 + (error / scale)))
                success_components.append(error <= scale)
            rewards.append(fmean(reward_components) if reward_components else 0.0)
            successes.append(all(success_components))
        rewards_by_strategy[spec.name] = tuple(rewards)
        successes_by_strategy[spec.name] = tuple(successes)

    return OutcomeTrace(
        dataset_name=dataset_name,
        score_name="normalized_multioutput_reward",
        rewards_by_strategy=rewards_by_strategy,
        successes_by_strategy=successes_by_strategy,
        source_description=source_description,
        source_url=source_url,
    )


class BenchmarkReplayRunner:
    """Run metacontrolled replay over precomputed stationary-strategy traces."""

    def __init__(
        self,
        *,
        controller: MetaController | None = None,
        evaluator: Evaluator | None = None,
    ) -> None:
        self._controller = controller or MetaController()
        self._evaluator = evaluator or Evaluator()
        self._profile_trace_cache: dict[tuple[str, str, tuple[str, ...], int | None], OutcomeTrace] = {}

    def run_prediction_trace(
        self,
        *,
        trace: PredictionTrace,
        output_root: str | Path,
        meta_config: MetaControllerConfig,
        evaluation_interval: int,
        start_strategy: str,
    ) -> ReplayBenchmarkResult:
        """Run adaptive replay for binary classification outcomes."""
        self._validate_prediction_trace(trace)
        outcome_trace = OutcomeTrace(
            dataset_name=trace.dataset_name,
            score_name="accuracy",
            rewards_by_strategy={
                name: tuple(float(prediction == target) for prediction, target in zip(predictions, trace.targets))
                for name, predictions in trace.predictions_by_strategy.items()
            },
            successes_by_strategy={
                name: tuple(prediction == target for prediction, target in zip(predictions, trace.targets))
                for name, predictions in trace.predictions_by_strategy.items()
            },
            source_description=trace.source_description,
            source_url=trace.source_url,
        )
        return self.run_outcome_trace(
            trace=outcome_trace,
            output_root=output_root,
            meta_config=meta_config,
            evaluation_interval=evaluation_interval,
            start_strategy=start_strategy,
        )

    def run_outcome_trace(
        self,
        *,
        trace: OutcomeTrace,
        output_root: str | Path,
        meta_config: MetaControllerConfig,
        evaluation_interval: int,
        start_strategy: str,
        progress_callback: Any | None = None,
    ) -> ReplayBenchmarkResult:
        """Run adaptive replay for generic per-sample reward outcomes."""
        if evaluation_interval <= 0:
            raise ValueError("evaluation_interval must be positive")
        if start_strategy not in trace.rewards_by_strategy:
            raise ValueError(f"unknown start_strategy: {start_strategy!r}")

        sample_count = self._validate_outcome_trace(trace)
        collectors = {name: MetricsCollector() for name in trace.rewards_by_strategy}
        window_histories = {name: [] for name in trace.rewards_by_strategy}
        current_strategy = start_strategy
        adaptive_rewards: list[float] = []
        decisions: list[ReplayDecisionRecord] = []

        for sample_index in range(sample_count):
            for name in trace.rewards_by_strategy:
                collectors[name].record_episode(
                    episode_index=sample_index,
                    reward=trace.rewards_by_strategy[name][sample_index],
                    success=trace.successes_by_strategy[name][sample_index],
                    active_strategy=name,
                    steps=1,
                    compute_cost=0.0,
                    learning_progress=0.0,
                )

            adaptive_rewards.append(trace.rewards_by_strategy[current_strategy][sample_index])

            if (sample_index + 1) % evaluation_interval != 0:
                continue

            for name, collector in collectors.items():
                window_metric = self._latest_window_metric(collector, meta_config)
                if window_metric is not None:
                    window_histories[name].append(window_metric)

            candidate_strategy = self._select_candidate(
                current_strategy=current_strategy,
                window_histories=window_histories,
                meta_config=meta_config,
            )
            if candidate_strategy is None or len(window_histories[current_strategy]) < meta_config.min_samples:
                _emit_replay_progress(
                    progress_callback,
                    trace=trace,
                    sample_index=sample_index,
                    sample_count=sample_count,
                    evaluation_index=max(0, len(window_histories[current_strategy]) - 1),
                    active_strategy=current_strategy,
                    candidate_strategy="",
                    switch_count=sum(1 for decision in decisions if decision.switched),
                    adaptive_rewards=adaptive_rewards,
                )
                continue

            meta_decision = self._controller.decide(
                evaluation_index=len(window_histories[current_strategy]) - 1,
                current_strategy=current_strategy,
                candidate_strategy=candidate_strategy,
                current_metrics=window_histories[current_strategy][-meta_config.min_samples :],
                candidate_metrics=window_histories[candidate_strategy][-meta_config.min_samples :],
                meta_config=meta_config,
            ).decision
            decisions.append(
                ReplayDecisionRecord(
                    sample_index=sample_index,
                    evaluation_index=meta_decision.evaluation_index,
                    current_strategy=meta_decision.current_strategy,
                    candidate_strategy=meta_decision.candidate_strategy,
                    action=meta_decision.action.value,
                    switched=meta_decision.switched,
                    reason_code=meta_decision.reason_code.value,
                    decision_margin=meta_decision.decision_margin,
                    decision_threshold=meta_decision.decision_threshold,
                    reason=meta_decision.reason,
                )
            )
            if meta_decision.switched and meta_decision.candidate_strategy is not None:
                current_strategy = meta_decision.candidate_strategy
            _emit_replay_progress(
                progress_callback,
                trace=trace,
                sample_index=sample_index,
                sample_count=sample_count,
                evaluation_index=meta_decision.evaluation_index,
                active_strategy=current_strategy,
                candidate_strategy=meta_decision.candidate_strategy or "",
                switch_count=sum(1 for decision in decisions if decision.switched),
                adaptive_rewards=adaptive_rewards,
            )

        fixed_scores = {
            name: fmean(rewards)
            for name, rewards in trace.rewards_by_strategy.items()
        }
        best_fixed_strategy, best_fixed_score = max(
            fixed_scores.items(),
            key=lambda item: (item[1], item[0]),
        )
        block_delta_mean, block_delta_std, block_delta_ci95, block_count = self._block_delta_statistics(
            adaptive_rewards=tuple(adaptive_rewards),
            best_fixed_rewards=trace.rewards_by_strategy[best_fixed_strategy],
            block_size=evaluation_interval,
        )
        result = ReplayBenchmarkResult(
            dataset_name=trace.dataset_name,
            score_name=trace.score_name,
            policy_name="hard_switch_lcb",
            sample_count=sample_count,
            evaluation_interval=evaluation_interval,
            window_size=meta_config.window_size,
            start_strategy=start_strategy,
            final_strategy=current_strategy,
            switch_count=sum(1 for decision in decisions if decision.switched),
            adaptive_score=fmean(adaptive_rewards),
            best_fixed_strategy=best_fixed_strategy,
            best_fixed_score=best_fixed_score,
            delta_vs_best_fixed=fmean(adaptive_rewards) - best_fixed_score,
            fixed_scores=fixed_scores,
            block_delta_mean=block_delta_mean,
            block_delta_std=block_delta_std,
            block_delta_ci95=block_delta_ci95,
            block_count=block_count,
            decision_csv_path="",
            summary_json_path="",
            report_md_path="",
        )
        return self._persist_result(
            result=result,
            trace=trace,
            decisions=decisions,
            output_root=output_root,
        )

    def run_outcome_trace_with_hedge(
        self,
        *,
        trace: OutcomeTrace,
        output_root: str | Path,
        evaluation_interval: int,
        start_strategy: str | None = None,
        eta: float = 0.5,
        switch_threshold: float = 0.02,
        warmup_samples: int = 64,
        progress_callback: Any | None = None,
    ) -> ReplayBenchmarkResult:
        """Run a safer online-expert controller with full-information Hedge updates.

        This mode targets low regret with respect to the best fixed strategy.
        It does not rely on uncertainty gating and therefore reacts faster when
        the leader among stationary strategies changes frequently.
        """
        if evaluation_interval <= 0:
            raise ValueError("evaluation_interval must be positive")
        if eta <= 0.0:
            raise ValueError("eta must be positive")
        sample_count = self._validate_outcome_trace(trace)

        strategy_names = tuple(sorted(trace.rewards_by_strategy))
        if not strategy_names:
            raise ValueError("trace.rewards_by_strategy must not be empty")
        current_strategy = start_strategy or strategy_names[0]
        if current_strategy not in trace.rewards_by_strategy:
            raise ValueError(f"unknown start_strategy: {current_strategy!r}")

        weights = {name: 1.0 for name in strategy_names}
        cumulative_rewards = {name: 0.0 for name in strategy_names}
        adaptive_rewards: list[float] = []
        decisions: list[ReplayDecisionRecord] = []
        switch_count = 0

        for sample_index in range(sample_count):
            if sample_index + 1 == warmup_samples:
                warmup_winner = max(
                    strategy_names,
                    key=lambda name: cumulative_rewards[name],
                )
                if warmup_winner != current_strategy:
                    switch_count += 1
                    decisions.append(
                        ReplayDecisionRecord(
                            sample_index=sample_index,
                            evaluation_index=sample_index // evaluation_interval,
                            current_strategy=current_strategy,
                            candidate_strategy=warmup_winner,
                            action="switch",
                            switched=True,
                            reason_code="warmup_leader",
                            decision_margin=None,
                            decision_threshold=switch_threshold,
                            reason=(
                                "Switch after warmup because cumulative reward leader differs from "
                                f"the starting strategy: {warmup_winner}."
                            ),
                        )
                    )
                    current_strategy = warmup_winner

            chosen_reward = trace.rewards_by_strategy[current_strategy][sample_index]
            adaptive_rewards.append(chosen_reward)

            for name in strategy_names:
                reward = trace.rewards_by_strategy[name][sample_index]
                cumulative_rewards[name] += reward
                weights[name] *= exp(eta * reward)

            if (sample_index + 1) % evaluation_interval != 0:
                continue

            total_weight = sum(weights.values())
            normalized_weights = {
                name: (weights[name] / total_weight if total_weight > 0.0 else 1.0 / len(strategy_names))
                for name in strategy_names
            }
            candidate_strategy = max(
                strategy_names,
                key=lambda name: (normalized_weights[name], cumulative_rewards[name], name),
            )
            current_weight = normalized_weights[current_strategy]
            candidate_weight = normalized_weights[candidate_strategy]
            if candidate_strategy == current_strategy:
                decisions.append(
                    ReplayDecisionRecord(
                        sample_index=sample_index,
                        evaluation_index=sample_index // evaluation_interval,
                        current_strategy=current_strategy,
                        candidate_strategy=candidate_strategy,
                        action="stay",
                        switched=False,
                        reason_code="hedge_same_leader",
                        decision_margin=0.0,
                        decision_threshold=switch_threshold,
                        reason="Stay because the current strategy remains the highest-weight Hedge expert.",
                    )
                )
                continue

            margin = candidate_weight - current_weight
            if margin >= switch_threshold:
                switch_count += 1
                decisions.append(
                    ReplayDecisionRecord(
                        sample_index=sample_index,
                        evaluation_index=sample_index // evaluation_interval,
                        current_strategy=current_strategy,
                        candidate_strategy=candidate_strategy,
                        action="switch",
                        switched=True,
                        reason_code="hedge_weight_advantage",
                        decision_margin=margin,
                        decision_threshold=switch_threshold,
                        reason=(
                            "Switch because candidate Hedge weight exceeds current weight beyond the switch threshold: "
                            f"{candidate_weight:.4f} - {current_weight:.4f} = {margin:.4f} >= {switch_threshold:.4f}."
                        ),
                    )
                )
                current_strategy = candidate_strategy
            else:
                decisions.append(
                    ReplayDecisionRecord(
                        sample_index=sample_index,
                        evaluation_index=sample_index // evaluation_interval,
                        current_strategy=current_strategy,
                        candidate_strategy=candidate_strategy,
                        action="stay",
                        switched=False,
                        reason_code="hedge_margin_too_small",
                        decision_margin=margin,
                        decision_threshold=switch_threshold,
                        reason=(
                            "Stay because candidate Hedge weight advantage is too small: "
                            f"margin={margin:.4f}, threshold={switch_threshold:.4f}."
                        ),
                    )
                )
            _emit_replay_progress(
                progress_callback,
                trace=trace,
                sample_index=sample_index,
                sample_count=sample_count,
                evaluation_index=sample_index // evaluation_interval,
                active_strategy=current_strategy,
                candidate_strategy=candidate_strategy,
                switch_count=switch_count,
                adaptive_rewards=adaptive_rewards,
            )

        fixed_scores = {name: fmean(trace.rewards_by_strategy[name]) for name in strategy_names}
        best_fixed_strategy, best_fixed_score = max(
            fixed_scores.items(),
            key=lambda item: (item[1], item[0]),
        )
        block_delta_mean, block_delta_std, block_delta_ci95, block_count = self._block_delta_statistics(
            adaptive_rewards=tuple(adaptive_rewards),
            best_fixed_rewards=trace.rewards_by_strategy[best_fixed_strategy],
            block_size=evaluation_interval,
        )
        result = ReplayBenchmarkResult(
            dataset_name=trace.dataset_name,
            score_name=trace.score_name,
            policy_name="hedge_portfolio",
            sample_count=sample_count,
            evaluation_interval=evaluation_interval,
            window_size=evaluation_interval,
            start_strategy=start_strategy or strategy_names[0],
            final_strategy=current_strategy,
            switch_count=switch_count,
            adaptive_score=fmean(adaptive_rewards),
            best_fixed_strategy=best_fixed_strategy,
            best_fixed_score=best_fixed_score,
            delta_vs_best_fixed=fmean(adaptive_rewards) - best_fixed_score,
            fixed_scores=fixed_scores,
            block_delta_mean=block_delta_mean,
            block_delta_std=block_delta_std,
            block_delta_ci95=block_delta_ci95,
            block_count=block_count,
            decision_csv_path="",
            summary_json_path="",
            report_md_path="",
        )
        return self._persist_result(
            result=result,
            trace=trace,
            decisions=decisions,
            output_root=output_root,
        )

    def run_outcome_trace_with_fixed_share(
        self,
        *,
        trace: OutcomeTrace,
        output_root: str | Path,
        evaluation_interval: int,
        start_strategy: str | None = None,
        eta: float = 0.6,
        share_alpha: float = 0.02,
        switch_threshold: float = 0.02,
        warmup_samples: int = 64,
        progress_callback: Any | None = None,
    ) -> ReplayBenchmarkResult:
        """Track the best shifting expert with Fixed-Share style weight sharing.

        This controller differs conceptually from Hedge in one key way: after every
        multiplicative update it redistributes a small fraction of total weight across
        all experts. That allows previously weak experts to recover quickly when the
        environment re-enters a regime where they become strong again.
        """
        if evaluation_interval <= 0:
            raise ValueError("evaluation_interval must be positive")
        if eta <= 0.0:
            raise ValueError("eta must be positive")
        if not 0.0 < share_alpha < 1.0:
            raise ValueError("share_alpha must lie in (0, 1)")
        if switch_threshold < 0.0:
            raise ValueError("switch_threshold must not be negative")

        sample_count = self._validate_outcome_trace(trace)
        strategy_names = tuple(sorted(trace.rewards_by_strategy))
        if not strategy_names:
            raise ValueError("trace.rewards_by_strategy must not be empty")
        current_strategy = start_strategy or strategy_names[0]
        if current_strategy not in trace.rewards_by_strategy:
            raise ValueError(f"unknown start_strategy: {current_strategy!r}")

        weights = {name: 1.0 / len(strategy_names) for name in strategy_names}
        cumulative_rewards = {name: 0.0 for name in strategy_names}
        adaptive_rewards: list[float] = []
        decisions: list[ReplayDecisionRecord] = []
        switch_count = 0

        for sample_index in range(sample_count):
            if sample_index + 1 == warmup_samples:
                warmup_winner = max(
                    strategy_names,
                    key=lambda name: cumulative_rewards[name],
                )
                if warmup_winner != current_strategy:
                    switch_count += 1
                    decisions.append(
                        ReplayDecisionRecord(
                            sample_index=sample_index,
                            evaluation_index=sample_index // evaluation_interval,
                            current_strategy=current_strategy,
                            candidate_strategy=warmup_winner,
                            action="switch",
                            switched=True,
                            reason_code="fixed_share_warmup_leader",
                            decision_margin=None,
                            decision_threshold=switch_threshold,
                            reason=(
                                "Switch after warmup because the cumulative reward leader differs from "
                                f"the starting strategy: {warmup_winner}."
                            ),
                        )
                    )
                    current_strategy = warmup_winner

            chosen_reward = trace.rewards_by_strategy[current_strategy][sample_index]
            adaptive_rewards.append(chosen_reward)

            post_loss_weights: dict[str, float] = {}
            total_post_loss_weight = 0.0
            for name in strategy_names:
                reward = trace.rewards_by_strategy[name][sample_index]
                cumulative_rewards[name] += reward
                updated_weight = weights[name] * exp(eta * reward)
                post_loss_weights[name] = updated_weight
                total_post_loss_weight += updated_weight

            shared_base = (share_alpha * total_post_loss_weight) / len(strategy_names)
            next_weights = {
                name: shared_base + ((1.0 - share_alpha) * post_loss_weights[name])
                for name in strategy_names
            }
            total_next_weight = sum(next_weights.values())
            if total_next_weight <= 0.0:
                weights = {name: 1.0 / len(strategy_names) for name in strategy_names}
            else:
                weights = {
                    name: next_weights[name] / total_next_weight
                    for name in strategy_names
                }

            if (sample_index + 1) % evaluation_interval != 0:
                continue

            candidate_strategy = max(
                strategy_names,
                key=lambda name: (weights[name], cumulative_rewards[name], name),
            )
            current_weight = weights[current_strategy]
            candidate_weight = weights[candidate_strategy]
            if candidate_strategy == current_strategy:
                decisions.append(
                    ReplayDecisionRecord(
                        sample_index=sample_index,
                        evaluation_index=sample_index // evaluation_interval,
                        current_strategy=current_strategy,
                        candidate_strategy=candidate_strategy,
                        action="stay",
                        switched=False,
                        reason_code="fixed_share_same_leader",
                        decision_margin=0.0,
                        decision_threshold=switch_threshold,
                        reason="Stay because the current strategy remains the highest-weight Fixed-Share expert.",
                    )
                )
                continue

            margin = candidate_weight - current_weight
            if margin >= switch_threshold:
                switch_count += 1
                decisions.append(
                    ReplayDecisionRecord(
                        sample_index=sample_index,
                        evaluation_index=sample_index // evaluation_interval,
                        current_strategy=current_strategy,
                        candidate_strategy=candidate_strategy,
                        action="switch",
                        switched=True,
                        reason_code="fixed_share_weight_advantage",
                        decision_margin=margin,
                        decision_threshold=switch_threshold,
                        reason=(
                            "Switch because Fixed-Share reallocated enough weight to the candidate expert: "
                            f"{candidate_weight:.4f} - {current_weight:.4f} = {margin:.4f} >= {switch_threshold:.4f}."
                        ),
                    )
                )
                current_strategy = candidate_strategy
            else:
                decisions.append(
                    ReplayDecisionRecord(
                        sample_index=sample_index,
                        evaluation_index=sample_index // evaluation_interval,
                        current_strategy=current_strategy,
                        candidate_strategy=candidate_strategy,
                        action="stay",
                        switched=False,
                        reason_code="fixed_share_margin_too_small",
                        decision_margin=margin,
                        decision_threshold=switch_threshold,
                        reason=(
                            "Stay because the recovered Fixed-Share candidate is still too close to the incumbent: "
                            f"margin={margin:.4f}, threshold={switch_threshold:.4f}."
                        ),
                    )
                )
            _emit_replay_progress(
                progress_callback,
                trace=trace,
                sample_index=sample_index,
                sample_count=sample_count,
                evaluation_index=sample_index // evaluation_interval,
                active_strategy=current_strategy,
                candidate_strategy=candidate_strategy,
                switch_count=switch_count,
                adaptive_rewards=adaptive_rewards,
            )

        fixed_scores = {name: fmean(trace.rewards_by_strategy[name]) for name in strategy_names}
        best_fixed_strategy, best_fixed_score = max(
            fixed_scores.items(),
            key=lambda item: (item[1], item[0]),
        )
        block_delta_mean, block_delta_std, block_delta_ci95, block_count = self._block_delta_statistics(
            adaptive_rewards=tuple(adaptive_rewards),
            best_fixed_rewards=trace.rewards_by_strategy[best_fixed_strategy],
            block_size=evaluation_interval,
        )
        result = ReplayBenchmarkResult(
            dataset_name=trace.dataset_name,
            score_name=trace.score_name,
            policy_name="fixed_share_portfolio",
            sample_count=sample_count,
            evaluation_interval=evaluation_interval,
            window_size=evaluation_interval,
            start_strategy=start_strategy or strategy_names[0],
            final_strategy=current_strategy,
            switch_count=switch_count,
            adaptive_score=fmean(adaptive_rewards),
            best_fixed_strategy=best_fixed_strategy,
            best_fixed_score=best_fixed_score,
            delta_vs_best_fixed=fmean(adaptive_rewards) - best_fixed_score,
            fixed_scores=fixed_scores,
            block_delta_mean=block_delta_mean,
            block_delta_std=block_delta_std,
            block_delta_ci95=block_delta_ci95,
            block_count=block_count,
            decision_csv_path="",
            summary_json_path="",
            report_md_path="",
        )
        return self._persist_result(
            result=result,
            trace=trace,
            decisions=decisions,
            output_root=output_root,
        )

    def run_outcome_trace_with_recent_leader(
        self,
        *,
        trace: OutcomeTrace,
        output_root: str | Path,
        evaluation_interval: int,
        start_strategy: str | None = None,
        lookback_blocks: int = 4,
        margin: float = 0.0,
        warmup_blocks: int = 1,
        cooldown_blocks: int = 0,
        incumbent_floor: float = 0.0,
        progress_callback: Any | None = None,
    ) -> ReplayBenchmarkResult:
        """Run a recent-leader champion-challenger controller on a reward trace."""
        if evaluation_interval <= 0:
            raise ValueError("evaluation_interval must be positive")
        if lookback_blocks <= 0:
            raise ValueError("lookback_blocks must be positive")
        if warmup_blocks <= 0:
            raise ValueError("warmup_blocks must be positive")
        if cooldown_blocks < 0:
            raise ValueError("cooldown_blocks must not be negative")
        if margin < 0.0:
            raise ValueError("margin must not be negative")
        if incumbent_floor < 0.0:
            raise ValueError("incumbent_floor must not be negative")

        sample_count = self._validate_outcome_trace(trace)
        strategy_names = tuple(sorted(trace.rewards_by_strategy))
        if not strategy_names:
            raise ValueError("trace.rewards_by_strategy must not be empty")

        current_strategy = start_strategy or strategy_names[0]
        if current_strategy not in trace.rewards_by_strategy:
            raise ValueError(f"unknown start_strategy: {current_strategy!r}")

        adaptive_rewards: list[float] = []
        decisions: list[ReplayDecisionRecord] = []
        switch_count = 0
        completed_blocks = 0
        cooldown_remaining = 0
        block_reward_sums = {name: 0.0 for name in strategy_names}
        block_reward_histories = {name: [] for name in strategy_names}
        cumulative_reward_sums = {name: 0.0 for name in strategy_names}

        for sample_index in range(sample_count):
            adaptive_rewards.append(trace.rewards_by_strategy[current_strategy][sample_index])
            for name in strategy_names:
                reward = trace.rewards_by_strategy[name][sample_index]
                cumulative_reward_sums[name] += reward
                block_reward_sums[name] += reward

            if (sample_index + 1) % evaluation_interval != 0:
                continue

            completed_blocks += 1
            for name in strategy_names:
                block_reward_histories[name].append(block_reward_sums[name] / evaluation_interval)
                block_reward_sums[name] = 0.0

            evaluation_index = completed_blocks - 1
            if completed_blocks < warmup_blocks:
                continue

            if completed_blocks == warmup_blocks:
                leader = max(
                    strategy_names,
                    key=lambda name: (
                        self._recent_block_mean(block_reward_histories[name], lookback_blocks),
                        cumulative_reward_sums[name],
                        name,
                    ),
                )
                if leader != current_strategy:
                    switch_count += 1
                    cooldown_remaining = cooldown_blocks
                    decisions.append(
                        ReplayDecisionRecord(
                            sample_index=sample_index,
                            evaluation_index=evaluation_index,
                            current_strategy=current_strategy,
                            candidate_strategy=leader,
                            action="switch",
                            switched=True,
                            reason_code="recent_leader_warmup",
                            decision_margin=None,
                            decision_threshold=margin,
                            reason=(
                                "Switch after warmup because the recent block leader outperformed the initial incumbent: "
                                f"{leader}."
                            ),
                        )
                    )
                    current_strategy = leader
                else:
                    decisions.append(
                        ReplayDecisionRecord(
                            sample_index=sample_index,
                            evaluation_index=evaluation_index,
                            current_strategy=current_strategy,
                            candidate_strategy=leader,
                            action="stay",
                            switched=False,
                            reason_code="recent_leader_warmup_same",
                            decision_margin=0.0,
                            decision_threshold=margin,
                            reason="Stay after warmup because the current strategy is already the recent leader.",
                        )
                    )
                _emit_replay_progress(
                    progress_callback,
                    trace=trace,
                    sample_index=sample_index,
                    sample_count=sample_count,
                    evaluation_index=evaluation_index,
                    active_strategy=current_strategy,
                    candidate_strategy=leader,
                    switch_count=switch_count,
                    adaptive_rewards=adaptive_rewards,
                )
                continue

            if cooldown_remaining > 0:
                decisions.append(
                    ReplayDecisionRecord(
                        sample_index=sample_index,
                        evaluation_index=evaluation_index,
                        current_strategy=current_strategy,
                        candidate_strategy=current_strategy,
                        action="stay",
                        switched=False,
                        reason_code="recent_leader_cooldown",
                        decision_margin=0.0,
                        decision_threshold=margin,
                        reason=(
                            "Stay because the controller is within the post-switch cooldown window: "
                            f"{cooldown_remaining} block(s) remaining."
                        ),
                    )
                )
                cooldown_remaining -= 1
                _emit_replay_progress(
                    progress_callback,
                    trace=trace,
                    sample_index=sample_index,
                    sample_count=sample_count,
                    evaluation_index=evaluation_index,
                    active_strategy=current_strategy,
                    candidate_strategy=current_strategy,
                    switch_count=switch_count,
                    adaptive_rewards=adaptive_rewards,
                )
                continue

            recent_scores = {
                name: self._recent_block_mean(block_reward_histories[name], lookback_blocks)
                for name in strategy_names
            }
            candidate_strategy = max(
                strategy_names,
                key=lambda name: (
                    recent_scores[name],
                    cumulative_reward_sums[name],
                    name,
                ),
            )
            candidate_score = recent_scores[candidate_strategy]
            current_score = recent_scores[current_strategy]

            if candidate_strategy == current_strategy:
                decisions.append(
                    ReplayDecisionRecord(
                        sample_index=sample_index,
                        evaluation_index=evaluation_index,
                        current_strategy=current_strategy,
                        candidate_strategy=candidate_strategy,
                        action="stay",
                        switched=False,
                        reason_code="recent_leader_same",
                        decision_margin=0.0,
                        decision_threshold=margin,
                        reason="Stay because the current strategy remains the recent block leader.",
                    )
                )
                _emit_replay_progress(
                    progress_callback,
                    trace=trace,
                    sample_index=sample_index,
                    sample_count=sample_count,
                    evaluation_index=evaluation_index,
                    active_strategy=current_strategy,
                    candidate_strategy=candidate_strategy,
                    switch_count=switch_count,
                    adaptive_rewards=adaptive_rewards,
                )
                continue

            decision_margin = candidate_score - current_score
            if decision_margin < margin:
                decisions.append(
                    ReplayDecisionRecord(
                        sample_index=sample_index,
                        evaluation_index=evaluation_index,
                        current_strategy=current_strategy,
                        candidate_strategy=candidate_strategy,
                        action="stay",
                        switched=False,
                        reason_code="recent_leader_margin_too_small",
                        decision_margin=decision_margin,
                        decision_threshold=margin,
                        reason=(
                            "Stay because the recent leader advantage is below the switching margin: "
                            f"{decision_margin:.6f} < {margin:.6f}."
                        ),
                    )
                )
                _emit_replay_progress(
                    progress_callback,
                    trace=trace,
                    sample_index=sample_index,
                    sample_count=sample_count,
                    evaluation_index=evaluation_index,
                    active_strategy=current_strategy,
                    candidate_strategy=candidate_strategy,
                    switch_count=switch_count,
                    adaptive_rewards=adaptive_rewards,
                )
                continue

            candidate_cumulative = cumulative_reward_sums[candidate_strategy] / ((sample_index + 1) or 1)
            current_cumulative = cumulative_reward_sums[current_strategy] / ((sample_index + 1) or 1)
            if candidate_cumulative + incumbent_floor < current_cumulative:
                decisions.append(
                    ReplayDecisionRecord(
                        sample_index=sample_index,
                        evaluation_index=evaluation_index,
                        current_strategy=current_strategy,
                        candidate_strategy=candidate_strategy,
                        action="stay",
                        switched=False,
                        reason_code="recent_leader_incumbent_floor",
                        decision_margin=decision_margin,
                        decision_threshold=margin,
                        reason=(
                            "Stay because the candidate fails the incumbent floor check: "
                            f"{candidate_cumulative:.6f} + {incumbent_floor:.6f} < {current_cumulative:.6f}."
                        ),
                    )
                )
                _emit_replay_progress(
                    progress_callback,
                    trace=trace,
                    sample_index=sample_index,
                    sample_count=sample_count,
                    evaluation_index=evaluation_index,
                    active_strategy=current_strategy,
                    candidate_strategy=candidate_strategy,
                    switch_count=switch_count,
                    adaptive_rewards=adaptive_rewards,
                )
                continue

            switch_count += 1
            cooldown_remaining = cooldown_blocks
            decisions.append(
                ReplayDecisionRecord(
                    sample_index=sample_index,
                    evaluation_index=evaluation_index,
                    current_strategy=current_strategy,
                    candidate_strategy=candidate_strategy,
                    action="switch",
                    switched=True,
                    reason_code="recent_leader_advantage",
                    decision_margin=decision_margin,
                    decision_threshold=margin,
                    reason=(
                        "Switch because the recent leader exceeds the current strategy over the lookback horizon: "
                        f"{candidate_score:.6f} - {current_score:.6f} = {decision_margin:.6f}."
                    ),
                )
            )
            current_strategy = candidate_strategy
            _emit_replay_progress(
                progress_callback,
                trace=trace,
                sample_index=sample_index,
                sample_count=sample_count,
                evaluation_index=evaluation_index,
                active_strategy=current_strategy,
                candidate_strategy=candidate_strategy,
                switch_count=switch_count,
                adaptive_rewards=adaptive_rewards,
            )

        fixed_scores = {name: fmean(trace.rewards_by_strategy[name]) for name in strategy_names}
        best_fixed_strategy, best_fixed_score = max(
            fixed_scores.items(),
            key=lambda item: (item[1], item[0]),
        )
        block_delta_mean, block_delta_std, block_delta_ci95, block_count = self._block_delta_statistics(
            adaptive_rewards=tuple(adaptive_rewards),
            best_fixed_rewards=trace.rewards_by_strategy[best_fixed_strategy],
            block_size=evaluation_interval,
        )
        result = ReplayBenchmarkResult(
            dataset_name=trace.dataset_name,
            score_name=trace.score_name,
            policy_name="recent_leader_meta",
            sample_count=sample_count,
            evaluation_interval=evaluation_interval,
            window_size=evaluation_interval * lookback_blocks,
            start_strategy=start_strategy or strategy_names[0],
            final_strategy=current_strategy,
            switch_count=switch_count,
            adaptive_score=fmean(adaptive_rewards),
            best_fixed_strategy=best_fixed_strategy,
            best_fixed_score=best_fixed_score,
            delta_vs_best_fixed=fmean(adaptive_rewards) - best_fixed_score,
            fixed_scores=fixed_scores,
            block_delta_mean=block_delta_mean,
            block_delta_std=block_delta_std,
            block_delta_ci95=block_delta_ci95,
            block_count=block_count,
            decision_csv_path="",
            summary_json_path="",
            report_md_path="",
        )
        return self._persist_result(
            result=result,
            trace=trace,
            decisions=decisions,
            output_root=output_root,
        )

    def run_named_benchmark(self, dataset_name: str, *, output_root: str | Path, max_samples: int | None = None) -> ReplayBenchmarkResult:
        """Run one named benchmark dataset."""
        normalized = dataset_name.strip().lower()
        if normalized == "elec2":
            return self.run_elec2_benchmark(output_root=output_root, max_samples=max_samples)
        if normalized == "bikes":
            return self.run_bikes_benchmark(output_root=output_root, max_samples=max_samples)
        if normalized == "trump_approval":
            return self.run_trump_approval_benchmark(output_root=output_root, max_samples=max_samples)
        if normalized == "web_traffic":
            return self.run_web_traffic_benchmark(output_root=output_root)
        if normalized == "waterflow":
            return self.run_waterflow_benchmark(output_root=output_root)
        if normalized == "airlines":
            return self.run_airlines_benchmark(output_root=output_root)
        if normalized == "insects_recurring":
            return self.run_insects_recurring_benchmark(output_root=output_root)
        raise ValueError(f"unsupported benchmark dataset: {dataset_name!r}")

    def run_named_benchmark_with_hedge(self, dataset_name: str, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run one named benchmark dataset with Hedge-style expert weighting."""
        normalized = dataset_name.strip().lower()
        if normalized == "elec2":
            return self.run_elec2_benchmark_with_hedge(output_root=output_root)
        if normalized == "bikes":
            return self.run_bikes_benchmark_with_hedge(output_root=output_root)
        if normalized == "trump_approval":
            return self.run_trump_approval_benchmark_with_hedge(output_root=output_root)
        if normalized == "web_traffic":
            return self.run_web_traffic_benchmark_with_hedge(output_root=output_root)
        if normalized == "waterflow":
            return self.run_waterflow_benchmark_with_hedge(output_root=output_root)
        if normalized == "airlines":
            return self.run_airlines_benchmark_with_hedge(output_root=output_root)
        if normalized == "insects_recurring":
            return self.run_insects_recurring_benchmark_with_hedge(output_root=output_root)
        raise ValueError(f"unsupported benchmark dataset: {dataset_name!r}")

    def run_named_benchmark_with_recent_leader(self, dataset_name: str, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run one named benchmark dataset with recent-leader strategy switching."""
        normalized = dataset_name.strip().lower()
        if normalized == "elec2":
            return self.run_elec2_benchmark_with_recent_leader(output_root=output_root)
        if normalized == "bikes":
            return self.run_bikes_benchmark_with_recent_leader(output_root=output_root)
        if normalized == "trump_approval":
            return self.run_trump_approval_benchmark_with_recent_leader(output_root=output_root)
        if normalized == "web_traffic":
            return self.run_web_traffic_benchmark_with_recent_leader(output_root=output_root)
        if normalized == "waterflow":
            return self.run_waterflow_benchmark_with_recent_leader(output_root=output_root)
        if normalized == "airlines":
            return self.run_airlines_benchmark_with_recent_leader(output_root=output_root)
        if normalized == "insects_recurring":
            return self.run_insects_recurring_benchmark_with_recent_leader(output_root=output_root)
        raise ValueError(f"unsupported benchmark dataset: {dataset_name!r}")

    def run_real_stream_suite(
        self,
        *,
        output_root: str | Path,
        datasets_to_run: Iterable[str] = ("elec2", "bikes", "trump_approval"),
        max_samples: int | None = None,
    ) -> ReplaySuiteResult:
        """Run a reproducible multi-dataset replay suite."""
        root = Path(output_root).resolve()
        root.mkdir(parents=True, exist_ok=True)

        results: list[ReplayBenchmarkResult] = []
        for dataset_name in datasets_to_run:
            dataset_root = root / dataset_name
            results.append(self.run_named_benchmark(dataset_name, output_root=dataset_root, max_samples=max_samples))

        summary_json_path = root / "suite_summary.json"
        report_md_path = root / "suite_summary.md"
        payload = {
            "dataset_count": len(results),
            "datasets": [
                {
                    "dataset_name": result.dataset_name,
                    "policy_name": result.policy_name,
                    "score_name": result.score_name,
                    "sample_count": result.sample_count,
                    "adaptive_score": result.adaptive_score,
                    "best_fixed_strategy": result.best_fixed_strategy,
                    "best_fixed_score": result.best_fixed_score,
                    "oracle_score": result.oracle_score,
                    "oracle_gain": result.oracle_gain,
                    "oracle_capture_ratio": result.oracle_capture_ratio,
                    "delta_vs_best_fixed": result.delta_vs_best_fixed,
                    "switch_count": result.switch_count,
                    "block_delta_mean": result.block_delta_mean,
                    "block_delta_ci95": result.block_delta_ci95,
                    "summary_json_path": result.summary_json_path,
                }
                for result in results
            ],
            "wins_vs_best_fixed": sum(1 for result in results if result.delta_vs_best_fixed > 0.0),
            "non_losses_vs_best_fixed": sum(1 for result in results if result.delta_vs_best_fixed >= 0.0),
            "oracle_gain_mean": fmean(result.oracle_gain for result in results) if results else 0.0,
            "oracle_capture_mean": fmean(result.oracle_capture_ratio for result in results) if results else 0.0,
        }
        summary_json_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        report_md_path.write_text(self._build_suite_report(tuple(results)), encoding="utf-8")
        return ReplaySuiteResult(
            results=tuple(results),
            summary_json_path=str(summary_json_path),
            report_md_path=str(report_md_path),
        )

    def run_real_stream_suite_with_hedge(
        self,
        *,
        output_root: str | Path,
        datasets_to_run: Iterable[str] = ("elec2", "bikes", "trump_approval"),
    ) -> ReplaySuiteResult:
        """Run a reproducible multi-dataset replay suite with Hedge weighting."""
        root = Path(output_root).resolve()
        root.mkdir(parents=True, exist_ok=True)

        results: list[ReplayBenchmarkResult] = []
        for dataset_name in datasets_to_run:
            dataset_root = root / dataset_name
            results.append(self.run_named_benchmark_with_hedge(dataset_name, output_root=dataset_root))

        summary_json_path = root / "suite_summary.json"
        report_md_path = root / "suite_summary.md"
        payload = {
            "dataset_count": len(results),
            "datasets": [
                {
                    "dataset_name": result.dataset_name,
                    "policy_name": result.policy_name,
                    "score_name": result.score_name,
                    "sample_count": result.sample_count,
                    "adaptive_score": result.adaptive_score,
                    "best_fixed_strategy": result.best_fixed_strategy,
                    "best_fixed_score": result.best_fixed_score,
                    "oracle_score": result.oracle_score,
                    "oracle_gain": result.oracle_gain,
                    "oracle_capture_ratio": result.oracle_capture_ratio,
                    "delta_vs_best_fixed": result.delta_vs_best_fixed,
                    "switch_count": result.switch_count,
                    "block_delta_mean": result.block_delta_mean,
                    "block_delta_ci95": result.block_delta_ci95,
                    "summary_json_path": result.summary_json_path,
                }
                for result in results
            ],
            "wins_vs_best_fixed": sum(1 for result in results if result.delta_vs_best_fixed > 0.0),
            "non_losses_vs_best_fixed": sum(1 for result in results if result.delta_vs_best_fixed >= 0.0),
            "oracle_gain_mean": fmean(result.oracle_gain for result in results) if results else 0.0,
            "oracle_capture_mean": fmean(result.oracle_capture_ratio for result in results) if results else 0.0,
        }
        summary_json_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        report_md_path.write_text(self._build_suite_report(tuple(results)), encoding="utf-8")
        return ReplaySuiteResult(
            results=tuple(results),
            summary_json_path=str(summary_json_path),
            report_md_path=str(report_md_path),
        )

    def run_real_stream_suite_with_recent_leader(
        self,
        *,
        output_root: str | Path,
        datasets_to_run: Iterable[str] = ("elec2", "bikes", "trump_approval"),
    ) -> ReplaySuiteResult:
        """Run a reproducible multi-dataset replay suite with recent-leader switching."""
        root = Path(output_root).resolve()
        root.mkdir(parents=True, exist_ok=True)

        results: list[ReplayBenchmarkResult] = []
        for dataset_name in datasets_to_run:
            dataset_root = root / dataset_name
            results.append(self.run_named_benchmark_with_recent_leader(dataset_name, output_root=dataset_root))

        summary_json_path = root / "suite_summary.json"
        report_md_path = root / "suite_summary.md"
        payload = {
            "dataset_count": len(results),
            "datasets": [
                {
                    "dataset_name": result.dataset_name,
                    "policy_name": result.policy_name,
                    "score_name": result.score_name,
                    "sample_count": result.sample_count,
                    "adaptive_score": result.adaptive_score,
                    "best_fixed_strategy": result.best_fixed_strategy,
                    "best_fixed_score": result.best_fixed_score,
                    "oracle_score": result.oracle_score,
                    "oracle_gain": result.oracle_gain,
                    "oracle_capture_ratio": result.oracle_capture_ratio,
                    "delta_vs_best_fixed": result.delta_vs_best_fixed,
                    "switch_count": result.switch_count,
                    "block_delta_mean": result.block_delta_mean,
                    "block_delta_ci95": result.block_delta_ci95,
                    "summary_json_path": result.summary_json_path,
                }
                for result in results
            ],
            "wins_vs_best_fixed": sum(1 for result in results if result.delta_vs_best_fixed > 0.0),
            "non_losses_vs_best_fixed": sum(1 for result in results if result.delta_vs_best_fixed >= 0.0),
            "oracle_gain_mean": fmean(result.oracle_gain for result in results) if results else 0.0,
            "oracle_capture_mean": fmean(result.oracle_capture_ratio for result in results) if results else 0.0,
        }
        summary_json_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        report_md_path.write_text(self._build_suite_report(tuple(results)), encoding="utf-8")
        return ReplaySuiteResult(
            results=tuple(results),
            summary_json_path=str(summary_json_path),
            report_md_path=str(report_md_path),
        )

    def run_profile_benchmark(
        self,
        *,
        profile_path: str | Path,
        dataset_name: str,
        output_root: str | Path,
        max_samples: int | None = None,
    ) -> ReplayBenchmarkResult:
        """Run one H1/H2 benchmark replay profile on one named dataset."""
        profile = self._load_benchmark_profile(profile_path)
        trace = self._get_cached_profile_trace(
            dataset_name=dataset_name,
            task_type=profile.task_type,
            candidate_models=profile.candidate_models,
            max_samples=max_samples,
        )
        result = self._run_profile_policy(
            trace=trace,
            controller_policy=profile.controller_policy,
            output_root=output_root,
        )
        return replace(result, policy_name=profile.controller_policy)

    def run_profile_suite(
        self,
        *,
        profile_paths: Iterable[str | Path],
        dataset_names: Iterable[str],
        output_root: str | Path,
        max_samples: int | None = None,
    ) -> ReplaySuiteResult:
        """Run multiple H1/H2 profiles over multiple datasets and persist a final suite summary."""
        root = Path(output_root).resolve()
        root.mkdir(parents=True, exist_ok=True)

        results: list[ReplayBenchmarkResult] = []
        for profile_path in profile_paths:
            profile = self._load_benchmark_profile(profile_path)
            profile_root = root / profile.profile_name
            profile_root.mkdir(parents=True, exist_ok=True)
            for dataset_name in dataset_names:
                dataset_root = profile_root / dataset_name
                trace = self._get_cached_profile_trace(
                    dataset_name=dataset_name,
                    task_type=profile.task_type,
                    candidate_models=profile.candidate_models,
                    max_samples=max_samples,
                )
                results.append(
                    replace(
                        self._run_profile_policy(
                            trace=trace,
                            controller_policy=profile.controller_policy,
                            output_root=dataset_root,
                        ),
                        policy_name=profile.controller_policy,
                    )
                )

        summary_json_path = root / "suite_summary.json"
        report_md_path = root / "suite_summary.md"
        payload = {
            "profile_count": len({result.policy_name for result in results}),
            "dataset_count": len({result.dataset_name for result in results}),
            "results": [
                {
                    "dataset_name": result.dataset_name,
                    "policy_name": result.policy_name,
                    "score_name": result.score_name,
                    "sample_count": result.sample_count,
                    "adaptive_score": result.adaptive_score,
                    "best_fixed_strategy": result.best_fixed_strategy,
                    "best_fixed_score": result.best_fixed_score,
                    "oracle_score": result.oracle_score,
                    "oracle_gain": result.oracle_gain,
                    "oracle_capture_ratio": result.oracle_capture_ratio,
                    "delta_vs_best_fixed": result.delta_vs_best_fixed,
                    "switch_count": result.switch_count,
                    "block_delta_mean": result.block_delta_mean,
                    "block_delta_ci95": result.block_delta_ci95,
                    "summary_json_path": result.summary_json_path,
                }
                for result in results
            ],
            "wins_vs_best_fixed": sum(1 for result in results if result.delta_vs_best_fixed > 0.0),
            "non_losses_vs_best_fixed": sum(1 for result in results if result.delta_vs_best_fixed >= 0.0),
            "oracle_gain_mean": fmean(result.oracle_gain for result in results) if results else 0.0,
            "oracle_capture_mean": fmean(result.oracle_capture_ratio for result in results) if results else 0.0,
        }
        summary_json_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        report_md_path.write_text(self._build_profile_suite_report(tuple(results)), encoding="utf-8")
        return ReplaySuiteResult(
            results=tuple(results),
            summary_json_path=str(summary_json_path),
            report_md_path=str(report_md_path),
        )

    def _get_cached_profile_trace(
        self,
        *,
        dataset_name: str,
        task_type: str,
        candidate_models: tuple[str, ...],
        max_samples: int | None,
    ) -> OutcomeTrace:
        cache_key = (dataset_name.strip().lower(), task_type.strip().lower(), candidate_models, max_samples)
        cached = self._profile_trace_cache.get(cache_key)
        if cached is not None:
            return cached
        trace = self._build_profile_trace(
            dataset_name=dataset_name,
            task_type=task_type,
            candidate_models=candidate_models,
            max_samples=max_samples,
        )
        self._profile_trace_cache[cache_key] = trace
        return trace

    def _load_benchmark_profile(self, profile_path: str | Path) -> BenchmarkProfile:
        path = Path(profile_path)
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        return BenchmarkProfile(
            profile_name=str(payload["profile_name"]),
            task_type=str(payload["task_type"]),
            controller_policy=str(payload["controller_policy"]),
            candidate_models=tuple(str(item) for item in list(payload["candidate_models"])),
            notes=str(payload.get("notes", "")),
        )

    def _build_profile_trace(
        self,
        *,
        dataset_name: str,
        task_type: str,
        candidate_models: tuple[str, ...],
        max_samples: int | None,
    ) -> OutcomeTrace:
        normalized_dataset = dataset_name.strip().lower()
        normalized_task = task_type.strip().lower()
        registry = {spec.name: spec for spec in build_candidate_model_registry(normalized_task)}
        strategy_specs = tuple(registry[name] for name in candidate_models)

        if normalized_task == "classification":
            if normalized_dataset == "elec2":
                prediction_trace = build_river_binary_prediction_trace(
                    dataset_name="Elec2",
                    stream=_limit_stream(datasets.Elec2(), max_samples=max_samples),
                    strategies=strategy_specs,
                    source_description=(
                        "Real NSW electricity market stream replayed in temporal order; "
                        "target is whether the electricity price goes up or down."
                    ),
                    source_url=getattr(datasets.Elec2(), "url", ""),
                )
                return _prediction_trace_to_outcome_trace(prediction_trace)
            if normalized_dataset == "airlines":
                prediction_trace = build_river_binary_prediction_trace(
                    dataset_name="Airlines",
                    stream=_iter_airlines_stream(max_samples=max_samples),
                    strategies=strategy_specs,
                    source_description=(
                        "MOA Airlines delay stream replayed in temporal order from the official SourceForge archive; "
                        "target is whether the flight is delayed."
                    ),
                    source_url="https://downloads.sourceforge.net/project/moa-datastream/Datasets/Classification/airlines.arff.zip",
                )
                return _prediction_trace_to_outcome_trace(prediction_trace)
            if normalized_dataset == "insects_recurring":
                prediction_trace = build_river_multiclass_prediction_trace(
                    dataset_name="InsectsRecurring",
                    stream=_iter_insects_stream(variant="incremental-reoccurring_balanced", max_samples=max_samples),
                    strategies=strategy_specs,
                    source_description=(
                        "USP DS Repository INSECTS recurring-drift stream replayed in temporal order; "
                        "target is the insect class under recurring concept drift."
                    ),
                    source_url="https://sites.google.com/view/uspdsrepository",
                )
                return _prediction_trace_to_outcome_trace(prediction_trace)
        if normalized_task == "regression":
            if normalized_dataset == "bikes":
                return build_river_regression_outcome_trace(
                    dataset_name="Bikes",
                    stream=datasets.Bikes(),
                    strategies=strategy_specs,
                    source_description="Real Toulouse bike-availability stream replayed in temporal order.",
                    source_url=getattr(datasets.Bikes(), "url", ""),
                    feature_transform=_default_feature_transform,
                    max_samples=max_samples,
                )
            if normalized_dataset == "waterflow":
                return self._build_system_waterflow_trace(max_samples=max_samples)
            if normalized_dataset == "trump_approval":
                return build_river_regression_outcome_trace(
                    dataset_name="TrumpApproval",
                    stream=datasets.TrumpApproval(),
                    strategies=strategy_specs,
                    source_description="Real approval-rating regression stream replayed in temporal order.",
                    source_url="https://riverml.xyz/",
                    feature_transform=_default_feature_transform,
                    max_samples=max_samples,
                )
        raise ValueError(f"unsupported profile benchmark dataset/task combination: {dataset_name!r} / {task_type!r}")

    def _build_system_waterflow_trace(self, *, max_samples: int | None = None) -> OutcomeTrace:
        candidate_trace = build_river_regression_outcome_trace(
            dataset_name="WaterFlow",
            stream=datasets.WaterFlow(),
            strategies=(
                ReplayStrategySpec("lin_lr_0_0005", 0.0005, "Stationary online linear regression with SGD learning_rate=0.0005"),
                ReplayStrategySpec("lin_lr_0_001", 0.001, "Stationary online linear regression with SGD learning_rate=0.001"),
                ReplayStrategySpec("lin_lr_0_002", 0.002, "Stationary online linear regression with SGD learning_rate=0.002"),
                ReplayStrategySpec("pa_regressor", 0.0, "Stationary online passive-aggressive regression", model_kind="pa_regressor"),
                ReplayStrategySpec("tree_regressor", 0.0, "Stationary online adaptive Hoeffding tree regression", model_kind="hoeffding_tree_regressor"),
            ),
            source_description=(
                "Real pipeline water-flow stream replayed in temporal order; "
                "evaluation includes anomalous low-flow segments and a pumping-induced peak."
            ),
            source_url=getattr(datasets.WaterFlow(), "url", ""),
            feature_transform=_default_feature_transform,
            max_samples=max_samples,
        )
        selected = self._select_balanced_portfolio(
            trace=candidate_trace,
            warmup_samples=240,
            block_size=24,
            max_strategies=3,
        )
        return _subset_outcome_trace(candidate_trace, selected)

    def _run_profile_policy(
        self,
        *,
        trace: OutcomeTrace,
        controller_policy: str,
        output_root: str | Path,
    ) -> ReplayBenchmarkResult:
        normalized = controller_policy.strip().lower()
        default_start_strategy = next(iter(trace.rewards_by_strategy))

        if normalized == "hard_switch_lcb":
            return self.run_outcome_trace(
                trace=trace,
                output_root=output_root,
                meta_config=self._default_profile_meta_config(trace),
                evaluation_interval=self._default_profile_evaluation_interval(trace),
                start_strategy=default_start_strategy,
            )
        if normalized in {"recent_leader_meta", "drift_aware_comparator", "greedy_reward"}:
            recent_kwargs = self._default_recent_leader_kwargs(trace, normalized)
            return self.run_outcome_trace_with_recent_leader(
                trace=trace,
                output_root=output_root,
                evaluation_interval=self._default_profile_evaluation_interval(trace),
                start_strategy=default_start_strategy,
                lookback_blocks=int(recent_kwargs["lookback_blocks"]),
                margin=float(recent_kwargs["margin"]),
                warmup_blocks=int(recent_kwargs["warmup_blocks"]),
                cooldown_blocks=int(recent_kwargs["cooldown_blocks"]),
                incumbent_floor=float(recent_kwargs["incumbent_floor"]),
            )
        if normalized == "fixed_share_portfolio":
            fixed_share_kwargs = self._default_fixed_share_kwargs(trace)
            return self.run_outcome_trace_with_fixed_share(
                trace=trace,
                output_root=output_root,
                evaluation_interval=self._default_profile_evaluation_interval(trace),
                start_strategy=default_start_strategy,
                eta=float(fixed_share_kwargs["eta"]),
                share_alpha=float(fixed_share_kwargs["share_alpha"]),
                switch_threshold=float(fixed_share_kwargs["switch_threshold"]),
                warmup_samples=int(fixed_share_kwargs["warmup_samples"]),
            )
        if normalized == "tempered_reward":
            return self.run_outcome_trace(
                trace=self._temper_outcome_trace(trace),
                output_root=output_root,
                meta_config=self._default_profile_meta_config(trace),
                evaluation_interval=self._default_profile_evaluation_interval(trace),
                start_strategy=default_start_strategy,
            )
        if normalized in {"search_profile", "adaptive_meta_final"}:
            return self._run_prefix_selected_profile(
                trace=trace,
                output_root=output_root,
                start_strategy=default_start_strategy,
            )
        raise ValueError(f"unsupported benchmark controller profile: {controller_policy!r}")

    def _run_prefix_selected_profile(
        self,
        *,
        trace: OutcomeTrace,
        output_root: str | Path,
        start_strategy: str,
    ) -> ReplayBenchmarkResult:
        sample_count = len(next(iter(trace.rewards_by_strategy.values()), ()))
        prefix_samples = max(128, min(sample_count // 4, 2048))
        prefix_trace = _subset_trace_by_length(trace, prefix_samples)
        fixed_share_kwargs = self._default_fixed_share_kwargs(trace)
        recent_kwargs = self._default_recent_leader_kwargs(trace, "recent_leader_meta")
        candidates = (
            self.run_outcome_trace(
                trace=prefix_trace,
                output_root=Path(output_root) / "_calibration_hard_switch",
                meta_config=self._default_profile_meta_config(trace),
                evaluation_interval=self._default_profile_evaluation_interval(trace),
                start_strategy=start_strategy,
            ),
            self.run_outcome_trace_with_recent_leader(
                trace=prefix_trace,
                output_root=Path(output_root) / "_calibration_recent_leader",
                evaluation_interval=self._default_profile_evaluation_interval(trace),
                start_strategy=start_strategy,
                lookback_blocks=int(recent_kwargs["lookback_blocks"]),
                margin=float(recent_kwargs["margin"]),
                warmup_blocks=int(recent_kwargs["warmup_blocks"]),
                cooldown_blocks=int(recent_kwargs["cooldown_blocks"]),
                incumbent_floor=float(recent_kwargs["incumbent_floor"]),
            ),
            self.run_outcome_trace_with_fixed_share(
                trace=prefix_trace,
                output_root=Path(output_root) / "_calibration_fixed_share",
                evaluation_interval=self._default_profile_evaluation_interval(trace),
                start_strategy=start_strategy,
                eta=float(fixed_share_kwargs["eta"]),
                share_alpha=float(fixed_share_kwargs["share_alpha"]),
                switch_threshold=float(fixed_share_kwargs["switch_threshold"]),
                warmup_samples=int(fixed_share_kwargs["warmup_samples"]),
            ),
        )
        selected = max(candidates, key=lambda item: (item.delta_vs_best_fixed, item.adaptive_score, -item.switch_count))
        if selected.policy_name == "fixed_share_portfolio":
            return self.run_outcome_trace_with_fixed_share(
                trace=trace,
                output_root=output_root,
                evaluation_interval=self._default_profile_evaluation_interval(trace),
                start_strategy=start_strategy,
                eta=float(fixed_share_kwargs["eta"]),
                share_alpha=float(fixed_share_kwargs["share_alpha"]),
                switch_threshold=float(fixed_share_kwargs["switch_threshold"]),
                warmup_samples=int(fixed_share_kwargs["warmup_samples"]),
            )
        if selected.policy_name == "recent_leader_meta":
            return self.run_outcome_trace_with_recent_leader(
                trace=trace,
                output_root=output_root,
                evaluation_interval=self._default_profile_evaluation_interval(trace),
                start_strategy=start_strategy,
                lookback_blocks=int(recent_kwargs["lookback_blocks"]),
                margin=float(recent_kwargs["margin"]),
                warmup_blocks=int(recent_kwargs["warmup_blocks"]),
                cooldown_blocks=int(recent_kwargs["cooldown_blocks"]),
                incumbent_floor=float(recent_kwargs["incumbent_floor"]),
            )
        return self.run_outcome_trace(
            trace=trace,
            output_root=output_root,
            meta_config=self._default_profile_meta_config(trace),
            evaluation_interval=self._default_profile_evaluation_interval(trace),
            start_strategy=start_strategy,
        )

    def _default_recent_leader_kwargs(self, trace: OutcomeTrace, normalized_policy: str) -> dict[str, float | int]:
        if trace.dataset_name == "WaterFlow":
            if normalized_policy in {"drift_aware_comparator", "greedy_reward"}:
                return {
                    "lookback_blocks": 1,
                    "margin": 0.0,
                    "warmup_blocks": 1,
                    "cooldown_blocks": 0,
                    "incumbent_floor": 0.0,
                }
            return {
                "lookback_blocks": 3,
                "margin": 0.002,
                "warmup_blocks": 2,
                "cooldown_blocks": 1,
                "incumbent_floor": 0.001,
            }
        return {
            "lookback_blocks": 1 if normalized_policy in {"drift_aware_comparator", "greedy_reward"} else 2,
            "margin": 0.0 if normalized_policy in {"drift_aware_comparator", "greedy_reward"} else 0.002,
            "warmup_blocks": 1 if normalized_policy == "greedy_reward" else 2,
            "cooldown_blocks": 0 if normalized_policy in {"drift_aware_comparator", "greedy_reward"} else 1,
            "incumbent_floor": 0.0 if normalized_policy == "greedy_reward" else 0.001,
        }

    def _default_fixed_share_kwargs(self, trace: OutcomeTrace) -> dict[str, float | int]:
        if trace.dataset_name == "WaterFlow":
            return {
                "eta": 0.45,
                "share_alpha": 0.03,
                "switch_threshold": 0.01,
                "warmup_samples": 48,
            }
        return {
            "eta": 0.35,
            "share_alpha": 0.08,
            "switch_threshold": 0.01,
            "warmup_samples": max(64, self._default_profile_evaluation_interval(trace)),
        }

    def _default_profile_evaluation_interval(self, trace: OutcomeTrace) -> int:
        if trace.dataset_name == "WaterFlow":
            return 24
        return 128 if trace.score_name == "accuracy" else 64

    def _default_profile_meta_config(self, trace: OutcomeTrace) -> MetaControllerConfig:
        if trace.dataset_name == "WaterFlow":
            return MetaControllerConfig(
                window_size=48,
                min_samples=2,
                delta=0.001,
                lambda_value=0.0,
                switch_cost=0.002,
                utility_weights={
                    "reward_mean": 1.0,
                    "reward_variance": 0.0,
                    "compute_cost": 0.0,
                    "switch_cost": 0.0,
                },
            )
        if trace.score_name == "accuracy":
            return MetaControllerConfig(
                window_size=256,
                min_samples=3,
                delta=0.002,
                lambda_value=0.0,
                switch_cost=0.012,
                utility_weights={
                    "reward_mean": 1.0,
                    "reward_variance": 0.0,
                    "compute_cost": 0.0,
                    "switch_cost": 0.0,
                },
            )
        return MetaControllerConfig(
            window_size=128,
            min_samples=2,
            delta=0.001,
            lambda_value=0.0,
            switch_cost=0.006,
            utility_weights={
                "reward_mean": 1.0,
                "reward_variance": 0.0,
                "compute_cost": 0.0,
                "switch_cost": 0.0,
            },
        )

    def _temper_outcome_trace(self, trace: OutcomeTrace, *, gamma: float = 0.75) -> OutcomeTrace:
        return OutcomeTrace(
            dataset_name=trace.dataset_name,
            score_name=trace.score_name,
            rewards_by_strategy={
                name: tuple(max(0.0, min(1.0, reward)) ** gamma for reward in rewards)
                for name, rewards in trace.rewards_by_strategy.items()
            },
            successes_by_strategy=trace.successes_by_strategy,
            source_description=trace.source_description,
            source_url=trace.source_url,
        )

    def run_elec2_benchmark(self, *, output_root: str | Path, max_samples: int | None = None) -> ReplayBenchmarkResult:
        """Run replay validation on the real Elec2 electricity stream."""
        dataset = datasets.Elec2()
        strategies = (
            ReplayStrategySpec(
                name="sgd_lr_0_1",
                learning_rate=0.1,
                description="Stationary online logistic regression with SGD learning_rate=0.1",
            ),
            ReplayStrategySpec(
                name="sgd_lr_0_5",
                learning_rate=0.5,
                description="Stationary online logistic regression with SGD learning_rate=0.5",
            ),
            ReplayStrategySpec(
                name="sgd_lr_1_0",
                learning_rate=1.0,
                description="Stationary online logistic regression with SGD learning_rate=1.0",
            ),
        )
        trace = build_river_binary_prediction_trace(
            dataset_name="Elec2",
            stream=_limit_stream(dataset, max_samples=max_samples),
            strategies=strategies,
            source_description=(
                "Real NSW electricity market stream replayed in temporal order; "
                "target is whether the electricity price goes up or down."
            ),
            source_url=getattr(dataset, "url", ""),
        )
        meta_config = MetaControllerConfig(
            window_size=256,
            min_samples=3,
            delta=0.002,
            lambda_value=0.0,
            switch_cost=0.016,
            utility_weights={
                "reward_mean": 1.0,
                "reward_variance": 0.0,
                "compute_cost": 0.0,
                "switch_cost": 0.0,
            },
        )
        return self.run_prediction_trace(
            trace=trace,
            output_root=output_root,
            meta_config=meta_config,
            evaluation_interval=128,
            start_strategy="sgd_lr_1_0",
        )

    def run_elec2_benchmark_with_hedge(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run Hedge replay validation on the real Elec2 electricity stream."""
        dataset = datasets.Elec2()
        strategies = (
            ReplayStrategySpec("sgd_lr_0_1", 0.1, "Stationary online logistic regression with SGD learning_rate=0.1"),
            ReplayStrategySpec("sgd_lr_0_5", 0.5, "Stationary online logistic regression with SGD learning_rate=0.5"),
            ReplayStrategySpec("sgd_lr_1_0", 1.0, "Stationary online logistic regression with SGD learning_rate=1.0"),
        )
        trace = build_river_binary_prediction_trace(
            dataset_name="Elec2",
            stream=dataset,
            strategies=strategies,
            source_description=(
                "Real NSW electricity market stream replayed in temporal order; "
                "target is whether the electricity price goes up or down."
            ),
            source_url=getattr(dataset, "url", ""),
        )
        outcome_trace = OutcomeTrace(
            dataset_name=trace.dataset_name,
            score_name="accuracy",
            rewards_by_strategy={
                name: tuple(float(prediction == target) for prediction, target in zip(predictions, trace.targets))
                for name, predictions in trace.predictions_by_strategy.items()
            },
            successes_by_strategy={
                name: tuple(prediction == target for prediction, target in zip(predictions, trace.targets))
                for name, predictions in trace.predictions_by_strategy.items()
            },
            source_description=trace.source_description,
            source_url=trace.source_url,
        )
        return self.run_outcome_trace_with_hedge(
            trace=outcome_trace,
            output_root=output_root,
            evaluation_interval=128,
            start_strategy="sgd_lr_1_0",
            eta=0.35,
            switch_threshold=0.015,
            warmup_samples=128,
        )

    def run_elec2_benchmark_with_recent_leader(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run recent-leader replay validation on the real Elec2 electricity stream."""
        dataset = datasets.Elec2()
        strategies = (
            ReplayStrategySpec("sgd_lr_0_1", 0.1, "Stationary online logistic regression with SGD learning_rate=0.1"),
            ReplayStrategySpec("sgd_lr_0_5", 0.5, "Stationary online logistic regression with SGD learning_rate=0.5"),
            ReplayStrategySpec("sgd_lr_1_0", 1.0, "Stationary online logistic regression with SGD learning_rate=1.0"),
        )
        trace = build_river_binary_prediction_trace(
            dataset_name="Elec2",
            stream=dataset,
            strategies=strategies,
            source_description=(
                "Real NSW electricity market stream replayed in temporal order; "
                "target is whether the electricity price goes up or down."
            ),
            source_url=getattr(dataset, "url", ""),
        )
        outcome_trace = OutcomeTrace(
            dataset_name=trace.dataset_name,
            score_name="accuracy",
            rewards_by_strategy={
                name: tuple(float(prediction == target) for prediction, target in zip(predictions, trace.targets))
                for name, predictions in trace.predictions_by_strategy.items()
            },
            successes_by_strategy={
                name: tuple(prediction == target for prediction, target in zip(predictions, trace.targets))
                for name, predictions in trace.predictions_by_strategy.items()
            },
            source_description=trace.source_description,
            source_url=trace.source_url,
        )
        return self.run_outcome_trace_with_recent_leader(
            trace=outcome_trace,
            output_root=output_root,
            evaluation_interval=128,
            start_strategy="sgd_lr_1_0",
            lookback_blocks=2,
            margin=0.015,
            warmup_blocks=4,
            cooldown_blocks=4,
            incumbent_floor=0.002,
        )

    def run_bikes_benchmark(self, *, output_root: str | Path, max_samples: int | None = None) -> ReplayBenchmarkResult:
        """Run replay validation on the real Toulouse bikes demand stream."""
        dataset = datasets.Bikes()
        strategies = (
            ReplayStrategySpec(
                name="sgd_lr_0_0001",
                learning_rate=0.0001,
                description="Stationary online linear regression with SGD learning_rate=0.0001",
            ),
            ReplayStrategySpec(
                name="sgd_lr_0_0005",
                learning_rate=0.0005,
                description="Stationary online linear regression with SGD learning_rate=0.0005",
            ),
            ReplayStrategySpec(
                name="sgd_lr_0_001",
                learning_rate=0.001,
                description="Stationary online linear regression with SGD learning_rate=0.001",
            ),
        )
        trace = build_river_regression_outcome_trace(
            dataset_name="Bikes",
            stream=dataset,
            strategies=strategies,
            source_description=(
                "Real Toulouse bike-availability stream replayed in temporal order; "
                "evaluation uses the first 40,000 samples for a reproducible CPU-bound benchmark."
            ),
            source_url=getattr(dataset, "url", ""),
            feature_transform=_default_feature_transform,
            max_samples=max_samples or 40_000,
        )
        meta_config = MetaControllerConfig(
            window_size=256,
            min_samples=2,
            delta=0.002,
            lambda_value=0.0,
            switch_cost=0.008,
            utility_weights={
                "reward_mean": 1.0,
                "reward_variance": 0.0,
                "compute_cost": 0.0,
                "switch_cost": 0.0,
            },
        )
        return self.run_outcome_trace(
            trace=trace,
            output_root=output_root,
            meta_config=meta_config,
            evaluation_interval=128,
            start_strategy="sgd_lr_0_0005",
        )

    def run_bikes_benchmark_with_hedge(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run Hedge replay validation on the real Toulouse bikes demand stream."""
        dataset = datasets.Bikes()
        strategies = (
            ReplayStrategySpec("sgd_lr_0_0001", 0.0001, "Stationary online linear regression with SGD learning_rate=0.0001"),
            ReplayStrategySpec("sgd_lr_0_0005", 0.0005, "Stationary online linear regression with SGD learning_rate=0.0005"),
            ReplayStrategySpec("sgd_lr_0_001", 0.001, "Stationary online linear regression with SGD learning_rate=0.001"),
        )
        trace = build_river_regression_outcome_trace(
            dataset_name="Bikes",
            stream=dataset,
            strategies=strategies,
            source_description=(
                "Real Toulouse bike-availability stream replayed in temporal order; "
                "evaluation uses the first 40,000 samples for a reproducible CPU-bound benchmark."
            ),
            source_url=getattr(dataset, "url", ""),
            feature_transform=_default_feature_transform,
            max_samples=40_000,
        )
        return self.run_outcome_trace_with_hedge(
            trace=trace,
            output_root=output_root,
            evaluation_interval=128,
            start_strategy="sgd_lr_0_0005",
            eta=0.45,
            switch_threshold=0.01,
            warmup_samples=128,
        )

    def run_bikes_benchmark_with_recent_leader(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run recent-leader replay validation on the real Toulouse bikes demand stream."""
        dataset = datasets.Bikes()
        strategies = (
            ReplayStrategySpec("sgd_lr_0_0001", 0.0001, "Stationary online linear regression with SGD learning_rate=0.0001"),
            ReplayStrategySpec("sgd_lr_0_0005", 0.0005, "Stationary online linear regression with SGD learning_rate=0.0005"),
            ReplayStrategySpec("sgd_lr_0_001", 0.001, "Stationary online linear regression with SGD learning_rate=0.001"),
        )
        trace = build_river_regression_outcome_trace(
            dataset_name="Bikes",
            stream=dataset,
            strategies=strategies,
            source_description=(
                "Real Toulouse bike-availability stream replayed in temporal order; "
                "evaluation uses the first 40,000 samples for a reproducible CPU-bound benchmark."
            ),
            source_url=getattr(dataset, "url", ""),
            feature_transform=_default_feature_transform,
            max_samples=40_000,
        )
        return self.run_outcome_trace_with_recent_leader(
            trace=trace,
            output_root=output_root,
            evaluation_interval=128,
            start_strategy="sgd_lr_0_0005",
            lookback_blocks=1,
            margin=0.0005,
            warmup_blocks=2,
            cooldown_blocks=0,
            incumbent_floor=0.002,
        )

    def run_trump_approval_benchmark(self, *, output_root: str | Path, max_samples: int | None = None) -> ReplayBenchmarkResult:
        """Run replay validation on the Trump approval regression stream."""
        dataset = datasets.TrumpApproval()
        strategies = (
            ReplayStrategySpec(
                name="sgd_lr_0_001",
                learning_rate=0.001,
                description="Stationary online linear regression with SGD learning_rate=0.001",
            ),
            ReplayStrategySpec(
                name="sgd_lr_0_01",
                learning_rate=0.01,
                description="Stationary online linear regression with SGD learning_rate=0.01",
            ),
            ReplayStrategySpec(
                name="sgd_lr_0_05",
                learning_rate=0.05,
                description="Stationary online linear regression with SGD learning_rate=0.05",
            ),
        )
        trace = build_river_regression_outcome_trace(
            dataset_name="TrumpApproval",
            stream=dataset,
            strategies=strategies,
            source_description=(
                "Real approval-rating regression stream replayed in temporal order; "
                "used as a compact regression case where one fixed learner may dominate."
            ),
            source_url="https://riverml.xyz/",
            feature_transform=_default_feature_transform,
            max_samples=max_samples,
        )
        meta_config = MetaControllerConfig(
            window_size=64,
            min_samples=2,
            delta=0.001,
            lambda_value=0.0,
            switch_cost=0.009,
            utility_weights={
                "reward_mean": 1.0,
                "reward_variance": 0.0,
                "compute_cost": 0.0,
                "switch_cost": 0.0,
            },
        )
        return self.run_outcome_trace(
            trace=trace,
            output_root=output_root,
            meta_config=meta_config,
            evaluation_interval=32,
            start_strategy="sgd_lr_0_01",
        )

    def run_trump_approval_benchmark_with_hedge(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run Hedge replay validation on the Trump approval regression stream."""
        dataset = datasets.TrumpApproval()
        strategies = (
            ReplayStrategySpec("sgd_lr_0_001", 0.001, "Stationary online linear regression with SGD learning_rate=0.001"),
            ReplayStrategySpec("sgd_lr_0_01", 0.01, "Stationary online linear regression with SGD learning_rate=0.01"),
            ReplayStrategySpec("sgd_lr_0_05", 0.05, "Stationary online linear regression with SGD learning_rate=0.05"),
        )
        trace = build_river_regression_outcome_trace(
            dataset_name="TrumpApproval",
            stream=dataset,
            strategies=strategies,
            source_description=(
                "Real approval-rating regression stream replayed in temporal order; "
                "used as a compact regression case where one fixed learner may dominate."
            ),
            source_url="https://riverml.xyz/",
            feature_transform=_default_feature_transform,
            max_samples=None,
        )
        return self.run_outcome_trace_with_hedge(
            trace=trace,
            output_root=output_root,
            evaluation_interval=32,
            start_strategy="sgd_lr_0_01",
            eta=0.6,
            switch_threshold=0.005,
            warmup_samples=64,
        )

    def run_trump_approval_benchmark_with_recent_leader(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run recent-leader replay validation on the Trump approval regression stream."""
        dataset = datasets.TrumpApproval()
        strategies = (
            ReplayStrategySpec("sgd_lr_0_001", 0.001, "Stationary online linear regression with SGD learning_rate=0.001"),
            ReplayStrategySpec("sgd_lr_0_01", 0.01, "Stationary online linear regression with SGD learning_rate=0.01"),
            ReplayStrategySpec("sgd_lr_0_05", 0.05, "Stationary online linear regression with SGD learning_rate=0.05"),
        )
        trace = build_river_regression_outcome_trace(
            dataset_name="TrumpApproval",
            stream=dataset,
            strategies=strategies,
            source_description=(
                "Real approval-rating regression stream replayed in temporal order; "
                "used as a compact regression case where one fixed learner may dominate."
            ),
            source_url="https://riverml.xyz/",
            feature_transform=_default_feature_transform,
            max_samples=None,
        )
        return self.run_outcome_trace_with_recent_leader(
            trace=trace,
            output_root=output_root,
            evaluation_interval=32,
            start_strategy="sgd_lr_0_01",
            lookback_blocks=8,
            margin=0.01,
            warmup_blocks=1,
            cooldown_blocks=4,
            incumbent_floor=0.0,
        )

    def run_web_traffic_benchmark(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run replay validation on the real WebTraffic multi-output stream."""
        dataset = datasets.WebTraffic()
        strategies = (
            ReplayStrategySpec("sgd_lr_1e-11", 1e-11, "Stationary online linear regression with SGD learning_rate=1e-11"),
            ReplayStrategySpec("sgd_lr_5e-11", 5e-11, "Stationary online linear regression with SGD learning_rate=5e-11"),
            ReplayStrategySpec("sgd_lr_1e-10", 1e-10, "Stationary online linear regression with SGD learning_rate=1e-10"),
        )
        trace = build_river_multioutput_regression_outcome_trace(
            dataset_name="WebTraffic",
            stream=dataset,
            strategies=strategies,
            source_description=(
                "Real South African web-traffic stream replayed in temporal order; "
                "target includes sessionsA and sessionsB under anomalous events and missing captures."
            ),
            source_url=getattr(dataset, "url", ""),
            feature_transform=_default_feature_transform,
            max_samples=44_160,
        )
        meta_config = MetaControllerConfig(
            window_size=256,
            min_samples=2,
            delta=0.001,
            lambda_value=0.0,
            switch_cost=0.004,
            utility_weights={
                "reward_mean": 1.0,
                "reward_variance": 0.0,
                "compute_cost": 0.0,
                "switch_cost": 0.0,
            },
        )
        return self.run_outcome_trace(
            trace=trace,
            output_root=output_root,
            meta_config=meta_config,
            evaluation_interval=96,
            start_strategy="sgd_lr_5e-11",
        )

    def run_web_traffic_benchmark_with_hedge(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run Hedge replay validation on the real WebTraffic multi-output stream."""
        dataset = datasets.WebTraffic()
        strategies = (
            ReplayStrategySpec("sgd_lr_1e-11", 1e-11, "Stationary online linear regression with SGD learning_rate=1e-11"),
            ReplayStrategySpec("sgd_lr_5e-11", 5e-11, "Stationary online linear regression with SGD learning_rate=5e-11"),
            ReplayStrategySpec("sgd_lr_1e-10", 1e-10, "Stationary online linear regression with SGD learning_rate=1e-10"),
        )
        trace = build_river_multioutput_regression_outcome_trace(
            dataset_name="WebTraffic",
            stream=dataset,
            strategies=strategies,
            source_description=(
                "Real South African web-traffic stream replayed in temporal order; "
                "target includes sessionsA and sessionsB under anomalous events and missing captures."
            ),
            source_url=getattr(dataset, "url", ""),
            feature_transform=_default_feature_transform,
            max_samples=44_160,
        )
        return self.run_outcome_trace_with_hedge(
            trace=trace,
            output_root=output_root,
            evaluation_interval=96,
            start_strategy="sgd_lr_5e-11",
            eta=0.5,
            switch_threshold=0.005,
            warmup_samples=192,
        )

    def run_web_traffic_benchmark_with_recent_leader(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run recent-leader replay validation on the real WebTraffic multi-output stream."""
        dataset = datasets.WebTraffic()
        strategies = (
            ReplayStrategySpec("sgd_lr_1e-11", 1e-11, "Stationary online linear regression with SGD learning_rate=1e-11"),
            ReplayStrategySpec("sgd_lr_5e-11", 5e-11, "Stationary online linear regression with SGD learning_rate=5e-11"),
            ReplayStrategySpec("sgd_lr_1e-10", 1e-10, "Stationary online linear regression with SGD learning_rate=1e-10"),
        )
        trace = build_river_multioutput_regression_outcome_trace(
            dataset_name="WebTraffic",
            stream=dataset,
            strategies=strategies,
            source_description=(
                "Real South African web-traffic stream replayed in temporal order; "
                "target includes sessionsA and sessionsB under anomalous events and missing captures."
            ),
            source_url=getattr(dataset, "url", ""),
            feature_transform=_default_feature_transform,
            max_samples=44_160,
        )
        return self.run_outcome_trace_with_recent_leader(
            trace=trace,
            output_root=output_root,
            evaluation_interval=96,
            start_strategy="sgd_lr_5e-11",
            lookback_blocks=2,
            margin=0.0005,
            warmup_blocks=2,
            cooldown_blocks=0,
            incumbent_floor=0.0005,
        )

    def run_waterflow_benchmark(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run replay validation on the real WaterFlow anomaly-robust forecasting stream."""
        trace = self._build_system_waterflow_trace()
        meta_config = MetaControllerConfig(
            window_size=48,
            min_samples=2,
            delta=0.001,
            lambda_value=0.0,
            switch_cost=0.002,
            utility_weights={
                "reward_mean": 1.0,
                "reward_variance": 0.0,
                "compute_cost": 0.0,
                "switch_cost": 0.0,
            },
        )
        return self.run_outcome_trace(
            trace=trace,
            output_root=output_root,
            meta_config=meta_config,
            evaluation_interval=24,
            start_strategy=next(iter(trace.rewards_by_strategy)),
        )

    def run_waterflow_benchmark_with_hedge(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run Hedge replay validation on the real WaterFlow stream."""
        trace = self._build_system_waterflow_trace()
        return self.run_outcome_trace_with_hedge(
            trace=trace,
            output_root=output_root,
            evaluation_interval=24,
            start_strategy=next(iter(trace.rewards_by_strategy)),
            eta=0.45,
            switch_threshold=0.01,
            warmup_samples=48,
        )

    def run_waterflow_benchmark_with_recent_leader(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run recent-leader replay validation on the real WaterFlow stream."""
        trace = self._build_system_waterflow_trace()
        return self.run_outcome_trace_with_recent_leader(
            trace=trace,
            output_root=output_root,
            evaluation_interval=24,
            start_strategy=next(iter(trace.rewards_by_strategy)),
            lookback_blocks=3,
            margin=0.002,
            warmup_blocks=2,
            cooldown_blocks=1,
            incumbent_floor=0.001,
        )

    def run_airlines_benchmark(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run replay validation on the external MOA Airlines delay stream."""
        prediction_trace = build_river_binary_prediction_trace(
            dataset_name="Airlines",
            stream=_iter_airlines_stream(max_samples=100_000),
            strategies=(
                ReplayStrategySpec("logistic_lr_0_01", 0.01, "Stationary online logistic regression with SGD learning_rate=0.01"),
                ReplayStrategySpec("logistic_lr_0_1", 0.1, "Stationary online logistic regression with SGD learning_rate=0.1"),
                ReplayStrategySpec("pa_classifier", 0.0, "Stationary online passive-aggressive classification", model_kind="pa_classifier"),
                ReplayStrategySpec("tree_classifier", 0.0, "Stationary online adaptive Hoeffding tree classification", model_kind="hoeffding_tree_classifier"),
                ReplayStrategySpec("gaussian_nb", 0.0, "Stationary online Gaussian naive Bayes", model_kind="gaussian_nb"),
            ),
            source_description=(
                "MOA Airlines delay stream replayed in temporal order from the official SourceForge archive; "
                "target is whether the flight is delayed."
            ),
            source_url="https://downloads.sourceforge.net/project/moa-datastream/Datasets/Classification/airlines.arff.zip",
        )
        candidate_trace = _prediction_trace_to_outcome_trace(prediction_trace)
        selected = self._select_balanced_portfolio(
            trace=candidate_trace,
            warmup_samples=20_000,
            block_size=256,
            max_strategies=3,
        )
        trace = _subset_outcome_trace(candidate_trace, selected)
        meta_config = MetaControllerConfig(
            window_size=256,
            min_samples=2,
            delta=0.002,
            lambda_value=0.0,
            switch_cost=0.004,
            utility_weights={
                "reward_mean": 1.0,
                "reward_variance": 0.0,
                "compute_cost": 0.0,
                "switch_cost": 0.0,
            },
        )
        return self.run_outcome_trace(
            trace=trace,
            output_root=output_root,
            meta_config=meta_config,
            evaluation_interval=256,
            start_strategy=selected[0],
        )

    def run_airlines_benchmark_with_hedge(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run Hedge replay validation on the external MOA Airlines stream."""
        prediction_trace = build_river_binary_prediction_trace(
            dataset_name="Airlines",
            stream=_iter_airlines_stream(max_samples=100_000),
            strategies=(
                ReplayStrategySpec("logistic_lr_0_01", 0.01, "Stationary online logistic regression with SGD learning_rate=0.01"),
                ReplayStrategySpec("logistic_lr_0_1", 0.1, "Stationary online logistic regression with SGD learning_rate=0.1"),
                ReplayStrategySpec("pa_classifier", 0.0, "Stationary online passive-aggressive classification", model_kind="pa_classifier"),
                ReplayStrategySpec("tree_classifier", 0.0, "Stationary online adaptive Hoeffding tree classification", model_kind="hoeffding_tree_classifier"),
                ReplayStrategySpec("gaussian_nb", 0.0, "Stationary online Gaussian naive Bayes", model_kind="gaussian_nb"),
            ),
            source_description=(
                "MOA Airlines delay stream replayed in temporal order from the official SourceForge archive; "
                "target is whether the flight is delayed."
            ),
            source_url="https://downloads.sourceforge.net/project/moa-datastream/Datasets/Classification/airlines.arff.zip",
        )
        candidate_trace = _prediction_trace_to_outcome_trace(prediction_trace)
        selected = self._select_balanced_portfolio(
            trace=candidate_trace,
            warmup_samples=20_000,
            block_size=256,
            max_strategies=3,
        )
        trace = _subset_outcome_trace(candidate_trace, selected)
        return self.run_outcome_trace_with_hedge(
            trace=trace,
            output_root=output_root,
            evaluation_interval=256,
            start_strategy=selected[0],
            eta=0.4,
            switch_threshold=0.01,
            warmup_samples=512,
        )

    def run_airlines_benchmark_with_recent_leader(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run recent-leader replay validation on the external MOA Airlines stream."""
        prediction_trace = build_river_binary_prediction_trace(
            dataset_name="Airlines",
            stream=_iter_airlines_stream(max_samples=100_000),
            strategies=(
                ReplayStrategySpec("logistic_lr_0_01", 0.01, "Stationary online logistic regression with SGD learning_rate=0.01"),
                ReplayStrategySpec("logistic_lr_0_1", 0.1, "Stationary online logistic regression with SGD learning_rate=0.1"),
                ReplayStrategySpec("pa_classifier", 0.0, "Stationary online passive-aggressive classification", model_kind="pa_classifier"),
                ReplayStrategySpec("tree_classifier", 0.0, "Stationary online adaptive Hoeffding tree classification", model_kind="hoeffding_tree_classifier"),
                ReplayStrategySpec("gaussian_nb", 0.0, "Stationary online Gaussian naive Bayes", model_kind="gaussian_nb"),
            ),
            source_description=(
                "MOA Airlines delay stream replayed in temporal order from the official SourceForge archive; "
                "target is whether the flight is delayed."
            ),
            source_url="https://downloads.sourceforge.net/project/moa-datastream/Datasets/Classification/airlines.arff.zip",
        )
        candidate_trace = _prediction_trace_to_outcome_trace(prediction_trace)
        selected = self._select_balanced_portfolio(
            trace=candidate_trace,
            warmup_samples=20_000,
            block_size=256,
            max_strategies=3,
        )
        trace = _subset_outcome_trace(candidate_trace, selected)
        return self.run_outcome_trace_with_recent_leader(
            trace=trace,
            output_root=output_root,
            evaluation_interval=256,
            start_strategy=selected[0],
            lookback_blocks=3,
            margin=0.002,
            warmup_blocks=2,
            cooldown_blocks=1,
            incumbent_floor=0.001,
        )

    def run_insects_recurring_benchmark(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run replay validation on the official INSECTS recurring-drift stream."""
        prediction_trace = build_river_multiclass_prediction_trace(
            dataset_name="InsectsRecurring",
            stream=_iter_insects_stream(variant="incremental-reoccurring_balanced", max_samples=60_000),
            strategies=(
                ReplayStrategySpec("softmax_lr_0_01", 0.01, "Stationary online softmax regression with SGD learning_rate=0.01"),
                ReplayStrategySpec("softmax_lr_0_1", 0.1, "Stationary online softmax regression with SGD learning_rate=0.1"),
                ReplayStrategySpec("pa_classifier", 0.0, "Stationary online passive-aggressive classification", model_kind="pa_classifier"),
                ReplayStrategySpec("tree_classifier", 0.0, "Stationary online adaptive Hoeffding tree classification", model_kind="hoeffding_tree_classifier"),
            ),
            source_description=(
                "Official USP INSECTS recurring-drift stream replayed in temporal order; "
                "target is the insect class under incremental recurring concept drift."
            ),
            source_url="https://sites.google.com/view/uspdsrepository",
        )
        candidate_trace = _prediction_trace_to_outcome_trace(prediction_trace)
        selected = self._select_balanced_portfolio(
            trace=candidate_trace,
            warmup_samples=12_000,
            block_size=256,
            max_strategies=3,
        )
        trace = _subset_outcome_trace(candidate_trace, selected)
        meta_config = MetaControllerConfig(
            window_size=256,
            min_samples=2,
            delta=0.002,
            lambda_value=0.0,
            switch_cost=0.004,
            utility_weights={
                "reward_mean": 1.0,
                "reward_variance": 0.0,
                "compute_cost": 0.0,
                "switch_cost": 0.0,
            },
        )
        return self.run_outcome_trace(
            trace=trace,
            output_root=output_root,
            meta_config=meta_config,
            evaluation_interval=256,
            start_strategy=selected[0],
        )

    def run_insects_recurring_benchmark_with_hedge(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run Hedge replay validation on the official INSECTS recurring-drift stream."""
        prediction_trace = build_river_multiclass_prediction_trace(
            dataset_name="InsectsRecurring",
            stream=_iter_insects_stream(variant="incremental-reoccurring_balanced", max_samples=60_000),
            strategies=(
                ReplayStrategySpec("softmax_lr_0_01", 0.01, "Stationary online softmax regression with SGD learning_rate=0.01"),
                ReplayStrategySpec("softmax_lr_0_1", 0.1, "Stationary online softmax regression with SGD learning_rate=0.1"),
                ReplayStrategySpec("pa_classifier", 0.0, "Stationary online passive-aggressive classification", model_kind="pa_classifier"),
                ReplayStrategySpec("tree_classifier", 0.0, "Stationary online adaptive Hoeffding tree classification", model_kind="hoeffding_tree_classifier"),
            ),
            source_description=(
                "Official USP INSECTS recurring-drift stream replayed in temporal order; "
                "target is the insect class under incremental recurring concept drift."
            ),
            source_url="https://sites.google.com/view/uspdsrepository",
        )
        candidate_trace = _prediction_trace_to_outcome_trace(prediction_trace)
        selected = self._select_balanced_portfolio(
            trace=candidate_trace,
            warmup_samples=12_000,
            block_size=256,
            max_strategies=3,
        )
        trace = _subset_outcome_trace(candidate_trace, selected)
        return self.run_outcome_trace_with_hedge(
            trace=trace,
            output_root=output_root,
            evaluation_interval=256,
            start_strategy=selected[0],
            eta=0.35,
            switch_threshold=0.01,
            warmup_samples=512,
        )

    def run_insects_recurring_benchmark_with_recent_leader(self, *, output_root: str | Path) -> ReplayBenchmarkResult:
        """Run recent-leader replay validation on the official INSECTS recurring-drift stream."""
        prediction_trace = build_river_multiclass_prediction_trace(
            dataset_name="InsectsRecurring",
            stream=_iter_insects_stream(variant="incremental-reoccurring_balanced", max_samples=60_000),
            strategies=(
                ReplayStrategySpec("softmax_lr_0_01", 0.01, "Stationary online softmax regression with SGD learning_rate=0.01"),
                ReplayStrategySpec("softmax_lr_0_1", 0.1, "Stationary online softmax regression with SGD learning_rate=0.1"),
                ReplayStrategySpec("pa_classifier", 0.0, "Stationary online passive-aggressive classification", model_kind="pa_classifier"),
                ReplayStrategySpec("tree_classifier", 0.0, "Stationary online adaptive Hoeffding tree classification", model_kind="hoeffding_tree_classifier"),
            ),
            source_description=(
                "Official USP INSECTS recurring-drift stream replayed in temporal order; "
                "target is the insect class under incremental recurring concept drift."
            ),
            source_url="https://sites.google.com/view/uspdsrepository",
        )
        candidate_trace = _prediction_trace_to_outcome_trace(prediction_trace)
        selected = self._select_balanced_portfolio(
            trace=candidate_trace,
            warmup_samples=12_000,
            block_size=256,
            max_strategies=3,
        )
        trace = _subset_outcome_trace(candidate_trace, selected)
        return self.run_outcome_trace_with_recent_leader(
            trace=trace,
            output_root=output_root,
            evaluation_interval=256,
            start_strategy=selected[0],
            lookback_blocks=3,
            margin=0.002,
            warmup_blocks=2,
            cooldown_blocks=1,
            incumbent_floor=0.001,
        )

    def _validate_prediction_trace(self, trace: PredictionTrace) -> int:
        sample_count = len(trace.targets)
        if sample_count == 0:
            raise ValueError("trace.targets must not be empty")
        for name, predictions in trace.predictions_by_strategy.items():
            if len(predictions) != sample_count:
                raise ValueError(
                    f"prediction trace length mismatch for {name!r}: "
                    f"{len(predictions)} != {sample_count}"
                )
        return sample_count

    def _validate_outcome_trace(self, trace: OutcomeTrace) -> int:
        if not trace.rewards_by_strategy:
            raise ValueError("trace.rewards_by_strategy must not be empty")
        if set(trace.rewards_by_strategy) != set(trace.successes_by_strategy):
            raise ValueError("trace reward/success strategy keys must match")
        sample_count = len(next(iter(trace.rewards_by_strategy.values())))
        if sample_count == 0:
            raise ValueError("trace rewards must not be empty")
        for name, rewards in trace.rewards_by_strategy.items():
            if len(rewards) != sample_count:
                raise ValueError(f"reward trace length mismatch for {name!r}")
            if len(trace.successes_by_strategy[name]) != sample_count:
                raise ValueError(f"success trace length mismatch for {name!r}")
        return sample_count

    def _latest_window_metric(
        self,
        collector: MetricsCollector,
        meta_config: MetaControllerConfig,
    ):
        if len(collector.episodes) < meta_config.window_size:
            return None

        temp = MetricsCollector()
        for episode in collector.episodes[-meta_config.window_size :]:
            temp.record_episode(
                episode_index=episode.episode_index,
                reward=episode.reward,
                success=episode.success,
                active_strategy=episode.active_strategy,
                steps=episode.steps,
                compute_cost=episode.compute_cost,
                learning_progress=episode.learning_progress,
                fallback_triggered=episode.fallback_triggered,
            )
        return temp.window_metrics(
            meta_config.window_size,
            switch_cost=meta_config.switch_cost,
            rolling=False,
        )[0]

    def _select_candidate(
        self,
        *,
        current_strategy: str,
        window_histories: Mapping[str, list],
        meta_config: MetaControllerConfig,
    ) -> str | None:
        candidates: list[tuple[float, float, str]] = []
        for name, metrics in window_histories.items():
            if name == current_strategy or len(metrics) < meta_config.min_samples:
                continue
            evaluation = self._evaluator.evaluate_strategy(
                name,
                metrics[-meta_config.min_samples :],
                meta_config=meta_config,
                decision_switch_cost=meta_config.switch_cost,
            )
            candidates.append((evaluation.lcb, evaluation.mean_utility, name))

        if not candidates:
            return None
        candidates.sort(reverse=True)
        return candidates[0][2]

    def _block_delta_statistics(
        self,
        *,
        adaptive_rewards: tuple[float, ...] | list[float],
        best_fixed_rewards: tuple[float, ...] | list[float],
        block_size: int,
    ) -> tuple[float, float, float, int]:
        deltas: list[float] = []
        total = min(len(adaptive_rewards), len(best_fixed_rewards))
        for start in range(0, total - block_size + 1, block_size):
            adaptive_block = adaptive_rewards[start : start + block_size]
            fixed_block = best_fixed_rewards[start : start + block_size]
            deltas.append(fmean(adaptive_block) - fmean(fixed_block))
        if not deltas:
            return 0.0, 0.0, 0.0, 0
        mean_delta = fmean(deltas)
        std_delta = pstdev(deltas) if len(deltas) > 1 else 0.0
        ci95 = 1.96 * (std_delta / sqrt(len(deltas))) if len(deltas) > 1 else 0.0
        return mean_delta, std_delta, ci95, len(deltas)

    def _recent_block_mean(self, block_rewards: list[float], lookback_blocks: int) -> float:
        recent = block_rewards[-lookback_blocks:]
        if not recent:
            return 0.0
        return fmean(recent)

    def _select_balanced_portfolio(
        self,
        *,
        trace: OutcomeTrace,
        warmup_samples: int,
        block_size: int,
        max_strategies: int,
        diversity_weight: float = 0.05,
    ) -> tuple[str, ...]:
        """Select a diverse stationary portfolio from a broader candidate bank."""
        names = tuple(sorted(trace.rewards_by_strategy))
        if len(names) <= max_strategies:
            return names

        effective_warmup = max(block_size, min(warmup_samples, len(next(iter(trace.rewards_by_strategy.values())))))
        calibration_start = effective_warmup // 2
        warmup_means = {
            name: fmean(trace.rewards_by_strategy[name][calibration_start:effective_warmup])
            for name in names
        }
        leader_counts = {name: 0 for name in names}
        for start in range(calibration_start, effective_warmup - block_size + 1, block_size):
            block_scores = {
                name: fmean(trace.rewards_by_strategy[name][start : start + block_size])
                for name in names
            }
            leader = max(block_scores, key=lambda name: (block_scores[name], warmup_means[name], name))
            leader_counts[leader] += 1

        selected: list[str] = []
        leader_ranked = sorted(
            names,
            key=lambda name: (leader_counts[name], warmup_means[name], name),
            reverse=True,
        )
        for name in leader_ranked:
            if leader_counts[name] <= 0:
                break
            selected.append(name)
            if len(selected) >= max_strategies:
                return tuple(selected)

        if not selected:
            selected.append(max(names, key=lambda name: (warmup_means[name], name)))

        while len(selected) < max_strategies:
            best_name: str | None = None
            best_composite: tuple[float, float, float, str] | None = None
            for name in names:
                if name in selected:
                    continue
                disagreement = min(
                    self._warmup_disagreement(trace, name, incumbent, calibration_start, effective_warmup)
                    for incumbent in selected
                )
                composite = (
                    warmup_means[name] + diversity_weight * disagreement,
                    warmup_means[name],
                    disagreement,
                    name,
                )
                if best_composite is None or composite > best_composite:
                    best_name = name
                    best_composite = composite
            if best_name is None:
                break
            selected.append(best_name)

        return tuple(selected)

    def _warmup_disagreement(
        self,
        trace: OutcomeTrace,
        left_name: str,
        right_name: str,
        start_index: int,
        warmup_samples: int,
    ) -> float:
        left = trace.successes_by_strategy[left_name][start_index:warmup_samples]
        right = trace.successes_by_strategy[right_name][start_index:warmup_samples]
        if not left:
            return 0.0
        return sum(1 for left_value, right_value in zip(left, right) if left_value != right_value) / len(left)

    def _persist_result(
        self,
        *,
        result: ReplayBenchmarkResult,
        trace: OutcomeTrace,
        decisions: list[ReplayDecisionRecord],
        output_root: str | Path,
    ) -> ReplayBenchmarkResult:
        root = Path(output_root).resolve()
        root.mkdir(parents=True, exist_ok=True)

        decisions_path = root / "decisions.csv"
        summary_json_path = root / "summary.json"
        report_md_path = root / "summary.md"
        oracle_score, oracle_gain, oracle_capture_ratio = self._oracle_statistics(
            trace=trace,
            adaptive_score=result.adaptive_score,
            best_fixed_score=result.best_fixed_score,
        )

        self._write_decisions_csv(decisions_path, decisions)
        summary_payload = {
            "dataset_name": result.dataset_name,
            "score_name": result.score_name,
            "policy_name": result.policy_name,
            "sample_count": result.sample_count,
            "evaluation_interval": result.evaluation_interval,
            "window_size": result.window_size,
            "start_strategy": result.start_strategy,
            "final_strategy": result.final_strategy,
            "switch_count": result.switch_count,
            "adaptive_score": result.adaptive_score,
            "best_fixed_strategy": result.best_fixed_strategy,
            "best_fixed_score": result.best_fixed_score,
            "oracle_score": oracle_score,
            "oracle_gain": oracle_gain,
            "oracle_capture_ratio": oracle_capture_ratio,
            "delta_vs_best_fixed": result.delta_vs_best_fixed,
            "fixed_scores": result.fixed_scores,
            "block_delta_mean": result.block_delta_mean,
            "block_delta_std": result.block_delta_std,
            "block_delta_ci95": result.block_delta_ci95,
            "block_count": result.block_count,
            "source_description": trace.source_description,
            "source_url": trace.source_url,
            "decision_rows": len(decisions),
            "adaptive_accuracy": result.adaptive_accuracy,
            "best_fixed_accuracy": result.best_fixed_accuracy,
            "fixed_accuracies": result.fixed_accuracies,
        }
        persisted_result = ReplayBenchmarkResult(
            dataset_name=result.dataset_name,
            score_name=result.score_name,
            policy_name=result.policy_name,
            sample_count=result.sample_count,
            evaluation_interval=result.evaluation_interval,
            window_size=result.window_size,
            start_strategy=result.start_strategy,
            final_strategy=result.final_strategy,
            switch_count=result.switch_count,
            adaptive_score=result.adaptive_score,
            best_fixed_strategy=result.best_fixed_strategy,
            best_fixed_score=result.best_fixed_score,
            delta_vs_best_fixed=result.delta_vs_best_fixed,
            fixed_scores=result.fixed_scores,
            block_delta_mean=result.block_delta_mean,
            block_delta_std=result.block_delta_std,
            block_delta_ci95=result.block_delta_ci95,
            block_count=result.block_count,
            decision_csv_path=str(decisions_path),
            summary_json_path=str(summary_json_path),
            report_md_path=str(report_md_path),
            oracle_score=oracle_score,
            oracle_gain=oracle_gain,
            oracle_capture_ratio=oracle_capture_ratio,
        )
        summary_json_path.write_text(json.dumps(summary_payload, ensure_ascii=True, indent=2), encoding="utf-8")
        report_md_path.write_text(
            self._build_report(result=persisted_result, trace=trace, decisions=decisions),
            encoding="utf-8",
        )
        return persisted_result

    def _write_decisions_csv(self, path: Path, decisions: list[ReplayDecisionRecord]) -> None:
        with path.open("w", encoding="utf-8", newline="") as handle:
            fallback_row = ReplayDecisionRecord(
                sample_index=0,
                evaluation_index=0,
                current_strategy="",
                candidate_strategy=None,
                action="stay",
                switched=False,
                reason_code="",
                decision_margin=None,
                decision_threshold=0.0,
                reason="",
            )
            fieldnames = list(asdict(decisions[0]).keys()) if decisions else list(asdict(fallback_row).keys())
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for decision in decisions:
                writer.writerow(asdict(decision))

    def _build_report(
        self,
        *,
        result: ReplayBenchmarkResult,
        trace: OutcomeTrace,
        decisions: list[ReplayDecisionRecord],
    ) -> str:
        lines = [
            "# Real-Stream Benchmark Replay",
            "",
            f"- dataset: `{result.dataset_name}`",
            f"- score_name: `{result.score_name}`",
            f"- policy_name: `{result.policy_name}`",
            f"- samples: `{result.sample_count}`",
            f"- source: {trace.source_description}",
            f"- source_url: `{trace.source_url}`",
            f"- start_strategy: `{result.start_strategy}`",
            f"- final_strategy: `{result.final_strategy}`",
            f"- switch_count: `{result.switch_count}`",
            "",
            "## Score Summary",
            "",
            "| Mode | Score |",
            "| --- | ---: |",
            f"| adaptive | {result.adaptive_score:.6f} |",
            f"| oracle | {result.oracle_score:.6f} |",
        ]
        for name, score in sorted(result.fixed_scores.items()):
            lines.append(f"| {name} | {score:.6f} |")
        lines.extend(
            [
                "",
                f"- best_fixed_strategy: `{result.best_fixed_strategy}`",
                f"- best_fixed_score: `{result.best_fixed_score:.6f}`",
                f"- oracle_score: `{result.oracle_score:.6f}`",
                f"- oracle_gain: `{result.oracle_gain:.6f}`",
                f"- oracle_capture_ratio: `{result.oracle_capture_ratio:.6f}`",
                f"- adaptive_delta_vs_best_fixed: `{result.delta_vs_best_fixed:.6f}`",
                f"- block_delta_mean: `{result.block_delta_mean:.6f}`",
                f"- block_delta_ci95: `{result.block_delta_ci95:.6f}`",
                f"- block_count: `{result.block_count}`",
                "",
                "## Decisions",
                "",
                "| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |",
                "| ---: | --- | --- | --- | ---: | ---: | --- |",
            ]
        )
        for decision in decisions[:20]:
            margin = "" if decision.decision_margin is None else f"{decision.decision_margin:.6f}"
            candidate = "" if decision.candidate_strategy is None else decision.candidate_strategy
            lines.append(
                f"| {decision.sample_index} | {decision.action} | {decision.current_strategy} | "
                f"{candidate} | {margin} | {decision.decision_threshold:.6f} | {decision.reason_code} |"
            )
        if len(decisions) > 20:
            lines.extend(["", f"... truncated {len(decisions) - 20} additional decision rows in `decisions.csv`."])
        return "\n".join(lines) + "\n"

    def _build_suite_report(self, results: tuple[ReplayBenchmarkResult, ...]) -> str:
        lines = [
            "# Real-Stream Benchmark Suite",
            "",
            "| Dataset | Policy | Score | Adaptive | Best Fixed | Oracle | Delta | Capture | Switches | Block CI95 |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for result in results:
            lines.append(
                f"| {result.dataset_name} | {result.policy_name} | {result.score_name} | {result.adaptive_score:.6f} | "
                f"{result.best_fixed_score:.6f} | {result.oracle_score:.6f} | {result.delta_vs_best_fixed:.6f} | "
                f"{result.oracle_capture_ratio:.6f} | {result.switch_count} | {result.block_delta_ci95:.6f} |"
            )
        lines.extend(
            [
                "",
                f"- wins_vs_best_fixed: `{sum(1 for result in results if result.delta_vs_best_fixed > 0.0)}`",
                f"- non_losses_vs_best_fixed: `{sum(1 for result in results if result.delta_vs_best_fixed >= 0.0)}`",
                f"- oracle_gain_mean: `{fmean(result.oracle_gain for result in results):.6f}`",
                f"- oracle_capture_mean: `{fmean(result.oracle_capture_ratio for result in results):.6f}`",
                "- interpretation note: benchmark profile suites compare controller families on replayed streams and should be read alongside sample counts, block CI95, best-fixed deltas, and oracle-capture ratios.",
            ]
        )
        return "\n".join(lines) + "\n"

    def _build_profile_suite_report(self, results: tuple[ReplayBenchmarkResult, ...]) -> str:
        lines = [
            "# Benchmark Profile Suite",
            "",
            "| Dataset | Profile | Score | Adaptive | Best Fixed | Oracle | Delta | Capture | Switches | Block CI95 |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for result in results:
            lines.append(
                f"| {result.dataset_name} | {result.policy_name} | {result.score_name} | {result.adaptive_score:.6f} | "
                f"{result.best_fixed_score:.6f} | {result.oracle_score:.6f} | {result.delta_vs_best_fixed:.6f} | "
                f"{result.oracle_capture_ratio:.6f} | {result.switch_count} | {result.block_delta_ci95:.6f} |"
            )
        lines.extend(
            [
                "",
                f"- wins_vs_best_fixed: `{sum(1 for result in results if result.delta_vs_best_fixed > 0.0)}`",
                f"- non_losses_vs_best_fixed: `{sum(1 for result in results if result.delta_vs_best_fixed >= 0.0)}`",
                f"- oracle_gain_mean: `{fmean(result.oracle_gain for result in results):.6f}`",
                f"- oracle_capture_mean: `{fmean(result.oracle_capture_ratio for result in results):.6f}`",
            ]
        )
        return "\n".join(lines) + "\n"

    def _oracle_statistics(
        self,
        *,
        trace: OutcomeTrace,
        adaptive_score: float,
        best_fixed_score: float,
    ) -> tuple[float, float, float]:
        sample_count = len(next(iter(trace.rewards_by_strategy.values()), ()))
        if sample_count <= 0:
            return best_fixed_score, 0.0, 0.0
        oracle_score = sum(
            max(rewards[offset] for rewards in trace.rewards_by_strategy.values())
            for offset in range(sample_count)
        ) / sample_count
        oracle_gain = oracle_score - best_fixed_score
        delta_vs_best_fixed = adaptive_score - best_fixed_score
        if oracle_gain <= 1e-12:
            return oracle_score, oracle_gain, 0.0
        return oracle_score, oracle_gain, max(0.0, delta_vs_best_fixed / oracle_gain)


def _default_feature_transform(features: Mapping[str, object]) -> dict[str, float]:
    """Convert mixed-type streaming features into a simple online-linear feature map."""
    transformed: dict[str, float] = {}
    for key, value in features.items():
        if isinstance(value, bool):
            transformed[key] = float(value)
            continue
        if isinstance(value, (int, float)):
            transformed[key] = float(value)
            continue
        if isinstance(value, datetime):
            transformed[f"{key}_ordinal"] = float(value.toordinal())
            transformed[f"{key}_hour"] = float(value.hour)
            transformed[f"{key}_dow"] = float(value.weekday())
            transformed[f"{key}_month"] = float(value.month)
            continue
        if value is None:
            continue
        transformed[f"{key}={value}"] = 1.0
    return transformed


def _resolve_regression_scale(targets: list[float]) -> float:
    """Compute a stable normalization scale for reward shaping."""
    scale = pstdev(targets) if len(targets) > 1 else 1.0
    if scale <= 1e-9:
        scale = max(1.0, abs(fmean(targets)) if targets else 1.0)
    return scale


def _prediction_trace_to_outcome_trace(trace: PredictionTrace) -> OutcomeTrace:
    """Convert a prediction trace into a generic reward trace."""
    return OutcomeTrace(
        dataset_name=trace.dataset_name,
        score_name="accuracy",
        rewards_by_strategy={
            name: tuple(float(prediction == target) for prediction, target in zip(predictions, trace.targets))
            for name, predictions in trace.predictions_by_strategy.items()
        },
        successes_by_strategy={
            name: tuple(prediction == target for prediction, target in zip(predictions, trace.targets))
            for name, predictions in trace.predictions_by_strategy.items()
        },
        source_description=trace.source_description,
        source_url=trace.source_url,
    )


def _subset_outcome_trace(trace: OutcomeTrace, selected_names: Iterable[str]) -> OutcomeTrace:
    """Restrict an outcome trace to a selected stationary portfolio."""
    selected = tuple(selected_names)
    return OutcomeTrace(
        dataset_name=trace.dataset_name,
        score_name=trace.score_name,
        rewards_by_strategy={name: trace.rewards_by_strategy[name] for name in selected},
        successes_by_strategy={name: trace.successes_by_strategy[name] for name in selected},
        source_description=trace.source_description,
        source_url=trace.source_url,
    )


def _subset_trace_by_length(trace: OutcomeTrace, sample_count: int) -> OutcomeTrace:
    """Restrict an outcome trace to its first N samples without changing the strategy set."""
    limited = max(1, sample_count)
    return OutcomeTrace(
        dataset_name=trace.dataset_name,
        score_name=trace.score_name,
        rewards_by_strategy={name: rewards[:limited] for name, rewards in trace.rewards_by_strategy.items()},
        successes_by_strategy={name: rewards[:limited] for name, rewards in trace.successes_by_strategy.items()},
        source_description=trace.source_description,
        source_url=trace.source_url,
    )


def _limit_stream(
    stream: Iterable[tuple[Mapping[str, object], object]],
    *,
    max_samples: int | None,
) -> Iterator[tuple[Mapping[str, object], object]]:
    """Yield at most N samples from an arbitrary stream."""
    if max_samples is None:
        yield from stream
        return
    for index, row in enumerate(stream, start=1):
        yield row
        if index >= max_samples:
            return


def _build_binary_classifier_model(spec: ReplayStrategySpec):
    """Instantiate one binary online classifier from a strategy spec."""
    model_kind = getattr(spec, "model_kind", "linear_sgd")
    learning_rate = getattr(spec, "learning_rate", 0.0)
    if model_kind == "linear_sgd":
        return preprocessing.StandardScaler() | linear_model.LogisticRegression(optimizer=optim.SGD(learning_rate))
    if model_kind == "pa_classifier":
        return preprocessing.StandardScaler() | linear_model.PAClassifier()
    if model_kind == "gaussian_nb":
        return naive_bayes.GaussianNB()
    if model_kind == "hoeffding_tree_classifier":
        return tree.HoeffdingAdaptiveTreeClassifier()
    if model_kind == "knn_classifier":
        return preprocessing.StandardScaler() | neighbors.KNNClassifier()
    if model_kind == "windowed_rf_classifier":
        return _WindowedSklearnClassifier(
            RandomForestClassifier(n_estimators=20, random_state=42),
            window_size=256,
            refit_interval=64,
        )
    if model_kind == "windowed_histgb_classifier":
        return _WindowedSklearnClassifier(
            HistGradientBoostingClassifier(random_state=42),
            window_size=256,
            refit_interval=128,
        )
    raise ValueError(f"unsupported binary classifier model_kind: {model_kind!r}")


def _build_multiclass_classifier_model(spec: ReplayStrategySpec):
    """Instantiate one multi-class online classifier from a strategy spec."""
    model_kind = getattr(spec, "model_kind", "linear_sgd")
    learning_rate = getattr(spec, "learning_rate", 0.0)
    if model_kind == "linear_sgd":
        return preprocessing.StandardScaler() | linear_model.SoftmaxRegression(optimizer=optim.SGD(learning_rate))
    if model_kind == "pa_classifier":
        return preprocessing.StandardScaler() | linear_model.PAClassifier()
    if model_kind == "gaussian_nb":
        return naive_bayes.GaussianNB()
    if model_kind == "hoeffding_tree_classifier":
        return tree.HoeffdingAdaptiveTreeClassifier()
    if model_kind == "knn_classifier":
        return preprocessing.StandardScaler() | neighbors.KNNClassifier()
    if model_kind == "windowed_rf_classifier":
        return _WindowedSklearnClassifier(
            RandomForestClassifier(n_estimators=20, random_state=42),
            window_size=256,
            refit_interval=64,
        )
    if model_kind == "windowed_histgb_classifier":
        return _WindowedSklearnClassifier(
            HistGradientBoostingClassifier(random_state=42),
            window_size=256,
            refit_interval=128,
        )
    raise ValueError(f"unsupported multiclass classifier model_kind: {model_kind!r}")


def _build_regressor_model(spec: ReplayStrategySpec):
    """Instantiate one online regressor from a strategy spec."""
    model_kind = getattr(spec, "model_kind", "linear_sgd")
    learning_rate = getattr(spec, "learning_rate", 0.0)
    if model_kind == "linear_sgd":
        return preprocessing.StandardScaler() | linear_model.LinearRegression(optimizer=optim.SGD(learning_rate))
    if model_kind == "pa_regressor":
        return preprocessing.StandardScaler() | linear_model.PARegressor()
    if model_kind == "hoeffding_tree_regressor":
        return tree.HoeffdingAdaptiveTreeRegressor()
    if model_kind == "knn_regressor":
        return preprocessing.StandardScaler() | neighbors.KNNRegressor()
    if model_kind == "windowed_rf_regressor":
        return _WindowedSklearnRegressor(
            RandomForestRegressor(n_estimators=20, random_state=42),
            window_size=256,
            refit_interval=64,
        )
    if model_kind == "windowed_histgb_regressor":
        return _WindowedSklearnRegressor(
            HistGradientBoostingRegressor(random_state=42),
            window_size=256,
            refit_interval=128,
        )
    raise ValueError(f"unsupported regressor model_kind: {model_kind!r}")


def _iter_airlines_stream(*, max_samples: int | None = None) -> Iterator[tuple[dict[str, object], bool]]:
    """Yield the MOA Airlines stream from the official SourceForge archive."""
    url = "https://downloads.sourceforge.net/project/moa-datastream/Datasets/Classification/airlines.arff.zip"
    raw = urllib.request.urlopen(url, timeout=120).read()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        with archive.open("airlines.arff") as handle:
            in_data = False
            yielded = 0
            for raw_line in handle:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line or line.startswith("%"):
                    continue
                if not in_data:
                    if line.lower() == "@data":
                        in_data = True
                    continue
                parts = [part.strip().strip("'") for part in line.split(",")]
                if len(parts) != 8:
                    continue
                features = {
                    "Airline": parts[0],
                    "Flight": float(parts[1]),
                    "AirportFrom": parts[2],
                    "AirportTo": parts[3],
                    "DayOfWeek": float(parts[4]),
                    "Time": float(parts[5]),
                    "Length": float(parts[6]),
                }
                target = parts[7] == "1"
                yield features, target
                yielded += 1
                if max_samples is not None and yielded >= max_samples:
                    return


def _ensure_usp_ds_repository_zip() -> Path:
    """Download and cache the official USP DS Repository archive."""
    cache_root = Path.home() / "autorl_data"
    cache_root.mkdir(parents=True, exist_ok=True)
    archive_path = cache_root / "usp_ds_repository.zip"
    if archive_path.exists():
        return archive_path

    landing_url = "https://drive.usercontent.google.com/download?id=1JERZnbGGToAEz_3LRV7n2Vz79LiDAEY-&export=download"
    html = urllib.request.urlopen(landing_url, timeout=120).read().decode("utf-8", errors="replace")
    uuid_match = re.search(r'name="uuid" value="([^"]+)"', html)
    if uuid_match is None:
        raise RuntimeError("failed to resolve Google Drive confirmation token for USP DS Repository")
    uuid = uuid_match.group(1)
    download_url = (
        "https://drive.usercontent.google.com/download"
        "?id=1JERZnbGGToAEz_3LRV7n2Vz79LiDAEY-&export=download&confirm=t"
        f"&uuid={uuid}"
    )
    urllib.request.urlretrieve(download_url, archive_path)
    return archive_path


def _iter_insects_stream(
    *,
    variant: str = "incremental-reoccurring_balanced",
    max_samples: int | None = None,
) -> Iterator[tuple[dict[str, float], int]]:
    """Yield one INSECTS variant from the official USP DS Repository archive."""
    archive_path = _ensure_usp_ds_repository_zip()
    member_name = f"USP DS Repository/INSECTS/INSECTS {variant}.csv"
    with zipfile.ZipFile(archive_path) as archive:
        with archive.open(member_name) as handle:
            yielded = 0
            for raw_line in handle:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                parts = [part.strip() for part in line.split(",")]
                values = [float(value) for value in parts]
                features = {f"f{index}": value for index, value in enumerate(values[:-1])}
                target = int(values[-1])
                yield features, target
                yielded += 1
                if max_samples is not None and yielded >= max_samples:
                    return
