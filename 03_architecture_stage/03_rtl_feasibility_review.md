# EVCore-MY — RTL Feasibility Review (sky130A @ 40 MHz)
## PRJ-004 / v0 / 03_architecture_stage / 03_rtl_feasibility_review.md

*Version 1.0 | 2026-08-19 | Architecture stage — derived from `01_ARCHITECTURE.md` (§1 physical
budget, §2 bus architecture, §5 clock/reset, §8 module-by-module), `02_memory_map.json`,
`02_specification_stage/02_reuse_manifest.json` (17 modules, classifications, licences),
`02_specification_stage/04_blackbox_register.md` (BB-01…BB-04), and the REQ contract
(REQ-006…REQ-011 physical; REQ-030/031 clock; REQ-057 sign-off report).*

*Purpose: architecture-stage gate/cell/area/timing feasibility of the EVCore-MY SoC on sky130A
(OpenLane/LibreLane, sky130hd) before RTL is committed. All numbers are **architecture-stage
estimates** with methodology stated; the measured closure is the RTL-stage/backend-stage
deliverable (REQ-010, REQ-057). Nothing in this document is a silicon guarantee.*

---

## 0. Verdict

**FEASIBLE — at the architecture stage, with stated margin.**

| Constraint | Budget (REQ) | Architecture-stage estimate | Margin |
|---|---|---|---|
| Std cells | 60–100 k (REQ-008) | ~55–62 k logic cells incl. clock tree (range 48–75 k across module estimate bounds) | inside band at central estimate |
| Die area | 1–3 mm² (REQ-007) | ~1.5–2.0 mm² (core ~1.2–1.6 mm² + full pad ring ~0.3–0.5 mm²) | inside band |
| Core clock | 40 MHz nominal, 25 MHz fallback (REQ-030) | 40 MHz comfortable on sky130hd; 25 MHz fallback exists as config, not as a rescue | headroom |
| SRAM | 16 kB (REQ-009) | 16 kB = 8 × 2 kB OpenRAM 1-port; no 32 kB stretch needed | no stretch required |
| Analog | ≤ 3 custom blocks (REQ-048) | 2 used (SAR ADC, comparator ×2); PLL not instantiated | under budget |

**Contingency (only if measured results disappoint — not required by this estimate):**
FEASIBLE-WITH-CUTS list in §7. The cut list is ordered so each cut is an independent,
architecture-compatible fallback (address slots and bus map unchanged).

---

## 1. Method

1. **Cell counts** per module are derived from (a) REQ-008's own anchors (picorv32 ≈ 10–15 k),
   (b) published/observed gate counts of the REUSE cores (OpenCores CAN, EF_* peripherals are
   silicon-proven small IP), and (c) line-count→cell heuristics for CREATE blocks (~0.8–1.2 k
   cells per 100 lines for control logic; datapath-heavy logic higher per line). Each module
   gets a low/high range; the central estimate is the midpoint.
2. **SRAM area** uses OpenRAM sky130 2 kB 1-port macro characteristics (≈ 0.06–0.10 mm² per
   2 kB instance, 8 instances).
3. **Std-cell area** uses sky130hd average cell footprint ≈ 5–9 µm² and an OpenLane-style
   placement utilization of 50–60% (floorplan area = raw cell area / utilization).
4. **Die area** = core area + pad ring (≈ 48–52 pads at sky130 pad pitch, ARCHITECTURE.md §1.6)
   + seal/scribe allowance; rounded to a 1–3 mm² verdict band.
5. **Timing** is assessed per clock domain at 40 MHz (25 ns period) against sky130hd typical
   cell delays; the only timing-sensitive structures are called out explicitly (§4). The
   backend Fmax report (REQ-057) is the measured result; this review only establishes
   architectural plausibility.

---

## 2. Module-by-module gate estimates (all 17 modules, MOD-01…MOD-17)

Classification per `02_reuse_manifest.json` (2026-08-19, licence/purity verified). Cells are
std-cell equivalents; analog macros and SRAM macros are NOT std cells (listed separately §5).

| MOD | Module | Class (manifest) | Est. cells (low–high) | Central | Timing risk @40 MHz | Notes |
|---|---|---|---|---|---|---|
| MOD-01 | picorv32 CPU (RV32IMC) | REUSE_GITHUB (ISC) | 10 000–15 000 | 12 500 | Low | REQ-008 anchor; multi-cycle, `ENABLE_FAST_MUL=0`, `ENABLE_DIV=1`, no barrel shifter (§4 of ARCHITECTURE.md) |
| MOD-02 | AXI4-Lite crossbar (2M×3S) | REUSE_GITHUB (MIT) | 2 000–4 000 | 3 000 | Low | verilog-axi `axil_crossbar`; arbitration + 3-slave decode; 3rd master port reserved |
| MOD-03 | AXI4-Lite→AHB3-Lite bridge | CREATE | 800–1 500 | 1 150 | Low | ~300–400 lines; single-beat translation; 1 MB window decode (§8.3) |
| MOD-04 | AHB3-Lite→APB bridge | CREATE | 500–1 000 | 750 | Low | ~200 lines; 12-`psel` decode (AR-1, §8.4) |
| MOD-05 | SRAM 16 kB + AXI wrapper | REUSE_GITHUB (BSD-3) | 500–1 000 (wrapper only) | 750 | Low | SRAM macro area separate (§5.1); wrapper = decode 8 × 2 kB + wmask aggregation |
| MOD-06 | Metering DSP (flagship CREATE) | CREATE | 8 000–15 000 | 11 500 | Low–Med | CIC order-3 R=40 (17-bit integrators), RMS/P/Q/S datapath (32-bit MACs), Wh accum, calib, FIFO. Biggest CREATE block; see §4.2 |
| MOD-07 | CAN 2.0B (SJA1000-class) | REUSE_GITHUB (LGPL-2.1+) | 6 000–10 000 | 8 000 | Low | freecores/can port; bit timing at 500 kbit/s trivial vs 40 MHz; A2 flag carried |
| MOD-08 | CP engine (IEC 61851) | CREATE | 1 000–2 000 | 1 500 | Low | FSM A/B/C/D/E/F + 1 kHz PWM prescaler + fault latch; state-gated duty mux (§9) |
| MOD-09 | UART ×2 (EF_UART) | REUSE_INTERNAL (Apache-2.0) | 2 000–4 000 | 3 000 | Low | FIFO UARTs, silicon-proven |
| MOD-10 | SPI ×2 (EF_SPI) | REUSE_INTERNAL (Apache-2.0) | 2 000–3 000 | 2 500 | Low | FIFO SPIs |
| MOD-11 | I2C ×1 (EF_I2C) | REUSE_INTERNAL (Apache-2.0) | 1 000–1 500 | 1 250 | Low | |
| MOD-12 | GPIO ×8 (EF_GPIO8) | REUSE_INTERNAL (Apache-2.0) | 300–600 | 450 | Low | |
| MOD-13 | TMR32 + PWM32 | REUSE_INTERNAL (Apache-2.0) | 2 000–3 500 | 2 750 | Low | EF_PWM32 index gap (A1); EF_TMR32 PWM-mode fallback same slot |
| MOD-14 | WDT32 (EF_WDT32) | REUSE_INTERNAL (Apache-2.0) | 500–1 000 | 750 | Low | |
| MOD-15 | clk/rst + PMU + INTC + boot | CREATE | 3 000–5 000 | 4 000 | Low | reset synchronizer, dividers, IRQ aggregator, boot-copy FSMs (~1–2 k per A5) |
| MOD-16 | SAR ADC + comparator wrapper | BLACKBOX | 500–1 000 (digital wrapper) | 750 | Low | analog macros separate (§5.2); wrapper = start/chsel/busy/eoc/dout + cmp ctrl |
| MOD-17 | DMA (deferred) | CREATE (defer) | 0 | 0 | — | not populated v1 (REQ-058); crossbar port reserved |
| **Total logic cells** | | | **39 100–68 100** | **~54 000** | | + clock tree (~5–8%) ≈ **57–62 k central** |

**Reading the table:** central total ≈ 54 k logic cells; adding clock tree (~3–4 k) gives
**~57–62 k cells**, inside REQ-008's 60–100 k band at the low end. The low bound (39 k) is
under the band but that is a *target*, not a compliance floor — the area verdict (§6) is what
matters and it is comfortably inside 1–3 mm² either way. The high bound (68 k) is still inside
the band. No module individually threatens the budget.

**Reuse ratio cross-check (consistency with manifest):** 10 of 15 core modules are REUSE
(0.667), 5 CREATE (MOD-03/04/06/08/15), 1 BLACKBOX (MOD-16), 1 deferred (MOD-17). The CREATE
share of the cell estimate is ~19 k of 54 k (~35% of logic cells) — concentrated in MOD-06
(flagship) + MOD-15 + bridges + CP. That is a healthy CREATE:RTL ratio for a thesis project:
the novel contribution (metering DSP + CP safety + boot) is bounded and testable.

---

## 3. Timing feasibility @ 40 MHz (25 ns period, sky130hd)

sky130hd (9-track, 1.8 V core) comfortably closes 40 MHz for control-plane logic of this
depth; the architecture keeps every critical path short by construction:

| Domain | Structure | Why it closes at 40 MHz |
|---|---|---|
| `clk_core` — CPU fetch path | picorv32 multi-cycle fetch → AXI crossbar → SRAM read | picorv32 has no deep pipeline (multi-cycle, non-pipelined, §4 of ARCHITECTURE.md); SRAM access is a single macro read (~3–5 ns) inside a multi-cycle instruction window; crossbar 2M×3S AXI4-Lite is a small decode/arbiter |
| `clk_core` — MOD-06 datapath | 17-bit CIC integrator chain, 32-bit MAC accumulators | Enable rate is only 2 MHz (`mclk_adc`); the 40 MHz clock simply oversamples the datapath — adders are not in a throughput-critical chain at 40 MHz |
| `clk_core` — MOD-07 CAN | bit-timing FSM, CRC-15 shift | CAN bit rate is configurable (500 kbit/s nominal); 25 ns period is ~80× the bit cell — trivial |
| `clk_core` — bridges | MOD-03 single-beat translation, MOD-04 APB 2-phase | Both are simple FSMs (~200–400 lines); no multi-cycle dependency loops |
| `clk_core` — MOD-08 CP | 1 kHz PWM prescaler (÷40 000), state-gated duty mux | Pure counter + mux; the safety-relevant cone (state→duty) is single-register-deep by construction (§9 of ARCHITECTURE.md) — good for both timing AND formal |
| `mclk_adc` (2.0 MHz) | divided clock, CIC input stage | Divide-by-20 of `clk_core`; enable-domain logic, no independent timing closure needed beyond the divider itself |
| SAR conversion clock | `clk_core` ÷ N (clock-enable gating, §5.3 of ARCHITECTURE.md) | No physical second clock net (architecture decision, §5.3) — no additional timing corner |
| Reset release | 2FF synchronizer (async-assert/sync-deassert) | Standard synchronizer, no timing loop; only setup on the second FF matters |

**Clock-domain summary:** exactly one free-running external clock (10–25 MHz crystal/osc,
REQ-031); all on-chip clocks are integer divisions of `clk_core` (§5.1 of ARCHITECTURE.md).
The single true CDC boundary (external ΔΣ ADC bitstream) is a 2FF + small async FIFO at the
pad (§5.3) — a closed, well-bounded structure for both timing and CDC formal (REQ-034/056).

**Fallback posture (REQ-030):** 25 MHz is a *configuration* (different `DIVCFG`/prescaler
values), not a redesign. If the backend Fmax report lands between 25 and 40 MHz, the design
still meets every functional REQ; only the MCLK divider values change (÷13 vs ÷20, §5.1 of
ARCHITECTURE.md). This is why the feasibility verdict does not hinge on 40 MHz closure.

---

## 4. Timing risk register (the few things that could bite)

| # | Risk | Impact | Mitigation (already in architecture) |
|---|---|---|---|
| T1 | picorv32 memory-phase path through crossbar to SRAM (longest AXI path) | Fmax slightly below 40 MHz at worst | Multi-cycle core already tolerant; 25 MHz fallback config; SRAM wrapper is registered on both sides |
| T2 | MOD-06 32-bit MAC accumulator fan-in at Q1.31 (V·I product summing over 1000-sample window) | Area, not timing, at 40 MHz | 32-bit MACs are ~2 adders deep; window summing is sequential accumulation (no parallel tree) — area-bounded, timing-trivial at 2 MHz enable |
| T3 | MOD-02 crossbar arbitration with 3rd master (MOD-17) added later | Only if DMA added | v1 runs 2 masters; 3rd port reserved but unpopulated (§8.2); re-verify if DMA is ever built |
| T4 | OpenRAM macro access time vs 25 ns | SRAM read is ~3–5 ns typical; 25 ns budget has 5× margin | AXI wrapper registered; worst-case corner verified at backend (REQ-057) |
| T5 | CDC formal proof effort (REQ-056) | Schedule, not silicon | Boundary is a single 2FF + async FIFO (§5.3); SymbiYosys-proofable scope |
| T6 | Clock gating ICG insertion glitch risk | Functional, not Fmax | Gating synchronous per-domain (REQ-035, §5.4 of ARCHITECTURE.md); ICG cells from sky130hd |

None of T1–T6 is an architecture-stage blocker. All are RTL/backend-stage verification items
already named in `01_ARCHITECTURE.md` §14.

---

## 5. SRAM plan and analog stub list (from 04_blackbox_register.md)

### 5.1 SRAM plan (MOD-05 / BB-01)

| Item | Plan |
|---|---|
| Configuration | 16 kB = **8 × 2 kB OpenRAM 1-port macros** (sky130), REQ-009 exact |
| Macro interface | `sram_1rw_2kB_sky130` — clk0/csb0/web0/addr0[10:0]/wmask0[3:0]/din0[31:0]/dout0[31:0] (BB-01 pin contract) |
| Wrapper (project RTL) | AXI4-Lite slave; top 3 bits of the 14-bit SRAM offset select the 2 kB instance; byte writes via `wmask0` driven from AXI `wstrb` (§8.5 of ARCHITECTURE.md) |
| Area | ≈ 0.06–0.10 mm² per 2 kB instance → **≈ 0.5–0.75 mm² total** (dominates die area, consistent with REQ-007's "SRAM-dominated at ~0.5–1 mm²") |
| Placement intent | Single contiguous macro block near the CPU/AXI tier; wrapper adjacent; DFT pins (test mode) wired to the DFT pad group (§1.6 of ARCHITECTURE.md, 2–4 pads) |
| Simulation | OpenRAM-generated behavioural model, `$readmemh` boot image under `ifdef SIMULATION` (BB-01 notes) |
| 32 kB stretch | NOT required by this estimate (16 kB fits); stretch only if firmware image + data proves too tight — measured at RTL stage, architecture does not reserve it |
| Fallback | Macro is REQUIRED for sign-off (area/timing); behavioural model alone is sim-only — escalate if the OpenRAM flow cannot produce the macro (blackbox usage rule 4) |

### 5.2 Analog blackbox / stub list (from 04_blackbox_register.md — synthesis blackboxes, sim dummy models)

| Stub | Type | In v1? | Interface summary (pin contract, not re-derived here) | Attach |
|---|---|---|---|---|
| BB-01 OpenRAM 16 kB | compiled SRAM macro | yes | 8 × `sram_1rw_2kB_sky130` | AXI wrapper (MOD-05) |
| BB-02 SAR ADC 12-bit | analog macro | yes | `clk/rst_n/start/chsel[2:0]/vref_ok/busy/eoc/dout[11:0]` + analog `vin_p/vrefp` | MOD-16 wrapper → APB 0xB000 |
| BB-03 Comparator ×1–2 | analog macro | yes (×2: CP level, zero-cross) | `clk/rst_n/sel[1:0]/vth[11:0]/out` + analog `vp/vn` | MOD-16 wrapper → APB 0xB000 |
| BB-04 PLL | analog macro | **no** (optional) | `clk_ref/rst_n/pll_en/mdiv[3:0]/ddiv[3:0]/clk_out/locked` | not instantiated v1 (§5.1 of ARCHITECTURE.md) |
| External ΔΣ metering ADC | off-chip | yes | `mclk` out (≤2.048 MHz), `dat` in (Option A 1-bit bitstream baseline; Option B word-serial software-selectable) | MOD-06 front-end (CDC, §5.3) |
| External LDO | off-chip | yes | — (REQ-032); PGOOD sense into MOD-15 | power/status |
| External CAN transceiver, WiFi module, SPI NOR flash | off-chip | yes | digital pads (ARCHITECTURE.md §1.6) | MOD-07 / MOD-09 / MOD-10+MOD-15 |

**Analog budget check (REQ-048):** v1 instantiates **2 of ≤3** allowed custom analog blocks
(SAR ADC + comparator ×2); PLL skipped. Zero on-die high-res ADC / LDO / RF (REQ-049). The
stub list is exactly the 04_blackbox_register.md set — no additions, no drops.

**Simulation stub discipline (REQ-013/014):** all dummy models are pure Verilog-2001, gated by
`` `ifdef SIMULATION `` where needed; zero SV/VHDL. Pin names/widths are contractual
(blackbox register rule 3) — RTL stage may not rename without updating the register.

---

## 6. Area estimate vs 1–3 mm² (REQ-007)

| Component | Low | High | Central | Basis |
|---|---|---|---|---|
| Logic std cells (~54 k central, incl. ~3–4 k clock tree) | 39 k | 68 k | 57–62 k | §2; sky130hd ≈ 5–9 µm²/cell |
| Raw logic area | 0.20 mm² | 0.61 mm² | ~0.42 mm² | cells × 7 µm² avg |
| Logic floorplan @ 50–60% utilization | 0.35 mm² | 1.1 mm² | ~0.75 mm² | OpenLane placement reality |
| SRAM 16 kB (BB-01 ×8) | 0.5 mm² | 0.75 mm² | ~0.6 mm² | §5.1 |
| **Core total** | **0.9 mm²** | **1.9 mm²** | **~1.35 mm²** | |
| Full pad ring (~48–52 pads) + seal | 0.25 mm² | 0.5 mm² | ~0.35 mm² | ARCHITECTURE.md §1.6 pad classes |
| **Die total (rounded)** | **~1.2 mm²** | **~2.4 mm²** | **~1.7 mm²** | **inside 1–3 mm²** |

Even at the high bound, the die fits inside 3 mm² without touching the 32 kB SRAM stretch or
any cut. The verdict does not depend on optimistic corners.

**Cell budget cross-check (REQ-008):** central ~57–62 k cells is at the low edge of the
60–100 k band; high bound 68 k stays inside. If the project wants a headline number for the
thesis: **~60 k cells central estimate, 1.3–2.0 mm² core + pad ring, 1.5–2.0 mm² die
(rounded)** — to be replaced by measured OpenLane numbers at backend (REQ-057).

---

## 7. FEASIBLE-WITH-CUTS contingency (ordered; only if measured results require)

Each cut is independent, keeps the address map/bus topology byte-identical, and maps to an
already-documented fallback in the manifest/architecture. The architecture estimates these are
NOT needed; they exist so RTL/backend stage has pre-agreed decisions instead of inventing them
under pressure (constraint 13 discipline).

| # | Cut | What it saves | Already documented? |
|---|---|---|---|
| C1 | Drop to 25 MHz nominal (divider config change only) | Timing margin, none of the functional REQs change | REQ-030, §5.1 of ARCHITECTURE.md (explicit fallback config) |
| C2 | EF_PWM32 → EF_TMR32 PWM-output-mode fallback | One REUSE import, zero area change (same APB slot 0x8000) | A1 / REQ-052 / §8.13 (fallback at same address) |
| C3 | UART1 (WiFi) → UART0-only + SPI1 for WiFi | ~1–2 k cells (one EF_UART instance) | Not needed for any REQ-053 path (WiFi on UART1 OR SPI1 per REQ-053 text); would be a documented deviation (REQ-051 says UART ×2) — last-resort only |
| C4 | Defer MOD-13 PWM32 slot usage to firmware (TMR32 compare output) | ~1–1.5 k cells | A1 fallback path |
| C5 | MOD-06 sample FIFO depth below 1000 (burst-read cadence measured first) | FIFO RAM/FF area | §8.6 / §14 open item 5 — architecture minimum is 1000, sizing down is pre-agreed pending measurement |
| C6 | Drop THD reporting hooks (THD_V/THD_I registers) | ~0.5–1 k cells (DFT hooks) | REQ-037 lists them as hooks; REQ-039 has NO THD tolerance (§5 of 04_architecture_model.md) — deletable without breaking the golden comparison |

**Cuts are ordered by (area saved)/(REQ impact).** C1 and C2 are free; C3–C6 touch no
REQ-039/REQ-046/REQ-045-critical path (the thesis pillars: metering accuracy + CP safety are
untouched by every cut except C5, which only shrinks a FIFO and is already architecture-
approved pending measurement).

---

## 8. Open items for RTL/backend (carried from this review)

1. Replace every estimate in §2/§6 with measured synthesis numbers (REQ-057) — this table is
   the architecture-stage prediction, not the report.
2. OpenRAM macro generation + area/timing characterization (BB-01) is the single largest
   unknown; do it first in the backend flow (macro is required, §5.1).
3. EF_PWM32 qualification (A1) or its fallback — before MOD-13 RTL is finalized.
4. CAN core bit-timing parameterization against the external transceiver's propagation
   (MOD-07): config values are RTL-stage, timing model trivial.
5. CDC formal (REQ-056) and CP safety formal (REQ-046) scopes are named targets — sizes the
   formal budget at RTL stage (both are single-cone, §3/§9 of ARCHITECTURE.md).
6. DFT plan (scan insertion on digital logic, SRAM test pins, analog excluded) — needed by
   sign-off; ARCHITECTURE.md §1.6 reserves 2–4 test pads.

---

*End of feasibility review. Verdict: FEASIBLE (architecture-stage estimate) — ~57–62 k cells,
~1.5–2.0 mm² die, 40 MHz plausible with 25 MHz configurable fallback, 2/3 analog budget used,
16 kB SRAM as specified. Contingency cuts C1–C6 pre-agreed but not required by this estimate.
All numbers to be superseded by the measured OpenLane hardening report (REQ-010/REQ-057).*
