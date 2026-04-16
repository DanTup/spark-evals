from __future__ import annotations

from datetime import timedelta
from typing import Any


def format_params(params: Any) -> str:
	if isinstance(params, dict):
		active = params.get("active")
		total = params.get("total")
		if active is not None and total is not None:
			return f"{format_billions(total)}-A{format_billions(active)}"
		return ", ".join(f"{key}={value}" for key, value in params.items())
	if params is None:
		return ""
	return format_billions(params)


def format_billions(value: Any) -> str:
	if isinstance(value, bool):
		return str(value)
	if isinstance(value, int):
		return f"{value}B"
	if isinstance(value, float):
		rendered = f"{value:.2f}".rstrip("0").rstrip(".")
		return f"{rendered}B"
	return str(value)


def format_flags(flags: Any) -> str:
	if flags is None:
		return ""
	if isinstance(flags, dict):
		return " ".join(f"{key}={value}" for key, value in flags.items())
	if isinstance(flags, list):
		return " ".join(str(item) for item in flags)
	return str(flags)


def format_score(score: float) -> str:
	return f"{score * 100:.1f}%"


def format_duration(duration: timedelta | None) -> str:
	if duration is None:
		return ""

	total_seconds = max(int(duration.total_seconds()), 0)
	hours, remainder = divmod(total_seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
	if hours:
		return f"{hours}h {minutes}m"
	if minutes:
		return f"{minutes}m {seconds}s"
	return f"{seconds}s"


def join_cell_lines(*lines: str) -> str:
	return "<br>".join(line for line in lines if line)


def format_score_display(score: float, is_highest: bool = False) -> str:
	formatted = f"**{format_score(score)}**"
	if is_highest:
		return f"<u>{formatted}</u>"
	return formatted


def format_score_cell(score: float, duration: timedelta | None, is_highest: bool = False) -> str:
	runtime = format_duration(duration)
	return join_cell_lines(format_score_display(score, is_highest), f"*{runtime}*" if runtime else "")


def escape_markdown(value: str) -> str:
	return value.replace("|", "\\|").replace("\n", " ")
