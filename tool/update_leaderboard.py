#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from leaderboard_formatting import escape_markdown, format_flags, format_params, format_score
from leaderboard_frontmatter import load_frontmatter


ROOT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT_DIR / "results"
README_PATH = ROOT_DIR / "README.md"
LEADERBOARD_START = "<!-- LEADERBOARD -->"
LEADERBOARD_END = "<!-- /LEADERBOARD -->"


@dataclass
class ModelResult:
	folder_name: str
	name: str
	params: Any
	flags: Any
	scores: dict[str, float]


def main() -> None:
	models = collect_model_results()
	benchmarks = sorted({benchmark for model in models for benchmark in model.scores})
	models.sort(key=lambda model: average_score(model, benchmarks), reverse=True)

	leaderboard = render_leaderboard(models, benchmarks)
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
				params=frontmatter.get("params"),
				flags=frontmatter.get("flags"),
				scores=scores,
			)
		)
	return models


def load_scores(model_dir: Path) -> dict[str, float]:
	scores_by_benchmark: dict[str, tuple[str, float]] = {}

	for result_path in sorted(model_dir.glob("*.json")):
		with result_path.open(encoding="utf-8") as handle:
			result = json.load(handle)

		benchmark = extract_benchmark_name(result, result_path)
		accuracy = extract_accuracy(result)
		created = str(result.get("eval", {}).get("created", ""))

		previous = scores_by_benchmark.get(benchmark)
		if previous is None or created >= previous[0]:
			scores_by_benchmark[benchmark] = (created, accuracy)

	return {benchmark: score for benchmark, (_, score) in scores_by_benchmark.items()}


def extract_benchmark_name(result: dict[str, Any], result_path: Path) -> str:
	eval_data = result.get("eval", {})
	name = eval_data.get("task_display_name") or eval_data.get("task")
	if isinstance(name, str) and name:
		return name.rsplit("/", maxsplit=1)[-1]
	return result_path.stem


def extract_accuracy(result: dict[str, Any]) -> float:
	scores = result.get("results", {}).get("scores", [])
	for score in scores:
		metrics = score.get("metrics", {})
		accuracy = metrics.get("accuracy")
		if isinstance(accuracy, dict) and isinstance(accuracy.get("value"), (int, float)):
			return float(accuracy["value"])

		for metric in metrics.values():
			if isinstance(metric, dict) and metric.get("name") == "accuracy":
				value = metric.get("value")
				if isinstance(value, (int, float)):
					return float(value)

	raise ValueError("Could not find accuracy metric in result file")


def average_score(model: ModelResult, benchmarks: list[str]) -> float:
	if not benchmarks:
		return 0.0
	return sum(model.scores.get(benchmark, 0.0) for benchmark in benchmarks) / len(benchmarks)


def render_leaderboard(models: list[ModelResult], benchmarks: list[str]) -> str:
	headers = ["name", "parameters", "flags", *benchmarks]
	alignments = ["---", "---", "---", *("---:" for _ in benchmarks)]
	rows = [
		"| " + " | ".join(headers) + " |",
		"| " + " | ".join(alignments) + " |",
	]

	for model in models:
		link = f"[{escape_markdown(model.name)}](results/{model.folder_name}/README.md)"
		row = [
			link,
			escape_markdown(format_params(model.params)),
			escape_markdown(format_flags(model.flags)),
		]
		for benchmark in benchmarks:
			score = model.scores.get(benchmark)
			row.append(format_score(score) if score is not None else "")
		rows.append("| " + " | ".join(row) + " |")

	return "\n".join(rows)


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
