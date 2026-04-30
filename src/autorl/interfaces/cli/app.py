"""Argument parsing and command execution for the local AutoRL CLI."""

from __future__ import annotations

import argparse
from pathlib import Path

from autorl.application import BenchmarkReplayRunner, ExperimentOrchestrator, Phase10ExperimentalSeriesRunner, PhaseValidationRunner, load_config


def build_parser() -> argparse.ArgumentParser:
    """Create the phase 6 CLI parser."""
    parser = argparse.ArgumentParser(prog="autorl", description="AutoRL Strategy Manager")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run one experiment from a configuration file")
    run_parser.add_argument("--config", required=True, help="Path to a YAML or JSON config file")

    list_parser = subparsers.add_parser("list", help="List persisted experiments")
    list_parser.add_argument("--artifacts-root", default="artifacts", help="Artifacts root containing autorl.db")

    report_parser = subparsers.add_parser("report", help="Print a text report for one experiment")
    report_parser.add_argument("--experiment-id", required=True, help="Experiment identifier")
    report_parser.add_argument("--artifacts-root", default="artifacts", help="Artifacts root containing autorl.db")

    rerun_parser = subparsers.add_parser("rerun", help="Re-run a persisted experiment by its identifier")
    rerun_parser.add_argument("--experiment-id", required=True, help="Experiment identifier to re-run")
    rerun_parser.add_argument("--artifacts-root", default="artifacts", help="Artifacts root containing autorl.db")

    status_parser = subparsers.add_parser("status", help="Print persisted status for one experiment")
    status_parser.add_argument("--experiment-id", required=True, help="Experiment identifier")
    status_parser.add_argument("--artifacts-root", default="artifacts", help="Artifacts root containing autorl.db")

    export_parser = subparsers.add_parser("export", help="Export one experiment bundle or report artifact")
    export_parser.add_argument("--experiment-id", required=True, help="Experiment identifier")
    export_parser.add_argument("--artifacts-root", default="artifacts", help="Artifacts root containing autorl.db")
    export_parser.add_argument("--format", default="zip", choices=["zip", "json", "html", "markdown"], help="Export format")

    validate_config_parser = subparsers.add_parser("validate-config", help="Validate a configuration file and print its hash")
    validate_config_parser.add_argument("--config", required=True, help="Path to a YAML or JSON config file")

    run_suite_parser = subparsers.add_parser("run-suite", help="Run one config repeatedly over multiple seeds")
    run_suite_parser.add_argument("--config", required=True, help="Path to a YAML or JSON config file")
    run_suite_parser.add_argument("--artifacts-root", default=None, help="Override output root for suite artifacts")
    run_suite_parser.add_argument("--seeds", nargs="+", type=int, default=[41, 42, 43, 44, 45], help="Seed list for the experiment suite")

    validate_suite_parser = subparsers.add_parser("validate-suite", help="Run the phase 0-7 validation suite")
    validate_suite_parser.add_argument("--artifacts-root", default="artifacts/validation_suite_0_7", help="Output root for validation artifacts")
    validate_suite_parser.add_argument("--seeds", nargs="+", type=int, default=[41, 42, 43, 44, 45], help="Seed list for the validation suite")

    benchmark_elec2_parser = subparsers.add_parser("benchmark-elec2", help="Run real-stream replay validation on the Elec2 dataset")
    benchmark_elec2_parser.add_argument("--artifacts-root", default="artifacts/real_stream_validation/elec2", help="Output root for benchmark artifacts")
    benchmark_elec2_parser.add_argument("--max-samples", type=int, default=None, help="Optional sample cap for faster replay smoke runs")

    benchmark_suite_parser = subparsers.add_parser("benchmark-suite", help="Run the real-stream replay suite on multiple datasets")
    benchmark_suite_parser.add_argument("--artifacts-root", default="artifacts/real_stream_validation/suite", help="Output root for benchmark suite artifacts")
    benchmark_suite_parser.add_argument("--datasets", nargs="+", default=["elec2", "bikes", "trump_approval"], help="Dataset list to run")
    benchmark_suite_parser.add_argument("--max-samples", type=int, default=None, help="Optional sample cap applied to built-in named benchmarks in the suite")

    benchmark_suite_hedge_parser = subparsers.add_parser("benchmark-suite-hedge", help="Run the real-stream replay suite with Hedge-style expert weighting")
    benchmark_suite_hedge_parser.add_argument("--artifacts-root", default="artifacts/real_stream_validation/suite_hedge", help="Output root for benchmark suite artifacts")
    benchmark_suite_hedge_parser.add_argument("--datasets", nargs="+", default=["elec2", "bikes", "trump_approval"], help="Dataset list to run")

    benchmark_suite_recent_leader_parser = subparsers.add_parser("benchmark-suite-recent-leader", help="Run the real-stream replay suite with recent-leader switching")
    benchmark_suite_recent_leader_parser.add_argument("--artifacts-root", default="artifacts/real_stream_validation/suite_recent_leader", help="Output root for benchmark suite artifacts")
    benchmark_suite_recent_leader_parser.add_argument("--datasets", nargs="+", default=["elec2", "bikes", "trump_approval"], help="Dataset list to run")

    benchmark_profile_parser = subparsers.add_parser("benchmark-profile", help="Run one H1/H2 benchmark profile on one named dataset")
    benchmark_profile_parser.add_argument("--profile", required=True, help="Path to a benchmark profile YAML file")
    benchmark_profile_parser.add_argument("--dataset", required=True, help="Named benchmark dataset to replay")
    benchmark_profile_parser.add_argument("--artifacts-root", default="artifacts/real_stream_validation/profile_run", help="Output root for profile artifacts")
    benchmark_profile_parser.add_argument("--max-samples", type=int, default=None, help="Optional sample cap for faster replay")

    benchmark_hypothesis_suite_parser = subparsers.add_parser("benchmark-hypothesis-suite", help="Run one suite of H1/H2 benchmark profiles across multiple datasets")
    benchmark_hypothesis_suite_parser.add_argument("--profiles", nargs="+", required=True, help="Benchmark profile YAML paths")
    benchmark_hypothesis_suite_parser.add_argument("--datasets", nargs="+", default=["elec2", "airlines", "insects_recurring"], help="Named benchmark datasets")
    benchmark_hypothesis_suite_parser.add_argument("--artifacts-root", default="artifacts/real_stream_validation/hypothesis_suite", help="Output root for hypothesis-suite artifacts")
    benchmark_hypothesis_suite_parser.add_argument("--max-samples", type=int, default=None, help="Optional sample cap for faster replay")

    phase10_suite_parser = subparsers.add_parser("phase10-suite", help="Run the formal phase 10 experimental series E1..E9")
    phase10_suite_parser.add_argument("--artifacts-root", default="artifacts/phase10_experimental_series", help="Output root for phase 10 artifacts")
    phase10_suite_parser.add_argument("--seeds", nargs="+", type=int, default=[41, 42, 43, 44, 45], help="Seed list for controlled experimental series")
    phase10_suite_parser.add_argument("--benchmark-datasets", nargs="+", default=["elec2", "bikes", "trump_approval", "waterflow", "insects_recurring"], help="Named benchmark datasets for profile-driven series")
    phase10_suite_parser.add_argument("--benchmark-max-samples", type=int, default=None, help="Optional sample cap for benchmark replay series")
    phase10_suite_parser.add_argument("--series", nargs="+", default=None, help="Optional subset of phase 10 series ids, for example: E1 E2 E3")
    phase10_suite_parser.add_argument("--profile-names", nargs="+", default=None, help="Optional subset of benchmark profile stems for E5/E6/E9 chunked execution")

    return parser


def run_cli(argv: list[str]) -> int:
    """Execute the CLI command."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        orchestrator = ExperimentOrchestrator()
        result = orchestrator.run_from_config_path(args.config)
        print(f"experiment_id: {result.experiment_id}")
        print(f"status: {result.status}")
        print(f"artifacts_path: {result.artifacts_path}")
        print(f"episodes: {result.episode_count}")
        print(f"decisions: {result.decision_count}")
        print(f"switches: {result.switch_count}")
        print(f"final_strategy: {result.final_strategy}")
        return 0

    if args.command == "list":
        orchestrator = ExperimentOrchestrator(default_artifacts_root=Path(args.artifacts_root))
        experiments = orchestrator.list_experiments(artifacts_root=args.artifacts_root)
        if not experiments:
            print("No experiments found.")
            return 0
        for experiment in experiments:
            print(
                " | ".join(
                    [
                        experiment["experiment_id"],
                        experiment["experiment_name"],
                        experiment["scenario_name"],
                        experiment["status"],
                        f"seed={experiment['seed']}",
                    ]
                )
            )
        return 0

    if args.command == "report":
        orchestrator = ExperimentOrchestrator(default_artifacts_root=Path(args.artifacts_root))
        print(orchestrator.report_experiment(args.experiment_id, artifacts_root=args.artifacts_root))
        return 0

    if args.command == "rerun":
        orchestrator = ExperimentOrchestrator(default_artifacts_root=Path(args.artifacts_root))
        result = orchestrator.rerun_experiment(args.experiment_id, artifacts_root=args.artifacts_root)
        print(f"source_experiment_id: {args.experiment_id}")
        print(f"experiment_id: {result.experiment_id}")
        print(f"status: {result.status}")
        print(f"artifacts_path: {result.artifacts_path}")
        return 0

    if args.command == "status":
        orchestrator = ExperimentOrchestrator(default_artifacts_root=Path(args.artifacts_root))
        status_payload = orchestrator.get_experiment_status(args.experiment_id, artifacts_root=args.artifacts_root)
        for key in (
            "experiment_id",
            "status",
            "source_experiment_id",
            "active_strategy",
            "current_episode",
            "episode_count",
            "decision_count",
            "switch_count",
        ):
            print(f"{key}: {status_payload.get(key)}")
        return 0

    if args.command == "export":
        orchestrator = ExperimentOrchestrator(default_artifacts_root=Path(args.artifacts_root))
        export_path = orchestrator.export_experiment(
            args.experiment_id,
            artifacts_root=args.artifacts_root,
            output_format=args.format,
        )
        print(f"experiment_id: {args.experiment_id}")
        print(f"format: {args.format}")
        print(f"export_path: {export_path}")
        return 0

    if args.command == "validate-config":
        config = load_config(args.config)
        print(f"experiment_name: {config.experiment_name}")
        print(f"scenario: {config.scenario.name.value}")
        print(f"seed: {config.seed}")
        print(f"config_hash: {config.config_hash}")
        return 0

    if args.command == "run-suite":
        orchestrator = ExperimentOrchestrator(default_artifacts_root=Path(args.artifacts_root or "artifacts"))
        result = orchestrator.run_suite_from_config_path(
            args.config,
            seeds=list(args.seeds),
            artifacts_root=args.artifacts_root,
        )
        print(f"suite_name: {result['suite_name']}")
        print(f"run_count: {result['run_count']}")
        print(f"reward_mean: {result['reward_mean']:.6f}")
        print(f"reward_std: {result['reward_std']:.6f}")
        print(f"reward_ci95: {result['reward_ci95']:.6f}")
        print(f"summary_json_path: {result['summary_json_path']}")
        print(f"summary_md_path: {result['summary_md_path']}")
        return 0

    if args.command == "validate-suite":
        result = PhaseValidationRunner(root=args.artifacts_root).run_nonstationary_suite(seeds=tuple(args.seeds))
        print(f"summary_json_path: {result.summary_json_path}")
        print(f"report_md_path: {result.report_md_path}")
        return 0

    if args.command == "benchmark-elec2":
        result = BenchmarkReplayRunner().run_elec2_benchmark(output_root=args.artifacts_root, max_samples=args.max_samples)
        print(f"dataset: {result.dataset_name}")
        print(f"score_name: {result.score_name}")
        print(f"samples: {result.sample_count}")
        print(f"adaptive_score: {result.adaptive_score:.6f}")
        print(f"best_fixed_strategy: {result.best_fixed_strategy}")
        print(f"best_fixed_score: {result.best_fixed_score:.6f}")
        print(f"delta_vs_best_fixed: {result.delta_vs_best_fixed:.6f}")
        print(f"switch_count: {result.switch_count}")
        print(f"decision_csv_path: {result.decision_csv_path}")
        print(f"summary_json_path: {result.summary_json_path}")
        print(f"report_md_path: {result.report_md_path}")
        return 0

    if args.command == "benchmark-suite":
        result = BenchmarkReplayRunner().run_real_stream_suite(
            output_root=args.artifacts_root,
            datasets_to_run=tuple(args.datasets),
            max_samples=args.max_samples,
        )
        print(f"dataset_count: {len(result.results)}")
        print(f"summary_json_path: {result.summary_json_path}")
        print(f"report_md_path: {result.report_md_path}")
        return 0

    if args.command == "benchmark-suite-hedge":
        result = BenchmarkReplayRunner().run_real_stream_suite_with_hedge(
            output_root=args.artifacts_root,
            datasets_to_run=tuple(args.datasets),
        )
        print(f"dataset_count: {len(result.results)}")
        print(f"summary_json_path: {result.summary_json_path}")
        print(f"report_md_path: {result.report_md_path}")
        return 0

    if args.command == "benchmark-suite-recent-leader":
        result = BenchmarkReplayRunner().run_real_stream_suite_with_recent_leader(
            output_root=args.artifacts_root,
            datasets_to_run=tuple(args.datasets),
        )
        print(f"dataset_count: {len(result.results)}")
        print(f"summary_json_path: {result.summary_json_path}")
        print(f"report_md_path: {result.report_md_path}")
        return 0

    if args.command == "benchmark-profile":
        result = BenchmarkReplayRunner().run_profile_benchmark(
            profile_path=args.profile,
            dataset_name=args.dataset,
            output_root=args.artifacts_root,
            max_samples=args.max_samples,
        )
        print(f"dataset: {result.dataset_name}")
        print(f"profile_policy: {result.policy_name}")
        print(f"score_name: {result.score_name}")
        print(f"samples: {result.sample_count}")
        print(f"adaptive_score: {result.adaptive_score:.6f}")
        print(f"best_fixed_strategy: {result.best_fixed_strategy}")
        print(f"best_fixed_score: {result.best_fixed_score:.6f}")
        print(f"delta_vs_best_fixed: {result.delta_vs_best_fixed:.6f}")
        print(f"switch_count: {result.switch_count}")
        print(f"summary_json_path: {result.summary_json_path}")
        print(f"report_md_path: {result.report_md_path}")
        return 0

    if args.command == "benchmark-hypothesis-suite":
        result = BenchmarkReplayRunner().run_profile_suite(
            profile_paths=tuple(args.profiles),
            dataset_names=tuple(args.datasets),
            output_root=args.artifacts_root,
            max_samples=args.max_samples,
        )
        print(f"result_count: {len(result.results)}")
        print(f"summary_json_path: {result.summary_json_path}")
        print(f"report_md_path: {result.report_md_path}")
        return 0

    if args.command == "phase10-suite":
        result = Phase10ExperimentalSeriesRunner(root=args.artifacts_root).run_phase10_suite(
            seeds=tuple(args.seeds),
            benchmark_datasets=tuple(args.benchmark_datasets),
            benchmark_max_samples=args.benchmark_max_samples,
            series_ids=args.series,
            profile_names=args.profile_names,
        )
        print(f"series_count: {len(result.series)}")
        print(f"summary_json_path: {result.summary_json_path}")
        print(f"report_md_path: {result.report_md_path}")
        return 0

    parser.print_help()
    return 1
