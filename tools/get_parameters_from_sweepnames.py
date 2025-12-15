#!/usr/bin/env python3
"""
Parse sweep folder/file tags like:
2500_Ohd_9p1e-5_Ohf_10_Ohe_5p0e-3_rho_d_1p2e-3_rho_f_0p9_rho_e_1_s1_0p67_s2_0p33_hf_0p03_Ldomain_3_delta_0p01

and write a CSV with columns:
id, Ohd, Ohf, Ohe, rho_d, rho_f, rho_e, s1, s2, hf, Ldomain, delta
"""

from __future__ import annotations
import argparse
import csv
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


KEYS = ["Ohd", "Ohf", "Ohe", "rho_d", "rho_f", "rho_e", "s1", "s2", "hf", "Ldomain", "delta"]


def p_to_float(s: str) -> float:
    """
    Convert tokens where '.' was replaced by 'p' in the mantissa.
    Examples:
      9p1e-5  -> 9.1e-5
      0p03    -> 0.03
      1p2e-3  -> 1.2e-3
      0p9     -> 0.9
      3       -> 3.0
    """
    s2 = s.replace("p", ".")
    try:
        return float(s2)
    except ValueError as e:
        raise ValueError(f"Could not parse numeric token '{s}' (as '{s2}')") from e


def parse_line(line: str) -> Dict[str, object]:
    """
    Parse one tag line into a dict.
    Assumes the first token is the run id.
    """
    line = line.strip()
    if not line or line.startswith("#"):
        return {}

    parts = line.split("_")
    if len(parts) < 3:
        raise ValueError(f"Line too short to parse: {line}")

    run_id = parts[0]
    out: Dict[str, object] = {"id": int(run_id) if run_id.isdigit() else run_id, "raw": line}

    i = 1
    while i < len(parts):
        tok = parts[i]

        # Handle keys that appear as two tokens: rho_d, rho_f, rho_e
        if tok == "rho" and i + 1 < len(parts):
            sub = parts[i + 1]  # d/f/e
            key = f"rho_{sub}"
            if key not in KEYS:
                # Unknown rho_* variant, skip safely
                i += 1
                continue
            if i + 2 >= len(parts):
                raise ValueError(f"Missing value after {key} in line: {line}")
            val_tok = parts[i + 2]
            out[key] = p_to_float(val_tok)
            i += 3
            continue

        # Normal single-token keys: Ohd, Ohf, Ohe, s1, s2, hf, Ldomain, delta
        if tok in KEYS:
            if i + 1 >= len(parts):
                raise ValueError(f"Missing value after {tok} in line: {line}")
            val_tok = parts[i + 1]
            out[tok] = p_to_float(val_tok)
            i += 2
            continue

        # If token is not a key, move on
        i += 1

    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_txt", type=Path, help="Text file containing one tag per line")
    ap.add_argument("-o", "--output_csv", type=Path, default=Path("sweep_params.csv"))
    args = ap.parse_args()

    if not args.input_txt.exists():
        raise SystemExit(f"Input file not found: {args.input_txt}")

    rows: List[Dict[str, object]] = []
    with args.input_txt.open("r", encoding="utf-8") as f:
        for ln, line in enumerate(f, start=1):
            try:
                d = parse_line(line)
                if d:
                    rows.append(d)
            except Exception as e:
                raise SystemExit(f"Error parsing line {ln}: {line.strip()}\n{e}") from e

    # Ensure consistent column order
    fieldnames = ["id"] + KEYS + ["raw"]

    # Fill missing keys with empty string to keep CSV rectangular
    for r in rows:
        for k in KEYS:
            r.setdefault(k, "")
        r.setdefault("raw", "")

    with args.output_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.output_csv}")


if __name__ == "__main__":
    main()
