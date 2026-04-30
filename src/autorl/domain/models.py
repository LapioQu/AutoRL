"""Core domain entities and configuration models for phase 1."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
import hashlib
import json
from typing import Any, Mapping

from autorl.domain.errors import ConfigValidationError


class ScenarioName(str, Enum):
    """Supported scenario types from the technical specification."""

    STATIONARY = "stationary"
    ABRUPT_DRIFT = "abrupt_drift"
    GRADUAL_DRIFT = "gradual_drift"
    NOISY_REWARD = "noisy_reward"
    FALLBACK = "fallback"
    REPRODUCIBILITY = "reproducibility"


class RunMode(str, Enum):
    """Experiment execution mode."""

    ADAPTIVE = "adaptive"
    BASELINE = "baseline"


class ExperimentStatus(str, Enum):
    """Persisted lifecycle states for orchestrated experiments."""

    CREATED = "created"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    COMPLETED = "completed"
    FAILED = "failed"


class DecisionAction(str, Enum):
    """Stay/Switch action types for future phases."""

    STAY = "stay"
    SWITCH = "switch"
    FALLBACK = "fallback"


class DecisionReason(str, Enum):
    """Structured reasons for metacontroller decisions."""

    SWITCH_ADVANTAGE = "switch_advantage"
    INSUFFICIENT_SAMPLES = "insufficient_samples"
    MISSING_METRICS = "missing_metrics"
    INVALID_CANDIDATE = "invalid_candidate"
    HIGH_UNCERTAINTY = "high_uncertainty"
    NO_CANDIDATE_IMPROVEMENT = "no_candidate_improvement"
    SAFE_STAY_AFTER_ERROR = "safe_stay_after_error"


class ArtifactKind(str, Enum):
    """Artifact types stored for an experiment."""

    CONFIG = "config"
    METRICS = "metrics"
    DECISIONS = "decisions"
    REPORT = "report"
    PLOT = "plot"
    LOG = "log"
    OTHER = "other"


def _now_utc() -> datetime:
    return datetime.now(tz=UTC)


def _ensure_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigValidationError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_positive_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ConfigValidationError(f"{field_name} must be a positive integer")
    return value


def _ensure_non_negative_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ConfigValidationError(f"{field_name} must be a non-negative integer")
    return value


def _ensure_non_negative_float(value: Any, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or float(value) < 0.0:
        raise ConfigValidationError(f"{field_name} must be a non-negative number")
    return float(value)


def _ensure_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ConfigValidationError(f"{field_name} must be a mapping")
    if not all(isinstance(key, str) for key in value):
        raise ConfigValidationError(f"{field_name} keys must be strings")
    return value


def _normalize_json_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _normalize_json_value(val) for key, val in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, tuple):
        return [_normalize_json_value(item) for item in value]
    if isinstance(value, list):
        return [_normalize_json_value(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    return value


def _canonical_hash(payload: Mapping[str, Any]) -> str:
    canonical_json = json.dumps(
        _normalize_json_value(dict(payload)),
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class LearningStrategy:
    """Declared learning strategy candidate for an experiment."""

    name: str
    parameters: Mapping[str, Any] = field(default_factory=dict)
    enabled: bool = True
    compute_cost: float = 0.0
    description: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _ensure_non_empty_text(self.name, "strategy.name"))
        object.__setattr__(self, "parameters", dict(_ensure_mapping(self.parameters, "strategy.parameters")))
        object.__setattr__(self, "compute_cost", _ensure_non_negative_float(self.compute_cost, "strategy.compute_cost"))
        if self.description is not None:
            object.__setattr__(self, "description", _ensure_non_empty_text(self.description, "strategy.description"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "parameters": dict(self.parameters),
            "enabled": self.enabled,
            "compute_cost": self.compute_cost,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "LearningStrategy":
        payload = _ensure_mapping(data, "strategy")
        return cls(
            name=payload.get("name"),
            parameters=payload.get("parameters", {}),
            enabled=bool(payload.get("enabled", True)),
            compute_cost=payload.get("compute_cost", 0.0),
            description=payload.get("description"),
        )


@dataclass(frozen=True, slots=True)
class ScenarioConfig:
    """Scenario parameters used by the future RL environment."""

    name: ScenarioName
    episodes: int
    steps_per_episode: int
    reward_noise_std: float = 0.0
    drift_episode: int | None = None
    drift_start_episode: int | None = None
    drift_end_episode: int | None = None
    fallback_patience: int | None = None
    tags: tuple[str, ...] = ()
    description: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "episodes", _ensure_positive_int(self.episodes, "scenario.episodes"))
        object.__setattr__(self, "steps_per_episode", _ensure_positive_int(self.steps_per_episode, "scenario.steps_per_episode"))
        object.__setattr__(self, "reward_noise_std", _ensure_non_negative_float(self.reward_noise_std, "scenario.reward_noise_std"))
        object.__setattr__(self, "tags", tuple(_ensure_non_empty_text(tag, "scenario.tags[]") for tag in self.tags))
        if self.description is not None:
            object.__setattr__(self, "description", _ensure_non_empty_text(self.description, "scenario.description"))

        if self.drift_episode is not None:
            object.__setattr__(self, "drift_episode", _ensure_positive_int(self.drift_episode, "scenario.drift_episode"))
        if self.drift_start_episode is not None:
            object.__setattr__(self, "drift_start_episode", _ensure_positive_int(self.drift_start_episode, "scenario.drift_start_episode"))
        if self.drift_end_episode is not None:
            object.__setattr__(self, "drift_end_episode", _ensure_positive_int(self.drift_end_episode, "scenario.drift_end_episode"))
        if self.fallback_patience is not None:
            object.__setattr__(self, "fallback_patience", _ensure_positive_int(self.fallback_patience, "scenario.fallback_patience"))

        if self.name is ScenarioName.STATIONARY:
            self._validate_stationary()
        elif self.name is ScenarioName.ABRUPT_DRIFT:
            self._validate_abrupt_drift()
        elif self.name is ScenarioName.GRADUAL_DRIFT:
            self._validate_gradual_drift()
        elif self.name is ScenarioName.NOISY_REWARD:
            self._validate_noisy_reward()
        elif self.name is ScenarioName.FALLBACK:
            self._validate_fallback()
        elif self.name is ScenarioName.REPRODUCIBILITY:
            self._validate_reproducibility()

    def _validate_stationary(self) -> None:
        if any(value is not None for value in (self.drift_episode, self.drift_start_episode, self.drift_end_episode, self.fallback_patience)):
            raise ConfigValidationError("stationary scenario must not define drift or fallback fields")

    def _validate_abrupt_drift(self) -> None:
        if self.drift_episode is None:
            raise ConfigValidationError("abrupt_drift scenario requires scenario.drift_episode")
        if not 1 <= self.drift_episode < self.episodes:
            raise ConfigValidationError("scenario.drift_episode must be between 1 and scenario.episodes - 1")
        if any(value is not None for value in (self.drift_start_episode, self.drift_end_episode, self.fallback_patience)):
            raise ConfigValidationError("abrupt_drift scenario only supports scenario.drift_episode")

    def _validate_gradual_drift(self) -> None:
        if self.drift_start_episode is None or self.drift_end_episode is None:
            raise ConfigValidationError("gradual_drift scenario requires scenario.drift_start_episode and scenario.drift_end_episode")
        if not 1 <= self.drift_start_episode < self.drift_end_episode < self.episodes:
            raise ConfigValidationError("gradual drift window must satisfy 1 <= start < end < scenario.episodes")
        if any(value is not None for value in (self.drift_episode, self.fallback_patience)):
            raise ConfigValidationError("gradual_drift scenario only supports gradual drift fields")

    def _validate_noisy_reward(self) -> None:
        if self.reward_noise_std <= 0.0:
            raise ConfigValidationError("noisy_reward scenario requires scenario.reward_noise_std > 0")
        if any(value is not None for value in (self.drift_episode, self.drift_start_episode, self.drift_end_episode, self.fallback_patience)):
            raise ConfigValidationError("noisy_reward scenario must not define drift or fallback fields")

    def _validate_fallback(self) -> None:
        if self.fallback_patience is None:
            raise ConfigValidationError("fallback scenario requires scenario.fallback_patience")
        if any(value is not None for value in (self.drift_episode, self.drift_start_episode, self.drift_end_episode)):
            raise ConfigValidationError("fallback scenario must not define drift fields")

    def _validate_reproducibility(self) -> None:
        if any(value is not None for value in (self.drift_episode, self.drift_start_episode, self.drift_end_episode, self.fallback_patience)):
            raise ConfigValidationError("reproducibility scenario must not define drift or fallback fields")

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name.value,
            "episodes": self.episodes,
            "steps_per_episode": self.steps_per_episode,
            "reward_noise_std": self.reward_noise_std,
            "drift_episode": self.drift_episode,
            "drift_start_episode": self.drift_start_episode,
            "drift_end_episode": self.drift_end_episode,
            "fallback_patience": self.fallback_patience,
            "tags": list(self.tags),
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ScenarioConfig":
        payload = _ensure_mapping(data, "scenario")
        raw_name = payload.get("name")
        try:
            name = ScenarioName(raw_name)
        except ValueError as exc:
            raise ConfigValidationError(f"unsupported scenario.name: {raw_name!r}") from exc
        return cls(
            name=name,
            episodes=payload.get("episodes"),
            steps_per_episode=payload.get("steps_per_episode"),
            reward_noise_std=payload.get("reward_noise_std", 0.0),
            drift_episode=payload.get("drift_episode"),
            drift_start_episode=payload.get("drift_start_episode"),
            drift_end_episode=payload.get("drift_end_episode"),
            fallback_patience=payload.get("fallback_patience"),
            tags=tuple(payload.get("tags", ())),
            description=payload.get("description"),
        )


@dataclass(frozen=True, slots=True)
class MetaControllerConfig:
    """Formalized metacontroller thresholds used by later phases."""

    window_size: int
    min_samples: int
    delta: float = 0.0
    lambda_value: float = 1.0
    switch_cost: float = 0.0
    utility_weights: Mapping[str, float] = field(default_factory=lambda: {
        "reward_mean": 1.0,
        "reward_variance": 0.0,
        "compute_cost": 0.0,
        "switch_cost": 0.0,
    })

    def __post_init__(self) -> None:
        object.__setattr__(self, "window_size", _ensure_positive_int(self.window_size, "meta_controller.window_size"))
        object.__setattr__(self, "min_samples", _ensure_positive_int(self.min_samples, "meta_controller.min_samples"))
        object.__setattr__(self, "delta", _ensure_non_negative_float(self.delta, "meta_controller.delta"))
        object.__setattr__(self, "lambda_value", _ensure_non_negative_float(self.lambda_value, "meta_controller.lambda"))
        object.__setattr__(self, "switch_cost", _ensure_non_negative_float(self.switch_cost, "meta_controller.switch_cost"))

        normalized_weights = {
            key: _ensure_non_negative_float(value, f"meta_controller.utility_weights.{key}")
            for key, value in dict(_ensure_mapping(self.utility_weights, "meta_controller.utility_weights")).items()
        }
        expected_keys = {"reward_mean", "reward_variance", "compute_cost", "switch_cost"}
        if set(normalized_weights) != expected_keys:
            raise ConfigValidationError(
                "meta_controller.utility_weights must define reward_mean, reward_variance, compute_cost, switch_cost"
            )
        if self.min_samples > self.window_size:
            raise ConfigValidationError("meta_controller.min_samples must be <= meta_controller.window_size")
        if normalized_weights["reward_mean"] <= 0.0:
            raise ConfigValidationError("meta_controller.utility_weights.reward_mean must be > 0")

        object.__setattr__(self, "utility_weights", normalized_weights)

    def to_dict(self) -> dict[str, Any]:
        return {
            "window_size": self.window_size,
            "min_samples": self.min_samples,
            "delta": self.delta,
            "lambda": self.lambda_value,
            "switch_cost": self.switch_cost,
            "utility_weights": dict(self.utility_weights),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MetaControllerConfig":
        payload = _ensure_mapping(data, "meta_controller")
        return cls(
            window_size=payload.get("window_size"),
            min_samples=payload.get("min_samples"),
            delta=payload.get("delta", 0.0),
            lambda_value=payload.get("lambda", 1.0),
            switch_cost=payload.get("switch_cost", 0.0),
            utility_weights=payload.get(
                "utility_weights",
                {
                    "reward_mean": 1.0,
                    "reward_variance": 0.0,
                    "compute_cost": 0.0,
                    "switch_cost": 0.0,
                },
            ),
        )


@dataclass(frozen=True, slots=True)
class Config:
    """Canonical experiment configuration model."""

    schema_version: str
    experiment_name: str
    seed: int
    mode: RunMode
    scenario: ScenarioConfig
    strategies: tuple[LearningStrategy, ...]
    meta_controller: MetaControllerConfig
    artifacts_root: str = "artifacts"
    tags: tuple[str, ...] = ()
    notes: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "schema_version", _ensure_non_empty_text(self.schema_version, "schema_version"))
        object.__setattr__(self, "experiment_name", _ensure_non_empty_text(self.experiment_name, "experiment_name"))
        object.__setattr__(self, "seed", _ensure_non_negative_int(self.seed, "seed"))
        object.__setattr__(self, "artifacts_root", _ensure_non_empty_text(self.artifacts_root, "artifacts_root"))
        object.__setattr__(self, "tags", tuple(_ensure_non_empty_text(tag, "tags[]") for tag in self.tags))
        if self.notes is not None:
            object.__setattr__(self, "notes", _ensure_non_empty_text(self.notes, "notes"))

        if not self.strategies:
            raise ConfigValidationError("strategies must not be empty")
        enabled_names = [strategy.name for strategy in self.strategies if strategy.enabled]
        if not enabled_names:
            raise ConfigValidationError("at least one strategy must be enabled")
        if len(set(strategy.name for strategy in self.strategies)) != len(self.strategies):
            raise ConfigValidationError("strategy names must be unique")

    @property
    def config_hash(self) -> str:
        return _canonical_hash(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "experiment_name": self.experiment_name,
            "seed": self.seed,
            "mode": self.mode.value,
            "scenario": self.scenario.to_dict(),
            "strategies": [strategy.to_dict() for strategy in self.strategies],
            "meta_controller": self.meta_controller.to_dict(),
            "artifacts_root": self.artifacts_root,
            "tags": list(self.tags),
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Config":
        payload = _ensure_mapping(data, "config")
        raw_mode = payload.get("mode", RunMode.ADAPTIVE.value)
        try:
            mode = RunMode(raw_mode)
        except ValueError as exc:
            raise ConfigValidationError(f"unsupported mode: {raw_mode!r}") from exc

        strategies_raw = payload.get("strategies", [])
        if not isinstance(strategies_raw, list):
            raise ConfigValidationError("strategies must be a list")

        return cls(
            schema_version=payload.get("schema_version", "1.0"),
            experiment_name=payload.get("experiment_name"),
            seed=payload.get("seed"),
            mode=mode,
            scenario=ScenarioConfig.from_dict(payload.get("scenario", {})),
            strategies=tuple(LearningStrategy.from_dict(item) for item in strategies_raw),
            meta_controller=MetaControllerConfig.from_dict(payload.get("meta_controller", {})),
            artifacts_root=payload.get("artifacts_root", "artifacts"),
            tags=tuple(payload.get("tags", ())),
            notes=payload.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class Experiment:
    """Persistable experiment aggregate root."""

    experiment_id: str
    config: Config
    seed: int
    config_hash: str
    status: str = ExperimentStatus.CREATED.value
    source_experiment_id: str | None = None
    created_at: datetime = field(default_factory=_now_utc)

    def __post_init__(self) -> None:
        object.__setattr__(self, "experiment_id", _ensure_non_empty_text(self.experiment_id, "experiment_id"))
        object.__setattr__(self, "seed", _ensure_non_negative_int(self.seed, "experiment.seed"))
        object.__setattr__(self, "config_hash", _ensure_non_empty_text(self.config_hash, "experiment.config_hash"))
        object.__setattr__(self, "status", normalize_experiment_status(self.status).value)
        if self.source_experiment_id is not None:
            object.__setattr__(
                self,
                "source_experiment_id",
                _ensure_non_empty_text(self.source_experiment_id, "experiment.source_experiment_id"),
            )
        if self.seed != self.config.seed:
            raise ConfigValidationError("experiment.seed must match config.seed")
        if self.config_hash != self.config.config_hash:
            raise ConfigValidationError("experiment.config_hash must match config.config_hash")


def normalize_experiment_status(value: str | ExperimentStatus) -> ExperimentStatus:
    """Normalize persisted status values to the standard enum."""
    if isinstance(value, ExperimentStatus):
        return value
    try:
        return ExperimentStatus(_ensure_non_empty_text(str(value), "experiment.status"))
    except ValueError as exc:
        raise ConfigValidationError(f"unsupported experiment.status: {value!r}") from exc


_ALLOWED_EXPERIMENT_STATUS_TRANSITIONS: dict[ExperimentStatus, set[ExperimentStatus]] = {
    ExperimentStatus.CREATED: {ExperimentStatus.RUNNING, ExperimentStatus.FAILED, ExperimentStatus.STOPPED},
    ExperimentStatus.RUNNING: {ExperimentStatus.STOPPING, ExperimentStatus.COMPLETED, ExperimentStatus.FAILED},
    ExperimentStatus.STOPPING: {ExperimentStatus.STOPPED, ExperimentStatus.FAILED},
    ExperimentStatus.STOPPED: set(),
    ExperimentStatus.COMPLETED: set(),
    ExperimentStatus.FAILED: set(),
}


def ensure_experiment_status_transition(
    current_status: str | ExperimentStatus,
    next_status: str | ExperimentStatus,
) -> ExperimentStatus:
    """Validate and normalize one experiment status transition."""
    current = normalize_experiment_status(current_status)
    next_value = normalize_experiment_status(next_status)
    if current is next_value:
        return next_value
    if next_value not in _ALLOWED_EXPERIMENT_STATUS_TRANSITIONS[current]:
        raise ConfigValidationError(
            f"invalid experiment status transition: {current.value!r} -> {next_value.value!r}"
        )
    return next_value


@dataclass(frozen=True, slots=True)
class EpisodeMetric:
    """Episode-level metric record."""

    episode_index: int
    reward: float
    success: bool
    active_strategy: str
    steps: int
    compute_cost: float = 0.0
    learning_progress: float = 0.0
    fallback_triggered: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "episode_index", _ensure_non_negative_int(self.episode_index, "episode_metric.episode_index"))
        object.__setattr__(self, "active_strategy", _ensure_non_empty_text(self.active_strategy, "episode_metric.active_strategy"))
        object.__setattr__(self, "steps", _ensure_positive_int(self.steps, "episode_metric.steps"))
        object.__setattr__(self, "compute_cost", _ensure_non_negative_float(self.compute_cost, "episode_metric.compute_cost"))
        object.__setattr__(self, "learning_progress", float(self.learning_progress))
        if isinstance(self.reward, bool) or not isinstance(self.reward, (int, float)):
            raise ConfigValidationError("episode_metric.reward must be numeric")
        if isinstance(self.learning_progress, bool) or not isinstance(self.learning_progress, (int, float)):
            raise ConfigValidationError("episode_metric.learning_progress must be numeric")


@dataclass(frozen=True, slots=True)
class WindowMetric:
    """Aggregated metric record across an evaluation window."""

    window_index: int
    start_episode: int
    end_episode: int
    reward_mean: float
    reward_variance: float
    success_rate: float
    cumulative_reward: float
    switches: int
    compute_cost_mean: float = 0.0
    recovery_time: float = 0.0
    learning_progress_mean: float = 0.0
    utility_reward_mean: float | None = None
    utility_reward_variance: float | None = None
    utility_compute_cost: float | None = None
    utility_switch_cost: float | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "window_index", _ensure_non_negative_int(self.window_index, "window_metric.window_index"))
        object.__setattr__(self, "start_episode", _ensure_non_negative_int(self.start_episode, "window_metric.start_episode"))
        object.__setattr__(self, "end_episode", _ensure_non_negative_int(self.end_episode, "window_metric.end_episode"))
        object.__setattr__(self, "reward_variance", _ensure_non_negative_float(self.reward_variance, "window_metric.reward_variance"))
        object.__setattr__(self, "switches", _ensure_non_negative_int(self.switches, "window_metric.switches"))
        object.__setattr__(self, "compute_cost_mean", _ensure_non_negative_float(self.compute_cost_mean, "window_metric.compute_cost_mean"))
        object.__setattr__(self, "recovery_time", _ensure_non_negative_float(self.recovery_time, "window_metric.recovery_time"))
        if self.end_episode < self.start_episode:
            raise ConfigValidationError("window_metric.end_episode must be >= window_metric.start_episode")
        if not 0.0 <= float(self.success_rate) <= 1.0:
            raise ConfigValidationError("window_metric.success_rate must be between 0 and 1")
        if isinstance(self.reward_mean, bool) or not isinstance(self.reward_mean, (int, float)):
            raise ConfigValidationError("window_metric.reward_mean must be numeric")
        if isinstance(self.cumulative_reward, bool) or not isinstance(self.cumulative_reward, (int, float)):
            raise ConfigValidationError("window_metric.cumulative_reward must be numeric")
        if isinstance(self.learning_progress_mean, bool) or not isinstance(self.learning_progress_mean, (int, float)):
            raise ConfigValidationError("window_metric.learning_progress_mean must be numeric")


@dataclass(frozen=True, slots=True)
class Decision:
    """Future Stay/Switch decision log record."""

    evaluation_index: int
    action: DecisionAction
    current_strategy: str
    candidate_strategy: str | None
    reason: str
    utility_current: float | None = None
    utility_candidate: float | None = None
    lcb_current: float | None = None
    lcb_candidate: float | None = None
    switched: bool = False
    reason_code: DecisionReason | None = None
    decision_margin: float | None = None
    decision_threshold: float | None = None
    is_fallback: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "evaluation_index", _ensure_non_negative_int(self.evaluation_index, "decision.evaluation_index"))
        object.__setattr__(self, "current_strategy", _ensure_non_empty_text(self.current_strategy, "decision.current_strategy"))
        object.__setattr__(self, "reason", _ensure_non_empty_text(self.reason, "decision.reason"))
        if self.candidate_strategy is not None:
            object.__setattr__(self, "candidate_strategy", _ensure_non_empty_text(self.candidate_strategy, "decision.candidate_strategy"))
        if self.action is DecisionAction.SWITCH and self.candidate_strategy is None:
            raise ConfigValidationError("decision.candidate_strategy is required for switch actions")


@dataclass(frozen=True, slots=True)
class Artifact:
    """Artifact metadata tracked for a run."""

    kind: ArtifactKind
    path: str
    created_at: datetime = field(default_factory=_now_utc)
    description: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "path", _ensure_non_empty_text(self.path, "artifact.path"))
        if self.description is not None:
            object.__setattr__(self, "description", _ensure_non_empty_text(self.description, "artifact.description"))
