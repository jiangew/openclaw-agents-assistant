#!/usr/bin/env python3
import csv
import re
from pathlib import Path
from datetime import datetime

def ensure_x_feed(path: Path, spec_version: str):
    if not path.exists():
        return ["x_feed.txt missing"], False

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Add source if missing
    fixed_lines = []
    changed = False
    for line in lines:
        if line.strip().startswith("[") and "(source:" not in line:
            fixed_lines.append(f"{line} (source: NA)")
            changed = True
        else:
            fixed_lines.append(line)

    # Ensure Meta block
    if "# Meta" not in fixed_lines:
        fixed_lines.append("")
        fixed_lines.append("# Meta")
        fixed_lines.append(f"- spec_version: {spec_version}")
        fixed_lines.append(f"- time_range: NA")
        fixed_lines.append("- kols: NA")
        fixed_lines.append("- filters: NA")
        fixed_lines.append("- duplicates_removed: NA")
        fixed_lines.append("- failures: auto-repair added missing source URLs")
        changed = True
    else:
        # Ensure spec_version line exists
        if not any(l.strip().startswith("- spec_version:") for l in fixed_lines):
            idx = fixed_lines.index("# Meta")
            fixed_lines.insert(idx + 1, f"- spec_version: {spec_version}")
            changed = True

    if changed:
        path.write_text("\n".join(fixed_lines) + "\n", encoding="utf-8")

    return [], changed

def convert_polymarket_legacy(path: Path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines:
        return None
    header = lines[0].strip()
    if header == "Market Title,Volume (USD),Liquidity (USD)":
        rows = []
        for i, row in enumerate(lines[1:], start=1):
            if not row.strip():
                continue
            parts = list(csv.reader([row]))[0]
            if len(parts) != 3:
                continue
            title, volume, liquidity = parts
            rows.append([str(i), title, "NA", volume, liquidity, "NA", "NA"])
        return rows
    return None

def ensure_polymarket(path: Path, spec_version: str):
    if not path.exists():
        return ["polymarket.csv missing"], False

    changed = False
    converted = convert_polymarket_legacy(path)
    if converted is not None:
        out_lines = ["rank,title,price,volume,liquidity,expiry,link"]
        out_lines += [
            ",".join([
                row[0],
                f"\"{row[1].replace('"', '""')}\"",
                row[2], row[3], row[4], row[5], row[6]
            ])
            for row in converted
        ]
        out_lines.append("# Meta")
        out_lines.append(f"# spec_version: {spec_version}")
        out_lines.append("# time_range: NA")
        out_lines.append("# scope: Crypto")
        out_lines.append("# sort: NA")
        out_lines.append(f"# total_rows: {len(converted)}")
        out_lines.append("# failures: auto-repair converted legacy format")
        path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        return [], True

    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        return ["polymarket.csv empty"], False

    if lines[0].strip() != "rank,title,price,volume,liquidity,expiry,link":
        # Cannot safely fix unknown header
        return ["polymarket.csv header mismatch"], False

    if "# Meta" not in lines:
        lines.append("# Meta")
        lines.append(f"# spec_version: {spec_version}")
        lines.append("# time_range: NA")
        lines.append("# scope: Crypto")
        lines.append("# sort: NA")
        lines.append("# total_rows: NA")
        lines.append("# failures: auto-repair added Meta")
        changed = True
    else:
        if not any(l.strip().startswith("# spec_version:") for l in lines):
            idx = lines.index("# Meta")
            lines.insert(idx + 1, f"# spec_version: {spec_version}")
            changed = True

    if changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return [], changed

def ensure_analysis_report(path: Path, spec_version: str):
    if not path.exists():
        return ["analysis_report.md missing"], False

    text = path.read_text(encoding="utf-8")
    required = [
        "# Sentiment Analysis Report",
        "## Summary",
        "## Market vs KOL",
        "## Divergences",
        "## Major Coins",
        "## Risks",
        "## Watchlist (24-72h)",
    ]
    changed = False
    if all(r in text for r in required) and f"Spec: {spec_version}" in text:
        return [], False

    # Auto-repair by wrapping legacy content
    ts = datetime.utcnow().strftime("%Y-%m-%d")
    repaired = [
        "# Sentiment Analysis Report",
        f"Date: {ts}",
        "Data Window: NA",
        "Sources: polymarket.csv, x_feed.txt",
        f"Spec: {spec_version}",
        "",
        "## Summary",
        "- AUTO-REPAIR: legacy report did not match spec; see Appendix.",
        "",
        "## Market vs KOL",
        "- Market: NA",
        "- KOL: NA",
        "- Evidence: NA",
        "",
        "## Divergences",
        "- NA",
        "",
        "## Major Coins",
        "- BTC: NA",
        "- ETH: NA",
        "- Stablecoins: NA",
        "",
        "## Risks",
        "- NA",
        "",
        "## Watchlist (24-72h)",
        "- NA",
        "",
        "## Appendix: Legacy Report",
        "```",
        text.strip(),
        "```",
    ]
    path.write_text("\n".join(repaired) + "\n", encoding="utf-8")
    changed = True

    return [], changed

def read_spec_version(spec_path: Path) -> str:
    text = spec_path.read_text(encoding="utf-8")
    m = re.search(r"^Version:\s*([0-9]+\.[0-9]+)\s*$", text, re.M)
    if not m:
        raise ValueError("Spec version not found in OUTPUT_SPEC.md")
    return m.group(1)

def main():
    root = Path(__file__).resolve().parent
    spec_version = read_spec_version(root / "OUTPUT_SPEC.md")

    ensure_x_feed(root / "x_feed.txt", spec_version)
    ensure_polymarket(root / "polymarket.csv", spec_version)
    ensure_analysis_report(root / "analysis_report.md", spec_version)

if __name__ == "__main__":
    main()
