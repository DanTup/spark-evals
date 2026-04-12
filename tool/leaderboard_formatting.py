from __future__ import annotations

from typing import Any


def format_params(params: Any) -> str:
	if isinstance(params, dict):
		active = params.get("active")
		total = params.get("total")
		if active is not None and total is not None:
			return f"{format_billions(active)} active / {format_billions(total)} total"
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
		return ", ".join(f"{key}={value}" for key, value in flags.items())
	if isinstance(flags, list):
		return ", ".join(str(item) for item in flags)
	return str(flags)


def format_score(score: float) -> str:
	return f"{score * 100:.2f}%"


def escape_markdown(value: str) -> str:
	return value.replace("|", "\\|").replace("\n", " ")
