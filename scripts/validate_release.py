#!/usr/bin/env python3
"""Validate the publishable skill package using only the standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
CASES = ROOT / "tests" / "behavior-cases.json"
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py"}


def main() -> int:
    errors: list[str] = []
    try:
        skill_text = SKILL.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, ensure_ascii=False))
        return 1

    frontmatter = re.match(r"\A---\s*\n(.*?)\n---\s*\n", skill_text, re.DOTALL)
    if not frontmatter:
        errors.append("SKILL.md must start with closed YAML front matter")
    else:
        header = frontmatter.group(1)
        if not re.search(r"(?m)^name:\s*job-application-assistant\s*$", header):
            errors.append("SKILL.md name must be job-application-assistant")
        if not re.search(r"(?m)^description:\s*\S", header):
            errors.append("SKILL.md must have a non-empty description")

    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", skill_text):
        if "://" in target or target.startswith(("#", "mailto:")):
            continue
        path = (ROOT / target).resolve()
        try:
            path.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"Reference escapes repository: {target}")
            continue
        if not path.is_file():
            errors.append(f"Missing referenced file: {target}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            errors.append(f"File is not valid UTF-8: {path.relative_to(ROOT)}")
            continue
        placeholder = "TO" + "DO"
        if f"[{placeholder}" in text or f"{placeholder}:" in text:
            errors.append(f"Unfinished scaffold placeholder in {path.relative_to(ROOT)}")
        if re.search(r"[A-Za-z]:\\Users\\[^\\]+", text):
            errors.append(f"Absolute user path in {path.relative_to(ROOT)}")

    try:
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        cases = payload.get("cases", [])
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid behavior cases: {exc}")
        cases = []

    required_ids = {
        "entry-level-backend", "portfolio-without-employment", "senior-data-engineer",
        "nontechnical-product-operations", "regulated-role", "unrealistic-deadline",
        "contradictory-answers", "early-stop", "privacy-redaction", "reassessment-update",
    }
    case_ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(cases) < 8:
        errors.append("At least eight behavior cases are required")
    if len(case_ids) != len(set(case_ids)):
        errors.append("Behavior case IDs must be unique")
    missing_ids = sorted(required_ids - set(case_ids))
    if missing_ids:
        errors.append(f"Missing required behavior cases: {', '.join(missing_ids)}")

    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            errors.append(f"Behavior case {index} must be an object")
            continue
        for key in ("id", "title", "prompt"):
            if not isinstance(case.get(key), str) or not case[key].strip():
                errors.append(f"Behavior case {index} has invalid {key}")
        for key in ("expected", "forbidden"):
            values = case.get(key)
            if not isinstance(values, list) or not values or not all(
                isinstance(value, str) and value.strip() for value in values
            ):
                errors.append(f"Behavior case {index} has invalid {key}")

    result = {"valid": not errors, "behavior_cases": len(cases), "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
