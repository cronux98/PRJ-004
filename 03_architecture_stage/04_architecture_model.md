# EVCore-MY — MOD-06 Metering DSP: Golden-Model Comparison Contract
## PRJ-004 / v0 / 03_architecture_stage / 04_architecture_model.md

*Version 1.0 | 2026-08-19 | Architecture stage — derived from `01_ARCHITECTURE.md` §8.6 (MOD-06),
`02_specification_stage/01_system_spec.md` §9 (REQ-036…REQ-040) and §14 (REQ-055), and
`02_specification_stage/golden_model/` (`golden_model.py`, `README.md`,
`golden_out_seed42.json`).*

---

## 0. Purpose & Scope

This document is the **architecture-stage contract** between the metering golden model
(`02_specification_stage/golden_model/golden_model.py`) and the RTL verification that
will exist for MOD-06 at `04_frontend_stage` / `06_verification_stage`. It defines:

- the RTL-visible interface (signals, widths, Q-format) that carries golden-model-comparable
  quantities off the DSP,
- the exact output structure of the golden model's JSON (field-by-field, no paraphrase),
- how each RTL/architecture Q-format result maps onto a golden model field, including the
  fixed-point-to-double conversion,
- the tolerance each field must meet, traced to REQ-039's error budget,
- how the architecture's CIC/sinc decimation + Vrms/Irms/P/Q/S/Wh + calibration pipeline
  (§8.6) maps onto the golden model's 64-scenario sweep, and
- the comparison methodology RTL verification will execute, and its pass/fail criteria.

This is a **contract document**, not a verification pipeline: it does not implement a
testbench, script, or comparison harness. It is the specification that
`04_frontend_stage`/`06_verification_stage` build against. No file other than this one is
written by this task.

---

## 1. Golden Model Recap (as-built, not re-derived)

Per `golden_model.py` and `README.md`:

- Waveform generation: closed-form (no RNG), 50 Hz fundamental + 3rd/5th/7th harmonics,
  deterministic phases, `SAMPLES_CYCLE = 1024` samples/cycle, `N_CYCLES = 16` integer line
  cycles (0.32 s window).
- Sweep grid: PF ∈ {1.00, 0.95, 0.85, 0.50}, Irms ∈ {1.0, 8.0, 16.0, 32.0} A,
  THD ∈ {0.00, 0.05, 0.10, 0.20} → 4×4×4 = **64 scenarios**, `v_nom_rms = 230.0` V fixed.
- All reference quantities computed in IEEE-754 double precision.
- Output: `golden_out_seed<SEED>.json`, byte-identical `tests` array across seeds
  (RNG-free); `tests_md5` recorded in `_metadata`.
- Self-tests: 11 checks (Vrms/Irms nominal at THD=0, P/Q/S/PF identities at PF=1 and
  PF=0.5, THD-target closure) must pass before the model emits output at all.

**Architecture-stage caveat carried from §8.6 (accumulation windows):** the golden model's
`N_CYCLES = 16` (0.32 s) is a reference-model constant chosen for determinism/efficiency,
**not** the hardware's class-window constant. The architecture's class-1/0.5s accumulation
register set uses `METERING_CLASS_WINDOW = 25` cycles (0.5 s, REQ-039). This document treats
the two windows as separate comparison targets (§5) rather than silently reconciling them —
regenerating `golden_model.py` with `N_CYCLES = 25` is the RTL/verification-stage action item
already flagged in `01_ARCHITECTURE.md` §8.6; it is not resolved here.

---

## 2. Interface Contract

### 2.1 Bus-level interface (AHB3-Lite slave S0, `01_ARCHITECTURE.md` §2.3/§3.2)

| Signal | Width | Direction | Role |
|---|---|---|---|
| `haddr` | 32-bit | in | Address into MOD-06's 4 kB AHB window (`0x4000_0000`) |
| `hwrite` | 1-bit | in | 1 = write (config/calib/control), 0 = read (results/status) |
| `hsize` | 3-bit | in | Transfer size (word, per architecture's 32-bit access width) |
| `htrans` | 2-bit | in | `NONSEQ` per transfer (no AHB bursts assumed, single-beat) |
| `hwdata` | 32-bit | in | Write data (calibration regs, control, sample FIFO in test mode) |
| `hrdata` | 32-bit | out | Read data (result/status/FIFO burst reads) |
| `hready` | 1-bit | out | Transfer complete |
| `hresp` | 1-bit | out | `OKAY`/`ERROR` |

Register/FIFO count stays ≤ 8 in-band groups per the §2.1 exception rule (streaming +
control both on AHB, no APB hop). Exact per-register byte offsets within the 4 kB window
are an RTL-stage decision (not fixed here); this contract only fixes the **semantic
content and Q-format** of the result values that verification will read back, so RTL is
free to lay out the register map without breaking the comparison contract below.

### 2.2 Front-end sample interface (§8.6, CDC boundary per §5.3)

| Signal | Width | Domain | Role |
|---|---|---|---|
| `mclk_adc` | 1-bit clock | chip-generated | 2.0 MHz (40 MHz core) / ~1.92 MHz (25 MHz fallback), sent off-chip |
| `dat` | 1-bit | pad-domain → 2FF-synced → async FIFO → `clk_core` | External ΔΣ ADC bitstream input (Option A, 1-bit PDM/ΔΣ) |

This is the stimulus injection point for RTL verification's stimulus generator (§6.1):
the golden model's scenario waveforms are re-expressed as a 1-bit ΔΣ bitstream driven on
`dat`, synchronized to `mclk_adc`.

### 2.3 Q-format contract (architecture decision, `01_ARCHITECTURE.md` §8.6, REQ-038)

| Signal class | Q-format | Width | Golden-model quantity it must compare against |
|---|---|---|---|
| ADC sample, post-CIC pre-scale | Q1.15 | 16-bit signed | intermediate only — not directly compared (pre-calibration) |
| CIC/power accumulators | Q1.31 | 32-bit signed | intermediate only — not directly compared (pre-readback scaling) |
| **Result registers: Vrms, Irms, P, Q, S, Wh** | **Q16.16** | **32-bit signed** | `values.vrms`, `values.irms`, `values.p_w`, `values.q_va`, `values.s_va`, `energy.wh_window` |
| Calibration gain | Q2.14 | 16-bit signed | n/a (config input, not a golden-model output) |
| Calibration phase/offset | Q1.31 | 32-bit signed | n/a (config input, not a golden-model output) |

**Fixed-point-to-double conversion for comparison (architecture-fixed, not left to
verification's discretion):** a Q16.16 result register value `r` (32-bit signed
two's-complement) converts to its physical double value as `r / 65536.0`. Verification
must apply exactly this conversion before computing error against the golden model — do
not re-derive a different scale factor per field.

---

## 3. Golden Model Output Structure (exact contract, `golden_out_seed<SEED>.json`)

Top level:

```
{
  "_metadata": { pid, timestamp_utc, seed, version, hostname, python, cmdline, tests_md5 },
  "summary":   { rated: {v_nom_rms, f_line_hz, samples_per_cycle, cycles},
                 sweeps: {pf: [...], load_a: [...], thd: [...]},
                 scenario_count: 64, method: "..." },
  "tests":     [ <64 scenario objects> ]
}
```

Each element of `tests[]` (this is the object RTL verification compares against,
one-to-one, per scenario):

```
{
  "scenario": {
    "v_nom_rms": 230.0, "i_nom_rms": <1.0|8.0|16.0|32.0>,
    "pf_target": <1.00|0.95|0.85|0.50>, "thd_target": <0.00|0.05|0.10|0.20>,
    "f_line_hz": 50.0, "cycles": 16, "samples_per_cycle": 1024
  },
  "values": {
    "vrms": <double, V>, "irms": <double, A>,
    "p_w": <double, W>, "s_va": <double, VA>,
    "q_va": <double, var, IEEE method √(S²−P²)>,
    "q1_var": <double, var, Budeanu-style fundamental reactive>,
    "pf": <double, dimensionless>
  },
  "computed_thd": { "thd_v": <double, fraction>, "thd_i": <double, fraction> },
  "errors_vs_ideal": {
    "vrms_ppm": <double>, "irms_ppm": <double>,
    "p_ppm": <double>, "thd_v_ppm": <double>
  },
  "energy": {
    "wh_window": <double, Wh over the 16-cycle/0.32s sampled window>,
    "kwh_1h": <double, kWh, 1-hour projection of instantaneous P>
  }
}
```

`errors_vs_ideal` is the golden model's own self-consistency check (double-precision
waveform generation vs. the ideal nominal grid values) — it is **not** the DSP error
budget. RTL verification's ppm error is a separate, new computation: DSP fixed-point
readback vs. `values`/`energy` in this same object (§6).

---

## 4. RTL Datapath → Golden Model Field Mapping

| Architecture pipeline stage (§8.6) | RTL result register (Q16.16 unless noted) | Golden field | Notes |
|---|---|---|---|
| CIC/sinc decimation (R=40, order 3) → sliding-window RMS | `VRMS_REG` | `values.vrms` | Fast window (1 cycle) and class window (25 cycles) both readable; compare fast-window readback against the golden per-scenario `vrms` (golden window = 16 cycles, see §1 caveat) |
| CIC/sinc decimation → sliding-window RMS | `IRMS_REG` | `values.irms` | Same window caveat as Vrms |
| Mean of instantaneous V·I product | `P_REG` | `values.p_w` | Active power |
| Vrms·Irms | `S_REG` | `values.s_va` | Apparent power |
| √(S²−P²) — architecture explicitly matches `golden_model.py:138`'s IEEE-apparent-power method | `Q_REG` | `values.q_va` | Not `q1_var` — architecture's Q datapath is the IEEE S/P method, so it compares against `q_va`, never `q1_var` |
| Wh/VAh accumulation registers, rollover handling | `WH_ACCUM_REG` | `energy.wh_window` | Window-length dependent — see §1 caveat; do not compare directly against `energy.kwh_1h` without re-deriving the projection |
| Per-channel calibration (gain/phase/offset) | applied upstream of all `*_REG` reads | n/a | Calibration is exercised by running the sweep with calibration registers at unity (gain=1.0, phase/offset=0) for the primary golden comparison; a separate calibration-residual scenario set (RTL/verification-stage, not this document) exercises non-unity trims |
| Fundamental/harmonic DFT hooks (THD_v/THD_i) | `THD_V_REG` / `THD_I_REG` (if implemented as readback registers; see REQ-037) | `computed_thd.thd_v` / `computed_thd.thd_i` | Comparison hooks only — REQ-039's numeric budget does not list a THD tolerance (§5); reporting accuracy is qualitative at this stage |
| `pf` (P/S) | derived by verification from `P_REG`/`S_REG` readback, not a separate hardware register | `values.pf` | Architecture does not allocate a dedicated PF register; verification computes it from P and S readbacks for comparison |

`q1_var` has no RTL datapath counterpart in this architecture and is **not** part of the
comparison surface — it exists in the golden model as an alternate (Budeanu) reactive
power definition for reference only.

---

## 5. Tolerances (REQ-039 error budget, per field)

Per-scenario, per-field ppm/percent error is computed as
`error_pct = (rtl_value − golden_value) / golden_value * 100` (relative), using the
Q16.16→double conversion from §2.3. All tolerances below are the **class-1 accuracy
budget** from REQ-039 / `01_ARCHITECTURE.md` §8.6, applied per scenario across the full
64-scenario sweep:

| Field (RTL register → golden field) | Tolerance | Applicability | Source |
|---|---|---|---|
| `VRMS_REG` → `values.vrms` | ≤ ±0.5% relative | 10–100% of rated (Irms grid 1.0–32.0 A already spans this), PF ≥ 0.5 | REQ-039 |
| `IRMS_REG` → `values.irms` | ≤ ±0.5% relative | same | REQ-039 |
| `P_REG` → `values.p_w` | ≤ ±0.8% relative | class-1 headroom | REQ-039 |
| `Q_REG` → `values.q_va` | ≤ ±1.5% relative | | REQ-039 |
| `WH_ACCUM_REG` → `energy.wh_window` | ≤ ±1.0% relative | over a 1-hour equivalent window at PF ≥ 0.5; the golden model's 0.32 s window value is a rate proxy — see §7 for how RTL verification projects it to the 1-hour budget | REQ-039 |
| `S_REG` → `values.s_va` | ≤ ±0.8% relative (inherits the P budget; S = Vrms·Irms with both inputs already inside the 0.5% budget, so S's compounded bound is bounded by P's tighter figure) | derived, not separately stated in REQ-039 | architecture inference, flagged for verification-stage confirmation |
| Low-load edge case: Irms = 1.0 A, PF = 0.50 | tolerances above still apply; this is the lowest-SNR corner in the sweep grid (lowest signal amplitude combined with the largest phase offset) and is the corner most likely to expose calibration/quantization error first | all fields | architecture note, not a separate REQ |

**No absolute (unit-valued) tolerance is defined at architecture stage.** REQ-039 states
the budget entirely in relative (%) terms; an absolute floor (e.g., a minimum-count LSB
tolerance to avoid divide-by-near-zero pathologies at very low Vrms/Irms) is a
verification-stage refinement, not fixed here. The sweep grid's minimum values
(Irms = 1.0 A, `v_nom_rms` fixed at 230.0 V) do not include a near-zero denominator case,
so this gap is not expected to block verification, but is flagged rather than silently
assumed.

---

## 6. Pipeline-to-Scenario Mapping

The architecture's datapath (front-end CIC decimation → Vrms/Irms → P/Q/S → Wh
accumulation → calibration, §8.6) is exercised end-to-end by each of the 64 golden
scenarios as follows:

1. **Stimulus generation.** Each scenario's `scenario` block (`v_nom_rms`, `i_nom_rms`,
   `pf_target`, `thd_target`, `f_line_hz`, `samples_per_cycle`) parameterizes the same
   closed-form waveform generator as `golden_model.py:generate_waveforms()`, re-expressed
   as a 1-bit ΔΣ bitstream on `dat` (§2.2) at the architecture's `mclk_adc` rate
   (2.0 MHz @ 40 MHz core). This is a verification-stage implementation detail; the
   architecture only fixes that the stimulus must be scenario-parameter-identical to the
   golden model's waveform generator, not bit-identical in its ΔΣ encoding (ΔΣ modulation
   of a given waveform is not unique).
2. **CIC/sinc decimation (R=40, order 3).** Consumes the bitstream at `mclk_adc`, outputs
   Q1.15 samples at the decimated 50 kHz rate (1000 samples per 50 Hz line cycle).
3. **Windowed Vrms/Irms.** Sliding-window RMS over the fast window (1 cycle / 20 ms) and
   class window (25 cycles / 0.5 s, REQ-039) — compare fast-window output against the
   golden model's per-scenario `values.vrms`/`values.irms` (computed over the golden
   model's fixed 16-cycle window; §1 caveat governs exact window-length reconciliation).
4. **P/Q/S.** Computed per the architecture's exact formulas (§4) from the same
   windowed Vrms/Irms/instantaneous-product stream.
5. **Wh/VAh accumulation.** Accumulates P over the window with rollover handling;
   compared against `energy.wh_window` after projecting to matching window lengths (§7).
6. **Calibration.** Gain/phase/offset registers applied in the datapath before the result
   registers latch; primary comparison sweep runs with calibration at unity (§4) so the
   64-scenario comparison isolates CIC/RMS/power-computation error from calibration
   residual, per the error-budget map in `01_ARCHITECTURE.md` §8.6 (which lists
   calibration-residual as a *separate*, smaller contributor, ≤0.01%).

The full PF × load × THD grid (4×4×4 = 64 points) exercises every corner the architecture's
error budget table (§8.6) attributes error to: post-CIC quantization (visible across the
THD=0 row, where only quantization/rounding contributes), calibration-multiply rounding
(isolated by running a unity-calibration pass first), and CIC passband droop at harmonics
up to the 7th (visible across the THD ∈ {0.05, 0.10, 0.20} rows, which is exactly where
the 3rd/5th/7th harmonic content lives).

---

## 7. Comparison Methodology

**What RTL verification will run (contract, not implementation):**

1. For each of the 64 scenarios in `golden_out_seed42.json["tests"]`, drive the DSP's
   `dat`/`mclk_adc` inputs with the scenario-parameterized stimulus (§6 step 1) for at
   least one full class window (25 line cycles, 0.5 s) so both the fast-window and
   class-window result registers settle.
2. Read back `VRMS_REG`, `IRMS_REG`, `P_REG`, `S_REG`, `Q_REG`, `WH_ACCUM_REG` (and
   `THD_V_REG`/`THD_I_REG` if implemented) via the AHB burst-read result path (§2.1),
   with calibration registers at unity gain/zero phase/zero offset for the primary pass.
3. Convert each Q16.16 readback to a double using `value / 65536.0` (§2.3) — no other
   scale factor is contract-valid.
4. Compute relative error per field against the matching `values.*`/`energy.wh_window`
   entry in the same scenario object, per §5's formula.
   - For `WH_ACCUM_REG` specifically: since the golden model's `energy.wh_window` is an
     energy value over its own 16-cycle (0.32 s) window while REQ-039's Wh budget is
     stated "over a 1-hour window," verification must project both sides to a common
     basis before applying the ±1.0% bound — either scale the golden `wh_window` value up
     to a 1-hour-equivalent using the scenario's constant power assumption (same
     projection logic as the golden model's own `energy.kwh_1h` field, which already
     performs this projection from instantaneous `p_w`), or scale the RTL's
     `WH_ACCUM_REG` down to the golden model's native window. This document fixes the
     *obligation* to reconcile bases before comparing; the specific scaling
     implementation is a verification-stage deliverable.
5. Record per-scenario, per-field pass/fail against §5's tolerance table, plus the raw
   ppm/percent error, in a verification-stage results artifact (not produced by this
   architecture-stage document).
6. Repeat the sweep with the golden model regenerated at `N_CYCLES = 25` (§1 caveat) for
   the class-window-specific comparison, once that regeneration is performed — this is
   the action item already carried into RTL stage by `01_ARCHITECTURE.md` §8.6, restated
   here as a precondition for a class-window-accurate comparison.

**Pass/fail criteria:**

- A scenario **passes** if every field in §5's table is within its stated relative
  tolerance for that scenario.
- The MOD-06 golden-model comparison **passes** (satisfies REQ-039/REQ-055) if **all 64
  scenarios** pass on every field in §5, for both the fast window and the class window
  (once the `N_CYCLES = 25` regeneration in step 6 is available).
- Any scenario/field combination outside tolerance is a fail requiring either an RTL fix
  (RTL_FIX) or a documented, adjudicated waiver — no silent exclusion of a scenario from
  the denominator (mirrors the "100% of modules compared" discipline this project already
  applies at the module level, `01_ARCHITECTURE.md` §0's REUSE/CREATE rule and the
  project's stage-gate practice of never shrinking a comparison set without a named
  waiver).
- Determinism: because `golden_model.py` is RNG-free and seed-invariant (`README.md`,
  determinism contract), verification may run the comparison against
  `golden_out_seed42.json` (or regenerate with any seed) — the comparison target is not
  seed-sensitive, only the eventual `N_CYCLES` regeneration (step 6) changes the target
  file's `tests` content.

---

## 8. Open Items Carried to RTL / Verification Stage

These are explicitly **not resolved** by this architecture-stage contract — they are
flagged so RTL/verification stage does not silently re-derive or skip them:

1. **Window-length reconciliation (§1, §6, §7 step 4/6).** Golden model uses
   `N_CYCLES = 16` (0.32 s); architecture's class window is 25 cycles (0.5 s, REQ-039).
   Regenerate `golden_model.py` with `N_CYCLES = 25` before the class-window comparison
   is authoritative. Already flagged in `01_ARCHITECTURE.md` §8.6.
2. **Exact AHB register offsets for `VRMS_REG`/`IRMS_REG`/`P_REG`/`S_REG`/`Q_REG`/
   `WH_ACCUM_REG` within the 4 kB MOD-06 window** are an RTL-stage decision; this
   document fixes their Q-format and golden-field mapping only (§2.3, §4).
3. **S_REG tolerance (§5)** is an architecture-stage inference (inherits P's ±0.8%
   bound), not a value directly stated in REQ-039 — confirm or tighten at verification
   stage.
4. **THD_V_REG/THD_I_REG** existence as readback registers is conditional on RTL
   implementing the "THD reporting hooks" named in REQ-037; no numeric tolerance is
   defined for them in REQ-039 (§5).
5. **Absolute-tolerance floor** for near-zero denominators is not defined (§5) — flagged,
   not expected to block the given sweep grid.
6. **Calibration-residual comparison set** (non-unity gain/phase/offset trims) is out of
   scope for the primary 64-scenario sweep (§6 step 6) and is a separate verification-stage
   deliverable.
