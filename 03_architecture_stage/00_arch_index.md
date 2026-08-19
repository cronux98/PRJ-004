# EVCore-MY — Architecture Stage Index & REQ Trace Summary
## PRJ-004 / v0 / 03_architecture_stage / 00_arch_index.md

*Version 1.0 | 2026-08-19 | Architecture stage — entry point and completion record for the
architecture stage of PRJ-004 (EVCore-MY). All paths absolute. Handoff contract for the RTL
wave (`04_frontend_stage`).*

---

## 1. Stage artifacts (7/7)

| # | Artifact | Path | Status | Content |
|---|---|---|---|---|
| AR-01 | System architecture | `/home/smdadmin/hermes_workspace/projects/PRJ-004/v0/03_architecture_stage/01_ARCHITECTURE.md` | DONE (62.7 kB / 983 lines) | Block diagram (mermaid + ASCII), 3-tier bus topology + tiering rule + master/slave map, 3-tier address map, clock/reset strategy @40 MHz (25 MHz fallback) + CDC points, boot/reset flow (both modes), IRQ map, module-by-module for all 17 modules (MOD-01…MOD-17, no adds/drops), CSR summary, coding constraints, analog budget, A1–A7 + AR-1 resolution |
| AR-02 | Memory map (machine-readable) | `/home/smdadmin/hermes_workspace/projects/PRJ-004/v0/03_architecture_stage/02_memory_map.json` | DONE (13.4 kB, valid JSON) | 3 tiers (AXI 3 windows / AHB 3 windows / APB 12 windows), 17-module addresses, IRQ map (0–15), reserved gaps, MOD-17 DMA port reserved |
| AR-03 | RTL feasibility review | `/home/smdadmin/hermes_workspace/projects/PRJ-004/v0/03_architecture_stage/03_rtl_feasibility_review.md` | DONE (18.9 kB) | Verdict **FEASIBLE**; gate estimates per module (17), SRAM plan, analog stub list, area estimate vs 1–3 mm², contingency cuts C1–C6 (not required) |
| AR-04 | Golden-model comparison contract | `/home/smdadmin/hermes_workspace/projects/PRJ-004/v0/03_architecture_stage/04_architecture_model.md` | DONE (20.0 kB / 322 lines) | MOD-06 ↔ golden_model interface contract, Q-format, golden-field mapping, REQ-039 tolerances, 64-scenario methodology, pass/fail criteria |
| AR-05 | Safety architecture | `/home/smdadmin/hermes_workspace/projects/PRJ-004/v0/03_architecture_stage/05_safety_architecture.md` | DONE (25.6 kB) | IEC 61851 CP FSM safety analysis, never-energise structural property (P1), fault latch, two watchdog nets, metering calibration-lock + tamper hooks, formal targets P1–P5, B2B non-certification framing |
| AR-06 | sky130 subsystem plan | `/home/smdadmin/hermes_workspace/projects/PRJ-004/v0/03_architecture_stage/06_sky130_subsystem.md` | DONE (18.9 kB) | Pad ring (~48–52 pads), clock plan (external XO + divider; PLL optional, not v1), SAR ADC + comparators (2 of ≤3 analog), external ΔΣ ADC interface, external LDO + PGOOD, OpenRAM 16 kB plan, single power domain + always-on PMU logic, reset synchronisation, floorplan intent |
| AR-07 | Stage index (this file) | `/home/smdadmin/hermes_workspace/projects/PRJ-004/v0/03_architecture_stage/00_arch_index.md` | DONE | Stage index + REQ trace summary + handoff |

*All 7 targets verified present and non-empty on 2026-08-19 (AR-01/AR-02 launcher-verified;
AR-04 manually verified after launcher exit-5 post-write; AR-03/AR-05/AR-06/AR-07 written
natively per Vera direction).*

---

## 2. REQ trace summary (60 REQs — which artifacts satisfy which groups)

The full REQ→module→binding trace lives in `02_specification_stage/03_traceability_matrix.md`;
this table is the architecture-stage satisfaction map — each REQ group and the artifact(s)
that carry its architecture-level satisfaction.

| REQ group | Requirements | Satisfied in |
|---|---|---|
| Product / market framing | REQ-001…REQ-005 | AR-01 §1.1; AR-05 §0/§3.2/§6 (non-billing REQ-005). **REQ-003** (NIMP 2030 policy positioning) is a business-stage requirement with no architectural mechanism — carried unchanged from `02_specification_stage` (traceability matrix binding), disposition: satisfied by product positioning, not by silicon; no architecture action required. |
| Physical budget | REQ-006…REQ-011 | AR-01 §1.2; AR-03 §0/§5/§6; AR-06 §1 |
| No on-die radio | REQ-012 | AR-01 §1.2; AR-06 §1 |
| Language purity / banned cores | REQ-013…REQ-016 | AR-01 §0/§1.3/§11 (zero SV/VHDL, no ibex/cv32e40p/pulp-axi) |
| CPU / boot / IRQ | REQ-017…REQ-020 | AR-01 §4 (picorv32 config), §6 (boot flows), §7 (IRQ map); AR-02 (interrupt_map) |
| Bus architecture (3-tier AMBA) | REQ-021…REQ-028 | AR-01 §2 (tiering rule, justification, master/slave map), §3 (address maps, AR-1); AR-02 (full map) |
| IRQ aggregator map | REQ-029 | AR-01 §7; AR-02 interrupt_map |
| Clock / reset / CDC / gating | REQ-030…REQ-035 | AR-01 §5; AR-06 §3/§4; AR-05 §1.4/§4 (reset safety) |
| Metering ADC external | REQ-036 | AR-01 §5.1/§8.6 (A4); AR-06 §5.4 |
| Metering DSP / accuracy / FIFO | REQ-037…REQ-040 | AR-01 §8.6 (datapath, Q-format, error budget, windows); AR-04 (golden contract, tolerances); AR-03 §2/§4 (area/timing) |
| CAN 2.0B | REQ-041…REQ-043 | AR-01 §8.7 (in-band AHB exception, SJA1000-class); AR-02 (MOD-07 window) |
| CP engine / safety | REQ-044…REQ-047 | AR-01 §8.8/§9 (FSM, duty map A6, structural property); AR-05 (full safety analysis, P1–P4); AR-02 (IRQ 11/12/13) |
| Analog budget / wrapper | REQ-048…REQ-050 | AR-01 §8.16/§12; AR-06 §5; AR-02 (MOD-16 APB slot) |
| EF_* peripherals | REQ-051…REQ-052 | AR-01 §8.9–§8.14 (A1 fallback at same slot); AR-02 (APB slots 0x1000–0x9000) |
| OCPP/WiFi external | REQ-053 | AR-01 §1.1/§8.9; AR-02 (UART1) |
| Verification / golden / GLS / sign-off | REQ-054…REQ-057 | AR-01 §14 (formal/CDC targets); AR-04 (golden comparison contract); AR-05 §5 (formal targets P1–P5); AR-03 §3/§8 (backend items); AR-06 §7 (floorplan handoff) |
| Scope guardrails | REQ-058 | AR-01 §8.17 (DMA deferred, port reserved); AR-03 §2 (MOD-17 = 0 cells) |
| Licence discipline / traceability | REQ-059…REQ-060 | AR-01 §0/§11 (REUSE/CREATE rule, md5 pinning); this index + `02_reuse_manifest.json` |

**Coverage statement:** all 60 REQs are carried at architecture level — none is dropped,
silently re-interpreted, or left without an owning artifact. Every REQ not fully "closed" at
architecture stage has an explicit open item naming the RTL/verification stage action (§5).

---

## 3. Module count and classification (17 modules, spec §15 — no adds, no drops)

| Class | Count | Modules |
|---|---|---|
| REUSE_INTERNAL | 6 | MOD-09 (EF_UART ×2), MOD-10 (EF_SPI ×2), MOD-11 (EF_I2C), MOD-12 (EF_GPIO8), MOD-13 (EF_TMR32 + EF_PWM32), MOD-14 (EF_WDT32) |
| REUSE_GITHUB | 4 | MOD-01 (picorv32, ISC), MOD-02 (verilog-axi, MIT), MOD-05 (OpenRAM, BSD-3), MOD-07 (freecores/can, LGPL-2.1+) |
| CREATE | 5 | MOD-03 (AXI→AHB bridge), MOD-04 (AHB→APB bridge), MOD-06 (Metering DSP — flagship), MOD-08 (CP engine), MOD-15 (clk/rst + PMU + INTC + boot) |
| BLACKBOX | 1 | MOD-16 (SAR ADC + comparator ×2 analog, BB-02/03; BB-04 PLL optional, not v1) |
| DEFERRED | 1 | MOD-17 (optional DMA, REQ-058 — port reserved, 0 cells) |
| **Total** | **17** | |

- Reuse ratio (core): **10/15 = 0.667** (manifest summary; excludes BLACKBOX MOD-16 and
  deferred MOD-17). With deferred DMA: 10/16 = 0.625.
- All licences verified 2026-08-19 (ISC/MIT/BSD-3/Apache-2.0/LGPL-2.1+); flags carried:
  A1 EF_PWM32 index gap, A2 CAN repo no root LICENSE (LGPL headers), A3 bridges CREATE
  fallback (wb2axip has no AHB bridge).

---

## 4. Bus map summary (3-tier AMBA, REQ-021)

| Tier | Masters | Slaves | Windows |
|---|---|---|---|
| **AXI4-Lite** (top) | M0 picorv32 · M1 MOD-15 boot-copy (boot-only) · M2 reserved (MOD-17) | S0 SRAM 16 kB `0x0000_0000` · S1 MOD-03 bridge (1 MB) `0x4000_0000` · S2 MOD-15 sys regs `0x7F00_0000` | 3 (REQ-026) |
| **AHB3-Lite** (mid) | M0 MOD-03 (sole) | S0 MOD-06 Metering DSP `0x4000_0000` · S1 MOD-07 CAN `0x4000_1000` · S2 MOD-04 APB window `0x4000_2000` (48 kB per AR-1) | 3 (REQ-027) |
| **APB** (leaf) | M0 MOD-04 (sole) | 12 peripherals `0x4000_2000`–`0x4000_DFFF`: MOD-08 CP · MOD-09 UART0/1 · MOD-10 SPI0/1 · MOD-11 I2C0 · MOD-12 GPIO8 · MOD-13 TMR32/PWM32 · MOD-14 WDT32 · MOD-15 PMU/INTC · MOD-16 SAR/CMP | 12 (REQ-028) |

- Tiering rule (REQ-022): AXI = memory-class multi-master; AHB = streaming datapaths
  (MOD-06 sample FIFO, MOD-07 frame FIFO + their ≤8 in-band registers); APB = control
  registers (9 leaf peripherals). Quantified trade-off table in AR-01 §2.2 (REQ-023
  measurement target for RTL stage).
- IRQ map: 16 sources (IRQ 0–15, single aggregated line to picorv32 `irq[3]`, aggregator in
  MOD-15) — AR-01 §7, AR-02.

---

## 5. Feasibility verdict (AR-03)

**FEASIBLE — architecture-stage estimate.**

- Cells: ~57–62 k central (range 48–75 k) vs REQ-008 60–100 k — inside band.
- Area: ~1.5–2.0 mm² die (core ~1.2–1.6 mm² incl. SRAM ~0.5–0.75 mm² + pad ring ~0.3–0.5 mm²)
  vs REQ-007 1–3 mm² — inside band, no 32 kB SRAM stretch required (REQ-009).
- Timing: 40 MHz plausible on sky130hd (multi-cycle CPU, enable-rate-bounded DSP, trivial
  CAN/CP paths); 25 MHz is a config-level fallback (REQ-030), not a rescue.
- Analog: 2 of ≤3 blocks used (REQ-048); PLL not instantiated.
- Contingency (NOT required, pre-agreed): cuts C1–C6 (25 MHz, EF_PWM32→EF_TMR32 fallback,
  single UART, PWM slot deferral, FIFO sizing, THD hooks) — none touch the thesis pillars
  (metering accuracy, CP safety).

---

## 6. Assumption resolution (spec §16 A1–A7 + AR-1)

| # | Item | Disposition | Where |
|---|---|---|---|
| A1 | EF_PWM32 not in IP index | **CARRIED** — primary target at APB `0x8000`; register during RTL-stage reuse qualification (REQ-052); fallback EF_TMR32 PWM mode at the same slot, no address/map change | AR-01 §8.13/§13; AR-02 (slot 0x8000); AR-03 C2 |
| A2 | OpenCores CAN no root LICENSE | **CARRIED** — LGPL-2.1+ declared in headers; thesis use fine per manifest; commercial path needs maintainer confirmation; fallback recorded (Apache-2.0 rewrite or licensed mirror) | AR-01 §8.7/§13; AR-03 §2 |
| A3 | wb2axip has no AHB bridge | **DECISION (confirmed)** — MOD-03/MOD-04 are CREATE custom bridges (~300–400 / ~200 lines); wb2axip is not a dependency anywhere; interfaces + address decode specified | AR-01 §8.3/§8.4/§13; AR-02; AR-03 §2 |
| A4 | External ΔΣ ADC part TBD | **RESOLVED (generic)** — Option A 1-bit bitstream baseline, `mclk_adc` 2.0/1.92 MHz ≤ 2.048 MHz, CIC R=40 order-3, 1000 samples/cycle; no part number named (BOM decision); generic `adc_ext_if` contract is sufficient | AR-01 §5.1/§8.6/§13; AR-06 §5.4 |
| A5 | SPI flash boot controller size | **RESOLVED** — dedicated bit-banged SPI master FSM in MOD-15, ~1–2 k cells, independent of EF_SPI1; matches original estimate | AR-01 §6.3/§13; AR-03 §2 (MOD-15) |
| A6 | CP PWM duty mapping | **RESOLVED** — REQ-045 canonical: B ≤5%, C 16–96%, D ~8%; REQ-044's figures superseded; state-gated duty mux makes the map structural | AR-01 §8.8/§9/§13; AR-05 §1.1 |
| A7 | Class-1 vs 0.5s claim | **CARRIED + partially resolved** — fast (1-cycle) + class (25-cycle/0.5 s) accumulation windows; no legal-metrology claim (REQ-005); verification-stage action: regenerate `golden_model.py` with `N_CYCLES=25` | AR-01 §8.6/§13/§14; AR-04 §1/§7/§8 |
| AR-1 | REQ-027 4 kB vs REQ-028 48 kB APB inconsistency (new, architecture-stage) | **RESOLVED** — REQ-027's "4 kB" = AHB slave-select decode granularity; bridge passes low 16 bits → 48 kB downstream APB range, all REQ-028 bases ±0 preserved | AR-01 §3.2/§13; AR-02 (MOD-04 window 0x0000C000) |

**Disposition summary:** 3 DECISION/RESOLVED (A3, A4, A5, A6 — 4 resolved), 3 CARRIED
(A1, A2, A7), 1 new clarification (AR-1) resolved. Zero assumptions silently dropped.

---

## 7. Open questions carried to RTL / verification stage (the RTL wave's to-do list)

From AR-01 §14, AR-03 §8, AR-04 §8, AR-05 §8, AR-06 §9 — consolidated:

| # | Item | Owner stage | Blocking? |
|---|---|---|---|
| 1 | REQ-023 quantified bus trade-off (replace AR-01 §2.2 estimates with measured Verilator cycles + OpenLane area) | RTL + backend | no — thesis Ch.3 result |
| 2 | CDC formal proof at the ΔΣ ADC boundary (2FF + async FIFO structure fixed; proof is the deliverable, REQ-034/056) | RTL (formal) | no — structure fixed |
| 3 | CP safety formal proofs P1–P4 (SymbiYosys BMC/induction; cones fixed) | RTL (formal) | no — REQ-046/054 |
| 4 | Golden-model window alignment: regenerate `golden_model.py` with `N_CYCLES=25` (0.5 s) before class-window comparison | verification | yes — for class-window closure (A7) |
| 5 | MOD-06 sample FIFO depth (architecture minimum 1000; size down after burst-read cadence measured) | RTL | no |
| 6 | EF_PWM32 RTL-stage qualification (A1) or EF_TMR32 PWM fallback — same APB slot 0x8000 | RTL (reuse import) | no — slot fixed |
| 7 | Bit-level CSR definitions (AR-01 §10 is register-block level) | RTL | no |
| 8 | Exact AHB register offsets for MOD-06 result regs within the 4 kB window (Q-format + golden mapping fixed in AR-04) | RTL | no |
| 9 | S_REG tolerance confirmation (AR-04 §5: inherits P's ±0.8%; confirm or tighten) | verification | no |
| 10 | CALIB_LOCK semantics (sticky-until-reset recommended) + WDT window values + PMU clock-fail thresholds | RTL | no — behavior fixed, values TBD |
| 11 | Oscillator choice Option A (external 40 MHz-capable XO, v1 default) vs Option B (crystal + PLL later) | product/BOM (RTL keeps both divider paths) | no |
| 12 | OpenRAM macro generation + characterization (first backend task; macro required for sign-off) | backend | yes for sign-off |
| 13 | Analog macro availability in local sky130 flow (SAR/cmp); fallback = external SAR over SPI + comparator-only CP (manifest) | backend/RTL | no — fallback recorded |
| 14 | DFT plan (scan on digital, SRAM test pins, analog excluded; 2–4 test pads reserved) | RTL + backend | no |
| 15 | Tamper heuristics thresholds (Irms-without-CP, drift windows) — hooks in RTL, values in firmware | firmware (post-RTL) | no |

---

## 8. Stage completion record

- Architecture stage deliverables: **7/7 complete** (this index + AR-01…AR-06), all traced to
  REQ ids, all consistent with `02_specification_stage` inputs (spec 60 REQs, reuse manifest,
  traceability matrix, blackbox register, golden model).
- Scope respected: architecture stage only — no RTL written, no verification pipeline, no
  git push (Vera gates and pushes). No kanban sub-tasks created.
- Handoff: the RTL wave (`04_frontend_stage`) builds against AR-01 (contract), AR-02
  (address map), AR-04 (golden comparison), AR-03 (feasibility + cuts), AR-05 (safety
  properties), AR-06 (silicon plan) — with §7 as its open-questions checklist.

*End of architecture stage index.*
