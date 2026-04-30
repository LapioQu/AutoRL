"""SQLite persistence for experiments, metrics, decisions, and artifacts."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum
import json
from pathlib import Path
import sqlite3
from typing import Any

from autorl.domain.models import (
    Artifact,
    Config,
    Decision,
    EpisodeMetric,
    Experiment,
    ensure_experiment_status_transition,
    normalize_experiment_status,
    WindowMetric,
)


def _json_ready(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    return value


class SQLiteRepository:
    """SQLite-backed repository for reproducible experiment data."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_schema()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_schema(self) -> None:
        schema = """
        CREATE TABLE IF NOT EXISTS experiments (
            experiment_id TEXT PRIMARY KEY,
            experiment_name TEXT NOT NULL,
            seed INTEGER NOT NULL,
            config_hash TEXT NOT NULL,
            status TEXT NOT NULL,
            scenario_name TEXT NOT NULL,
            artifacts_path TEXT NOT NULL,
            source_experiment_id TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS configs (
            config_hash TEXT PRIMARY KEY,
            experiment_name TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS episode_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id TEXT NOT NULL,
            episode_index INTEGER NOT NULL,
            reward REAL NOT NULL,
            success INTEGER NOT NULL,
            active_strategy TEXT NOT NULL,
            steps INTEGER NOT NULL,
            compute_cost REAL NOT NULL,
            learning_progress REAL NOT NULL,
            fallback_triggered INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS window_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id TEXT NOT NULL,
            window_index INTEGER NOT NULL,
            start_episode INTEGER NOT NULL,
            end_episode INTEGER NOT NULL,
            reward_mean REAL NOT NULL,
            reward_variance REAL NOT NULL,
            success_rate REAL NOT NULL,
            cumulative_reward REAL NOT NULL,
            switches INTEGER NOT NULL,
            compute_cost_mean REAL NOT NULL,
            recovery_time REAL NOT NULL,
            learning_progress_mean REAL NOT NULL,
            utility_reward_mean REAL,
            utility_reward_variance REAL,
            utility_compute_cost REAL,
            utility_switch_cost REAL
        );
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id TEXT NOT NULL,
            evaluation_index INTEGER NOT NULL,
            action TEXT NOT NULL,
            current_strategy TEXT NOT NULL,
            candidate_strategy TEXT,
            reason TEXT NOT NULL,
            utility_current REAL,
            utility_candidate REAL,
            lcb_current REAL,
            lcb_candidate REAL,
            switched INTEGER NOT NULL,
            reason_code TEXT,
            decision_margin REAL,
            decision_threshold REAL,
            is_fallback INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id TEXT NOT NULL,
            kind TEXT NOT NULL,
            path TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id TEXT NOT NULL,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            details_json TEXT,
            created_at TEXT NOT NULL
        );
        """
        with self._connect() as connection:
            connection.executescript(schema)
            self._ensure_column(connection, "experiments", "source_experiment_id", "TEXT")
            connection.commit()

    def _ensure_column(self, connection: sqlite3.Connection, table_name: str, column_name: str, column_type_sql: str) -> None:
        columns = {
            row["name"]
            for row in connection.execute(f"PRAGMA table_info({table_name})").fetchall()
        }
        if column_name not in columns:
            connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type_sql}")

    def save_experiment(self, experiment: Experiment, *, artifacts_path: str) -> None:
        payload = (
            experiment.experiment_id,
            experiment.config.experiment_name,
            experiment.seed,
            experiment.config_hash,
            normalize_experiment_status(experiment.status).value,
            experiment.config.scenario.name.value,
            artifacts_path,
            experiment.source_experiment_id,
            experiment.created_at.isoformat(),
        )
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO experiments (
                    experiment_id, experiment_name, seed, config_hash, status, scenario_name, artifacts_path, source_experiment_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                payload,
            )
            connection.commit()

    def get_experiment(self, experiment_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM experiments WHERE experiment_id = ?",
                (experiment_id,),
            ).fetchone()
        return None if row is None else dict(row)

    def list_experiments(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM experiments ORDER BY created_at DESC, experiment_id DESC"
            ).fetchall()
        return [dict(row) for row in rows]

    def update_experiment_status(self, experiment_id: str, status: str) -> None:
        with self._connect() as connection:
            current = connection.execute(
                "SELECT status FROM experiments WHERE experiment_id = ?",
                (experiment_id,),
            ).fetchone()
            if current is None:
                raise FileNotFoundError(f"experiment not found: {experiment_id}")
            next_status = ensure_experiment_status_transition(str(current["status"]), status).value
            connection.execute(
                "UPDATE experiments SET status = ? WHERE experiment_id = ?",
                (next_status, experiment_id),
            )
            connection.commit()

    def save_config(self, config: Config) -> None:
        payload_json = json.dumps(_json_ready(config.to_dict()), ensure_ascii=True, sort_keys=True)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO configs (config_hash, experiment_name, payload_json, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    config.config_hash,
                    config.experiment_name,
                    payload_json,
                    datetime.now().astimezone().isoformat(),
                ),
            )
            connection.commit()

    def get_config(self, config_hash: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM configs WHERE config_hash = ?",
                (config_hash,),
            ).fetchone()
        return None if row is None else dict(row)

    def save_episode_metrics(self, experiment_id: str, metrics: list[EpisodeMetric] | tuple[EpisodeMetric, ...]) -> None:
        rows = [
            (
                experiment_id,
                metric.episode_index,
                metric.reward,
                int(metric.success),
                metric.active_strategy,
                metric.steps,
                metric.compute_cost,
                metric.learning_progress,
                int(metric.fallback_triggered),
            )
            for metric in metrics
        ]
        with self._connect() as connection:
            connection.executemany(
                """
                INSERT INTO episode_metrics (
                    experiment_id, episode_index, reward, success, active_strategy, steps, compute_cost, learning_progress, fallback_triggered
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            connection.commit()

    def list_episode_metrics(self, experiment_id: str) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM episode_metrics WHERE experiment_id = ? ORDER BY episode_index",
                (experiment_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def save_window_metrics(self, experiment_id: str, metrics: list[WindowMetric] | tuple[WindowMetric, ...]) -> None:
        rows = [
            (
                experiment_id,
                metric.window_index,
                metric.start_episode,
                metric.end_episode,
                metric.reward_mean,
                metric.reward_variance,
                metric.success_rate,
                metric.cumulative_reward,
                metric.switches,
                metric.compute_cost_mean,
                metric.recovery_time,
                metric.learning_progress_mean,
                metric.utility_reward_mean,
                metric.utility_reward_variance,
                metric.utility_compute_cost,
                metric.utility_switch_cost,
            )
            for metric in metrics
        ]
        with self._connect() as connection:
            connection.executemany(
                """
                INSERT INTO window_metrics (
                    experiment_id, window_index, start_episode, end_episode, reward_mean, reward_variance, success_rate,
                    cumulative_reward, switches, compute_cost_mean, recovery_time, learning_progress_mean,
                    utility_reward_mean, utility_reward_variance, utility_compute_cost, utility_switch_cost
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            connection.commit()

    def list_window_metrics(self, experiment_id: str) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM window_metrics WHERE experiment_id = ? ORDER BY window_index",
                (experiment_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def save_decisions(self, experiment_id: str, decisions: list[Decision] | tuple[Decision, ...]) -> None:
        rows = [
            (
                experiment_id,
                decision.evaluation_index,
                decision.action.value,
                decision.current_strategy,
                decision.candidate_strategy,
                decision.reason,
                decision.utility_current,
                decision.utility_candidate,
                decision.lcb_current,
                decision.lcb_candidate,
                int(decision.switched),
                None if decision.reason_code is None else decision.reason_code.value,
                decision.decision_margin,
                decision.decision_threshold,
                int(decision.is_fallback),
            )
            for decision in decisions
        ]
        with self._connect() as connection:
            connection.executemany(
                """
                INSERT INTO decisions (
                    experiment_id, evaluation_index, action, current_strategy, candidate_strategy, reason,
                    utility_current, utility_candidate, lcb_current, lcb_candidate, switched, reason_code,
                    decision_margin, decision_threshold, is_fallback
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            connection.commit()

    def list_decisions(self, experiment_id: str) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM decisions WHERE experiment_id = ? ORDER BY evaluation_index",
                (experiment_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def save_artifacts(self, experiment_id: str, artifacts: list[Artifact] | tuple[Artifact, ...]) -> None:
        rows = [
            (
                experiment_id,
                artifact.kind.value,
                artifact.path,
                artifact.description,
                artifact.created_at.isoformat(),
            )
            for artifact in artifacts
        ]
        with self._connect() as connection:
            connection.executemany(
                "INSERT INTO artifacts (experiment_id, kind, path, description, created_at) VALUES (?, ?, ?, ?, ?)",
                rows,
            )
            connection.commit()

    def list_artifacts(self, experiment_id: str) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM artifacts WHERE experiment_id = ? ORDER BY id",
                (experiment_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def append_event(self, experiment_id: str, *, level: str, message: str, details: dict[str, Any] | None = None) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO events (experiment_id, level, message, details_json, created_at) VALUES (?, ?, ?, ?, ?)",
                (
                    experiment_id,
                    level,
                    message,
                    None if details is None else json.dumps(_json_ready(details), ensure_ascii=True, sort_keys=True),
                    datetime.now().astimezone().isoformat(),
                ),
            )
            connection.commit()

    def list_events(self, experiment_id: str) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM events WHERE experiment_id = ? ORDER BY id",
                (experiment_id,),
            ).fetchall()
        return [dict(row) for row in rows]
