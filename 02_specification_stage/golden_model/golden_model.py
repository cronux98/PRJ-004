#!/usr/bin/env python3
"""
PRJ-004 EVCore-MY — Metering Accuracy Golden Model (double-precision reference).

The accuracy reference for the on-chip metering DSP (MOD-06) at verification
time (REQ-039, REQ-055). Generates ideal CT/voltage waveforms (fundamental +
3rd/5th/7th harmonics), computes reference Vrms / Irms / P / Q / S / PF / THD /
Wh in IEEE-754 double precision, and sweeps:

  * power factor  : PF in {1.00, 0.95, 0.85, 0.50} (inductive lag)
  * load (Irms)   : {1.0, 8.0, 16.0, 32.0} A
  * harmonic THD  : {0.00, 0.05, 0.10, 0.20} (applied to V and I)

Determinism contract (audit rule 1.10 / F14):
  * The model contains NO randomness: waveform generation is closed-form math,
    so any seed produces byte-identical `tests` output.
  * `--seed` is accepted and recorded in `_metadata` only (audit-format
    compatibility; the run_determinism.sh harness runs N distinct seeds and
    verifies identical tests MD5).
  * The determinism MD5 is computed over the `tests` array ONLY — `_metadata`
    (pid, timestamp, seed, hostname) is EXCLUDED from the hash, so runs are
    comparable. See run_determinism.sh.

Usage:
    python3 golden_model.py --seed 42 --out golden_out_seed42.json
    python3 golden_model.py --seed 123 --out golden_out_seed123.json
    # compare: MD5 of tests array must be identical across seeds

Output schema:
    {
      "_metadata": {pid, timestamp_utc, seed, version, hostname, python, cmdline},
      "summary":   {rated, sweep grids, scenario_count, method},
      "tests":     [ {scenario, values, computed_thd, errors_vs_ideal, wh}, ... ]
    }
"""

import argparse
import hashlib
import json
import math
import os
import platform
import sys
import time
from datetime import datetime, timezone

VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Rated / reference conditions (Malaysia 240V nominal -> use 230 V RMS class)
# ---------------------------------------------------------------------------
F_LINE        = 50.0          # Hz
V_NOM_RMS     = 230.0         # V
SAMPLES_CYCLE = 1024          # samples per line cycle (fs = 51.2 kS/s)
N_CYCLES      = 16            # integer number of cycles (exact integration)
HARMONICS     = (3, 5, 7)     # harmonic orders
HARM_WEIGHTS  = (1.0, 0.5, 0.25)  # relative weights (normalised to target THD)
HARM_PHASES   = (0.0, math.pi / 4.0, math.pi / 3.0)  # deterministic phases (rad)

PF_GRID    = (1.00, 0.95, 0.85, 0.50)
LOAD_GRID  = (1.0, 8.0, 16.0, 32.0)     # A (Irms)
THD_GRID   = (0.00, 0.05, 0.10, 0.20)   # total harmonic distortion (fraction)


# ---------------------------------------------------------------------------
# Waveform generation (closed form, no RNG)
# ---------------------------------------------------------------------------
def generate_waveforms(v_rms, i_rms, pf, thd):
    """Return (v, i) sample lists for N_CYCLES at SAMPLES_CYCLE/c.

    Fundamental phase lag phi = acos(PF) (inductive: current lags voltage).
    Harmonic amplitudes are set so that sqrt(sum h_n^2) / fundamental == THD
    exactly (per-channel), with deterministic phases from HARM_PHASES.
    """
    fs = SAMPLES_CYCLE * F_LINE
    n = N_CYCLES * SAMPLES_CYCLE
    w = 2.0 * math.pi * F_LINE
    phi = math.acos(max(-1.0, min(1.0, pf)))

    v_peak = v_rms * math.sqrt(2.0)
    i_peak = i_rms * math.sqrt(2.0)

    # harmonic amplitude weights: sum(amp_n^2) = (thd * fund_peak)^2
    wsum = math.sqrt(sum(wk * wk for wk in HARM_WEIGHTS))
    v_harms = tuple(thd * v_peak * wk / wsum for wk in HARM_WEIGHTS)
    i_harms = tuple(thd * i_peak * wk / wsum for wk in HARM_WEIGHTS)

    v = []
    i = []
    for k in range(n):
        t = k / fs
        vt = v_peak * math.sin(w * t)
        it = i_peak * math.sin(w * t - phi)
        for (h, amp_v, amp_i, ph) in zip(HARMONICS, v_harms, i_harms, HARM_PHASES):
            vt += amp_v * math.sin(h * w * t + ph)
            it += amp_i * math.sin(h * w * t + ph)
        v.append(vt)
        i.append(it)
    return v, i


# ---------------------------------------------------------------------------
# Reference computations (double precision)
# ---------------------------------------------------------------------------
def rms(x):
    n = len(x)
    return math.sqrt(sum(xk * xk for xk in x) / n)


def mean(x):
    x = list(x)
    return sum(x) / len(x)


def dft_harmonic(x, order):
    """Fundamental/harmonic RMS via DFT at `order` (exact for integer cycles).

    The window is N_CYCLES line cycles; harmonic `order` completes
    `order * N_CYCLES` cycles over the window, i.e. its phase advances by
    2*pi*order per SAMPLES_CYCLE samples. Dividing by SAMPLES_CYCLE (not n)
    selects the correct bin.
    """
    n = len(x)
    re, im = 0.0, 0.0
    for k, xk in enumerate(x):
        ang = 2.0 * math.pi * order * k / SAMPLES_CYCLE
        re += xk * math.cos(ang)
        im -= xk * math.sin(ang)
    return math.sqrt(2.0) * math.hypot(re, im) / n  # RMS of component


def reference_values(v, i):
    """Compute all reference metering quantities from sample arrays."""
    vrms = rms(v)
    irms = rms(i)
    p = mean(vk * ik for vk, ik in zip(v, i))          # active power (W)
    s = vrms * irms                                     # apparent power (VA)
    q_s = math.sqrt(max(0.0, s * s - p * p))            # Q from S-P (IEEE app.)
    pf = p / s if s > 0.0 else 0.0

    v1 = dft_harmonic(v, 1)
    i1 = dft_harmonic(i, 1)
    thd_v = math.sqrt(sum(dft_harmonic(v, h) ** 2 for h in HARMONICS)) / v1
    thd_i = math.sqrt(sum(dft_harmonic(i, h) ** 2 for h in HARMONICS)) / i1
    # fundamental reactive power (Budeanu-style fundamental component)
    phi_fund = math.acos(max(-1.0, min(1.0, pf)))
    q1 = v1 * i1 * math.sin(phi_fund)

    # Energy: window energy (Wh over the sampled window) and 1-hour projection
    t_win_s = N_CYCLES / F_LINE
    energy_wh_window = p * t_win_s / 3600.0
    energy_kwh_1h = p * 1.0 / 1000.0

    return {
        "vrms": vrms, "irms": irms,
        "p_w": p, "s_va": s, "q_va": q_s, "q1_var": q1,
        "pf": pf,
        "thd_v": thd_v, "thd_i": thd_i,
        "v1_rms": v1, "i1_rms": i1,
        "energy_wh_window": energy_wh_window,
        "energy_kwh_1h": energy_kwh_1h,
    }


def errors_vs_ideal(vals, v_rms, i_rms, pf, thd):
    """ppm errors of the ideal (zero-error) reference vs the nominal grid."""
    vrms_ppm = (vals["vrms"] - v_rms) / v_rms * 1e6
    irms_ppm = (vals["irms"] - i_rms) / i_rms * 1e6
    p_ideal = v_rms * i_rms * pf
    p_ppm = (vals["p_w"] - p_ideal) / p_ideal * 1e6 if p_ideal else 0.0
    return {
        "vrms_ppm": vrms_ppm, "irms_ppm": irms_ppm, "p_ppm": p_ppm,
        "thd_v_ppm": (vals["thd_v"] - thd) / thd * 1e6 if thd else 0.0,
    }


# ---------------------------------------------------------------------------
# Self-test (every model must prove itself before generating golden output)
# ---------------------------------------------------------------------------
def self_test():
    ok = True

    # 1) THD=0, PF=1: Vrms/Irms must equal nominal, P = V*I, Q = 0
    v, i = generate_waveforms(V_NOM_RMS, 8.0, 1.0, 0.0)
    vals = reference_values(v, i)
    checks = [
        ("Vrms==230", abs(vals["vrms"] - 230.0) < 1e-9),
        ("Irms==8",   abs(vals["irms"] - 8.0) < 1e-9),
        ("P==V*I",    abs(vals["p_w"] - 1840.0) < 1e-6),
        ("Q==0",      abs(vals["q_va"]) < 1e-6),
        ("PF==1",     abs(vals["pf"] - 1.0) < 1e-12),
        ("THD_v==0",  abs(vals["thd_v"]) < 1e-9),
        ("THD_i==0",  abs(vals["thd_i"]) < 1e-9),
    ]
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed

    # 2) PF=0.5 inductive: P = V*I*0.5, Q1 = V1*I1*sin(acos(0.5))
    v, i = generate_waveforms(V_NOM_RMS, 16.0, 0.5, 0.0)
    vals = reference_values(v, i)
    p_exp = 230.0 * 16.0 * 0.5
    q_exp = 230.0 * 16.0 * math.sin(math.acos(0.5))
    checks2 = [
        ("PF=0.5 P",  abs(vals["p_w"] - p_exp) < 1e-6),
        ("PF=0.5 Q1", abs(vals["q1_var"] - q_exp) < 1e-6),
        ("PF=0.5 S",  abs(vals["s_va"] - 3680.0) < 1e-6),
    ]
    for name, passed in checks2:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed

    # 3) THD=0.10: computed THD must equal target to 1e-6
    v, i = generate_waveforms(V_NOM_RMS, 8.0, 0.95, 0.10)
    vals = reference_values(v, i)
    checks3 = [
        ("THD target 10%", abs(vals["thd_v"] - 0.10) < 1e-6 and abs(vals["thd_i"] - 0.10) < 1e-6),
    ]
    for name, passed in checks3:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed

    return ok


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=42, help="audit seed (recorded in _metadata; model is RNG-free)")
    ap.add_argument("--out", default="golden_output.json", help="output JSON path")
    args = ap.parse_args()

    print("=== PRJ-004 EVCore-MY Metering Golden Model v%s ===" % VERSION)
    print(f"seed={args.seed}  python={platform.python_version()}  pid={os.getpid()}")

    print("--- Self-test ---")
    if not self_test():
        print("SELF-TEST FAILED — refusing to generate golden output")
        sys.exit(1)
    print("Self-test PASS")

    # Sweep: PF x load x THD (4x4x4 = 64 scenarios)
    tests = []
    for pf in PF_GRID:
        for load_a in LOAD_GRID:
            for thd in THD_GRID:
                v, i = generate_waveforms(V_NOM_RMS, load_a, pf, thd)
                vals = reference_values(v, i)
                tests.append({
                    "scenario": {
                        "v_nom_rms": V_NOM_RMS, "i_nom_rms": load_a,
                        "pf_target": pf, "thd_target": thd,
                        "f_line_hz": F_LINE, "cycles": N_CYCLES,
                        "samples_per_cycle": SAMPLES_CYCLE,
                    },
                    "values": {
                        "vrms": vals["vrms"], "irms": vals["irms"],
                        "p_w": vals["p_w"], "s_va": vals["s_va"],
                        "q_va": vals["q_va"], "q1_var": vals["q1_var"],
                        "pf": vals["pf"],
                    },
                    "computed_thd": {"thd_v": vals["thd_v"], "thd_i": vals["thd_i"]},
                    "errors_vs_ideal": errors_vs_ideal(vals, V_NOM_RMS, load_a, pf, thd),
                    "energy": {
                        "wh_window": vals["energy_wh_window"],
                        "kwh_1h": vals["energy_kwh_1h"],
                    },
                })

    data = {
        "_metadata": {
            "project": "PRJ-004", "codename": "EVCore-MY",
            "model": "metering_golden", "version": VERSION,
            "seed": args.seed,
            "pid": os.getpid(),
            "hostname": platform.node(),
            "python": platform.python_version(),
            "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "cmdline": " ".join(sys.argv),
        },
        "summary": {
            "rated": {"v_nom_rms": V_NOM_RMS, "f_line_hz": F_LINE,
                      "samples_per_cycle": SAMPLES_CYCLE, "cycles": N_CYCLES},
            "sweeps": {"pf": list(PF_GRID), "load_a": list(LOAD_GRID),
                       "thd": list(THD_GRID)},
            "scenario_count": len(tests),
            "method": ("Closed-form waveform generation (fundamental + 3rd/5th/7th "
                       "harmonics, deterministic phases); reference quantities in "
                       "IEEE-754 double precision over integer line cycles; "
                       "no randomness (seed is audit-only)."),
        },
        "tests": tests,
    }

    # Self-referential-hash safety (audit 1.10): hash computed over the tests
    # array ONLY; _metadata (pid/timestamp/seed/hostname) is EXCLUDED so that
    # runs with different seeds/timestamps remain byte-comparable.
    tests_md5 = hashlib.md5(
        json.dumps(data["tests"], sort_keys=True).encode("utf-8")
    ).hexdigest()
    data["_metadata"]["tests_md5"] = tests_md5

    with open(args.out, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")

    print(f"--- Output ---")
    print(f"scenarios: {len(tests)}  tests_md5: {tests_md5}")
    print(f"wrote: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
