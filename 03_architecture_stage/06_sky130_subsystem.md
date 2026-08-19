# EVCore-MY — sky130 Subsystem Plan (Analog / Silicon)
## PRJ-004 / v0 / 03_architecture_stage / 06_sky130_subsystem.md

*Version 1.0 | 2026-08-19 | Architecture stage — derived from `01_ARCHITECTURE.md` (§1.2 physical
budget, §1.6 pad-ring sketch, §5 clock/reset strategy, §8.16 MOD-16, §12 analog budget),
`02_specification_stage/04_blackbox_register.md` (BB-01…BB-04 pin contracts),
`02_specification_stage/01_system_spec.md` (REQ-006…REQ-011, REQ-030…REQ-036, REQ-048…REQ-050),
and `03_rtl_feasibility_review.md` (§5 stubs, §6 area).*

*Purpose: the analog/silicon-level plan for the standalone sky130A die (REQ-006 — no Caravel):
pad ring, clocking (PLL optional / external clock + divider), SAR ADC + comparators (the 2
instantiated analog blocks of the ≤3 budget, REQ-048), external ΔΣ metering ADC interface,
external LDO, OpenRAM 16 kB macro plan, power domains, and reset synchronisation. Floorplan
detail (exact pad order, macro placement coordinates, DRC) is a backend-stage deliverable —
this document fixes the architecture-level decisions that the floorplan must honour.*

---

## 1. Die context (carried from ARCHITECTURE.md §1.2, REQ-006…REQ-011)

| Item | Value |
|---|---|
| Flow | OpenLane / LibreLane, sky130A PDK, **sky130hd** std cells primary (REQ-011) |
| Form factor | Standalone die, **full pad ring**, own I/O — no Caravel harness (REQ-006) |
| Target area | 1–3 mm² (architecture estimate ~1.5–2.0 mm², `03_rtl_feasibility_review.md` §6) |
| Std cells | 60–100 k target (est. ~57–62 k central) |
| SRAM | 16 kB = 8 × 2 kB OpenRAM 1-port (REQ-009) |
| Deliverable | Verified RTL + OpenLane hardening report (area/timing/power) + GLS w/ SDF; **no tapeout** (REQ-010) |
| Analog budget | ≤ 3 custom blocks (REQ-048); v1 uses **2** (SAR ADC + comparator ×2); PLL not instantiated |

---

## 2. Pad ring

### 2.1 Pad classes and counts (ARCHITECTURE.md §1.6 — not a pin-out, a class budget)

| Pad class | Count | Driven by | Pad type (sky130 I/O) |
|---|---|---|---|
| Power/ground (core 1.8 V + I/O 3.3 V, separate rails) | 8–12 | external LDO rails | power pads (multiple VDD/VSS pairs; ESD cells) |
| External clock in (XOSC 10–25 MHz) | 1 | MOD-15 | clock input (special buffer/ESD) |
| Async reset in | 1 | MOD-15 | digital input, Schmitt |
| BOOT_MODE strap | 1 | MOD-15 | digital input w/ pull (sampled at reset release, §4.3) |
| UART0/UART1 TX/RX | 4 | MOD-09 | digital I/O |
| SPI0/SPI1 SCLK/MOSI/MISO/CS | 8 | MOD-10 | digital I/O |
| I2C0 SDA/SCL | 2 | MOD-11 | open-drain-capable digital I/O |
| GPIO8 | 8 | MOD-12 | digital I/O (configurable pull) |
| CAN TX/RX (to external transceiver) | 2 | MOD-07 | digital I/O |
| CP PWM out + CP level sense (analog) | 2 | MOD-08 / MOD-16 | 1 digital output (PWM) + 1 analog input (level) |
| SAR ADC analog in + Vref | 2 | MOD-16 / BB-02 | analog pads (vin_p, vrefp) |
| Comparator analog in ×2 (CP level, zero-cross) | 4 | MOD-16 / BB-03 | analog pads (vp/vn ×2) |
| External ΔΣ ADC: MCLK out, DAT in | 2 | MOD-06 | 1 digital output (clock) + 1 digital input (bitstream) |
| Debug/test (DFT, SRAM test mode) | 2–4 | sign-off only | digital I/O |
| **Total** | **~48–52** | | |

### 2.2 Pad-ring architecture decisions

1. **Full custom pad ring in OpenLane/LibreLane** with sky130 I/O cells: digital I/O cells
   with ESD, dedicated analog I/O cells for the SAR/comparator inputs (analog pads must NOT
   pass through digital ESD/buffer cells — they route to the analog macro pins directly),
   and power pads for both the 1.8 V core rail and the 3.3 V I/O rail.
2. **Pad pitch/area feasibility:** ~48–52 pads at sky130 pad pitch fits a 1.5–2.0 mm² die
   with a ring (est. ring contribution ~0.3–0.5 mm² — `03_rtl_feasibility_review.md` §6).
   Exact ordering, corner cells, and seal ring are backend-stage deliverables (REQ-057).
3. **Analog pin hygiene:** the SAR ADC `vin_p/vrefp` and comparator `vp/vn` pads are
   dedicated analog pins; they are not shared with digital functions, and the blackbox
   register's pin contract (BB-02/BB-03) is the boundary — floorplan must keep analog pad →
   macro routing short and away from the digital clock distribution (noise coupling note,
   architecture-level).
4. **BOOT_MODE strap and reset** are strapped pads sampled while `rst_n_core` is low (§4.3);
   both need defined pull behavior so an unconnected strap reads a safe default (SRAM boot,
   reset asserted).

---

## 3. Clocking plan (REQ-030/031/034/036)

### 3.1 Clock sources and dividers

| Clock | Source | Frequency | Generation |
|---|---|---|---|
| `clk_core` | external crystal/osc 10–25 MHz via XOSC pad (REQ-031) | **40 MHz nominal / 25 MHz fallback** | on-chip integer divider `DIVCFG` (MOD-15). 40 MHz reached by dividing an external 10–25 MHz source per REQ-031's framing (e.g., 20 MHz ×2 is NOT used — no PLL in v1; divider-only path means `clk_core` ≤ external source... see note below) |
| PLL (BB-04) | — | — | **not instantiated in v1** (§5.1 of ARCHITECTURE.md); external-clock + divider path is the REQ-031-compliant baseline |
| `mclk_adc` | `clk_core` ÷ `DIVCFG_ADC` | 2.0 MHz (40 MHz mode) / ~1.92 MHz (25 MHz fallback) | MOD-06, sent off-chip to the external ΔΣ ADC (REQ-036); both ≤ 2.048 MHz ceiling |
| SAR conversion clock | `clk_core` ÷ `SAR_CLKDIV` | divided core clock | clock-ENABLE-gated single-domain design (no physical second net — §5.3 of ARCHITECTURE.md decision) |
| Comparator sampling clock | `clk_core` | 40/25 MHz | direct (BB-03 contract: registered output) |

**Clock-source note (architecture decision, REQ-031):** the divider-only path can only
produce `clk_core` ≤ the external source frequency. "40 MHz nominal" therefore assumes an
external oscillator at ≥ 40 MHz (e.g., 40 MHz XO directly, or 10–25 MHz crystal only for the
25 MHz fallback configuration). Two concrete, REQ-031-compliant options exist and RTL/backend
stage picks by BOM:
- **Option A (default):** external 40 MHz XO → `clk_core` = 40 MHz directly (DIVCFG=1). 25 MHz
  fallback = external 25 MHz XO or DIVCFG on a 50 MHz source (not available) — practically:
  fallback config runs the 25 MHz XO.
- **Option B:** external 10–25 MHz crystal + internal divider → `clk_core` ≤ 25 MHz (fallback
  config); 40 MHz nominal then requires the optional PLL (BB-04) later (v2).
The v1 architecture baseline is Option A with a 40 MHz-capable external oscillator; the PLL
stays in the blackbox register (BB-04) as the documented upgrade path, exactly per REQ-031's
"external clock with divider; PLL optional, may be skipped" text. This is recorded as an
architecture-stage decision so RTL stage does not re-derive it.

### 3.2 Clock distribution and gating

- Single `clk_core` tree across the die; divided clocks are enable-domain logic where
  possible (SAR ADC, CIC input stage) — the architecture deliberately avoids physical second
  clock nets except `mclk_adc`'s off-chip pad (REQ-034 CDC boundary, §5.3 of ARCHITECTURE.md).
- Clock gating (REQ-035): sky130 **integrated clock-gating (ICG) cells** inserted at
  synthesis for MOD-06 (metering datapath) and MOD-07 (CAN) idle gating, enabled via
  `CLK_GATE_EN` bits in MOD-15 (APB 0xA000). Gating is synchronous to each block's clock
  edge (no glitch; the CDC 2FF + async FIFO at the ADC pad is on the ungated `clk_core`, so
  gating cannot disturb the CDC boundary — §5.4 of ARCHITECTURE.md).
- Activity-based power from GLS (REQ-035/056/057) is the backend measure; no power estimate
  is claimed at architecture stage.

---

## 4. Power domains and reset

### 4.1 Power domains (single core + always-on PMU logic)

| Domain | Rail | Contents | Notes |
|---|---|---|---|
| Core | 1.8 V (sky130hd VDD) | all digital logic, SRAM macros, MOD-15 | single core domain per REQ-034 framing |
| I/O | 3.3 V | pad ring I/O cells, open-drain I2C, CAN | standard sky130 I/O rail; level-shift at pad boundary |
| Analog (within core rail) | 1.8 V analog supply | BB-02 SAR ADC, BB-03 comparators | separate analog supply pins to the macros, filtered externally per datasheet practice |
| "Always-on" PMU logic | 1.8 V | MOD-15 reset synchronizer, brown-out detect, `PGOOD` monitor | architecturally always-on (must run before/independent of the rest); physically on the same single 1.8 V rail — no second power domain on this die. "Always-on" is a *functional* attribute of MOD-15's reset/boot path, not a separate voltage island (sky130 flow simplicity; REQ-032 keeps all regulation external) |

**Decision recorded:** EVCore-MY is a **single core power domain** die. There is no
voltage-islanded always-on domain; the always-on *function* (reset release, PGOOD/brown-out
monitor, boot-strap sampling) is implemented in MOD-15 on the same rail, with the reset
synchronizer's async-assert path requiring no clock (§4.3). If a future revision adds deep
sleep, that is a new architecture decision — out of v1 scope (REQ-058 guardrails).

### 4.2 External LDO (REQ-032)

- All regulation is external: the product board provides the 3.3 V rail (from mains-side
  supply) and the 1.8 V core rail via an external LDO/DC-DC.
- `PGOOD` (LDO good signal) is monitored by MOD-15: loss of `PGOOD` asserts the async reset
  net (brown-out protection, IRQ 14, `05_safety_architecture.md` §2.3). Power-on sequence:
  LDO up → `PGOOD` → reset release → boot (ARCHITECTURE.md §6.1).
- No on-die LDO, no on-die regulators (REQ-032/049).

### 4.3 Reset synchronisation (REQ-033)

Architecture (ARCHITECTURE.md §5.2) — the physical plan:

```
ext_rst_n / PGOOD / WDT-timeout / soft-reset  ──►[async assert]
                                                   ▼
clk_core ──►[FF]──►[FF]──► rst_n_core (sync-deasserted, glitch-free)
```

- **Assert path:** asynchronous, no clock dependency — POR, `ext_rst_n`, brown-out, or
  WDT-timeout can pull the whole die into reset within one edge.
- **Deassert path:** 2-flop synchronizer releases `rst_n_core` only on a `clk_core` edge
  (metastability-safe release). All flops in all modules reset to defined states (REQ-033);
  CP PWM output reset value = de-energized level (`05_safety_architecture.md` §1.4).
- **Divided-clock domains** (`mclk_adc`, SAR enable clock) reuse `rst_n_core`; if a divided
  clock needs its own release edge, a local synchronizer on that clock is used — standard
  divided-clock reset fan-out, NOT a new CDC boundary (integer-divided clocks, §5.2 of
  ARCHITECTURE.md).
- **BOOT_MODE sampling:** strap sampled while `rst_n_core` is low (ARCHITECTURE.md §6.1);
  MOD-15 holds the CPU in reset through the boot-copy phase (CPU-hold gate) so the boot
  engine (AXI master M1) runs alone (§6 of ARCHITECTURE.md).

---

## 5. Analog blocks (the 2 of ≤3 instantiated, REQ-048)

### 5.1 BB-02 — 12-bit SAR ADC (required)

| Item | Plan |
|---|---|
| Role | CP voltage sampling + aux sense (REQ-047/048), shared with MOD-08 via channel select |
| Pin contract | `clk` (SAR conversion clock, divided core clock), `rst_n`, `start` (pulse), `chsel[2:0]` (CP, aux0, aux1…), `vref_ok`, `busy`, `eoc`, `dout[11:0]`; analog `vin_p`, `vrefp` (04_blackbox_register.md §2) |
| Clocking | `clk_core` ÷ `SAR_CLKDIV` — implemented as clock-enable gating, not a physical clock net (§5.3 of ARCHITECTURE.md) |
| Conversion | 12-bit successive approximation; dummy model latency default 16 clocks (BB-02 notes); IRQ 12 on `eoc` |
| Analog hookup | `vin_p` ← dedicated analog pad (CP level / aux mux), `vrefp` ← external reference (analog pad) with `vref_ok` status into MOD-16 |
| Fallback (manifest) | SAR macro unavailable → external SAR chip over SPI + comparator-only CP sampling (documented deviation path, 04_blackbox_register.md rule 4) |

### 5.2 BB-03 — Comparator ×1–2 (required)

| Item | Plan |
|---|---|
| Role | CP level detection (threshold) + line zero-cross (REQ-047/048); 2 instances |
| Pin contract | `clk` (core clock), `rst_n`, `sel[1:0]` (0 = CP level, 1 = zero-cross), `vth[11:0]` (SAR-consistent scale), `out` (registered); analog `vp`, `vn` (04_blackbox_register.md §3) |
| Clocking | core clock directly — registered output, no CDC needed |
| Usage | instance 0 → CP level detect (drives CP FSM fault path, `05_safety_architecture.md` §1.3); instance 1 → line zero-cross (IRQ 13, PF/phase hooks) |
| Hysteresis | `CMP_HYST` param (default 8 codes) in the sim model; threshold `vth` programmable from MOD-16 APB block |

### 5.3 BB-04 — PLL (OPTIONAL, not instantiated v1)

- Not instantiated (ARCHITECTURE.md §5.1/§12): external-clock + divider path is sufficient.
- Remains in the blackbox register (BB-04 pin contract) as the documented 40 MHz upgrade
  path if the external oscillator option proves BOM-unfriendly (§3.1 Option B).
- **Analog budget outcome:** 2 of ≤3 custom blocks used (REQ-048) — under budget, no PLL
  risk in v1.

### 5.4 External ΔΣ metering ADC (off-chip, REQ-036)

- Part class (A4, generic): low-cost 16-bit ΔΣ metering ADC (class-0.5s/1 modulator class).
  No specific part number is named — BOM/procurement decision; the interface is generic and
  fixed (04_blackbox_register.md §5):
  - `mclk` out (chip-generated, 2.0/1.92 MHz ≤ 2.048 MHz ceiling) to the ADC,
  - `dat` in (Option A: 1-bit PDM/ΔΣ bitstream — v1 baseline; Option B: word-serial 16-bit,
    software-selectable by reconfiguring the CIC front-end input width),
  - pad-boundary 2FF synchronizer + small async FIFO (4–8 entries, Gray-coded) — the single
    true CDC boundary (REQ-034, §5.3 of ARCHITECTURE.md; formal CDC check at RTL stage,
    REQ-056).
- No on-die high-resolution ADC (REQ-049).

---

## 6. OpenRAM 16 kB macro plan (MOD-05 / BB-01)

| Item | Plan |
|---|---|
| Configuration | 8 × 2 kB 1-port sky130 OpenRAM macros (REQ-009 exact); each `sram_1rw_2kB_sky130`: clk0/csb0/web0/addr0[10:0]/wmask0[3:0]/din0[31:0]/dout0[31:0] |
| Aggregation | project AXI4-Lite wrapper (synthesizable RTL): top 3 bits of the 14-bit offset select the instance; byte writes via `wmask0` from AXI `wstrb` (§8.5 of ARCHITECTURE.md) |
| Area | ~0.06–0.10 mm² per 2 kB instance → ~0.5–0.75 mm² total (die's largest single component, consistent with REQ-007's SRAM-dominated note) |
| Placement intent | single contiguous macro block adjacent to the AXI tier/CPU; wrapper logic beside it; keep macro away from the analog pin group (noise) — floorplan stage |
| DFT | SRAM test-mode pins wired to the 2–4 debug/test pads (ARCHITECTURE.md §1.6); scan not applied to macros (04_blackbox_register.md rule 5) |
| Simulation | OpenRAM behavioural model, `$readmemh` boot image under `ifdef SIMULATION` (BB-01) |
| Flow requirement | Macro is REQUIRED for sign-off (area/timing); behavioural model is sim-only — escalate if the OpenRAM flow cannot generate it (blackbox rule 4) |
| 32 kB stretch | Not required by the feasibility estimate (16 kB fits); only if firmware image + data proves tight at RTL stage — architecture does not reserve it |

---

## 7. Floorplan-intent summary (hand-off to backend, REQ-057)

| Region | Content | Constraint from architecture |
|---|---|---|
| Core west/north | CPU (MOD-01) + AXI crossbar (MOD-02) + SRAM block (BB-01 ×8) + wrapper | SRAM block adjacent to CPU; AXI paths short |
| Core centre | MOD-03/04 bridges, MOD-15 (clk/reset/PMU/INTC), MOD-14 WDT | reset distribution central (short fan-out) |
| Core east | MOD-06 metering DSP | near ΔΣ ADC pads (MCLK/DAT) and its 2FF+FIFO boundary |
| Core south | MOD-07 CAN, MOD-08 CP + MOD-16 wrapper | MOD-08 near CP PWM/analog pad group (short analog routing) |
| Analog island | BB-02 SAR ADC, BB-03 comparators | adjacent to analog pads; separated from digital clock tree (noise) |
| Ring | ~48–52 pads (§2.1) | analog pads dedicated; power pads distributed; DFT pads at corner |

Exact coordinates, routing, and DRC are backend-stage; this table fixes the architectural
placement intent so the backend does not have to re-derive the die's shape.

---

## 8. REQ trace for this document

| REQ | Where satisfied |
|---|---|
| REQ-006 | §1, §2 (standalone die, full pad ring, no Caravel) |
| REQ-007 | §1, §2.2, `03_rtl_feasibility_review.md` §6 (1–3 mm²) |
| REQ-008 | §1 (cell budget, est. in feasibility review) |
| REQ-009 | §6 (16 kB = 8 × 2 kB OpenRAM) |
| REQ-010 | §1 (deliverable framing), §7 (backend handoff) |
| REQ-011 | §1 (sky130A, sky130hd) |
| REQ-030 | §3.1 (40/25 MHz plan, Fmax reported at backend) |
| REQ-031 | §3.1 (external clock + divider; PLL optional, not v1; options A/B decision) |
| REQ-032 | §4.2 (external LDO, PGOOD monitor) |
| REQ-033 | §4.3 (async-assert/sync-deassert reset synchronizer) |
| REQ-034 | §3.2, §5.4 (single core domain, CDC boundary = ΔΣ ADC pad path) |
| REQ-035 | §3.2 (ICG gating for MOD-06/MOD-07) |
| REQ-036 | §5.4 (external 16-bit ΔΣ ADC, MCLK+DAT generic interface) |
| REQ-048 | §5 (2 of ≤3 analog blocks) |
| REQ-049 | §5.4 (no on-die high-res ADC / LDO / RF) |
| REQ-050 | §5.1–5.2 (analog wrapper registers on APB 0xB000 via MOD-16) |
| REQ-056 | §5.4 (CDC formal at RTL stage) |
| REQ-057 | §7 (floorplan-intent handoff for hardening report) |

---

## 9. Open items carried to RTL / backend

1. **Oscillator choice (Option A vs B, §3.1)** — BOM decision; RTL keeps both divider paths
   (`DIVCFG`), architecture default = external 40 MHz-capable XO.
2. **`SAR_CLKDIV` value and conversion latency budget** — RTL-stage parameterization against
   BB-02's dummy model (default 16 cycles).
3. **PMU clock-fail/brown-out detect thresholds** (`05_safety_architecture.md` §8 item 3) —
   RTL-stage parameters; async reset path fixed.
4. **Exact pad order, I/O cell selection, seal ring** — backend-stage deliverable (REQ-057);
   the class budget (§2.1) is fixed at architecture.
5. **OpenRAM macro generation + characterization** — first backend-flow task (feasibility
   review §8 item 2; macro required for sign-off).
6. **Analog macro availability in the local sky130 flow** (SAR ADC, comparator instances) —
   if unavailable, the manifest fallback applies (external SAR over SPI + comparator-only CP
   sampling, 04_blackbox_register.md rule 4) — escalation path recorded, not assumed.

---

*End of sky130 subsystem plan. Decisions fixed: standalone full pad ring (~48–52 pads),
external-clock + divider baseline (Option A; PLL BB-04 documented upgrade path), 2 of ≤3
analog blocks (SAR ADC + comparator ×2) with dedicated analog pads, external LDO with PGOOD
monitoring, single 1.8 V core domain with functional always-on PMU logic (no voltage island),
16 kB OpenRAM 8 × 2 kB plan, async-assert/sync-deassert reset synchronisation, and a
floorplan-intent handoff for the OpenLane hardening report (REQ-057).*
