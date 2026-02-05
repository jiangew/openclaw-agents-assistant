#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def main():
    root = Path(__file__).resolve().parent
    report_path = root / "quality_gate_report.md"
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    proc = subprocess.run([str(root / "validate_outputs.py")], capture_output=True, text=True)
    status = "PASS" if proc.returncode == 0 else "FAIL"

    report_lines = [
        "# Output Quality Gate Report",
        f"Time: {ts}",
        f"Status: {status}",
        "",
        "## validate_outputs.py output",
        "```",
        (proc.stdout.strip() or proc.stderr.strip() or "(no output)"),
        "```",
    ]
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    if proc.returncode != 0:
        print("Quality gate failed. See quality_gate_report.md")
        sys.exit(1)

    print("Quality gate passed")

if __name__ == "__main__":
    main()
