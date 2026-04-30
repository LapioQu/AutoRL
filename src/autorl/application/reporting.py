"""Report and plot generation for phase 7 experiment outputs."""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
import struct
from typing import Iterable, Mapping
import zlib

import yaml

from autorl.domain import ArtifactKind, Config, Decision, EpisodeMetric, Experiment, WindowMetric
from autorl.infrastructure import ExperimentArtifactStore, SQLiteRepository


Color = tuple[int, int, int]


@dataclass(frozen=True, slots=True)
class GeneratedReportArtifacts:
    """Paths to generated report and plot artifacts."""

    report_path: str
    html_report_path: str
    reward_curve_path: str
    strategy_timeline_path: str
    utility_lcb_path: str


class PngCanvas:
    """Small dependency-free RGB canvas used for simple PNG plots."""

    def __init__(self, width: int, height: int, *, background: Color = (255, 255, 255)) -> None:
        self.width = width
        self.height = height
        self._pixels = bytearray(width * height * 3)
        self.fill_rect(0, 0, width - 1, height - 1, background)

    def fill_rect(self, x0: int, y0: int, x1: int, y1: int, color: Color) -> None:
        left = max(0, min(x0, x1))
        right = min(self.width - 1, max(x0, x1))
        top = max(0, min(y0, y1))
        bottom = min(self.height - 1, max(y0, y1))
        if right < left or bottom < top:
            return
        red, green, blue = color
        for y_coord in range(top, bottom + 1):
            row_offset = y_coord * self.width * 3
            for x_coord in range(left, right + 1):
                offset = row_offset + (x_coord * 3)
                self._pixels[offset] = red
                self._pixels[offset + 1] = green
                self._pixels[offset + 2] = blue

    def draw_line(self, x0: int, y0: int, x1: int, y1: int, color: Color, *, thickness: int = 1) -> None:
        delta_x = x1 - x0
        delta_y = y1 - y0
        steps = max(abs(delta_x), abs(delta_y), 1)
        for step in range(steps + 1):
            x_coord = round(x0 + (delta_x * step / steps))
            y_coord = round(y0 + (delta_y * step / steps))
            radius = max(0, thickness - 1)
            self.fill_rect(x_coord - radius, y_coord - radius, x_coord + radius, y_coord + radius, color)

    def to_png_bytes(self) -> bytes:
        scanlines = bytearray()
        row_width = self.width * 3
        for row_index in range(self.height):
            scanlines.append(0)
            start = row_index * row_width
            scanlines.extend(self._pixels[start : start + row_width])

        compressed = zlib.compress(bytes(scanlines), level=9)
        return b"".join(
            [
                b"\x89PNG\r\n\x1a\n",
                self._png_chunk(b"IHDR", struct.pack(">IIBBBBB", self.width, self.height, 8, 2, 0, 0, 0)),
                self._png_chunk(b"IDAT", compressed),
                self._png_chunk(b"IEND", b""),
            ]
        )

    def _png_chunk(self, chunk_type: bytes, data: bytes) -> bytes:
        checksum = zlib.crc32(chunk_type)
        checksum = zlib.crc32(data, checksum)
        return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", checksum & 0xFFFFFFFF)


class ExperimentReportBuilder:
    """Generate markdown report and plot artifacts from experiment results."""

    def __init__(self, repository: SQLiteRepository, store: ExperimentArtifactStore) -> None:
        self._repository = repository
        self._store = store
        self._palette = [
            (31, 119, 180),
            (214, 39, 40),
            (44, 160, 44),
            (255, 127, 14),
            (148, 103, 189),
            (140, 86, 75),
        ]

    def generate_for_run(
        self,
        *,
        experiment: Experiment,
        episode_metrics: Iterable[EpisodeMetric],
        window_metrics: Iterable[WindowMetric],
        decisions: Iterable[Decision],
    ) -> GeneratedReportArtifacts:
        episode_list = list(episode_metrics)
        window_list = list(window_metrics)
        decision_list = list(decisions)
        markdown = self._build_markdown(
            experiment_id=experiment.experiment_id,
            experiment_name=experiment.config.experiment_name,
            config=experiment.config,
            config_hash=experiment.config_hash,
            status="completed",
            artifacts_path=str(Path(experiment.config.artifacts_root) / "experiments" / experiment.experiment_id),
            episode_metrics=episode_list,
            window_metrics=window_list,
            decisions=decision_list,
        )
        report_path = self._store.write_text_artifact(
            experiment.experiment_id,
            "report.md",
            markdown,
            kind=ArtifactKind.REPORT,
            description="Markdown experiment report",
        )
        html_report_path = self._store.write_text_artifact(
            experiment.experiment_id,
            "report.html",
            self._build_html(
                experiment_id=experiment.experiment_id,
                experiment_name=experiment.config.experiment_name,
                config=experiment.config,
                config_hash=experiment.config_hash,
                status="completed",
                artifacts_path=str(Path(experiment.config.artifacts_root) / "experiments" / experiment.experiment_id),
                episode_metrics=episode_list,
                window_metrics=window_list,
                decisions=decision_list,
            ),
            kind=ArtifactKind.REPORT,
            description="HTML experiment report",
        )
        reward_curve_path = self._store.write_bytes_artifact(
            experiment.experiment_id,
            "reward_curve.png",
            self._build_reward_curve(episode_list),
            kind=ArtifactKind.PLOT,
            description="Reward curve plot",
        )
        timeline_path = self._store.write_bytes_artifact(
            experiment.experiment_id,
            "strategy_timeline.png",
            self._build_strategy_timeline(episode_list),
            kind=ArtifactKind.PLOT,
            description="Strategy timeline plot",
        )
        utility_lcb_path = self._store.write_bytes_artifact(
            experiment.experiment_id,
            "utility_lcb.png",
            self._build_utility_lcb_plot(decision_list),
            kind=ArtifactKind.PLOT,
            description="Utility and LCB comparison plot",
        )
        return GeneratedReportArtifacts(
            report_path=str(report_path),
            html_report_path=str(html_report_path),
            reward_curve_path=str(reward_curve_path),
            strategy_timeline_path=str(timeline_path),
            utility_lcb_path=str(utility_lcb_path),
        )

    def generate_for_experiment(self, experiment_id: str) -> GeneratedReportArtifacts:
        experiment_row = self._repository.get_experiment(experiment_id)
        if experiment_row is None:
            raise FileNotFoundError(f"experiment not found: {experiment_id}")
        config_row = self._repository.get_config(experiment_row["config_hash"])
        if config_row is None:
            raise FileNotFoundError(f"config payload not found for experiment: {experiment_id}")

        config = Config.from_dict(json.loads(config_row["payload_json"]))
        episode_metrics = [self._episode_metric_from_row(row) for row in self._repository.list_episode_metrics(experiment_id)]
        window_metrics = [self._window_metric_from_row(row) for row in self._repository.list_window_metrics(experiment_id)]
        decisions = [self._decision_from_row(row) for row in self._repository.list_decisions(experiment_id)]
        experiment = Experiment(
            experiment_id=experiment_row["experiment_id"],
            config=config,
            seed=int(experiment_row["seed"]),
            config_hash=experiment_row["config_hash"],
            status=experiment_row["status"],
        )
        return self.generate_for_run(
            experiment=experiment,
            episode_metrics=episode_metrics,
            window_metrics=window_metrics,
            decisions=decisions,
        )

    def _build_markdown(
        self,
        *,
        experiment_id: str,
        experiment_name: str,
        config: Config,
        config_hash: str,
        status: str,
        artifacts_path: str,
        episode_metrics: list[EpisodeMetric],
        window_metrics: list[WindowMetric],
        decisions: list[Decision],
    ) -> str:
        average_reward = sum(metric.reward for metric in episode_metrics) / max(1, len(episode_metrics))
        success_rate = sum(1 for metric in episode_metrics if metric.success) / max(1, len(episode_metrics))
        switch_count = sum(1 for decision in decisions if decision.switched)
        fallback_count = sum(1 for decision in decisions if decision.is_fallback)
        final_strategy = episode_metrics[-1].active_strategy if episode_metrics else ""
        cumulative_reward = sum(metric.reward for metric in episode_metrics)
        mean_window_variance = (
            sum(metric.reward_variance for metric in window_metrics) / len(window_metrics)
            if window_metrics
            else 0.0
        )
        decision_lines = [
            "| Evaluation | Action | Current | Candidate | Margin | Threshold | Reason |",
            "| --- | --- | --- | --- | ---: | ---: | --- |",
        ]
        for decision in decisions[:20]:
            decision_lines.append(
                "| "
                + " | ".join(
                    [
                        str(decision.evaluation_index),
                        decision.action.value,
                        decision.current_strategy,
                        decision.candidate_strategy or "-",
                        self._format_number(decision.decision_margin),
                        self._format_number(decision.decision_threshold),
                        decision.reason_code.value if decision.reason_code is not None else "unknown",
                    ]
                )
                + " |"
            )
        if len(decisions) > 20:
            decision_lines.append("")
            decision_lines.append(f"_Showing first 20 of {len(decisions)} decisions._")

        config_yaml = yaml.safe_dump(config.to_dict(), sort_keys=False, allow_unicode=False)
        lines = [
            "# AutoRL Experiment Report",
            "",
            "## Experiment Summary",
            "",
            "| Field | Value |",
            "| --- | --- |",
            f"| Experiment ID | {experiment_id} |",
            f"| Experiment Name | {experiment_name} |",
            f"| Status | {status} |",
            f"| Scenario | {config.scenario.name.value} |",
            f"| Seed | {config.seed} |",
            f"| Config Hash | {config_hash} |",
            f"| Artifacts Path | `{artifacts_path}` |",
            "",
            "## Results Summary",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Episodes | {len(episode_metrics)} |",
            f"| Decisions | {len(decisions)} |",
            f"| Switches | {switch_count} |",
            f"| Fallback Decisions | {fallback_count} |",
            f"| Average Reward | {average_reward:.6f} |",
            f"| Success Rate | {success_rate:.6f} |",
            f"| Cumulative Reward | {cumulative_reward:.6f} |",
            f"| Mean Window Variance | {mean_window_variance:.6f} |",
            f"| Final Strategy | {final_strategy} |",
            "",
            "## Plot Artifacts",
            "",
            "- `reward_curve.png`",
            "- `strategy_timeline.png`",
            "- `utility_lcb.png`",
            "",
            "## Stay/Switch Summary",
            "",
            *decision_lines,
            "",
            "## Config Snapshot",
            "",
            "```yaml",
            config_yaml.strip(),
            "```",
        ]
        return "\n".join(lines) + "\n"

    def _build_reward_curve(self, metrics: list[EpisodeMetric]) -> bytes:
        series = [metric.reward for metric in metrics]
        return self._line_plot(
            series_map={"reward": (series, (31, 119, 180))},
            vertical_switches=[],
            width=960,
            height=480,
        )

    def _build_strategy_timeline(self, metrics: list[EpisodeMetric]) -> bytes:
        canvas = PngCanvas(960, 220, background=(255, 255, 255))
        canvas.fill_rect(0, 0, 959, 219, (250, 250, 250))
        canvas.fill_rect(30, 40, 929, 180, (240, 240, 240))
        strategy_names = sorted({metric.active_strategy for metric in metrics})
        color_map = {name: self._palette[index % len(self._palette)] for index, name in enumerate(strategy_names)}
        count = max(1, len(metrics))
        for index, metric in enumerate(metrics):
            left = 30 + math.floor((index / count) * 900)
            right = 30 + math.floor(((index + 1) / count) * 900) - 1
            if right < left:
                right = left
            canvas.fill_rect(left, 70, right, 150, color_map[metric.active_strategy])
        canvas.draw_line(30, 70, 929, 70, (90, 90, 90))
        canvas.draw_line(30, 150, 929, 150, (90, 90, 90))
        canvas.draw_line(30, 70, 30, 150, (90, 90, 90))
        canvas.draw_line(929, 70, 929, 150, (90, 90, 90))
        for legend_index, strategy_name in enumerate(strategy_names):
            top = 10 + (legend_index * 18)
            color = color_map[strategy_name]
            canvas.fill_rect(30, top, 42, top + 12, color)
            canvas.draw_line(30, top, 42, top, (70, 70, 70))
            canvas.draw_line(30, top + 12, 42, top + 12, (70, 70, 70))
            canvas.draw_line(30, top, 30, top + 12, (70, 70, 70))
            canvas.draw_line(42, top, 42, top + 12, (70, 70, 70))
        return canvas.to_png_bytes()

    def _build_utility_lcb_plot(self, decisions: list[Decision]) -> bytes:
        current_lcb = [decision.lcb_current if decision.lcb_current is not None else 0.0 for decision in decisions]
        candidate_lcb = [decision.lcb_candidate if decision.lcb_candidate is not None else 0.0 for decision in decisions]
        switch_positions = [decision.evaluation_index for decision in decisions if decision.switched]
        return self._line_plot(
            series_map={
                "current_lcb": (current_lcb, (214, 39, 40)),
                "candidate_lcb": (candidate_lcb, (44, 160, 44)),
            },
            vertical_switches=switch_positions,
            width=960,
            height=480,
        )

    def _line_plot(
        self,
        *,
        series_map: Mapping[str, tuple[list[float], Color]],
        vertical_switches: list[int],
        width: int,
        height: int,
    ) -> bytes:
        canvas = PngCanvas(width, height, background=(255, 255, 255))
        left = 64
        right = width - 32
        top = 32
        bottom = height - 48
        canvas.fill_rect(left, top, right, bottom, (248, 248, 248))

        max_points = max((len(values) for values, _ in series_map.values()), default=0)
        flattened = [value for values, _ in series_map.values() for value in values]
        if not flattened:
            flattened = [0.0]
        minimum = min(flattened)
        maximum = max(flattened)
        if math.isclose(minimum, maximum):
            minimum -= 1.0
            maximum += 1.0
        padding = (maximum - minimum) * 0.1
        minimum -= padding
        maximum += padding

        for grid_index in range(6):
            y_coord = top + round((bottom - top) * grid_index / 5)
            canvas.draw_line(left, y_coord, right, y_coord, (220, 220, 220))

        if max_points > 1:
            for switch_index in vertical_switches:
                x_coord = left + round((right - left) * switch_index / max(1, max_points - 1))
                canvas.draw_line(x_coord, top, x_coord, bottom, (200, 210, 255))

        for series_index, (_, (values, color)) in enumerate(series_map.items()):
            if not values:
                continue
            previous_point: tuple[int, int] | None = None
            for point_index, value in enumerate(values):
                x_coord = left if len(values) == 1 else left + round((right - left) * point_index / max(1, len(values) - 1))
                normalized = (value - minimum) / (maximum - minimum)
                y_coord = bottom - round((bottom - top) * normalized)
                canvas.fill_rect(x_coord - 2, y_coord - 2, x_coord + 2, y_coord + 2, color)
                if previous_point is not None:
                    canvas.draw_line(previous_point[0], previous_point[1], x_coord, y_coord, color, thickness=2)
                previous_point = (x_coord, y_coord)
            legend_top = 10 + (series_index * 18)
            canvas.fill_rect(left, legend_top, left + 14, legend_top + 10, color)

        canvas.draw_line(left, top, left, bottom, (90, 90, 90))
        canvas.draw_line(left, bottom, right, bottom, (90, 90, 90))
        return canvas.to_png_bytes()

    def _episode_metric_from_row(self, row: Mapping[str, object]) -> EpisodeMetric:
        return EpisodeMetric(
            episode_index=int(row["episode_index"]),
            reward=float(row["reward"]),
            success=bool(row["success"]),
            active_strategy=str(row["active_strategy"]),
            steps=int(row["steps"]),
            compute_cost=float(row["compute_cost"]),
            learning_progress=float(row["learning_progress"]),
            fallback_triggered=bool(row["fallback_triggered"]),
        )

    def _window_metric_from_row(self, row: Mapping[str, object]) -> WindowMetric:
        return WindowMetric(
            window_index=int(row["window_index"]),
            start_episode=int(row["start_episode"]),
            end_episode=int(row["end_episode"]),
            reward_mean=float(row["reward_mean"]),
            reward_variance=float(row["reward_variance"]),
            success_rate=float(row["success_rate"]),
            cumulative_reward=float(row["cumulative_reward"]),
            switches=int(row["switches"]),
            compute_cost_mean=float(row["compute_cost_mean"]),
            recovery_time=float(row["recovery_time"]),
            learning_progress_mean=float(row["learning_progress_mean"]),
            utility_reward_mean=self._optional_float(row["utility_reward_mean"]),
            utility_reward_variance=self._optional_float(row["utility_reward_variance"]),
            utility_compute_cost=self._optional_float(row["utility_compute_cost"]),
            utility_switch_cost=self._optional_float(row["utility_switch_cost"]),
        )

    def _decision_from_row(self, row: Mapping[str, object]) -> Decision:
        from autorl.domain import DecisionAction, DecisionReason

        reason_code = row["reason_code"]
        return Decision(
            evaluation_index=int(row["evaluation_index"]),
            action=DecisionAction(str(row["action"])),
            current_strategy=str(row["current_strategy"]),
            candidate_strategy=None if row["candidate_strategy"] is None else str(row["candidate_strategy"]),
            reason=str(row["reason"]),
            utility_current=self._optional_float(row["utility_current"]),
            utility_candidate=self._optional_float(row["utility_candidate"]),
            lcb_current=self._optional_float(row["lcb_current"]),
            lcb_candidate=self._optional_float(row["lcb_candidate"]),
            switched=bool(row["switched"]),
            reason_code=None if reason_code is None else DecisionReason(str(reason_code)),
            decision_margin=self._optional_float(row["decision_margin"]),
            decision_threshold=self._optional_float(row["decision_threshold"]),
            is_fallback=bool(row["is_fallback"]),
        )

    def _optional_float(self, value: object) -> float | None:
        return None if value is None else float(value)

    def _format_number(self, value: float | None) -> str:
        return "-" if value is None else f"{value:.6f}"

    def _build_html(
        self,
        *,
        experiment_id: str,
        experiment_name: str,
        config: Config,
        config_hash: str,
        status: str,
        artifacts_path: str,
        episode_metrics: list[EpisodeMetric],
        window_metrics: list[WindowMetric],
        decisions: list[Decision],
    ) -> str:
        average_reward = sum(metric.reward for metric in episode_metrics) / max(1, len(episode_metrics))
        success_rate = sum(1 for metric in episode_metrics if metric.success) / max(1, len(episode_metrics))
        switch_count = sum(1 for decision in decisions if decision.switched)
        fallback_count = sum(1 for decision in decisions if decision.is_fallback)
        final_strategy = episode_metrics[-1].active_strategy if episode_metrics else ""
        cumulative_reward = sum(metric.reward for metric in episode_metrics)
        mean_window_variance = (
            sum(metric.reward_variance for metric in window_metrics) / len(window_metrics)
            if window_metrics
            else 0.0
        )
        config_yaml = yaml.safe_dump(config.to_dict(), sort_keys=False, allow_unicode=False).strip()

        def esc(value: object) -> str:
            return (
                str(value)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )

        decision_rows = "".join(
            [
                "<tr>"
                f"<td>{decision.evaluation_index}</td>"
                f"<td>{esc(decision.action.value)}</td>"
                f"<td>{esc(decision.current_strategy)}</td>"
                f"<td>{esc(decision.candidate_strategy or '-')}</td>"
                f"<td>{esc(self._format_number(decision.decision_margin))}</td>"
                f"<td>{esc(self._format_number(decision.decision_threshold))}</td>"
                f"<td>{esc(decision.reason_code.value if decision.reason_code is not None else 'unknown')}</td>"
                "</tr>"
                for decision in decisions[:20]
            ]
        )
        if not decision_rows:
            decision_rows = '<tr><td colspan="7">No decisions recorded.</td></tr>'

        return "\n".join(
            [
                "<!doctype html>",
                '<html lang="uk"><head><meta charset="utf-8"><title>AutoRL Experiment Report</title>',
                "<style>",
                "body{font-family:Segoe UI,Tahoma,sans-serif;margin:24px;color:#0f172a;background:#fff;}",
                "h1,h2{margin:0 0 12px;} h2{margin-top:28px;}",
                "table{border-collapse:collapse;width:100%;margin:12px 0;}",
                "th,td{border:1px solid #dbe3ee;padding:8px 10px;text-align:left;vertical-align:top;}",
                "th{background:#f8fafc;} pre{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:12px;overflow:auto;}",
                "ul{margin-top:8px;} .muted{color:#64748b;}",
                "</style></head><body>",
                "<h1>AutoRL Experiment Report</h1>",
                "<h2>Experiment Summary</h2>",
                "<table><tbody>",
                f"<tr><th>Experiment ID</th><td>{esc(experiment_id)}</td></tr>",
                f"<tr><th>Experiment Name</th><td>{esc(experiment_name)}</td></tr>",
                f"<tr><th>Status</th><td>{esc(status)}</td></tr>",
                f"<tr><th>Scenario</th><td>{esc(config.scenario.name.value)}</td></tr>",
                f"<tr><th>Seed</th><td>{config.seed}</td></tr>",
                f"<tr><th>Config Hash</th><td>{esc(config_hash)}</td></tr>",
                f"<tr><th>Artifacts Path</th><td><code>{esc(artifacts_path)}</code></td></tr>",
                "</tbody></table>",
                "<h2>Results Summary</h2>",
                "<table><tbody>",
                f"<tr><th>Episodes</th><td>{len(episode_metrics)}</td></tr>",
                f"<tr><th>Decisions</th><td>{len(decisions)}</td></tr>",
                f"<tr><th>Switches</th><td>{switch_count}</td></tr>",
                f"<tr><th>Fallback Decisions</th><td>{fallback_count}</td></tr>",
                f"<tr><th>Average Reward</th><td>{average_reward:.6f}</td></tr>",
                f"<tr><th>Success Rate</th><td>{success_rate:.6f}</td></tr>",
                f"<tr><th>Cumulative Reward</th><td>{cumulative_reward:.6f}</td></tr>",
                f"<tr><th>Mean Window Variance</th><td>{mean_window_variance:.6f}</td></tr>",
                f"<tr><th>Final Strategy</th><td>{esc(final_strategy)}</td></tr>",
                "</tbody></table>",
                "<h2>Plot Artifacts</h2>",
                "<ul><li><code>reward_curve.png</code></li><li><code>strategy_timeline.png</code></li><li><code>utility_lcb.png</code></li></ul>",
                "<h2>Stay/Switch Summary</h2>",
                "<table><thead><tr><th>Evaluation</th><th>Action</th><th>Current</th><th>Candidate</th><th>Margin</th><th>Threshold</th><th>Reason</th></tr></thead><tbody>",
                decision_rows,
                "</tbody></table>",
                f'<p class="muted">Showing first {min(len(decisions), 20)} decision rows.</p>' if len(decisions) > 20 else "",
                "<h2>Config Snapshot</h2>",
                f"<pre>{esc(config_yaml)}</pre>",
                "</body></html>",
            ]
        )
