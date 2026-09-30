#!/usr/bin/env python3
"""Verify the BeanRunner Python entry point for milestone 1."""

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
def main() -> int:
    result = subprocess.run(
        [sys.executable, "-m", "src.main"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    expected_output = (
        "[BeanRunner] Servicio JobRunner inicializado correctamente.\n"
    )

    if result.returncode != 0:
        print(f"[FAIL] BeanRunner terminó con código {result.returncode}.")
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        return 1

    if result.stdout != expected_output:
        print("[FAIL] La salida de inicio no coincide con la esperada.")
        print(result.stdout, end="")
        return 1

    if result.stderr:
        print("[FAIL] BeanRunner produjo salida inesperada en stderr.")
        print(result.stderr, file=sys.stderr, end="")
        return 1

    print("[PASS] El punto de entrada Python inició correctamente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
