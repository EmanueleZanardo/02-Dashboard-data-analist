#!/usr/bin/env python3
"""Esegue TUTTA la suite test del repo e aggrega i risultati.

- File pytest-style (test_*.py senza SystemExit): via pytest.
- File legacy QA standalone: eseguiti come script, parsing di
  "checks: N, fails: M" / "N check / M fail" dallo stdout.

Uso:  python3 tests/run_all.py   (dalla root del repo)
Esce con codice 1 se c'e' almeno un fallimento.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS = Path(__file__).resolve().parent


def is_legacy(path: Path) -> bool:
    src = path.read_text(encoding="utf-8")
    return "raise SystemExit" in src or "\nsys.exit(" in src


def main() -> int:
    files = sorted(TESTS.glob("test_*.py"))
    legacy = [f for f in files if is_legacy(f)]
    modern = [f for f in files if not is_legacy(f)]

    tot_checks = tot_fails = 0
    problems = []

    # --- legacy standalone ---
    for f in legacy:
        r = subprocess.run([sys.executable, str(f)], cwd=ROOT,
                           capture_output=True, text=True, timeout=600)
        out = r.stdout + r.stderr
        m = re.search(r"checks:\s*(\d+),\s*fails:\s*(\d+)", out)
        if not m:
            m = re.search(r"(\d+)\s+check\s*/\s*(\d+)\s*fail", out)
        if not m and re.search(r"FAILURES:\s*none", out, re.IGNORECASE):
            # stile legacy alternativo: riepilogo "FAILURES: none",
            # i check si contano dalle righe PASS
            c, fl = len(re.findall(r"(?m)^PASS\b", out)), 0
        elif m:
            c, fl = int(m.group(1)), int(m.group(2))
        else:
            c = fl = None
        if c is not None:
            tot_checks += c
            tot_fails += fl
            stato = "OK " if fl == 0 and r.returncode == 0 else "FAIL"
            print(f"[{stato}] {f.name}: {c} check, {fl} fail")
            if fl or r.returncode != 0:
                problems.append(f.name)
        else:
            print(f"[FAIL] {f.name}: output non parsabile (rc={r.returncode})")
            print(out[-2000:])
            problems.append(f.name)

    # --- pytest-style ---
    if modern:
        r = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--no-header",
             "-p", "no:cacheprovider"]
            + [str(f) for f in modern],
            cwd=ROOT, capture_output=True, text=True, timeout=900)
        print(r.stdout[-3000:])
        m = re.search(r"(\d+)\s+passed", r.stdout)
        passed = int(m.group(1)) if m else 0
        m = re.search(r"(\d+)\s+failed", r.stdout)
        failed = int(m.group(1)) if m else 0
        tot_checks += passed + failed
        tot_fails += failed
        if r.returncode != 0 or failed:
            problems.append("pytest-style")

    print(f"\nTOTALE: {tot_checks} check, {tot_fails} fail")
    if problems:
        print("PROBLEMI:", ", ".join(problems))
        return 1
    print("TUTTI VERDI")
    return 0


if __name__ == "__main__":
    sys.exit(main())
