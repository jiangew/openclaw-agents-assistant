#!/usr/bin/env python3
import csv
import re
import sys
from pathlib import Path

def read_spec_version(spec_path: Path) -> str:
    text = spec_path.read_text(encoding="utf-8")
    m = re.search(r"^Version:\s*([0-9]+\.[0-9]+)\s*$", text, re.M)
    if not m:
        raise ValueError("Spec version not found in OUTPUT_SPEC.md")
    return m.group(1)

def validate_x_feed(path: Path, spec_version: str):
    errors = []
    if not path.exists():
        errors.append(f"missing: {path}")
        return errors

    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        errors.append("x_feed.txt is empty")
        return errors

    meta_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "# Meta":
            meta_idx = i
            break
    if meta_idx is None:
        errors.append("x_feed.txt missing # Meta block")
        return errors

    # Validate content lines before # Meta
    pattern = re.compile(r"^\[(\d{4}-\d{2}-\d{2})\] (INSIGHT|ALERT|BULLISH|BEARISH|NEUTRAL): .+ \(source: .+\)$")
    for i, line in enumerate(lines[:meta_idx]):
        if not line.strip():
            continue
        if not pattern.match(line):
            errors.append(f"x_feed.txt line {i+1} format invalid: {line}")
        if "(source: NA)" in line:
            errors.append(f"x_feed.txt line {i+1} source is NA")

    # Validate spec_version in Meta
    meta_lines = lines[meta_idx + 1 :]
    spec_line = None
    for line in meta_lines:
        if line.strip().startswith("- spec_version:"):
            spec_line = line.strip()
            break
    if spec_line is None:
        errors.append("x_feed.txt Meta missing spec_version")
    else:
        if spec_line != f"- spec_version: {spec_version}":
            errors.append(f"x_feed.txt spec_version mismatch: {spec_line}")

    return errors

def validate_polymarket(path: Path, spec_version: str):
    errors = []
    if not path.exists():
        errors.append(f"missing: {path}")
        return errors

    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        errors.append("polymarket.csv is empty")
        return errors

    header = lines[0].strip()
    if header != "rank,title,price,volume,liquidity,expiry,link":
        errors.append("polymarket.csv header mismatch")

    # Find Meta block
    meta_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "# Meta":
            meta_idx = i
            break
    if meta_idx is None:
        errors.append("polymarket.csv missing # Meta block")
        return errors

    # Validate CSV rows before Meta
    csv_lines = lines[1:meta_idx]
    reader = csv.reader(csv_lines)
    for i, row in enumerate(reader, start=2):
        if not row:
            continue
        if len(row) != 7:
            errors.append(f"polymarket.csv line {i} column count != 7")
            continue
        # Basic rank check
        rank = row[0].strip()
        if not rank.isdigit():
            errors.append(f"polymarket.csv line {i} rank not numeric")
        # Require expiry and link not NA
        if row[5].strip().upper() == "NA":
            errors.append(f"polymarket.csv line {i} expiry is NA")
        if row[6].strip().upper() == "NA":
            errors.append(f"polymarket.csv line {i} link is NA")

    # Validate spec_version in Meta
    meta_lines = lines[meta_idx + 1 :]
    spec_line = None
    for line in meta_lines:
        if line.strip().startswith("# spec_version:"):
            spec_line = line.strip()
            break
    if spec_line is None:
        errors.append("polymarket.csv Meta missing spec_version")
    else:
        if spec_line != f"# spec_version: {spec_version}":
            errors.append(f"polymarket.csv spec_version mismatch: {spec_line}")

    return errors

def validate_analysis_report(path: Path, spec_version: str):
    errors = []
    if not path.exists():
        errors.append(f"missing: {path}")
        return errors

    text = path.read_text(encoding="utf-8")
    required_sections = [
        "# Sentiment Analysis Report",
        "## Summary",
        "## Market vs KOL",
        "## Divergences",
        "## Major Coins",
        "## Risks",
        "## Watchlist (24-72h)",
    ]
    for sec in required_sections:
        if sec not in text:
            errors.append(f"analysis_report.md missing section: {sec}")

    if f"Spec: {spec_version}" not in text:
        errors.append("analysis_report.md missing or mismatched Spec line")

    return errors

def main():
    root = Path(__file__).resolve().parent
    spec_path = root / "OUTPUT_SPEC.md"
    try:
        spec_version = read_spec_version(spec_path)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(2)

    errors = []
    errors += validate_x_feed(root / "x_feed.txt", spec_version)
    errors += validate_polymarket(root / "polymarket.csv", spec_version)
    errors += validate_analysis_report(root / "analysis_report.md", spec_version)

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    print("Validation passed")

if __name__ == "__main__":
    main()
