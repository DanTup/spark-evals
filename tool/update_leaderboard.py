#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from leaderboard_formatting import escape_markdown, format_duration, format_flags, format_score, format_score_display, format_tokens, join_cell_lines
from leaderboard_frontmatter import load_frontmatter


ROOT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT_DIR / "results"
README_PATH = ROOT_DIR / "README.md"
LEADERBOARD_START = "<!-- LEADERBOARD -->"
LEADERBOARD_END = "<!-- /LEADERBOARD -->"
LANGUAGES = ["typescript", "csharp", "dart", "python", "shell"]
IGNORED_RESULT_FILENAMES = {"eval-set.json", "logs.json"}
BENCHMARK_ALIASES = {
	"agent_bench_os": "Agent<br>Bench",
	"arc_challenge": "ARC<br>Challenge",
	"ifevalcode": "IfEvalCode",
	"mbpp": "MBPP",
	"swe_bench": "SWE-bench",
	"swe_lancer": "SWE Lancer",
	"assistant_bench_closed_book_one_shot": "Assis'<br>Bench<br>CBOS",
	"assistant_bench_closed_book_zero_shot": "Assis'<br>Bench<br>CBZS",
	"theagentcompany": "The<br>Agent<br>Co",
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
	scored_samples: int
	duration: timedelta | None
	input_tokens: int | None
	output_tokens: int | None


@dataclass
class ModelResult:
	folder_name: str
	name: str
	flags: Any
	scores: dict[str, BenchmarkResult]
	total_duration: timedelta | None
	total_input_tokens: int | None
	total_output_tokens: int | None


@dataclass(frozen=True)
class BenchmarkColumn:
	benchmark: str
	languages: list[str]


@dataclass(frozen=True)
class ExtractedBenchmarkScore:
	score: float
	scored_samples: int


def main() -> None:
	models = collect_model_results()
	benchmarks = ordered_benchmarks(models)
	columns = ordered_benchmark_columns(models)
	scoring_benchmarks = benchmarks
	highest_scores = benchmark_high_scores(models, benchmarks)
	highest_overall_score = max((overall_score(model, scoring_benchmarks) for model in models), default=0.0)
	models.sort(key=lambda model: model.name)
	models.sort(
		key=lambda model: (overall_score(model, scoring_benchmarks), total_scored_samples(model, scoring_benchmarks)),
		reverse=True,
	)

	leaderboard = render_leaderboard(models, columns, highest_scores, scoring_benchmarks, highest_overall_score)
	update_readme(leaderboard)


def collect_model_results() -> list[ModelResult]:
	models: list[ModelResult] = []
	for model_dir in sorted(path for path in RESULTS_DIR.iterdir() if path.is_dir()):
		frontmatter = load_frontmatter(model_dir / "README.md")
		scores, total_duration, total_input_tokens, total_output_tokens = load_scores(model_dir)
		models.append(
			ModelResult(
				folder_name=model_dir.name,
				name=str(frontmatter.get("name", model_dir.name)),
				flags=frontmatter.get("flags"),
				scores=scores,
				total_duration=total_duration,
				total_input_tokens=total_input_tokens,
				total_output_tokens=total_output_tokens,
			)
		)
	return models


def load_scores(model_dir: Path) -> tuple[dict[str, BenchmarkResult], timedelta | None, int | None, int | None]:
	selected_results: dict[str, tuple[str, dict[str, ExtractedBenchmarkScore], timedelta | None, int | None, int | None]] = {}

	for result_path in sorted(model_dir.glob("*.json")):
		if result_path.name in IGNORED_RESULT_FILENAMES:
			continue

		with result_path.open(encoding="utf-8") as handle:
			result = json.load(handle)

		benchmark_scores = extract_benchmark_scores(result, result_path)
		benchmark = extract_benchmark_name(result, result_path)
		created = str(result.get("eval", {}).get("created", ""))
		duration = extract_duration(result)
		input_tokens, output_tokens = extract_token_usage(result)
		previous = selected_results.get(benchmark)
		if previous is None or created >= previous[0]:
			selected_results[benchmark] = (created, benchmark_scores, duration, input_tokens, output_tokens)

	scores_by_benchmark: dict[str, BenchmarkResult] = {}
	total_duration = timedelta()
	has_duration = False
	total_input_tokens = 0
	total_output_tokens = 0
	has_tokens = False

	for _, benchmark_scores, duration, input_tokens, output_tokens in selected_results.values():
		for benchmark_name, benchmark_score in benchmark_scores.items():
			scores_by_benchmark[benchmark_name] = BenchmarkResult(
				score=benchmark_score.score,
				scored_samples=benchmark_score.scored_samples,
				duration=duration,
				input_tokens=input_tokens,
				output_tokens=output_tokens,
			)

		if duration is not None:
			total_duration += duration
			has_duration = True

		if input_tokens is not None and output_tokens is not None:
			total_input_tokens += input_tokens
			total_output_tokens += output_tokens
			has_tokens = True

	return (
		scores_by_benchmark,
		total_duration if has_duration else None,
		total_input_tokens if has_tokens else None,
		total_output_tokens if has_tokens else None,
	)


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


def extract_token_usage(result: dict[str, Any]) -> tuple[int | None, int | None]:
	stats = result.get("stats", {})
	model_usage = stats.get("model_usage")
	if not isinstance(model_usage, dict):
		return None, None

	input_tokens = 0
	output_tokens = 0
	found_usage = False
	for usage in model_usage.values():
		if not isinstance(usage, dict):
			continue
		usage_input_tokens = usage.get("input_tokens")
		usage_output_tokens = usage.get("output_tokens")
		if not isinstance(usage_input_tokens, int) or not isinstance(usage_output_tokens, int):
			continue
		input_tokens += usage_input_tokens
		output_tokens += usage_output_tokens
		found_usage = True

	if not found_usage:
		return None, None
	return input_tokens, output_tokens


def extract_benchmark_name(result: dict[str, Any], result_path: Path) -> str:
	eval_data = result.get("eval", {})
	name = eval_data.get("task_display_name") or eval_data.get("task")
	if isinstance(name, str) and name:
		return name.rsplit("/", maxsplit=1)[-1]
	return result_path.stem


def extract_benchmark_scores(result: dict[str, Any], result_path: Path) -> dict[str, ExtractedBenchmarkScore]:
	benchmark = extract_benchmark_name(result, result_path)
	scores = result.get("results", {}).get("scores", [])
	for score in scores:
		if not isinstance(score, dict):
			continue

		scored_samples = score.get("scored_samples")
		if not isinstance(scored_samples, int) or scored_samples <= 0:
			continue

		metrics = score.get("metrics", {})
		if not isinstance(metrics, dict):
			continue

		accuracy = metrics.get("accuracy") or metrics.get("mean") or metrics.get("overall_accuracy") or metrics.get("assistant_bench_accuracy")

		benchmark_scores: dict[str, ExtractedBenchmarkScore] = {}
		if isinstance(accuracy, dict) and isinstance(accuracy.get("value"), (int, float)):
			benchmark_scores[benchmark] = ExtractedBenchmarkScore(float(accuracy["value"]), scored_samples)

		for metric in metrics.values():
			if isinstance(metric, dict) and metric.get("name") == "accuracy":
				value = metric.get("value")
				if isinstance(value, (int, float)):
					benchmark_scores.setdefault(benchmark, ExtractedBenchmarkScore(float(value), scored_samples))

		for language in LANGUAGES:
			correctness = extract_metric_value(metrics.get(f"{language}_correctness"))
			if correctness is not None:
				benchmark_scores[f"{benchmark} {language}"] = ExtractedBenchmarkScore(correctness, scored_samples)

			instruction = extract_metric_value(metrics.get(f"{language}_instruction"))
			if instruction is not None:
				benchmark_scores[f"{benchmark} {language} instruction"] = ExtractedBenchmarkScore(instruction, scored_samples)

		if benchmark_scores:
			return benchmark_scores

	raise ValueError(
		"Could not find accuracy metric in result file "
		f"{result_path}: {describe_result_payload(result)}"
	)


def describe_result_payload(result: dict[str, Any]) -> str:
	results = result.get("results")
	if isinstance(results, dict):
		results_summary = {
			"results_keys": sorted(results.keys()),
			"score_count": len(results.get("scores", [])) if isinstance(results.get("scores"), list) else None,
			"score_metric_keys": [
				sorted(score.get("metrics", {}).keys())
				for score in results.get("scores", [])
				if isinstance(score, dict) and isinstance(score.get("metrics"), dict)
			],
		}
	else:
		results_summary = {
			"results_type": type(results).__name__,
			"top_level_keys": sorted(result.keys()),
		}

	return json.dumps(results_summary, ensure_ascii=True, sort_keys=True, indent=2)


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


def total_scored_samples(model: ModelResult, benchmarks: list[str]) -> int:
	return sum(model.scores[benchmark].scored_samples for benchmark in benchmarks if benchmark in model.scores)


def overall_score(model: ModelResult, benchmarks: list[str]) -> float:
	total_samples = 0
	total_passed = 0.0
	for benchmark in benchmarks:
		result = model.scores.get(benchmark)
		if result is None:
			continue
		total_samples += result.scored_samples
		total_passed += result.score * result.scored_samples
	if total_samples == 0:
		return 0.0
	return total_passed / total_samples


def render_leaderboard(
	models: list[ModelResult],
	columns: list[BenchmarkColumn],
	highest_scores: dict[str, float | None],
	scoring_benchmarks: list[str],
	highest_overall_score: float,
) -> str:
	headers = ["name", *(display_benchmark_name(column.benchmark) for column in columns), "Overall"]
	alignments = ["---", *("---:" for _ in columns), "---:"]
	rows = [
		"| " + " | ".join(headers) + " |",
		"| " + " | ".join(alignments) + " |",
	]

	for model in models:
		model_overall_score = overall_score(model, scoring_benchmarks)
		link = f"[{escape_markdown(model.name)}](results/{model.folder_name}/)"
		flags = escape_markdown(format_flags(model.flags))
		row = [
			join_cell_lines(
				link,
				flags,
				format_model_totals(model.total_duration, model.total_input_tokens, model.total_output_tokens),
			)
		]
		for column in columns:
			row.append(render_benchmark_cell(model, column, highest_scores))
		row.append(format_score_display(model_overall_score, model_overall_score == highest_overall_score))
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
		lines.append(format_score_display(base_result.score, base_result.score == highest_scores[column.benchmark]))

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


def format_model_totals(duration: timedelta | None, input_tokens: int | None, output_tokens: int | None) -> str:
	lines: list[str] = []
	lines.append("&nbsp;&nbsp;&nbsp;&nbsp;<nobr>")

	runtime = format_duration(duration)
	tokens = format_tokens(input_tokens, output_tokens)

	if runtime:
		lines.append(f"{runtime}")
	if runtime and tokens:
		lines.append(", ")
	if tokens:
		lines.append(tokens)

	lines.append("</nobr>")
	return "".join(lines)


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
