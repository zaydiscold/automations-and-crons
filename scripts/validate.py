#!/usr/bin/env python3
"""Validate automation/cron contracts and reject likely private runtime material."""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

REQUIRED = {
    "schema_version",
    "id",
    "title",
    "domain",
    "enabled",
    "schedule",
    "runtime",
    "inputs",
    "outputs",
    "output_format",
    "risk",
    "verification",
    "logging",
    "failure_policy",
    "secrets_policy",
    "limitations",
    "copying",
}
RISKY = {"account-write", "auth-write", "filesystem-write", "monitoring-write"}
FORBIDDEN = {
    "live job id": re.compile(
        r'(?i)"job_id"\s*:|"id"\s*:\s*"[0-9a-f]{12}"|\b[0-9a-f]{12}\b'
    ),
    "telegram/chat id": re.compile(
        r"(?i)telegram:\d{6,}|chat[_ -]?id\s*[:=]\s*\d{6,}"
    ),
    "personal windows path": re.compile(r"(?i)[a-z]:\\users\\[^\\\s]+"),
    "tailscale ip": re.compile(r"\b100\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
    "token material": re.compile(
        r"(?i)gh[oprsu]_[a-z0-9]{20,}|bearer\s+[a-z0-9._-]{20,}|session-token="
    ),
}
SCAN_EXCLUDES = {Path("scripts/validate.py"), Path("tests/test_validate.py")}


def validate_spec(path: Path, data: dict) -> list[str]:
    issues: list[str] = []
    missing = sorted(REQUIRED - set(data))
    if missing:
        issues.append(f"{path}: missing {missing}")

    if data.get("schema_version") != 2:
        issues.append(f"{path}: schema_version must be 2")

    cron = (data.get("schedule") or {}).get("cron", "")
    if len(cron.split()) != 5:
        issues.append(f"{path}: cron must have five fields")
    if (data.get("schedule") or {}).get("timezone") != "America/Los_Angeles":
        issues.append(f"{path}: timezone must be explicit")
    if not data.get("verification"):
        issues.append(f"{path}: verification is empty")

    runtime = data.get("runtime") or {}
    uses_llm = runtime.get("uses_llm")
    attached = runtime.get("model_attached")
    model = runtime.get("model")
    if uses_llm is True:
        if attached is not True or not isinstance(model, dict):
            issues.append(f"{path}: model-backed runtime lacks attached model metadata")
        else:
            required_model = {"provider", "name", "reasoning", "fallback_policy", "fallbacks"}
            absent = sorted(required_model - set(model))
            if absent:
                issues.append(f"{path}: model metadata missing {absent}")
            if not model.get("fallbacks"):
                issues.append(f"{path}: model-backed runtime lacks fallbacks")
    elif uses_llm is False:
        if attached is not False or model is not None:
            issues.append(f"{path}: no-agent runtime must declare model_attached=false and model=null")
    else:
        issues.append(f"{path}: runtime.uses_llm must be boolean")

    output_format = data.get("output_format") or {}
    template = output_format.get("template")
    if not template or not (path.parent / template).is_file():
        issues.append(f"{path}: output template is missing")
    if output_format.get("exact_contract") is not True:
        issues.append(f"{path}: output format must declare exact_contract=true")

    copying = data.get("copying") or {}
    if copying.get("ready_to_run") is not False or not copying.get("requires"):
        issues.append(f"{path}: copying limitations must say ready_to_run=false and list requirements")
    if not data.get("limitations"):
        issues.append(f"{path}: limitations are empty")

    risk = data.get("risk") or {}
    if risk.get("level") in RISKY and not risk.get("confirmation"):
        issues.append(f"{path}: risky workflow lacks confirmation boundary")
    if (data.get("failure_policy") or {}).get("never_infer_success") is not True:
        issues.append(f"{path}: must never infer success")
    if (data.get("logging") or {}).get("business_verification_required") is not True:
        issues.append(f"{path}: scheduler status cannot be business proof")
    return issues


def validate(root: Path) -> list[str]:
    issues: list[str] = []
    ids: set[str] = set()
    specs = sorted((root / "workflows").glob("**/job.json"))

    for path in specs:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            issues.append(f"{path}: invalid JSON: {exc}")
            continue
        issues.extend(validate_spec(path, data))
        identifier = data.get("id")
        if identifier in ids:
            issues.append(f"{path}: duplicate id {identifier}")
        ids.add(identifier)

    matrix = root / "matrix.csv"
    if matrix.exists():
        with matrix.open(encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    else:
        rows = []
    if {row.get("automation") for row in rows} != ids:
        issues.append("matrix.csv workflow set does not match specs")

    for path in root.rglob("*"):
        if (
            not path.is_file()
            or ".git" in path.parts
            or "__pycache__" in path.parts
            or path.suffix == ".pyc"
            or path.name == "LICENSE"
        ):
            continue
        relative = path.relative_to(root)
        if relative in SCAN_EXCLUDES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in FORBIDDEN.items():
            if pattern.search(text):
                issues.append(f"{relative}: forbidden {label}")

    return sorted(set(issues))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    issues = validate(args.root)
    print(
        json.dumps(
            {
                "ok": not issues,
                "specs": len(list((args.root / "workflows").glob("**/job.json"))),
                "issues": issues,
            },
            indent=2,
        )
    )
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
