from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def load_frontmatter(readme_path: Path) -> dict[str, Any]:
	content = readme_path.read_text(encoding="utf-8")
	match = re.match(r"^---\n(.*?)\n---\n?", content, re.DOTALL)
	if not match:
		return {}

	frontmatter = match.group(1)
	try:
		import yaml  # type: ignore
	except ImportError:
		return parse_simple_yaml(frontmatter)

	data = yaml.safe_load(frontmatter)
	return data if isinstance(data, dict) else {}


def parse_simple_yaml(frontmatter: str) -> dict[str, Any]:
	lines = []
	for raw_line in frontmatter.splitlines():
		if not raw_line.strip() or raw_line.lstrip().startswith("#"):
			continue
		lines.append(raw_line.rstrip())

	if not lines:
		return {}

	parsed, next_index = parse_block(lines, start_index=0, indent=0)
	if next_index != len(lines) or not isinstance(parsed, dict):
		raise ValueError("Unsupported YAML frontmatter")
	return parsed


def parse_block(lines: list[str], start_index: int, indent: int) -> tuple[Any, int]:
	if lines[start_index].lstrip().startswith("- "):
		return parse_list(lines, start_index, indent)
	return parse_dict(lines, start_index, indent)


def parse_dict(lines: list[str], start_index: int, indent: int) -> tuple[dict[str, Any], int]:
	result: dict[str, Any] = {}
	index = start_index

	while index < len(lines):
		line = lines[index]
		current_indent = leading_spaces(line)
		if current_indent < indent:
			break
		if current_indent != indent:
			raise ValueError("Invalid YAML indentation")

		stripped = line.strip()
		if stripped.startswith("- "):
			break

		key, separator, remainder = stripped.partition(":")
		if not separator:
			raise ValueError("Invalid YAML mapping entry")

		key = key.strip()
		remainder = remainder.strip()
		index += 1

		if remainder:
			result[key] = parse_scalar(remainder)
			continue

		if index < len(lines) and leading_spaces(lines[index]) > current_indent:
			value, index = parse_block(lines, index, leading_spaces(lines[index]))
			result[key] = value
			continue

		result[key] = None

	return result, index


def parse_list(lines: list[str], start_index: int, indent: int) -> tuple[list[Any], int]:
	result: list[Any] = []
	index = start_index

	while index < len(lines):
		line = lines[index]
		current_indent = leading_spaces(line)
		if current_indent < indent:
			break
		if current_indent != indent:
			raise ValueError("Invalid YAML indentation")

		stripped = line.strip()
		if not stripped.startswith("- "):
			break

		item_text = stripped[2:].strip()
		index += 1

		if item_text:
			result.append(parse_scalar(item_text))
			continue

		if index < len(lines) and leading_spaces(lines[index]) > current_indent:
			value, index = parse_block(lines, index, leading_spaces(lines[index]))
			result.append(value)
			continue

		result.append(None)

	return result, index


def leading_spaces(line: str) -> int:
	return len(line) - len(line.lstrip(" "))


def parse_scalar(value: str) -> Any:
	if value in {"true", "True"}:
		return True
	if value in {"false", "False"}:
		return False
	if value in {"null", "Null", "none", "None", "~"}:
		return None
	if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
		return value[1:-1]

	number = parse_number(value)
	if number is not None:
		return number

	return value


def parse_number(value: str) -> int | float | None:
	try:
		return int(value)
	except ValueError:
		pass

	try:
		return float(value)
	except ValueError:
		return None
