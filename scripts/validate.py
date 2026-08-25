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
    for key in ("inputs", "outputs", "verification"):
        values = data.get(key)
        if not isinstance(values, list) or not values or not all(
            isinstance(item, str) and item.strip() for item in values
        ):
            issues.append(f"{path}: {key} must be a nonempty list of nonempty strings")

    runtime = data.get("runtime") or {}
    for key in ("scheduler", "execution_mode", "kind"):
        if not isinstance(runtime.get(key), str) or not runtime[key].strip():
            issues.append(f"{path}: runtime.{key} must be a nonempty string")
    if runtime.get("execution_mode") not in {"agent", "script/no-agent"}:
        issues.append(f"{path}: runtime.execution_mode is invalid")
    if runtime.get("kind") not in {"agent", "script"}:
        issues.append(f"{path}: runtime.kind is invalid")
    portable_to = runtime.get("portable_to")
    if not isinstance(portable_to, list) or not portable_to or not all(
        isinstance(item, str) and item.strip() for item in portable_to
    ):
        issues.append(f"{path}: runtime.portable_to must contain nonempty strings")
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
            for key in ("provider", "name", "reasoning", "fallback_policy"):
                if not isinstance(model.get(key), str) or not model[key].strip():
                    issues.append(f"{path}: model.{key} must be a nonempty string")
            fallbacks = model.get("fallbacks")
            if not isinstance(fallbacks, list) or not fallbacks:
                issues.append(f"{path}: model-backed runtime lacks fallbacks")
            elif not all(
                isinstance(item, dict)
                and isinstance(item.get("provider"), str)
                and item["provider"].strip()
                and isinstance(item.get("model"), str)
                and item["model"].strip()
                for item in fallbacks
            ):
                issues.append(f"{path}: every fallback needs nonempty provider/model strings")
    elif uses_llm is False:
        if attached is not False or model is not None:
            issues.append(f"{path}: no-agent runtime must declare model_attached=false and model=null")
    else:
        issues.append(f"{path}: runtime.uses_llm must be boolean")

    output_format = data.get("output_format") or {}
    if not isinstance(output_format.get("delivery"), str) or not output_format["delivery"].strip():
        issues.append(f"{path}: output_format.delivery must be a nonempty string")
    template = output_format.get("template")
    if not template or not (path.parent / template).is_file():
        issues.append(f"{path}: output template is missing")
    if output_format.get("exact_contract") is not True:
        issues.append(f"{path}: output format must declare exact_contract=true")
    expected_always_reports = (data.get("failure_policy") or {}).get("deliver_every_run") is True
    if output_format.get("always_reports") != expected_always_reports:
        issues.append(f"{path}: output_format.always_reports disagrees with failure policy")

    copying = data.get("copying") or {}
    requires = copying.get("requires")
    if copying.get("ready_to_run") is not False or not requires:
        issues.append(f"{path}: copying limitations must say ready_to_run=false and list requirements")
    if not isinstance(requires, list) or not all(
        isinstance(item, str) and item.strip() for item in requires
    ):
        issues.append(f"{path}: copying.requires must contain nonempty strings")
    limitations = data.get("limitations")
    if not limitations:
        issues.append(f"{path}: limitations are empty")
    elif not isinstance(limitations, list) or not all(
        isinstance(item, str) and item.strip() for item in limitations
    ):
        issues.append(f"{path}: limitations must contain nonempty strings")

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
