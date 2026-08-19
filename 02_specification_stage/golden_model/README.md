# PRJ-004 EVCore-MY — Metering Accuracy Golden Model

*02_specification_stage/golden_model | 2026-08-19 | REQ-039 / REQ-055*

Double-precision reference model for the on-chip metering DSP (MOD-06). The
DSP's fixed-point output is compared against these golden values at
verification time; the difference is the DSP error budget (REQ-038/039).

## What it computes

Generates ideal CT/voltage waveforms (50 Hz, 230 V nominal) — fundamental plus
3rd/5th/7th harmonics with deterministic phases — over 16 integer line cycles
at 1024 samples/cycle, then computes in IEEE-754 double precision:

- Vrms, Irms (exact RMS over integer cycles)
- Active power P, apparent power S, reactive power Q (= √(S²−P²)) and
  fundamental reactive Q1 (Budeanu-style)
- Power factor PF = P/S
- THD_v / THD_i via DFT at harmonic bins (self-validated: computed THD matches
  target THD to <1e-6)
- Energy: Wh over the sampled window and kWh over a 1-hour projection

## Sweep grid (64 scenarios)

| Axis | Values |
|---|---|
| Power factor | 1.00, 0.95, 0.85, 0.50 (inductive lag) |
| Load (Irms) | 1.0, 8.0, 16.0, 32.0 A |
| THD (V and I) | 0%, 5%, 10%, 20% |

## Files

| File | Purpose |
|---|---|
| `golden_model.py` | The model (self-test + sweep + JSON output). Pure Python 3 stdlib. |
| `run_determinism.sh [N]` | Determinism harness: N distinct seeds (default 3) → per-run logs (PID+timestamp) + `determinism.json` |
| `golden_out_seed<SEED>.json` | Per-run outputs (identical `tests` content across seeds) |
| `run_log_seed<SEED>_<PID>.txt` | Run evidence: PID + timestamps + tests MD5 per run |
| `determinism.json` | Verdict: `identical: true`, per-run hashes, harness PID/timestamp |

## Determinism contract (audit 1.10 / F14)

- The model is **RNG-free**: waveforms are closed-form math, so any `--seed`
  produces byte-identical `tests` output. The seed is recorded in `_metadata`
  only.
- The determinism hash covers the `tests` array ONLY (`json.dumps(tests,
  sort_keys=True)` MD5); `_metadata` (pid, timestamp, seed, hostname) is
  **excluded**, so runs with different seeds remain comparable.
- Every run writes a log containing the model PID, run timestamps, and the
  tests MD5 — non-forgeable evidence that the outputs were actually produced.

## Usage

```bash
python3 golden_model.py --seed 42 --out golden_out_seed42.json   # single run
./run_determinism.sh 3                                           # determinism proof
```

## Self-test

`golden_model.py` refuses to emit output unless all 11 self-tests pass:
Vrms/Irms nominal at THD=0, P = V·I at PF=1, Q = 0, P = V·I·0.5 and
Q1 = V·I·sin(acos(0.5)) at PF=0.5, S = V·I, computed THD == target.

## Result (this run, 2026-08-19)

- 64 scenarios, all 11 self-tests PASS
- determinism: `identical: true`, 3/3 runs, tests MD5
  `b35ac2cbe14b8a9055aa978a4fc23c27` (seeds 42/123/999)
- Cross-checks: PF=1 → P = 1840.0000 W at 8 A; PF=0.5, 16 A → P = 1840.0000 W,
  Q1 = 3186.9735 var; THD=20% → Vrms = 230·√1.04 = 234.5549 V — all consistent.

## Consumption contract (verification stage)

The metering DSP testbench (MOD-06) shall:
1. Feed the same scenario parameters (V_nom, I_nom, PF, THD, f=50 Hz) into the
   DSP's stimulus generator (external-ADC bitstream/word driver, see
   `04_blackbox_register.md` §5),
2. Run the DSP fixed-point datapath,
3. Compare DSP outputs against `values` in `golden_out_seed42.json` (or
   regenerate with any seed — output is seed-invariant),
4. Report per-scenario ppm error; spec targets (REQ-039): Vrms/Irms ≤ ±0.5%,
   P ≤ ±0.8%, Q ≤ ±1.5%, Wh ≤ ±1.0% over the full sweep grid.
