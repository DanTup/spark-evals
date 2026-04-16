#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from leaderboard_formatting import escape_markdown, format_flags, format_score_cell, format_score_display, join_cell_lines
from leaderboard_frontmatter import load_frontmatter


ROOT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT_DIR / "results"
README_PATH = ROOT_DIR / "README.md"
LEADERBOARD_START = "<!-- LEADERBOARD -->"
LEADERBOARD_END = "<!-- /LEADERBOARD -->"
LANGUAGES = ["typescript", "csharp", "dart", "python", "shell"]
BENCHMARK_ALIASES = {
	"agent_bench_os": "AgentBench",
	"arc_challenge": "ARC Challenge",
	"ifevalcode": "IfEvalCode",
	"mbpp": "MBPP",
	"swe_bench": "SWE-bench",
	"swe_lancer": "SWE Lancer",
}
LANGUAGE_ALIASES = {
	"typescript": "ts",
	"csharp": "c#",
	"python": "py",
	"shell": "sh",
}


@dataclass
class BenchmarkResult:
	score: float
	duration: timedelta | None


@dataclass
class ModelResult:
	folder_name: str
	name: str
	flags: Any
	scores: dict[str, BenchmarkResult]


@dataclass(frozen=True)
class BenchmarkColumn:
	benchmark: str
	languages: list[str]


def main() -> None:
	models = collect_model_results()
	benchmarks = ordered_benchmarks(models)
	columns = ordered_benchmark_columns(models)
	highest_scores = benchmark_high_scores(models, benchmarks)
	primary_benchmarks = [benchmark for benchmark in benchmarks if not is_language_benchmark(benchmark)]
	models.sort(key=lambda model: average_score(model, primary_benchmarks, highest_scores), reverse=True)

	leaderboard = render_leaderboard(models, columns, highest_scores)
	update_readme(leaderboard)


def collect_model_results() -> list[ModelResult]:
	models: list[ModelResult] = []
	for model_dir in sorted(path for path in RESULTS_DIR.iterdir() if path.is_dir()):
		frontmatter = load_frontmatter(model_dir / "README.md")
		scores = load_scores(model_dir)
		models.append(
			ModelResult(
				folder_name=model_dir.name,
				name=str(frontmatter.get("name", model_dir.name)),
				flags=frontmatter.get("flags"),
				scores=scores,
			)
		)
	return models


def load_scores(model_dir: Path) -> dict[str, BenchmarkResult]:
	scores_by_benchmark: dict[str, tuple[str, BenchmarkResult]] = {}

	for result_path in sorted(model_dir.glob("*.json")):
		with result_path.open(encoding="utf-8") as handle:
			result = json.load(handle)

		benchmark_scores = extract_benchmark_scores(result, result_path)
		created = str(result.get("eval", {}).get("created", ""))
		duration = extract_duration(result)

		for benchmark, accuracy in benchmark_scores.items():
			previous = scores_by_benchmark.get(benchmark)
			if previous is None or created >= previous[0]:
				scores_by_benchmark[benchmark] = (created, BenchmarkResult(score=accuracy, duration=duration))

	return {benchmark: score for benchmark, (_, score) in scores_by_benchmark.items()}


def extract_duration(result: dict[str, Any]) -> timedelta | None:
	stats = result.get("stats", {})
	started_at = stats.get("started_at")
	completed_at = stats.get("completed_at")
	if not isinstance(started_at, str) or not isinstance(completed_at, str):
		return None

	try:
		return datetime.fromisoformat(completed_at) - datetime.fromisoformat(started_at)
	except ValueError:
		return None


def extract_benchmark_name(result: dict[str, Any], result_path: Path) -> str:
	eval_data = result.get("eval", {})
	name = eval_data.get("task_display_name") or eval_data.get("task")
	if isinstance(name, str) and name:
		return name.rsplit("/", maxsplit=1)[-1]
	return result_path.stem


def extract_benchmark_scores(result: dict[str, Any], result_path: Path) -> dict[str, float]:
	benchmark = extract_benchmark_name(result, result_path)
	scores = result.get("results", {}).get("scores", [])
	for score in scores:
		metrics = score.get("metrics", {})
		accuracy = metrics.get("accuracy") or metrics.get("overall_accuracy")
		if not isinstance(metrics, dict):
			continue

		benchmark_scores: dict[str, float] = {}
		if isinstance(accuracy, dict) and isinstance(accuracy.get("value"), (int, float)):
			benchmark_scores[benchmark] = float(accuracy["value"])

		for metric in metrics.values():
			if isinstance(metric, dict) and metric.get("name") == "accuracy":
				value = metric.get("value")
				if isinstance(value, (int, float)):
					benchmark_scores.setdefault(benchmark, float(value))

		for language in LANGUAGES:
			correctness = extract_metric_value(metrics.get(f"{language}_correctness"))
			if correctness is not None:
				benchmark_scores[f"{benchmark} {language}"] = correctness

			instruction = extract_metric_value(metrics.get(f"{language}_instruction"))
			if instruction is not None:
				benchmark_scores[f"{benchmark} {language} instruction"] = instruction

		if benchmark_scores:
			return benchmark_scores

	raise ValueError("Could not find accuracy metric in result file")


def extract_metric_value(metric: Any) -> float | None:
	if isinstance(metric, dict) and isinstance(metric.get("value"), (int, float)):
		return float(metric["value"])
	return None


def ordered_benchmarks(models: list[ModelResult]) -> list[str]:
	all_benchmarks = {benchmark for model in models for benchmark in model.scores}
	base_benchmarks = sorted({base_benchmark_name(benchmark) for benchmark in all_benchmarks})
	ordered: list[str] = []

	for base_benchmark in base_benchmarks:
		if base_benchmark in all_benchmarks:
			ordered.append(base_benchmark)

		for language in LANGUAGES:
			language_benchmark = f"{base_benchmark} {language}"
			if language_benchmark in all_benchmarks:
				ordered.append(language_benchmark)

			instruction_benchmark = f"{base_benchmark} {language} instruction"
			if instruction_benchmark in all_benchmarks:
				ordered.append(instruction_benchmark)

	return ordered


def ordered_benchmark_columns(models: list[ModelResult]) -> list[BenchmarkColumn]:
	all_benchmarks = {benchmark for model in models for benchmark in model.scores}
	base_benchmarks = sorted({base_benchmark_name(benchmark) for benchmark in all_benchmarks})
	columns: list[BenchmarkColumn] = []

	for base_benchmark in base_benchmarks:
		languages = [
			language
			for language in LANGUAGES
			if f"{base_benchmark} {language}" in all_benchmarks
			or f"{base_benchmark} {language} instruction" in all_benchmarks
		]
		if base_benchmark in all_benchmarks or languages:
			columns.append(BenchmarkColumn(benchmark=base_benchmark, languages=languages))

	return columns


def base_benchmark_name(benchmark: str) -> str:
	for language in LANGUAGES:
		instruction_suffix = f" {language} instruction"
		if benchmark.endswith(instruction_suffix):
			return benchmark[: -len(instruction_suffix)]

		language_suffix = f" {language}"
		if benchmark.endswith(language_suffix):
			return benchmark[: -len(language_suffix)]

	return benchmark


def is_language_benchmark(benchmark: str) -> bool:
	return base_benchmark_name(benchmark) != benchmark


def benchmark_high_scores(models: list[ModelResult], benchmarks: list[str]) -> dict[str, float | None]:
	return {
		benchmark: max((model.scores[benchmark].score for model in models if benchmark in model.scores), default=None)
		for benchmark in benchmarks
	}


def average_score(model: ModelResult, benchmarks: list[str], highest_scores: dict[str, float | None]) -> float:
	if not benchmarks:
		return 0.0
	normalized_scores = [
		model.scores[benchmark].score / highest_scores[benchmark]
		for benchmark in benchmarks
		if benchmark in model.scores and highest_scores[benchmark] not in (None, 0)
	]
	if not normalized_scores:
		return 0.0
	return sum(normalized_scores) / len(normalized_scores)


def render_leaderboard(
	models: list[ModelResult],
	columns: list[BenchmarkColumn],
	highest_scores: dict[str, float | None],
) -> str:
	headers = ["name", *(display_benchmark_name(column.benchmark) for column in columns)]
	alignments = ["---", *("---:" for _ in columns)]
	rows = [
		"| " + " | ".join(headers) + " |",
		"| " + " | ".join(alignments) + " |",
	]

	for model in models:
		link = f"[{escape_markdown(model.name)}](results/{model.folder_name}/README.md)"
		flags = escape_markdown(format_flags(model.flags))
		row = [join_cell_lines(link, flags)]
		for column in columns:
			row.append(render_benchmark_cell(model, column, highest_scores))
		rows.append("| " + " | ".join(row) + " |")

	return "\n".join(rows)


def render_benchmark_cell(
	model: ModelResult,
	column: BenchmarkColumn,
	highest_scores: dict[str, float | None],
) -> str:
	lines: list[str] = []
	base_result = model.scores.get(column.benchmark)
	if base_result is not None:
		lines.append(
			format_score_cell(
				base_result.score,
				base_result.duration,
				base_result.score == highest_scores[column.benchmark],
			)
		)

	for language in column.languages:
		language_line = render_language_line(model, column.benchmark, language, highest_scores)
		if language_line:
			lines.append(language_line)

	return join_cell_lines(*lines)


def render_language_line(
	model: ModelResult,
	benchmark: str,
	language: str,
	highest_scores: dict[str, float | None],
) -> str:
	variant_scores: list[str] = []
	for suffix in ("", " instruction"):
		benchmark_name = f"{benchmark} {language}{suffix}"
		result = model.scores.get(benchmark_name)
		if result is None:
			continue
		variant_scores.append(format_score_display(result.score, result.score == highest_scores[benchmark_name]))

	if not variant_scores:
		return ""

	return f"{display_language_name(language)}: {' / '.join(variant_scores)}"


def display_benchmark_name(benchmark: str) -> str:
	return BENCHMARK_ALIASES.get(benchmark, benchmark)


def display_language_name(language: str) -> str:
	return LANGUAGE_ALIASES.get(language, language)


def update_readme(leaderboard: str) -> None:
	readme = README_PATH.read_text(encoding="utf-8")
	pattern = rf"({re.escape(LEADERBOARD_START)}\n)(.*?)(\n{re.escape(LEADERBOARD_END)})"
	match = re.search(pattern, readme, flags=re.DOTALL)
	if match is None:
		raise ValueError("Could not locate leaderboard markers in README")
	updated = re.sub(pattern, rf"\1{leaderboard}\3", readme, count=1, flags=re.DOTALL)
	README_PATH.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
	main()
