"""Metrics collection and rolling aggregation for phase 3."""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum
from statistics import fmean, pvariance
from typing import Any

from autorl.domain.models import EpisodeMetric, WindowMetric


@dataclass(frozen=True, slots=True)
class MetricsSummary:
    """High-level aggregate metrics for a run or window."""

    reward_mean: float
    reward_variance: float
    cumulative_reward: float
    success_rate: float
    switches: int
    recovery_time: float
    compute_cost_mean: float
    learning_progress_mean: float
    utility_inputs: dict[str, float]


class MetricsCollector:
    """Collect episode metrics and compute summary and rolling windows."""

    def __init__(self) -> None:
        self._episodes: list[EpisodeMetric] = []
        self._current_failure_run = 0
        self._recovery_runs: list[int] = []

    @property
    def episodes(self) -> tuple[EpisodeMetric, ...]:
        return tuple(self._episodes)

    def record_episode(
        self,
        *,
        episode_index: int,
        reward: float,
        success: bool,
        active_strategy: str,
        steps: int,
        compute_cost: float = 0.0,
        learning_progress: float = 0.0,
        fallback_triggered: bool = False,
    ) -> EpisodeMetric:
        episode_metric = EpisodeMetric(
            episode_index=episode_index,
            reward=reward,
            success=success,
            active_strategy=active_strategy,
            steps=steps,
            compute_cost=compute_cost,
            learning_progress=learning_progress,
            fallback_triggered=fallback_triggered,
        )
        self._episodes.append(episode_metric)

        if success:
            if self._current_failure_run > 0:
                self._recovery_runs.append(self._current_failure_run)
                self._current_failure_run = 0
        else:
            self._current_failure_run += 1

        return episode_metric

    def summary(self, *, switch_cost: float = 1.0) -> MetricsSummary:
        return self._build_summary(self._episodes, switch_cost=switch_cost)

    def window_metrics(self, window_size: int, *, switch_cost: float = 1.0, rolling: bool = True) -> list[WindowMetric]:
        if window_size <= 0:
            raise ValueError("window_size must be positive")
        if not self._episodes:
            return []

        windows: list[WindowMetric] = []
        step = 1 if rolling else window_size
        for start in range(0, len(self._episodes) - window_size + 1, step):
            chunk = self._episodes[start : start + window_size]
            summary = self._build_summary(chunk, switch_cost=switch_cost)
            windows.append(
                WindowMetric(
                    window_index=len(windows),
                    start_episode=chunk[0].episode_index,
                    end_episode=chunk[-1].episode_index,
                    reward_mean=summary.reward_mean,
                    reward_variance=summary.reward_variance,
                    success_rate=summary.success_rate,
                    cumulative_reward=summary.cumulative_reward,
                    switches=summary.switches,
                    compute_cost_mean=summary.compute_cost_mean,
                    recovery_time=summary.recovery_time,
                    learning_progress_mean=summary.learning_progress_mean,
                    utility_reward_mean=summary.utility_inputs["reward_mean"],
                    utility_reward_variance=summary.utility_inputs["reward_variance"],
                    utility_compute_cost=summary.utility_inputs["compute_cost"],
                    utility_switch_cost=summary.utility_inputs["switch_cost"],
                )
            )
        return windows

    def _build_summary(self, episodes: list[EpisodeMetric], *, switch_cost: float) -> MetricsSummary:
        if not episodes:
            return MetricsSummary(
                reward_mean=0.0,
                reward_variance=0.0,
                cumulative_reward=0.0,
                success_rate=0.0,
                switches=0,
                recovery_time=0.0,
                compute_cost_mean=0.0,
                learning_progress_mean=0.0,
                utility_inputs={
                    "reward_mean": 0.0,
                    "reward_variance": 0.0,
                    "compute_cost": 0.0,
                    "switch_cost": 0.0,
                    "switches": 0.0,
                },
            )

        rewards = [episode.reward for episode in episodes]
        successes = [1.0 if episode.success else 0.0 for episode in episodes]
        compute_costs = [episode.compute_cost for episode in episodes]
        learning_progress = [episode.learning_progress for episode in episodes]
        switches = self._count_switches(episodes)
        recovery_time = self._window_recovery_time(episodes)

        reward_mean = fmean(rewards)
        reward_variance = pvariance(rewards) if len(rewards) > 1 else 0.0
        cumulative_reward = fsum(rewards)
        success_rate = fmean(successes)
        compute_cost_mean = fmean(compute_costs)
        learning_progress_mean = fmean(learning_progress)
        utility_inputs = {
            "reward_mean": reward_mean,
            "reward_variance": reward_variance,
            "compute_cost": compute_cost_mean,
            "switch_cost": switches * switch_cost,
            "switches": float(switches),
        }
        return MetricsSummary(
            reward_mean=reward_mean,
            reward_variance=reward_variance,
            cumulative_reward=cumulative_reward,
            success_rate=success_rate,
            switches=switches,
            recovery_time=recovery_time,
            compute_cost_mean=compute_cost_mean,
            learning_progress_mean=learning_progress_mean,
            utility_inputs=utility_inputs,
        )

    def _count_switches(self, episodes: list[EpisodeMetric]) -> int:
        switches = 0
        previous_strategy: str | None = None
        for episode in episodes:
            if previous_strategy is not None and episode.active_strategy != previous_strategy:
                switches += 1
            previous_strategy = episode.active_strategy
        return switches

    def _window_recovery_time(self, episodes: list[EpisodeMetric]) -> float:
        recovery_runs: list[int] = []
        current_failure_run = 0
        for episode in episodes:
            if episode.success:
                if current_failure_run > 0:
                    recovery_runs.append(current_failure_run)
                    current_failure_run = 0
            else:
                current_failure_run += 1
        return fmean(recovery_runs) if recovery_runs else 0.0
