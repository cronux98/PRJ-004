# EVCore-MY — Smart EV AC-Charger Controller SoC
## System Specification — PRJ-004 / v0 / 02_specification_stage

*Version 1.0 | 2026-08-19 | Spec stage (contract for architecture + RTL stages)*
*Basis: `01_business_stage/candidate_03_evcore-my/01_pitch_candidate_C.md` (winning pitch), `10_top3_review_opus.md` §3 (scoped plan, revised 2026-08-19: NO Caravel), `candidates_scores.json` (Candidate C), `IP/index.md` (reuse registry).*

---

## 1. Project Identity & Product Framing

### 1.1 Identity

| Field | Value |
|---|---|
| Project | PRJ-004 — EVCore-MY (CANDIDATE-C) |
| Product | RM139 smart EV AC-charger (EVSE) controller module SoC |
| Target application | AC (Type 2) EV charger controller: energy metering DSP + CAN 2.0B + IEC 61851 control-pilot + OCPP-ready host (WiFi external) |
| Owner profile | Masters student, first SoC, sky130, pure Verilog-2001/2005, 3-tier AMBA, retail < RM150 |
| Stage | 02_specification_stage (spec only — no architecture, no RTL) |

### 1.2 Product & market requirements

**REQ-001 — RM139 controller module.** The SoC shall be the core of a controller module priced at RM139 retail, with a modelled BOM of RM75–105 (SoC RM18–22 + WiFi module RM25–35 + power RM10–15 + PCB RM12–18 + relay/CT RM10–15), supporting a 25–45% margin at volume.

**REQ-002 — B2B channel.** The primary sales channel shall be Malaysian charger OEMs / wallbox makers (white-label), CPOs (Gentari, JomCharge, ChargEV/TNB), and retrofit installers undercutting the imported RM150–300 OCPP retrofit module.

**REQ-003 — Policy narrative.** The SoC shall be positioned as a NIMP 2030 / National Semiconductor Strategy "Malaysia designs silicon" flagship for the EV charging build-out gap (3,600 points at end-2024 vs 10,000 target end-2025; gap persists through 2026–2030).

**REQ-004 — IP portability.** The metering DSP and CAN IP shall be designed to be reusable in smart meters (TNB AMI), solar inverters, industrial submetering, motor drives, and BMS (dual-use from day one; Candidate E SolarSync shares the metering DSP).

**REQ-005 — Non-billing metering claim.** The product shall be framed as *non-billing* energy metering (no legal-metrology claims), targeting EVSE charging statistics and monitoring use.

---

## 2. Physical & Process Budget

**REQ-006 — Standalone sky130A die, NO Caravel.** The SoC shall be implemented as a standalone sky130A die via the OpenLane/LibreLane flow with a full pad ring and own I/O. The Caravel harness shall NOT be used (owner decision 2026-08-19). *(Deviation record: pitch C implied Caravel-era reuse; opus review §3.1 overrides — no Caravel.)*

**REQ-007 — Die area target.** Target die area 1–3 mm² (comfortable for the block count; SRAM-dominated at ~0.5–1 mm²).

**REQ-008 — Std-cell budget.** Target 60–100 k standard cells (picorv32 ≈ 10–15 k; peripherals + metering DSP + CAN are small).

**REQ-009 — SRAM 16 kB.** On-chip SRAM shall be 16 kB single bank (8 × 2 kB OpenRAM 1-port macros); 32 kB is an accepted stretch only if area/timing analysis shows headroom. *(64 kB dual-bank explicitly cut per opus §3.5.)*

**REQ-010 — Thesis deliverable = sign-off analysis, NOT tapeout.** The stage-agnostic end deliverable is: verified RTL + OpenLane hardening report (area/timing/power) + GLS with back-annotated SDF. Tapeout is explicitly out of scope.

**REQ-011 — PDK.** SkyWater 130 nm (sky130A) via OpenLane/LibreLane, sky130hd standard cells as the primary target.

**REQ-012 — No on-die radio.** No RF of any kind on the die. WiFi/OCPP connectivity is provided by an external pre-certified module over UART/SPI (fastest regulatory path; never attempt RF on a first SoC).

---

## 3. RTL Language Purity (Gating Design Rule)

**REQ-013 — 100% pure Verilog-2001/2005.** Every synthesizable source file in the design shall be Verilog-2001 or Verilog-2005. Zero SystemVerilog, zero VHDL in synthesizable RTL. (Verification code in Python/cocotb/pyuvm is explicitly allowed and encouraged — it is not RTL.)

**REQ-014 — Zero-SV/VHDL proof at RTL stage.** The RTL stage shall demonstrate, from the final RTL tree, that:
```
find <rtl_root> -name "*.sv" -o -name "*.vhd" -o -name "*.vhdl" | wc -l   # MUST equal 0
```
Any non-zero result is a stage gate FAIL.

**REQ-015 — REUSE sources md5-verified pure Verilog.** Every REUSE source imported from an external repo shall be pinned to an md5-checked commit and shall pass the same zero-SV/VHDL scan before inclusion. Any REUSE source containing SV/VHDL shall be rejected and replaced per its manifest fallback (constraint 13). *(Known flags: wb2axip repo contains `axlite_wrapper.vhd` — excluded from the RTL file list; see manifest MOD-03/MOD-04.)*

**REQ-016 — Banned cores.** Ibex, cv32e40p, pulp-axi, and any other SystemVerilog core are banned from this project. No exceptions.

---

## 4. CPU, Reset & Boot

**REQ-017 — picorv32 CPU.** The CPU shall be the YosysHQ PicoRV32 (RV32IMC class, pure Verilog-2001/2005) used through its native `picorv32_axi` AXI4-Lite master wrapper. *(Replaces cv32e40p per opus §3.6; ISC licence, md5-pinnable.)*

**REQ-018 — Reset vector PROGADDR_RESET = 0x0000_0000.** The CPU reset vector shall be 0x0000_0000 (base of SRAM).

**REQ-019 — Boot modes.** Two boot modes shall be supported:
- **(a) SRAM boot (primary):** firmware pre-loaded into SRAM at 0x0000_0000 by an external host (debug/UART loader), then reset release.
- **(b) SPI flash boot (option):** a small on-chip boot controller (part of MOD-15 system control) copies the first 16 kB of an external SPI flash into SRAM, then releases CPU reset. No hardcoded boot ROM in logic (uses `ifdef SIMULATION` + `$readmemh` pattern for sim where needed).

**REQ-020 — Interrupt aggregation.** picorv32 exposes a single `irq` line; the SoC shall implement a small APB interrupt aggregator (enable/pending/status registers) mapping all peripheral interrupt sources to the single CPU IRQ (see IRQ map §7).

---

## 5. Bus Architecture — 3-Tier AMBA (REQ-030-class rules)

### 5.1 Tiering rule (the "which block attaches where and why" rule)

**REQ-021 — Three-tier AMBA fabric required.** The SoC shall implement AXI4-Lite → AHB3-Lite → APB, connected by two bridges, as the single on-chip interconnect. One fabric, three tiers.

**REQ-022 — Tiering rule (normative).** A block attaches to a tier by its *transaction character*:
1. **AXI4-Lite (top tier)** — multi-master, low-latency, memory-class: the CPU (picorv32 master), the optional DMA (master), and SRAM (slave). Only this tier may have multiple masters.
2. **AHB3-Lite (mid tier)** — *streaming datapaths*: any block whose traffic is continuous sample/frame flow (metering DSP sample ingestion and result bursts; CAN frame FIFO). Single master (the AXI→AHB bridge).
3. **APB (leaf tier)** — *control registers*: every block whose traffic is slow, sparse register reads/writes (CP engine, UART, SPI, I2C, GPIO, timers/PWM, WDT, PMU/system control, SAR ADC/analog control). Single master (the AHB→APB bridge).
4. **Exception rule:** a block with BOTH streaming and register traffic (metering DSP, CAN) attaches its streaming path to AHB and its control registers to APB, or keeps registers in-band on AHB if the register count is ≤ 8 (documented per block in the traceability matrix). Default: registers on APB.

**REQ-023 — Tiering justification (thesis result).** The architecture stage shall quantify the tiering trade-off (measurement, not checkbox): latency/throughput/area of the metering stream on AHB vs forcing it onto AXI4-Lite, and register access on APB vs AHB. This becomes thesis Chapter 3.

**REQ-024 — AXI4-Lite interconnect = verilog-axi (REUSE).** The AXI4-Lite interconnect shall be alexforencich `verilog-axi` (MIT, pure Verilog, GitHub-confirmed 2026-08-19). *(Replaces pulp-axi per opus §3.6.)*

**REQ-025 — Bridges.** Two bridges shall connect the tiers:
- MOD-03 AXI4-Lite → AHB3-Lite bridge.
- MOD-04 AHB3-Lite → APB bridge.
Both are classified **CREATE (fallback)** in the reuse manifest: verification on 2026-08-19 found **no qualified pure-Verilog AXI→AHB bridge** in wb2axip (the repo is Wishbone↔AXI/APB only and contains a `.vhd` wrapper) and no licence-clean pure-Verilog AHB→APB bridge in open sources (GitHub search: hobby repos without licences). Per constraint 13 the small custom bridges (~200–400 lines each) are the honest fallback; `wb2axip` `axil2apb.v` is recorded as an alternative only if the tiering rule is relaxed (see manifest).

### 5.2 Bus topology

```
                 ┌──────────────┐
   picorv32 ─────► AXI4-Lite     │  TOP TIER (multi-master, low-latency)
   (AXI-Lite      │  interconnect│◄──── optional 1-ch DMA (master, deferred)
    master)       └──┬────────┬──┘
                     │        │
              SRAM 16kB      AXI-Lite→AHB bridge (MOD-03)
             (AXIL slave)         │
                          ┌───────▼────────┐  MID TIER (streaming datapaths)
                          │   AHB-lite bus  │
                          │  ┌───────────┐  │
                          │  │Metering   │  │  ← CT/voltage samples (from EXTERNAL ADC)
                          │  │DSP (CREATE)│  │
                          │  └───────────┘  │
                          │  CAN 2.0B FIFO   │
                          └───────┬─────────┘
                             AHB→APB bridge (MOD-04)
                                  │
                    ┌─────────────▼──────────────┐  LEAF TIER (control regs, slow)
                    │            APB bus           │
                    │ CP · UART0/1 · SPI0/1 · I2C  │
                    │ GPIO · TMR/PWM · WDT · PMU   │
                    └─────────────────────────────┘
```

---

## 6. Memory Map

**REQ-026 — AXI4-Lite address map (CPU-visible):**

| Base | Size | Slave | Notes |
|---|---|---|---|
| 0x0000_0000 | 16 kB | SRAM (OpenRAM 16 kB) | Boot target; PROGADDR_RESET = 0x0 |
| 0x4000_0000 | 1 MB window | AXI→AHB bridge (MOD-03) | All AHB/APB devices behind this window |
| 0x7F00_0000 | 4 kB | AXI4-Lite system regs (MOD-15) | CPU-side system control (bridge config, ID, debug) |

*(AXI address space otherwise unmapped → default slave returns error/zero per verilog-axi default responder.)*

**REQ-027 — AHB3-Lite address map (behind MOD-03 window):**

| AHB address | Size | Slave | Notes |
|---|---|---|---|
| 0x4000_0000 | 4 kB | Metering DSP (MOD-06) | Sample ingress FIFO + result/status burst regs (≤8 in-band) |
| 0x4000_1000 | 4 kB | CAN 2.0B frame FIFO (MOD-07) | Stream path: TX/RX frame FIFOs + FIFO status |
| 0x4000_2000 | 4 kB | AHB→APB bridge (MOD-04) | APB tier window |

**REQ-028 — APB address map (behind MOD-04, 4 kB each):**

| APB offset (from 0x4000_2000) | Peripheral | Notes |
|---|---|---|
| 0x0000 | MOD-08 CP engine (IEC 61851) | PWM config, state, fault, level registers |
| 0x1000 | MOD-09 UART0 (debug) | EF_UART |
| 0x2000 | MOD-09 UART1 (WiFi module) | EF_UART |
| 0x3000 | MOD-10 SPI0 (display/EEPROM) | EF_SPI |
| 0x4000 | MOD-10 SPI1 (SPI flash boot) | EF_SPI |
| 0x5000 | MOD-11 I2C0 (RTC/EEPROM) | EF_I2C |
| 0x6000 | MOD-12 GPIO8 | EF_GPIO8 |
| 0x7000 | MOD-13 TMR32 | EF_TMR32 |
| 0x8000 | MOD-13 PWM32 | EF_PWM32 |
| 0x9000 | MOD-14 WDT32 | EF_WDT32 |
| 0xA000 | MOD-15 PMU / clk-rst / INTC / boot ctrl | CREATE |
| 0xB000 | MOD-16 SAR ADC + comparator control | Analog wrapper control |

---

## 7. Interrupt Map

**REQ-029 — IRQ sources → aggregator (single picorv32 `irq`):**

| IRQ# | Source | Trigger | Notes |
|---|---|---|---|
| 0 | UART0 (debug) | RX/TX FIFO events | EF_UART |
| 1 | UART1 (WiFi) | RX/TX FIFO events | EF_UART |
| 2 | SPI0 (display) | transfer done / FIFO | EF_SPI |
| 3 | SPI1 (flash) | transfer done / FIFO | EF_SPI |
| 4 | I2C0 | transaction / error | EF_I2C |
| 5 | GPIO8 | per-pin edge | EF_GPIO8 |
| 6 | TMR32 | compare match | EF_TMR32 |
| 7 | PWM32 | (optional) | EF_PWM32 |
| 8 | WDT32 | timeout → reset + IRQ | EF_WDT32 |
| 9 | CAN 2.0B | RX frame, TX done, bus error | MOD-07 |
| 10 | Metering DSP | Wh accumulation done, sample FIFO threshold | MOD-06 |
| 11 | CP engine | state change, fault latch, CP level change | MOD-08 |
| 12 | SAR ADC | conversion done | MOD-16 |
| 13 | Comparator (zero-cross) | edge | MOD-16 |
| 14 | PMU | brown-out / power status change | MOD-15 |
| 15 | (reserved) | — | — |

Aggregator behaviour: level-sensitive enables + pending/status registers on APB (part of MOD-15).

---

## 8. Clock, Reset & Power

**REQ-030 — 40 MHz core clock (NOT 100 MHz).** The core clock shall be 40 MHz nominal, with a 25 MHz safe fallback configuration. 100 MHz is explicitly cut (sky130 back-end fight; opus §3.5). Fmax shall be *reported as a result*, not assumed.

**REQ-031 — Clock source.** v1 shall accept an external clock (e.g., 10–25 MHz crystal/oscillator) with an on-chip divider to reach 40 MHz/25 MHz; an on-chip PLL is **optional** (analog block budget permitting) and may be skipped entirely for v1. *(PLL remains in the blackbox register as OPTIONAL.)*

**REQ-032 — LDO external.** All power regulation is external (no on-die LDO).

**REQ-033 — Reset.** Asynchronous assert, synchronous deassert reset synchronizer (MOD-15 CREATE). All flops reset to defined states.

**REQ-034 — Clock domains & CDC.** Primary domain: single 40 MHz core domain. Secondary domain: metering sample clock domain if the external ΔΣ ADC streams on its own clock (e.g., 1.024 MHz MCLK) — CDC between sample domain and core domain shall be documented and covered as a verification item (two-flop/async-FIFO synchronisation, formal CDC check at RTL stage).

**REQ-035 — Clock gating.** The metering DSP datapath and CAN shall support clock gating during idle (power chapter input; activity-based power from GLS).

---

## 9. Metering DSP (Flagship CREATE)

**REQ-036 — External 16-bit metering ADC.** The 16-bit metering ADC is **external** (off-chip ΔΣ/ADC chip, e.g., class-0.5s/1 ΔΣ modulator). The SoC ingests the digital bitstream or word samples on a dedicated serial input. No custom high-resolution analog on die. *(On-chip ΔΣ is explicit future work, not v1.)*

**REQ-037 — Digital metrology datapath (CREATE, flagship).** The on-chip metering DSP shall implement:
- CIC/sinc decimation of the external ΔΣ bitstream/sample stream (decimation + low-pass),
- Vrms and Irms computation (per line cycle, sliding window),
- Active power P, reactive power Q, apparent power S,
- Wh (and VAh) accumulation registers with rollover handling,
- Fundamental/harmonic decomposition support (THD reporting hooks for the golden-model comparison),
- Calibration registers: per-channel gain, phase, offset.

**REQ-038 — Fixed-point implementation with documented error model.** All datapath arithmetic shall be fixed-point with a documented Q-format (e.g., Q1.15 / Q0.31 accumulators, 32-bit MACs) and a written error budget: coefficient rounding, truncation, decimation passband ripple, and calibration residual. The architecture stage shall map each error source to the golden-model reference comparison.

**REQ-039 — Accuracy target (class-1 framing, 0.5s stretch).** The metering DSP shall meet **class-1** accuracy framing (IEC 62053-21-style limits, ±1% active energy at reference conditions) with an analysis path toward **0.5s** limits (±0.5%) for the thesis error-model chapter. Budget example (to be refined in architecture):
- Vrms/Irms error ≤ ±0.5% (10–100% of rated, PF ≥ 0.5),
- Active power P error ≤ ±0.8% (class-1 headroom),
- Reactive power Q error ≤ ±1.5%,
- Wh accumulation error ≤ ±1.0% over a 1-hour window at PF ≥ 0.5,
- Validated against the golden model (see golden_model/) over PF ∈ {1.0, 0.95, 0.85, 0.5}, load sweep, and THD ∈ {0, 5, 10, 20}%.

**REQ-040 — Sample streaming & FIFO.** The DSP shall ingest samples via an AHB-accessible input FIFO (stream path), with a programmable threshold IRQ (IRQ 10) and burst-read result registers (Vrms/Irms/P/Q/Wh/status).

---

## 10. CAN 2.0B (REUSE — reclassified from CREATE)

**REQ-041 — CAN 2.0B controller = REUSE.** The CAN controller shall be the OpenCores CAN Protocol Controller (freecores/can, Igor Mohor; SJA1000-class register interface, single CAN node), pure Verilog, LGPL-2.1+ (verified from source headers 2026-08-19; repo has no LICENSE file at root → licence declared in file headers; flagged in manifest). *(Reclassification record: pitch C listed CAN as CREATE; opus review §3.2 reclassifies to REUSE/port — this spec confirms.)*

**REQ-042 — CAN data path.** CAN TX/RX frame FIFOs attach to the AHB tier (streaming); control/status registers (SJA1000-class) on APB via the MOD-07 register sub-block or in-band (≤8 regs) — binding decided in traceability matrix (default: APB window within MOD-07's AHB slave).

**REQ-043 — CAN scope.** Single CAN 2.0B node, standard+extended frames, arbitration + bit-stuffing + CRC-15 per Bosch spec. CAN-FD/TTCAN explicitly out of scope (future work).

---

## 11. Control-Pilot (CP) Engine — IEC 61851 (CREATE)

**REQ-044 — CP engine CREATE (small).** The CP engine shall implement the IEC 61851-1 control-pilot interface: state machine (A/B/C/D/E/F + fault), 1 kHz ± 0.5% PWM generation (duty configurable: 8% D, 10% C, 16% B per standard), and CP level sampling.

**REQ-045 — CP states & safety.** States per IEC 61851-1:
- **A** — no vehicle connected (12 V, no PWM),
- **B** — vehicle connected, not charging (12 V, PWM ≤ 5% idle),
- **C** — charging, ventilation not required (12 V, PWM 16%–96%),
- **D** — charging with ventilation (12 V, PWM ~8%),
- **E/F** — fault conditions (no CP / 0 V) → de-energise the pilot, latch the fault, require a reset/clear.

**REQ-046 — CP safety liveness (formal target).** The CP FSM shall satisfy the safety property: *the pilot is never energised into a charging duty in state A or fault* — targeted for formal verification (SymbiYosys) at RTL stage (thesis Chapter 5).

**REQ-047 — CP sensing.** CP level shall be sampled via the on-chip 12-bit SAR ADC and/or the comparator (CP level detect, zero-cross). PWM generation from the 40 MHz core clock (1 kHz via prescaler).

---

## 12. Analog Blocks (≤ 3 custom, blackboxed)

**REQ-048 — Analog block budget ≤ 3.** Custom analog blocks are limited to:
1. **PLL (OPTIONAL)** — only if the external-clock+divider path proves insufficient; may be omitted for v1,
2. **12-bit SAR ADC** (CP voltage / aux sense) — required,
3. **1–2 comparators** (CP level detect, zero-cross) — required.
All three are blackboxes for synthesis (pin-exact interfaces) with behavioural/dummy models for simulation — see `04_blackbox_register.md`.

**REQ-049 — No custom high-res ADC.** No on-die 16-bit ΔΣ ADC, no on-die LDO, no RF front-end. (REQ-012, REQ-032, REQ-036.)

**REQ-050 — Analog wrapper registers.** SAR ADC + comparator control/status registers on APB (MOD-16, base 0x4000_2000 + 0xB000).

---

## 13. Peripheral Set (REUSE — Efabless)

**REQ-051 — EF_* peripherals.** The following Efabless peripherals (Apache-2.0, pure Verilog, silicon-proven on Efabless MPW shuttles per IP index, STRONG) shall be reused: EF_UART (×2), EF_SPI (×2), EF_I2C (×1), EF_GPIO8 (×1), EF_TMR32 (×1), EF_PWM32 (×1), EF_WDT32 (×1). All attach to APB via their APB wrappers.

**REQ-052 — EF_PWM32 index gap.** EF_PWM32 (efabless/EF_PWM32, Apache-2.0 header-verified 2026-08-19, dual-channel 32-bit PWM) is **not yet in the IP index** — it shall be registered in `IP/INDEX.md` during the reuse-qualification pass (manifest flag). Fallback if unavailable: EF_TMR32 PWM output mode.

**REQ-053 — OCPP/WiFi external.** The OCPP 1.6J stack is firmware (runs on picorv32 / external host) and the WiFi link is an external pre-certified module over UART1/SPI1. Nothing OCPP/WiFi is RTL. OCA conformance is a product-phase activity (partner OEMs absorb system-level certification).

---

## 14. Non-Functional & Thesis Requirements

**REQ-054 — Verification flow.** Verification shall be coverage-driven cocotb/PyUVM over Verilator (matches existing toolchain: tabbypy3 3.11 venv, venv-bin-first PATH), with formal verification (SymbiYosys) of the CP FSM and CAN arbitration/bit-stuffing properties. This is a first-class thesis pillar (Chapter 6).

**REQ-055 — Golden model.** A deterministic metering-accuracy golden model (double-precision reference for Vrms/Irms/P/Q/S/Wh) shall exist in `golden_model/`, sweeping power factor, load, and harmonic content, with N=3 seed determinism proof (see golden_model README + determinism.json). This is the accuracy reference for the metering DSP at verification time.

**REQ-056 — GLS + CDC analysis.** Gate-level simulation with back-annotated SDF, plus CDC review (metering sample domain ↔ core domain) is a required thesis deliverable (Chapter 7) — the RTL→silicon gap chapter.

**REQ-057 — Physical sign-off report.** OpenLane hardening report with area, timing (Fmax), and power (activity-based from GLS) is required (REQ-010).

**REQ-058 — Scope guardrails (hard).** Deferred/cut: on-die WiFi/RF, 100 MHz, 64 kB SRAM, on-chip 16-bit ADC, from-scratch CAN, OCPP/ISO 15118 in RTL, full descriptor DMA, CAN-FD/TTCAN, tapeout. Optional DMA (MOD-16) is CREATE-lite and deferred until a measured CPU-copy bottleneck justifies it.

**REQ-059 — IP licence discipline.** Every REUSE module carries a manifest entry with source, licence, md5-pinnable commit, and — where licence/availability is uncertain — an explicit fallback. Never silently assumed (constraint 13).

**REQ-060 — Doc traceability.** Every requirement shall be traceable to a module and to a configuration/register binding in `03_traceability_matrix.md`.

---

## 15. Module List (per opus §3.2, verified 2026-08-19)

| # | Module | Class | Bus attach | Source / note |
|---|---|---|---|---|
| MOD-01 | picorv32 CPU (RV32IM) | REUSE | AXI4-Lite master | YosysHQ/picorv32 `picorv32_axi.v` — ISC, pure Verilog (verified) |
| MOD-02 | AXI4-Lite interconnect | REUSE | — | alexforencich/verilog-axi — MIT, pure Verilog (verified) |
| MOD-03 | AXI-Lite→AHB bridge | CREATE (fallback) | AXI4-Lite↔AHB | **No qualified pure-Verilog AXI→AHB bridge found (2026-08-19); small custom bridge; wb2axip evaluated — Wishbone↔AXI only** |
| MOD-04 | AHB→APB bridge | CREATE (fallback) | AHB↔APB | **No licence-clean pure-Verilog AHB→APB found; small custom bridge (~200 lines); wb2axip `axil2apb.v` alternative only if tiering relaxed** |
| MOD-05 | SRAM 16 kB | REUSE | AXI4-Lite slave | OpenRAM sky130 macros + behavioural Verilog model for sim (BSD-3-Clause) |
| MOD-06 | Metering DSP datapath | **CREATE (flagship)** | AHB slave (stream) | CIC/sinc + Vrms/Irms + P/Q/S + Wh + calib (REQ-037/038/039) |
| MOD-07 | CAN 2.0B controller | REUSE (port) | AHB (FIFO) + APB (regs) | OpenCores freecores/can — LGPL-2.1+, pure Verilog (verified) |
| MOD-08 | Control-Pilot (CP) engine | CREATE (small) | APB | IEC 61851 FSM + 1 kHz PWM + comparator sampling (REQ-044/045) |
| MOD-09 | UART ×2 (debug, WiFi) | REUSE | APB | EF_UART (Apache-2.0) |
| MOD-10 | SPI ×2 (display, flash) | REUSE | APB | EF_SPI (Apache-2.0) |
| MOD-11 | I2C ×1 (RTC/EEPROM) | REUSE | APB | EF_I2C (Apache-2.0) |
| MOD-12 | GPIO ×8 | REUSE | APB | EF_GPIO8 (Apache-2.0) |
| MOD-13 | Timer + PWM | REUSE | APB | EF_TMR32 + EF_PWM32 (Apache-2.0; PWM32 index gap REQ-052) |
| MOD-14 | Watchdog | REUSE | APB | EF_WDT32 (Apache-2.0) |
| MOD-15 | clk/reset + PMU + INTC + boot ctrl | CREATE (small) | APB + AXI sys regs | clock gating, reset sync, power/status regs, IRQ aggregator, SPI-flash boot controller (REQ-019/020/033) |
| MOD-16 | SAR ADC + comparators (analog) | BLACKBOX | APB (ctrl) | 12-bit SAR ADC + 1–2 comparators — blackbox for synth, dummy for sim (REQ-048, 04_blackbox_register.md) |
| MOD-17 | *(optional)* 1-ch DMA | CREATE-lite (defer) | AXI4-Lite master | Only if metering→SRAM copy is a measured CPU bottleneck (REQ-058) |

**CREATE count (core): 5** — MOD-03 (AXI→AHB bridge), MOD-04 (AHB→APB bridge), MOD-06 (metering DSP, flagship), MOD-08 (CP engine), MOD-15 (clk/reset+PMU+INTC+boot). **REUSE count: 10** — MOD-01, MOD-02, MOD-05, MOD-07, MOD-09, MOD-10, MOD-11, MOD-12, MOD-13, MOD-14. Blackbox analog: MOD-16. Deferred: MOD-17 (CREATE-lite, optional DMA). Reuse ratio (core 15, excluding optional DMA): **10 REUSE / 15 = 0.667**; with optional DMA: 10/16 = 0.625. *(Opus §3.2 listed 12/15 = 0.80 under its "wb2axip REUSE" assumption; the verified classification moves both bridges to CREATE-fallback → 0.667. Documented deviation, see manifest §5.)*

---

## 16. Open Questions / Assumptions

| # | Item | Status | Action |
|---|---|---|---|
| A1 | EF_PWM32 not in IP index | FLAG | Register during reuse qualification (REQ-052); fallback EF_TMR32 PWM |
| A2 | OpenCores CAN repo has no LICENSE file at root | FLAG | Licence declared in source headers (LGPL-2.1+); confirm with maintainers before any commercial path; thesis use fine |
| A3 | wb2axip has NO AHB bridge | DECISION | Bridges MOD-03/04 = CREATE fallback (REQ-025); wb2axip no longer a REUSE dependency |
| A4 | External ΔΣ ADC part number | ASSUME | TBD in architecture stage (e.g., class-1 ΔΣ with MCLK ≤ 2.048 MHz); interface kept generic (bitstream + MCLK) |
| A5 | SPI flash boot controller size | ASSUME | Small (~1–2 k cells); part of MOD-15; may be deferred to firmware-assisted boot via UART if timeline tight |
| A6 | CP PWM duty mapping (B/C/D) | ASSUME | Per IEC 61851-1: B ≤ 5% idle, C 16–96%, D ~8%; verify against latest standard text in architecture stage |
| A7 | Class-1 vs 0.5s claim | ASSUME | Spec targets class-1 with 0.5s analysis path (REQ-039); no legal-metrology claims (REQ-005) |

---

*End of system specification. 60 numbered requirements (REQ-001 … REQ-060).*
