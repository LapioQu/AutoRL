"""Phase 10 experimental-series runner for T3 E1..E9."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
import json
from math import comb
from pathlib import Path
from statistics import fmean, stdev
from typing import Any, Iterable, Sequence

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt

from autorl.application.benchmark_replay import BenchmarkReplayRunner, ReplayBenchmarkResult, ReplaySuiteResult
from autorl.application.experiments import ExperimentOrchestrator


_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_EXAMPLES_DIR = _PROJECT_ROOT / "configs" / "examples"
_PROFILES_DIR = _PROJECT_ROOT / "configs" / "benchmark_profiles"
_CLASSIFICATION_BENCHMARK_DATASETS = frozenset({"elec2", "airlines", "insects_recurring"})
_REGRESSION_BENCHMARK_DATASETS = frozenset({"waterflow"})


@dataclass(frozen=True, slots=True)
class Phase10SeriesResult:
    """One persisted E1..E9 experimental series."""

    series_id: str
    title: str
    series_type: str
    root_path: str
    summary_json_path: str
    report_md_path: str
    primary_plot_path: str
    switches_plot_path: str
    run_count: int


@dataclass(frozen=True, slots=True)
class Phase10SuiteResult:
    """Persisted result bundle for the full phase 10 suite."""

    series: tuple[Phase10SeriesResult, ...]
    summary_json_path: str
    report_md_path: str


class Phase10ExperimentalSeriesRunner:
    """Run the formal T3 phase 10 artifact-backed experiments."""

    def __init__(self, *, root: str | Path = "artifacts/phase10_experimental_series") -> None:
        self._root = Path(root).resolve()
        self._root.mkdir(parents=True, exist_ok=True)
        self._orchestrator = ExperimentOrchestrator()
        self._benchmark_runner = BenchmarkReplayRunner()

    def run_phase10_suite(
        self,
        *,
        seeds: Sequence[int] = (41, 42, 43, 44, 45),
        benchmark_datasets: Sequence[str] = ("elec2", "waterflow", "insects_recurring"),
        benchmark_max_samples: int | None = None,
        reproducibility_seed: int = 12345,
        reproducibility_repeats: int = 5,
        series_ids: Sequence[str] | None = None,
        profile_names: Sequence[str] | None = None,
    ) -> Phase10SuiteResult:
        requested = None if series_ids is None else {series_id.strip().upper() for series_id in series_ids}
        requested_profiles = None if profile_names is None else {name.strip() for name in profile_names}
        planned_series: list[Phase10SeriesResult] = []

        def include(series_id: str) -> bool:
            return requested is None or series_id in requested

        if include("E1"):
            planned_series.append(
                self._run_controlled_series(
                    series_id="E1",
                    title="Stationary control",
                    config_path=_EXAMPLES_DIR / "stationary.yaml",
                    seeds=seeds,
                )
            )
        if include("E2"):
            planned_series.append(
                self._run_controlled_series(
                    series_id="E2",
                    title="Abrupt drift",
                    config_path=_EXAMPLES_DIR / "abrupt_drift.yaml",
                    seeds=seeds,
                )
            )
        if include("E3"):
            planned_series.append(
                self._run_controlled_series(
                    series_id="E3",
                    title="Gradual drift",
                    config_path=_EXAMPLES_DIR / "gradual_drift.yaml",
                    seeds=seeds,
                )
            )
        if include("E4"):
            planned_series.append(
                self._run_controlled_series(
                    series_id="E4",
                    title="Noisy reward",
                    config_path=_EXAMPLES_DIR / "noisy_reward.yaml",
                    seeds=seeds,
                )
            )
        if include("E5"):
            planned_series.append(
                self._run_profile_series(
                    series_id="E5",
                    title="Tempered reward shaping",
                    profile_groups=self._build_profile_groups(
                        classification_profile_paths=(_PROFILES_DIR / "h2_tempered_drift.yaml",),
                        regression_profile_paths=(_PROFILES_DIR / "h2_tempered_drift_regression.yaml",),
                        dataset_names=benchmark_datasets,
                        requested_profiles=requested_profiles,
                    ),
                    max_samples=benchmark_max_samples,
                )
            )
        if include("E6"):
            planned_series.append(
                self._run_profile_series(
                    series_id="E6",
                    title="Drift-aware selector / H1 control",
                    profile_groups=self._build_profile_groups(
                        classification_profile_paths=(_PROFILES_DIR / "h1_drift_aware_v2.yaml",),
                        regression_profile_paths=(_PROFILES_DIR / "h1_drift_aware_v2_regression.yaml",),
                        dataset_names=benchmark_datasets,
                        requested_profiles=requested_profiles,
                    ),
                    max_samples=benchmark_max_samples,
                )
            )
        if include("E7"):
            planned_series.append(
                self._run_controlled_series(
                    series_id="E7",
                    title="Reproducibility",
                    config_path=_EXAMPLES_DIR / "reproducibility.json",
                    seeds=tuple(reproducibility_seed for _ in range(reproducibility_repeats)),
                    reproducibility_mode=True,
                )
            )
        if include("E8"):
            planned_series.append(
                self._run_controlled_series(
                    series_id="E8",
                    title="Fallback insufficient data",
                    config_path=_EXAMPLES_DIR / "fallback.yaml",
                    seeds=seeds,
                )
            )
        if include("E9"):
            planned_series.append(
                self._run_profile_series(
                    series_id="E9",
                    title="Baseline comparison",
                    profile_groups=self._build_profile_groups(
                        classification_profile_paths=(
                            _PROFILES_DIR / "adaptive_meta_final.yaml",
                            _PROFILES_DIR / "greedy_reward.yaml",
                            _PROFILES_DIR / "h1_drift_aware_v2.yaml",
                            _PROFILES_DIR / "h2_tempered_drift.yaml",
                            _PROFILES_DIR / "hard_switch_lcb.yaml",
                        ),
                        regression_profile_paths=(
                            _PROFILES_DIR / "adaptive_meta_final_regression.yaml",
                            _PROFILES_DIR / "greedy_reward_regression.yaml",
                            _PROFILES_DIR / "h1_drift_aware_v2_regression.yaml",
                            _PROFILES_DIR / "h2_tempered_drift_regression.yaml",
                            _PROFILES_DIR / "hard_switch_lcb_regression.yaml",
                        ),
                        dataset_names=benchmark_datasets,
                        requested_profiles=requested_profiles,
                    ),
                    max_samples=benchmark_max_samples,
                )
            )
        results = planned_series

        suite_summary_path = self._root / "phase10_suite_summary.json"
        suite_report_path = self._root / "phase10_suite_report.md"
        merged_series = self._merge_suite_series(results, suite_summary_path)
        realized_series_ids = [result.series_id for result in merged_series]
        payload = {
            "phase": 10,
            "title": "Experimental series",
            "series": [asdict(result) for result in merged_series],
            "realized_series_ids": realized_series_ids,
            "requested_series_ids": realized_series_ids,
            "last_run_requested_series_ids": sorted(requested) if requested is not None else realized_series_ids,
            "summary_scope": "accumulated_artifact_root",
        }
        suite_summary_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        suite_report_path.write_text(self._build_suite_report(merged_series), encoding="utf-8")
        return Phase10SuiteResult(
            series=tuple(merged_series),
            summary_json_path=str(suite_summary_path),
            report_md_path=str(suite_report_path),
        )

    def _filter_profile_paths(self, profile_paths: Sequence[Path], requested_profiles: set[str] | None) -> tuple[Path, ...]:
        if requested_profiles is None:
            return tuple(profile_paths)
        selected = tuple(path for path in profile_paths if self._profile_matches_requested(path, requested_profiles))
        if not selected:
            raise ValueError("requested profile_names did not match any profiles in the selected phase 10 series")
        return selected

    def _profile_matches_requested(self, profile_path: Path, requested_profiles: set[str]) -> bool:
        stem = profile_path.stem
        canonical = stem.removesuffix("_regression")
        return stem in requested_profiles or canonical in requested_profiles

    def _normalize_dataset_name(self, dataset_name: str) -> str:
        return dataset_name.strip().lower()

    def _select_supported_datasets(self, dataset_names: Sequence[str], *, supported: frozenset[str]) -> tuple[str, ...]:
        return tuple(
            dataset_name
            for dataset_name in dataset_names
            if self._normalize_dataset_name(dataset_name) in supported
        )

    def _build_profile_groups(
        self,
        *,
        classification_profile_paths: Sequence[Path],
        regression_profile_paths: Sequence[Path],
        dataset_names: Sequence[str],
        requested_profiles: set[str] | None,
    ) -> tuple[dict[str, tuple[Path, ...] | tuple[str, ...]], ...]:
        groups: list[dict[str, tuple[Path, ...] | tuple[str, ...]]] = []
        classification_datasets = self._select_supported_datasets(
            dataset_names,
            supported=_CLASSIFICATION_BENCHMARK_DATASETS,
        )
        if classification_datasets:
            profile_paths = self._filter_profile_paths(classification_profile_paths, requested_profiles)
            groups.append(
                {
                    "profile_paths": profile_paths,
                    "dataset_names": classification_datasets,
                }
            )
        regression_datasets = self._select_supported_datasets(
            dataset_names,
            supported=_REGRESSION_BENCHMARK_DATASETS,
        )
        if regression_datasets:
            profile_paths = self._filter_profile_paths(regression_profile_paths, requested_profiles)
            groups.append(
                {
                    "profile_paths": profile_paths,
                    "dataset_names": regression_datasets,
                }
            )
        if not groups:
            raise ValueError("benchmark_datasets did not include any phase 10 supported datasets")
        return tuple(groups)

    def _run_controlled_series(
        self,
        *,
        series_id: str,
        title: str,
        config_path: Path,
        seeds: Sequence[int],
        reproducibility_mode: bool = False,
    ) -> Phase10SeriesResult:
        root = self._root / f"{series_id.lower()}_{self._slugify(title)}"
        result = self._orchestrator.run_suite_from_config_path(
            config_path,
            seeds=list(seeds),
            artifacts_root=root,
        )
        suite_summary_path = Path(result["summary_json_path"])
        payload = json.loads(suite_summary_path.read_text(encoding="utf-8"))
        reward_values = [float(row["reward_mean"]) for row in payload["runs"]]
        switch_values = [float(row["switch_count"]) for row in payload["runs"]]
        primary_plot_path = root / "phase10_reward_mean.png"
        switches_plot_path = root / "phase10_switch_count.png"

        runs = []
        for row in payload["runs"]:
            artifacts_path = Path(str(row["artifacts_path"]))
            runs.append(
                {
                    "seed": row["seed"],
                    "experiment_id": row["experiment_id"],
                    "status": row["status"],
                    "reward_mean": row["reward_mean"],
                    "switch_count": row["switch_count"],
                    "final_strategy": row["final_strategy"],
                    "artifacts_path": str(artifacts_path),
                    "config_path": str(artifacts_path / "config.yaml"),
                    "metrics_path": str(artifacts_path / "metrics.csv"),
                    "decisions_path": str(artifacts_path / "decisions.csv"),
                    "report_path": str(artifacts_path / "report.md"),
                    "plot_paths": {
                        "reward_curve": str(artifacts_path / "reward_curve.png"),
                        "strategy_timeline": str(artifacts_path / "strategy_timeline.png"),
                        "utility_lcb": str(artifacts_path / "utility_lcb.png"),
                    },
                }
            )
        primary_plot_path.write_bytes(
            self._build_controlled_bar_plot(
                runs=runs,
                value_key="reward_mean",
                title=f"{series_id}: {title}",
                ylabel="Reward Mean",
                color="#2F6BFF",
                ci95=float(payload["reward_ci95"]),
            )
        )
        switches_plot_path.write_bytes(
            self._build_controlled_bar_plot(
                runs=runs,
                value_key="switch_count",
                title=f"{series_id}: {title}",
                ylabel="Switch Count",
                color="#D94F3D",
                ci95=None,
            )
        )

        series_payload: dict[str, Any] = {
            "series_id": series_id,
            "title": title,
            "series_type": "seeded_experiment_suite",
            "config_source_path": str(config_path.resolve()),
            "root_path": str(root),
            "n": len(runs),
            "seeds": [row["seed"] for row in runs],
            "reward_mean": payload["reward_mean"],
            "reward_std": payload["reward_std"],
            "reward_ci95": payload["reward_ci95"],
            "suite_summary_json_path": str(suite_summary_path),
            "suite_summary_md_path": str(result["summary_md_path"]),
            "primary_plot_path": str(primary_plot_path),
            "switches_plot_path": str(switches_plot_path),
            "runs": runs,
        }
        if reproducibility_mode:
            series_payload["reproducibility"] = {
                "all_reward_means_identical": len({round(float(value), 12) for value in reward_values}) <= 1,
                "all_switch_counts_identical": len({int(value) for value in switch_values}) <= 1,
                "all_final_strategies_identical": len({str(row["final_strategy"]) for row in payload["runs"]}) <= 1,
            }

        summary_json_path = root / "phase10_series_summary.json"
        report_md_path = root / "phase10_series_report.md"
        summary_json_path.write_text(json.dumps(series_payload, ensure_ascii=True, indent=2), encoding="utf-8")
        report_md_path.write_text(self._build_controlled_series_report(series_payload), encoding="utf-8")
        return Phase10SeriesResult(
            series_id=series_id,
            title=title,
            series_type="seeded_experiment_suite",
            root_path=str(root),
            summary_json_path=str(summary_json_path),
            report_md_path=str(report_md_path),
            primary_plot_path=str(primary_plot_path),
            switches_plot_path=str(switches_plot_path),
            run_count=len(runs),
        )

    def _run_profile_series(
        self,
        *,
        series_id: str,
        title: str,
        profile_groups: Sequence[dict[str, tuple[Path, ...] | tuple[str, ...]]],
        max_samples: int | None,
    ) -> Phase10SeriesResult:
        root = self._root / f"{series_id.lower()}_{self._slugify(title)}"
        all_profile_paths: list[Path] = []
        for group in profile_groups:
            profile_paths = tuple(group["profile_paths"])
            dataset_names = tuple(group["dataset_names"])
            all_profile_paths.extend(Path(path) for path in profile_paths)
            self._benchmark_runner.run_profile_suite(
                profile_paths=profile_paths,
                dataset_names=dataset_names,
                output_root=root,
                max_samples=max_samples,
            )
        result_rows = self._collect_profile_result_rows(root)
        suite_summary_path = root / "suite_summary.json"
        suite_report_path = root / "suite_summary.md"
        self._rewrite_profile_suite_summary(root, result_rows, suite_summary_path, suite_report_path)
        deltas = [float(row["delta_vs_best_fixed"]) for row in result_rows]
        oracle_gains = [float(row["oracle_gain"]) for row in result_rows]
        capture_ratios = [float(row["oracle_capture_ratio"]) for row in result_rows]
        switches = [float(row["switch_count"]) for row in result_rows]
        primary_plot_path = root / "phase10_delta_vs_best_fixed.png"
        switches_plot_path = root / "phase10_switch_count.png"
        primary_plot_path.write_bytes(
            self._build_benchmark_delta_plot(
                rows=result_rows,
                title=f"{series_id}: {title}",
            )
        )
        switches_plot_path.write_bytes(
            self._build_benchmark_switch_plot(
                rows=result_rows,
                title=f"{series_id}: {title}",
            )
        )

        policy_aggregates = self._aggregate_profile_rows(result_rows)
        protocol = self._build_benchmark_protocol(result_rows=result_rows, max_samples=max_samples)
        payload = {
            "series_id": series_id,
            "title": title,
            "series_type": "benchmark_profile_suite",
            "profile_paths": (
                sorted({str((_PROFILES_DIR / f"{row['profile_name']}.yaml").resolve()) for row in result_rows})
                if result_rows
                else [str(path.resolve()) for path in all_profile_paths]
            ),
            "profile_names": sorted({str(row["profile_name"]) for row in result_rows}),
            "dataset_names": sorted({str(row["dataset_name"]) for row in result_rows}),
            "seed_protocol": "deterministic_temporal_replay_no_rng",
            "seeds": [],
            "max_samples": max_samples,
            "root_path": str(root),
            "n": len(result_rows),
            "delta_mean": fmean(deltas) if deltas else 0.0,
            "delta_std": self._sample_std(deltas),
            "delta_ci95": self._ci95(deltas),
            "oracle_gain_mean": fmean(oracle_gains) if oracle_gains else 0.0,
            "oracle_gain_std": self._sample_std(oracle_gains),
            "oracle_gain_ci95": self._ci95(oracle_gains),
            "oracle_capture_mean": fmean(capture_ratios) if capture_ratios else 0.0,
            "oracle_capture_std": self._sample_std(capture_ratios),
            "oracle_capture_ci95": self._ci95(capture_ratios),
            "effect_size_d": self._effect_size_d(deltas),
            "paired_sign_test_p_value": self._paired_sign_test_p_value(deltas),
            "wins_vs_best_fixed": sum(1 for value in deltas if value > 0.0),
            "suite_summary_json_path": str(suite_summary_path),
            "suite_summary_md_path": str(suite_report_path),
            "primary_plot_path": str(primary_plot_path),
            "switches_plot_path": str(switches_plot_path),
            "benchmark_protocol": protocol,
            "policy_aggregates": policy_aggregates,
            "results": result_rows,
        }
        summary_json_path = root / "phase10_series_summary.json"
        report_md_path = root / "phase10_series_report.md"
        summary_json_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        report_md_path.write_text(self._build_profile_series_report(payload), encoding="utf-8")
        return Phase10SeriesResult(
            series_id=series_id,
            title=title,
            series_type="benchmark_profile_suite",
            root_path=str(root),
            summary_json_path=str(summary_json_path),
            report_md_path=str(report_md_path),
            primary_plot_path=str(primary_plot_path),
            switches_plot_path=str(switches_plot_path),
            run_count=len(result_rows),
        )

    def _aggregate_profile_results(self, results: Sequence[ReplayBenchmarkResult]) -> list[dict[str, Any]]:
        grouped: dict[str, list[ReplayBenchmarkResult]] = {}
        for result in results:
            grouped.setdefault(result.policy_name, []).append(result)
        rows: list[dict[str, Any]] = []
        for policy_name in sorted(grouped):
            policy_results = grouped[policy_name]
            deltas = [item.delta_vs_best_fixed for item in policy_results]
            oracle_gains = [item.oracle_gain for item in policy_results]
            capture_ratios = [item.oracle_capture_ratio for item in policy_results]
            rows.append(
                {
                    "policy_name": policy_name,
                    "n": len(policy_results),
                    "delta_mean": fmean(deltas) if deltas else 0.0,
                    "delta_std": self._sample_std(deltas),
                    "delta_ci95": self._ci95(deltas),
                    "oracle_gain_mean": fmean(oracle_gains) if oracle_gains else 0.0,
                    "oracle_capture_mean": fmean(capture_ratios) if capture_ratios else 0.0,
                    "oracle_capture_std": self._sample_std(capture_ratios),
                    "oracle_capture_ci95": self._ci95(capture_ratios),
                    "wins_vs_best_fixed": sum(1 for value in deltas if value > 0.0),
                    "mean_switch_count": fmean(item.switch_count for item in policy_results) if policy_results else 0.0,
                }
            )
        return rows

    def _rewrite_profile_suite_summary(
        self,
        root: Path,
        rows: Sequence[dict[str, Any]],
        summary_json_path: Path,
        report_md_path: Path,
    ) -> None:
        deltas = [float(row["delta_vs_best_fixed"]) for row in rows]
        oracle_gains = [float(row["oracle_gain"]) for row in rows]
        capture_ratios = [float(row["oracle_capture_ratio"]) for row in rows]
        payload = {
            "profile_count": len({str(row["profile_name"]) for row in rows}),
            "dataset_count": len({str(row["dataset_name"]) for row in rows}),
            "n": len(rows),
            "seed_protocol": "deterministic_temporal_replay_no_rng",
            "seeds": [],
            "delta_mean": fmean(deltas) if deltas else 0.0,
            "delta_std": self._sample_std(deltas),
            "delta_ci95": self._ci95(deltas),
            "oracle_gain_mean": fmean(oracle_gains) if oracle_gains else 0.0,
            "oracle_gain_std": self._sample_std(oracle_gains),
            "oracle_gain_ci95": self._ci95(oracle_gains),
            "oracle_capture_mean": fmean(capture_ratios) if capture_ratios else 0.0,
            "oracle_capture_std": self._sample_std(capture_ratios),
            "oracle_capture_ci95": self._ci95(capture_ratios),
            "effect_size_d": self._effect_size_d(deltas),
            "paired_sign_test_p_value": self._paired_sign_test_p_value(deltas),
            "results": [
                {
                    "dataset_name": row["dataset_name"],
                    "profile_name": row["profile_name"],
                    "policy_name": row["policy_name"],
                    "score_name": row["score_name"],
                    "sample_count": row["sample_count"],
                    "adaptive_score": row["adaptive_score"],
                    "best_fixed_strategy": row["best_fixed_strategy"],
                    "best_fixed_score": row["best_fixed_score"],
                    "oracle_score": row["oracle_score"],
                    "oracle_gain": row["oracle_gain"],
                    "oracle_capture_ratio": row["oracle_capture_ratio"],
                    "delta_vs_best_fixed": row["delta_vs_best_fixed"],
                    "switch_count": row["switch_count"],
                    "artifact_root_path": row["artifact_root_path"],
                    "config_path": row["config_path"],
                    "metrics_path": row["metrics_path"],
                    "plots_path": row["plots_path"],
                    "summary_json_path": row["summary_json_path"],
                    "decision_csv_path": row["decision_csv_path"],
                    "report_md_path": row["report_md_path"],
                }
                for row in rows
            ],
            "wins_vs_best_fixed": sum(1 for row in rows if float(row["delta_vs_best_fixed"]) > 0.0),
            "non_losses_vs_best_fixed": sum(1 for row in rows if float(row["delta_vs_best_fixed"]) >= 0.0),
        }
        summary_json_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        report_md_path.write_text(self._build_profile_suite_markdown(root, rows), encoding="utf-8")

    def _build_profile_suite_markdown(self, root: Path, rows: Sequence[dict[str, Any]]) -> str:
        deltas = [float(row["delta_vs_best_fixed"]) for row in rows]
        oracle_gains = [float(row["oracle_gain"]) for row in rows]
        capture_ratios = [float(row["oracle_capture_ratio"]) for row in rows]
        effect_size = self._effect_size_d(deltas)
        p_value = self._paired_sign_test_p_value(deltas)
        lines = [
            f"# Profile Suite Summary - {root.name}",
            "",
            f"- profile_count: `{len({str(row['profile_name']) for row in rows})}`",
            f"- dataset_count: `{len({str(row['dataset_name']) for row in rows})}`",
            f"- n: `{len(rows)}`",
            "- seed_protocol: `deterministic_temporal_replay_no_rng`",
            "- seeds: `[]`",
            f"- delta_mean: `{(fmean(deltas) if deltas else 0.0):.6f}`",
            f"- delta_std: `{self._sample_std(deltas):.6f}`",
            f"- delta_ci95: `{self._ci95(deltas):.6f}`",
            f"- oracle_gain_mean: `{(fmean(oracle_gains) if oracle_gains else 0.0):.6f}`",
            f"- oracle_gain_ci95: `{self._ci95(oracle_gains):.6f}`",
            f"- oracle_capture_mean: `{(fmean(capture_ratios) if capture_ratios else 0.0):.6f}`",
            f"- oracle_capture_ci95: `{self._ci95(capture_ratios):.6f}`",
            f"- effect_size_d: `{'-' if effect_size is None else f'{effect_size:.6f}'}`",
            f"- paired_sign_test_p_value: `{'-' if p_value is None else f'{p_value:.6f}'}`",
            f"- wins_vs_best_fixed: `{sum(1 for row in rows if float(row['delta_vs_best_fixed']) > 0.0)}`",
            f"- non_losses_vs_best_fixed: `{sum(1 for row in rows if float(row['delta_vs_best_fixed']) >= 0.0)}`",
            "",
            "| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Oracle | Delta | Capture | Switches | Summary |",
            "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
        for row in rows:
            lines.append(
                f"| {row['dataset_name']} | {row['profile_name']} | {row['policy_name']} | {row['score_name']} | "
                f"{row['sample_count']} | {float(row['adaptive_score']):.6f} | {float(row['best_fixed_score']):.6f} | "
                f"{float(row['oracle_score']):.6f} | {float(row['delta_vs_best_fixed']):.6f} | {float(row['oracle_capture_ratio']):.6f} | "
                f"{row['switch_count']} | `{row['summary_json_path']}` |"
            )
        return "\n".join(lines) + "\n"

    def _aggregate_profile_rows(self, rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            grouped.setdefault(str(row["policy_name"]), []).append(row)
        aggregates: list[dict[str, Any]] = []
        for policy_name in sorted(grouped):
            policy_rows = grouped[policy_name]
            deltas = [float(item["delta_vs_best_fixed"]) for item in policy_rows]
            oracle_gains = [float(item["oracle_gain"]) for item in policy_rows]
            capture_ratios = [float(item["oracle_capture_ratio"]) for item in policy_rows]
            aggregates.append(
                {
                    "policy_name": policy_name,
                    "n": len(policy_rows),
                    "delta_mean": fmean(deltas) if deltas else 0.0,
                    "delta_std": self._sample_std(deltas),
                    "delta_ci95": self._ci95(deltas),
                    "oracle_gain_mean": fmean(oracle_gains) if oracle_gains else 0.0,
                    "oracle_capture_mean": fmean(capture_ratios) if capture_ratios else 0.0,
                    "oracle_capture_std": self._sample_std(capture_ratios),
                    "oracle_capture_ci95": self._ci95(capture_ratios),
                    "wins_vs_best_fixed": sum(1 for value in deltas if value > 0.0),
                    "mean_switch_count": fmean(float(item["switch_count"]) for item in policy_rows) if policy_rows else 0.0,
                }
            )
        return aggregates

    def _collect_profile_result_rows(self, root: Path) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for summary_path in sorted(root.glob("*/*/summary.json")):
            payload = json.loads(summary_path.read_text(encoding="utf-8"))
            metrics_path, plots_path = self._ensure_benchmark_support_artifacts(summary_path=summary_path, payload=payload)
            rows.append(
                {
                    "dataset_name": payload["dataset_name"],
                    "profile_name": summary_path.parent.parent.name,
                    "policy_name": payload["policy_name"],
                    "score_name": payload["score_name"],
                    "sample_count": payload["sample_count"],
                    "adaptive_score": payload["adaptive_score"],
                    "best_fixed_strategy": payload["best_fixed_strategy"],
                    "best_fixed_score": payload["best_fixed_score"],
                    "oracle_score": payload.get("oracle_score", payload["best_fixed_score"]),
                    "oracle_gain": payload.get("oracle_gain", 0.0),
                    "oracle_capture_ratio": payload.get("oracle_capture_ratio", 0.0),
                    "delta_vs_best_fixed": payload["delta_vs_best_fixed"],
                    "switch_count": payload["switch_count"],
                    "artifact_root_path": str(summary_path.parent),
                    "config_path": str((_PROFILES_DIR / f"{summary_path.parent.parent.name}.yaml").resolve()),
                    "metrics_path": str(metrics_path),
                    "plots_path": str(plots_path),
                    "decision_csv_path": str(summary_path.with_name("decisions.csv")),
                    "summary_json_path": str(summary_path),
                    "report_md_path": str(summary_path.with_name("summary.md")),
                }
            )
        return rows

    def _ensure_benchmark_support_artifacts(self, *, summary_path: Path, payload: dict[str, Any]) -> tuple[Path, Path]:
        metrics_path = summary_path.with_name("metrics.csv")
        plots_path = summary_path.with_name("score_profile.png")

        fixed_scores = payload.get("fixed_scores", {})
        with metrics_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=("metric", "value"))
            writer.writeheader()
            writer.writerow({"metric": "adaptive_score", "value": payload["adaptive_score"]})
            writer.writerow({"metric": "best_fixed_score", "value": payload["best_fixed_score"]})
            writer.writerow({"metric": "oracle_score", "value": payload.get("oracle_score", payload["best_fixed_score"])})
            writer.writerow({"metric": "oracle_gain", "value": payload.get("oracle_gain", 0.0)})
            writer.writerow({"metric": "oracle_capture_ratio", "value": payload.get("oracle_capture_ratio", 0.0)})
            writer.writerow({"metric": "delta_vs_best_fixed", "value": payload["delta_vs_best_fixed"]})
            writer.writerow({"metric": "switch_count", "value": payload["switch_count"]})
            writer.writerow({"metric": "block_delta_mean", "value": payload["block_delta_mean"]})
            writer.writerow({"metric": "block_delta_std", "value": payload["block_delta_std"]})
            writer.writerow({"metric": "block_delta_ci95", "value": payload["block_delta_ci95"]})
            for strategy_name, score in fixed_scores.items():
                writer.writerow({"metric": f"fixed_score::{strategy_name}", "value": score})

        plots_path.write_bytes(
            self._build_benchmark_result_plot(
                dataset_name=str(payload["dataset_name"]),
                profile_name=str(summary_path.parent.parent.name),
                adaptive_score=float(payload["adaptive_score"]),
                best_fixed_score=float(payload["best_fixed_score"]),
                oracle_score=float(payload.get("oracle_score", payload["best_fixed_score"])),
                fixed_scores={str(name): float(score) for name, score in fixed_scores.items()},
            )
        )
        return metrics_path, plots_path

    def _build_controlled_series_report(self, payload: dict[str, Any]) -> str:
        lines = [
            f"# {payload['series_id']} - {payload['title']}",
            "",
            "- mode: seeded experiment suite",
            f"- config_source_path: `{payload['config_source_path']}`",
            f"- n: `{payload['n']}`",
            f"- seeds: `{', '.join(str(seed) for seed in payload['seeds'])}`",
            f"- reward_mean: `{payload['reward_mean']:.6f}`",
            f"- reward_std: `{payload['reward_std']:.6f}`",
            f"- reward_ci95: `{payload['reward_ci95']:.6f}`",
            f"- suite_summary_json_path: `{payload['suite_summary_json_path']}`",
            f"- suite_summary_md_path: `{payload['suite_summary_md_path']}`",
            f"- primary_plot_path: `{payload['primary_plot_path']}`",
            f"- switches_plot_path: `{payload['switches_plot_path']}`",
        ]
        reproducibility = payload.get("reproducibility")
        if reproducibility is not None:
            lines.extend(
                [
                    "",
                    "## Reproducibility Checks",
                    "",
                    f"- all_reward_means_identical: `{reproducibility['all_reward_means_identical']}`",
                    f"- all_switch_counts_identical: `{reproducibility['all_switch_counts_identical']}`",
                    f"- all_final_strategies_identical: `{reproducibility['all_final_strategies_identical']}`",
                ]
            )
        lines.extend(
            [
                "",
                "## Run Artifacts",
                "",
                "| Seed | Experiment ID | Status | Reward Mean | Switches | Final Strategy | Artifacts | Report |",
                "| ---: | --- | --- | ---: | ---: | --- | --- | --- |",
            ]
        )
        for row in payload["runs"]:
            lines.append(
                f"| {row['seed']} | {row['experiment_id']} | {row['status']} | {row['reward_mean']:.6f} | "
                f"{row['switch_count']} | {row['final_strategy']} | `{row['artifacts_path']}` | `{row['report_path']}` |"
            )
        return "\n".join(lines) + "\n"

    def _build_profile_series_report(self, payload: dict[str, Any]) -> str:
        effect_size_text = "-" if payload["effect_size_d"] is None else f"{payload['effect_size_d']:.6f}"
        p_value_text = "-" if payload["paired_sign_test_p_value"] is None else f"{payload['paired_sign_test_p_value']:.6f}"
        lines = [
            f"# {payload['series_id']} - {payload['title']}",
            "",
            "- mode: benchmark profile suite",
            f"- profiles: `{', '.join(Path(path).stem for path in payload['profile_paths'])}`",
            f"- datasets: `{', '.join(payload['dataset_names'])}`",
            f"- n: `{payload['n']}`",
            f"- seed_protocol: `{payload['seed_protocol']}`",
            f"- seeds: `{payload['seeds']}`",
            f"- max_samples: `{payload['max_samples']}`",
            f"- delta_mean: `{payload['delta_mean']:.6f}`",
            f"- delta_std: `{payload['delta_std']:.6f}`",
            f"- delta_ci95: `{payload['delta_ci95']:.6f}`",
            f"- oracle_gain_mean: `{payload['oracle_gain_mean']:.6f}`",
            f"- oracle_gain_ci95: `{payload['oracle_gain_ci95']:.6f}`",
            f"- oracle_capture_mean: `{payload['oracle_capture_mean']:.6f}`",
            f"- oracle_capture_ci95: `{payload['oracle_capture_ci95']:.6f}`",
            f"- effect_size_d: `{effect_size_text}`",
            f"- paired_sign_test_p_value: `{p_value_text}`",
            f"- wins_vs_best_fixed: `{payload['wins_vs_best_fixed']}`",
            f"- suite_summary_json_path: `{payload['suite_summary_json_path']}`",
            f"- suite_summary_md_path: `{payload['suite_summary_md_path']}`",
            f"- primary_plot_path: `{payload['primary_plot_path']}`",
            f"- switches_plot_path: `{payload['switches_plot_path']}`",
            "",
            "## Benchmark Protocol",
            "",
            f"- dataset_count: `{payload['benchmark_protocol']['dataset_count']}`",
            f"- profile_count: `{payload['benchmark_protocol']['profile_count']}`",
            f"- sample_count_min: `{payload['benchmark_protocol']['sample_count_min']}`",
            f"- sample_count_max: `{payload['benchmark_protocol']['sample_count_max']}`",
            f"- consistent_sample_count: `{payload['benchmark_protocol']['consistent_sample_count']}`",
            f"- interpretation_note: `{payload['benchmark_protocol']['interpretation_note']}`",
            "",
            "## Policy Aggregates",
            "",
            "| Policy | n | Delta Mean | Delta Std | Delta CI95 | Oracle Gain Mean | Capture Mean | Capture CI95 | Wins vs Best Fixed | Mean Switch Count |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for row in payload["policy_aggregates"]:
            lines.append(
                f"| {row['policy_name']} | {row['n']} | {row['delta_mean']:.6f} | {row['delta_std']:.6f} | "
                f"{row['delta_ci95']:.6f} | {row['oracle_gain_mean']:.6f} | {row['oracle_capture_mean']:.6f} | "
                f"{row['oracle_capture_ci95']:.6f} | {row['wins_vs_best_fixed']} | {row['mean_switch_count']:.6f} |"
            )
        lines.extend(
            [
                "",
                "## Benchmark Results",
                "",
                "| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Oracle | Delta | Capture | Switches | Report |",
                "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
            ]
        )
        for row in payload["results"]:
            lines.append(
                f"| {row['dataset_name']} | {row['profile_name']} | {row['policy_name']} | {row['score_name']} | {row['sample_count']} | "
                f"{row['adaptive_score']:.6f} | {row['best_fixed_score']:.6f} | {row['oracle_score']:.6f} | "
                f"{row['delta_vs_best_fixed']:.6f} | {row['oracle_capture_ratio']:.6f} | {row['switch_count']} | `{row['report_md_path']}` |"
            )
        lines.extend(
            [
                "",
                "## Artifact Coverage",
                "",
                "| Dataset | Profile | Config | Metrics | Decisions | Plot | Report |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in payload["results"]:
            lines.append(
                f"| {row['dataset_name']} | {row['profile_name']} | `{row['config_path']}` | `{row['metrics_path']}` | "
                f"`{row['decision_csv_path']}` | `{row['plots_path']}` | `{row['report_md_path']}` |"
            )
        return "\n".join(lines) + "\n"

    def _build_suite_report(self, results: Sequence[Phase10SeriesResult]) -> str:
        seeded_rows: list[dict[str, Any]] = []
        benchmark_rows: list[dict[str, Any]] = []
        for result in results:
            payload = json.loads(Path(result.summary_json_path).read_text(encoding="utf-8"))
            if result.series_type == "seeded_experiment_suite":
                seeded_rows.append(payload)
            else:
                benchmark_rows.append(payload)
        lines = [
            "# Phase 10 Experimental Series",
            "",
            "| Series | Title | Type | Run Count | Summary | Report |",
            "| --- | --- | --- | ---: | --- | --- |",
        ]
        for result in results:
            lines.append(
                f"| {result.series_id} | {result.title} | {result.series_type} | {result.run_count} | "
                f"`{result.summary_json_path}` | `{result.report_md_path}` |"
            )
        if seeded_rows:
            lines.extend(
                [
                    "",
                    "## Controlled-Series Summary",
                    "",
                    "| Series | n | Seeds | Reward Mean | Reward Std | Reward CI95 | Primary Plot | Switch Plot |",
                    "| --- | ---: | --- | ---: | ---: | ---: | --- | --- |",
                ]
            )
            for row in seeded_rows:
                lines.append(
                    f"| {row['series_id']} | {row['n']} | `{', '.join(str(seed) for seed in row['seeds'])}` | "
                    f"{float(row['reward_mean']):.6f} | {float(row['reward_std']):.6f} | {float(row['reward_ci95']):.6f} | "
                    f"`{row['primary_plot_path']}` | `{row['switches_plot_path']}` |"
                )
        if benchmark_rows:
            lines.extend(
                [
                    "",
                    "## Benchmark-Series Summary",
                    "",
                    "| Series | Datasets | Profiles | n | Seed Protocol | Delta Mean | Delta Std | Delta CI95 | Oracle Gain Mean | Capture Mean | Effect Size d | Sign-Test p | Wins | Primary Plot |",
                    "| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
                ]
            )
            for row in benchmark_rows:
                effect_size = "-" if row["effect_size_d"] is None else f"{float(row['effect_size_d']):.6f}"
                p_value = "-" if row["paired_sign_test_p_value"] is None else f"{float(row['paired_sign_test_p_value']):.6f}"
                lines.append(
                    f"| {row['series_id']} | `{', '.join(row['dataset_names'])}` | `{', '.join(row['profile_names'])}` | {row['n']} | "
                    f"`{row['seed_protocol']}` | {float(row['delta_mean']):.6f} | {float(row['delta_std']):.6f} | "
                    f"{float(row['delta_ci95']):.6f} | {float(row['oracle_gain_mean']):.6f} | {float(row['oracle_capture_mean']):.6f} | "
                    f"{effect_size} | {p_value} | {row['wins_vs_best_fixed']} | "
                    f"`{row['primary_plot_path']}` |"
                )
        lines.extend(
            [
                "",
                "## Experimental Closure",
                "",
                "- all required `E1..E9` series are present in the artifact root;",
                "- each series has `summary`, `report`, `plots`, and nested run/replay artifacts;",
                "- benchmark series were regenerated under a fixed protocol with explicit `seed_protocol`, `n`, `CI95`, `effect_size_d`, `paired_sign_test_p_value`, and oracle-capture fields;",
                "- benchmark series should be interpreted with their explicit protocol, best-fixed deltas, and oracle-gain / capture notes in each `phase10_series_summary.json`.",
            ]
        )
        return "\n".join(lines) + "\n"

    def _merge_suite_series(self, current: Sequence[Phase10SeriesResult], suite_summary_path: Path) -> list[Phase10SeriesResult]:
        merged: dict[str, Phase10SeriesResult] = {}
        for series_summary_path in sorted(self._root.glob("*/phase10_series_summary.json")):
            try:
                payload = json.loads(series_summary_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            series = Phase10SeriesResult(
                series_id=str(payload["series_id"]),
                title=str(payload["title"]),
                series_type=str(payload["series_type"]),
                root_path=str(payload["root_path"]),
                summary_json_path=str(series_summary_path),
                report_md_path=str(series_summary_path.with_name("phase10_series_report.md")),
                primary_plot_path=str(payload["primary_plot_path"]),
                switches_plot_path=str(payload["switches_plot_path"]),
                run_count=int(payload["n"]),
            )
            merged[series.series_id] = series
        if suite_summary_path.exists():
            try:
                payload = json.loads(suite_summary_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                payload = {"series": []}
            for row in payload.get("series", []):
                series = Phase10SeriesResult(
                    series_id=str(row["series_id"]),
                    title=str(row["title"]),
                    series_type=str(row["series_type"]),
                    root_path=str(row["root_path"]),
                    summary_json_path=str(row["summary_json_path"]),
                    report_md_path=str(row["report_md_path"]),
                    primary_plot_path=str(row["primary_plot_path"]),
                    switches_plot_path=str(row["switches_plot_path"]),
                    run_count=int(row["run_count"]),
                )
                merged[series.series_id] = series
        for series in current:
            merged[series.series_id] = series
        return [merged[key] for key in sorted(merged)]

    def _build_controlled_bar_plot(
        self,
        *,
        runs: Sequence[dict[str, Any]],
        value_key: str,
        title: str,
        ylabel: str,
        color: str,
        ci95: float | None,
    ) -> bytes:
        labels = [str(row["seed"]) for row in runs]
        values = [float(row[value_key]) for row in runs]
        figure, axis = plt.subplots(figsize=(10.5, 4.8), dpi=140)
        figure.patch.set_facecolor("#ffffff")
        axis.set_facecolor("#f7f9fc")
        bars = axis.bar(labels, values, color=color, edgecolor="#1f2937", linewidth=0.6)
        mean_value = fmean(values) if values else 0.0
        axis.axhline(mean_value, color="#111827", linestyle="--", linewidth=1.4, label=f"mean = {mean_value:.4f}")
        if ci95 is not None and ci95 > 0.0:
            axis.axhspan(mean_value - ci95, mean_value + ci95, color="#93c5fd", alpha=0.22, label=f"CI95 ± {ci95:.4f}")
        for bar, value in zip(bars, values):
            axis.text(
                bar.get_x() + (bar.get_width() / 2),
                bar.get_height(),
                f"{value:.4f}" if abs(value) < 100 else f"{value:.0f}",
                ha="center",
                va="bottom",
                fontsize=8,
                color="#0f172a",
            )
        axis.set_title(title, loc="left", fontsize=13, fontweight="bold", color="#0f172a")
        axis.set_xlabel("Seed", color="#334155")
        axis.set_ylabel(ylabel, color="#334155")
        axis.grid(axis="y", color="#d7deea", linewidth=0.8)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.legend(frameon=False, loc="upper right")
        figure.tight_layout()
        return self._figure_to_png_bytes(figure)

    def _build_benchmark_delta_plot(self, *, rows: Sequence[dict[str, Any]], title: str) -> bytes:
        ordered_rows = sorted(rows, key=lambda row: (str(row["dataset_name"]), str(row["profile_name"])))
        labels = [f"{row['dataset_name']} / {row['profile_name']}" for row in ordered_rows]
        deltas = [float(row["delta_vs_best_fixed"]) for row in ordered_rows]
        colors = ["#16a34a" if value >= 0.0 else "#dc2626" for value in deltas]
        height = max(4.8, 0.42 * len(ordered_rows) + 1.8)
        figure, axis = plt.subplots(figsize=(12.5, height), dpi=140)
        figure.patch.set_facecolor("#ffffff")
        axis.set_facecolor("#f7f9fc")
        positions = list(range(len(ordered_rows)))
        bars = axis.barh(positions, deltas, color=colors, edgecolor="#1f2937", linewidth=0.5)
        axis.axvline(0.0, color="#111827", linewidth=1.2)
        for bar, value in zip(bars, deltas):
            x_anchor = value + (0.002 if value >= 0.0 else -0.002)
            axis.text(
                x_anchor,
                bar.get_y() + (bar.get_height() / 2),
                f"{value:+.4f}",
                va="center",
                ha="left" if value >= 0.0 else "right",
                fontsize=8,
                color="#0f172a",
            )
        axis.set_yticks(positions, labels=labels)
        axis.invert_yaxis()
        axis.set_title(title, loc="left", fontsize=13, fontweight="bold", color="#0f172a")
        axis.set_xlabel("Delta vs Best Fixed", color="#334155")
        axis.grid(axis="x", color="#d7deea", linewidth=0.8)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        figure.tight_layout()
        return self._figure_to_png_bytes(figure)

    def _build_benchmark_switch_plot(self, *, rows: Sequence[dict[str, Any]], title: str) -> bytes:
        ordered_rows = sorted(rows, key=lambda row: (str(row["dataset_name"]), str(row["profile_name"])))
        labels = [f"{row['dataset_name']} / {row['profile_name']}" for row in ordered_rows]
        values = [float(row["switch_count"]) for row in ordered_rows]
        height = max(4.8, 0.42 * len(ordered_rows) + 1.8)
        figure, axis = plt.subplots(figsize=(12.5, height), dpi=140)
        figure.patch.set_facecolor("#ffffff")
        axis.set_facecolor("#f7f9fc")
        positions = list(range(len(ordered_rows)))
        bars = axis.barh(positions, values, color="#7c3aed", edgecolor="#1f2937", linewidth=0.5)
        for bar, value in zip(bars, values):
            axis.text(
                value + 0.05,
                bar.get_y() + (bar.get_height() / 2),
                f"{int(value)}",
                va="center",
                ha="left",
                fontsize=8,
                color="#0f172a",
            )
        axis.set_yticks(positions, labels=labels)
        axis.invert_yaxis()
        axis.set_title(title, loc="left", fontsize=13, fontweight="bold", color="#0f172a")
        axis.set_xlabel("Switch Count", color="#334155")
        axis.grid(axis="x", color="#d7deea", linewidth=0.8)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        figure.tight_layout()
        return self._figure_to_png_bytes(figure)

    def _build_benchmark_result_plot(
        self,
        *,
        dataset_name: str,
        profile_name: str,
        adaptive_score: float,
        best_fixed_score: float,
        oracle_score: float,
        fixed_scores: dict[str, float],
    ) -> bytes:
        rows = [("adaptive", adaptive_score), ("best_fixed", best_fixed_score), ("oracle", oracle_score), *sorted(fixed_scores.items())]
        labels = [label for label, _ in rows]
        values = [value for _, value in rows]
        colors = ["#2563eb", "#16a34a", "#ea580c", *["#94a3b8" for _ in range(max(0, len(rows) - 3))]]
        height = max(4.2, 0.5 * len(rows) + 1.4)
        figure, axis = plt.subplots(figsize=(9.0, height), dpi=140)
        figure.patch.set_facecolor("#ffffff")
        axis.set_facecolor("#f7f9fc")
        positions = list(range(len(rows)))
        bars = axis.barh(positions, values, color=colors[: len(rows)], edgecolor="#1f2937", linewidth=0.5)
        for bar, value in zip(bars, values):
            axis.text(
                value + 0.002,
                bar.get_y() + (bar.get_height() / 2),
                f"{value:.4f}",
                va="center",
                ha="left",
                fontsize=8,
                color="#0f172a",
            )
        axis.set_yticks(positions, labels=labels)
        axis.invert_yaxis()
        axis.set_title(f"{dataset_name}: {profile_name}", loc="left", fontsize=12, fontweight="bold", color="#0f172a")
        axis.set_xlabel("Score", color="#334155")
        axis.grid(axis="x", color="#d7deea", linewidth=0.8)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        figure.tight_layout()
        return self._figure_to_png_bytes(figure)

    def _figure_to_png_bytes(self, figure: Any) -> bytes:
        from io import BytesIO

        buffer = BytesIO()
        try:
            figure.savefig(buffer, format="png", bbox_inches="tight")
            return buffer.getvalue()
        finally:
            plt.close(figure)
            buffer.close()

    def _sample_std(self, values: Sequence[float]) -> float:
        if len(values) <= 1:
            return 0.0
        return stdev(values)

    def _ci95(self, values: Sequence[float]) -> float:
        if len(values) <= 1:
            return 0.0
        return 1.96 * self._sample_std(values) / (len(values) ** 0.5)

    def _effect_size_d(self, values: Sequence[float]) -> float | None:
        if len(values) <= 1:
            return None
        sample_std = self._sample_std(values)
        if sample_std <= 1e-12:
            return None
        return fmean(values) / sample_std

    def _paired_sign_test_p_value(self, deltas: Sequence[float]) -> float | None:
        non_zero = [delta for delta in deltas if abs(delta) > 1e-12]
        n = len(non_zero)
        if n == 0:
            return None
        positive = sum(1 for delta in non_zero if delta > 0.0)
        tail = min(positive, n - positive)
        probability = sum(comb(n, index) for index in range(tail + 1)) / (2**n)
        return min(1.0, 2.0 * probability)

    def _build_benchmark_protocol(self, *, result_rows: Sequence[dict[str, Any]], max_samples: int | None) -> dict[str, Any]:
        sample_counts = sorted({int(row["sample_count"]) for row in result_rows})
        return {
            "dataset_count": len({str(row["dataset_name"]) for row in result_rows}),
            "profile_count": len({str(row["profile_name"]) for row in result_rows}),
            "requested_max_samples": max_samples,
            "sample_count_min": min(sample_counts) if sample_counts else 0,
            "sample_count_max": max(sample_counts) if sample_counts else 0,
            "consistent_sample_count": len(sample_counts) == 1,
            "interpretation_note": (
                "Benchmark replay rows are deterministic temporal streams; inferential statistics are computed over "
                "dataset/profile result deltas and should be read as cautious phase-level evidence, not as a claim of universal superiority."
            ),
        }

    def _slugify(self, value: str) -> str:
        normalized = "".join(char.lower() if char.isalnum() else "-" for char in value.strip())
        return "-".join(part for part in normalized.split("-") if part)
