"""Run the README's lightweight checks and keep their genuine console logs."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    directory = ROOT / "submission" / "logs"
    directory.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONUTF8="1")
    outcomes = {}
    commands = [
        ("smoke", ["scripts/verify_lite.py"]),
        ("generate_data", ["scripts/generate_data_lite.py"]),
        ("generate_ai_data", ["scripts/generate_ai_data.py"]),
        ("pytest", ["-m", "pytest"]),
        ("run_all", ["scripts/run_all.py"]),
    ]
    for name, args in commands:
        print(f"Running {name} ...", flush=True)
        start = time.perf_counter()
        proc = subprocess.run([sys.executable, *args], cwd=ROOT, env=env,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, encoding="utf-8")
        (directory / f"{name}.txt").write_text(proc.stdout, encoding="utf-8")
        print(proc.stdout, flush=True)
        outcomes[name] = dict(command=[sys.executable, *args], exit_code=proc.returncode,
                              elapsed_seconds=time.perf_counter()-start)
        (directory / "validation.json").write_text(json.dumps(
            dict(executed_at=datetime.now(ZoneInfo("Asia/Bangkok")).isoformat(timespec="seconds"),
                 checks=outcomes), ensure_ascii=False, indent=2), encoding="utf-8")
        if proc.returncode:
            return proc.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
