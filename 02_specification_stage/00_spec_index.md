# PRJ-004 EVCore-MY — Specification Stage Index

*02_specification_stage | 2026-08-19 | status: COMPLETE*

EVCore-MY (CANDIDATE-C) — smart EV AC-charger controller SoC: energy-metrology
DSP + CAN 2.0B + IEC 61851 control-pilot + OCPP-ready host (WiFi external).
Standalone sky130A die (NO Caravel), picorv32 @ 40 MHz, 16 kB OpenRAM SRAM,
3-tier AMBA (AXI4-Lite → AHB3-Lite → APB), pure Verilog-2001/2005 only.

## Deliverables

| # | File | Description | Status |
|---|---|---|---|
| 1 | `01_system_spec.md` | System specification: 60 numbered requirements (REQ-001…REQ-060), module list (17 rows), memory map (3 tiers), IRQ map (16 sources), clock/reset/boot, metering accuracy targets, CP safety states, product requirements | ✅ |
| 2 | `02_reuse_manifest.json` | Module classification REUSE_INTERNAL / REUSE_GITHUB / CREATE / BLACKBOX with source + licence + md5-pinnable commits + flags; reuse_ratio 0.667 core (10/15), 0.625 with deferred DMA (10/16) | ✅ |
| 3 | `03_traceability_matrix.md` | REQ → module → config/register binding, 60/60 REQs bound, 30+ config keys | ✅ |
| 4 | `04_blackbox_register.md` | sky130 analog + SRAM stubs: BB-01 OpenRAM 16 kB, BB-02 SAR ADC 12-bit, BB-03 comparator ×2, BB-04 PLL (optional); pin-exact interfaces + behavioural model notes + external ΔΣ ADC pin contract | ✅ |
| 5 | `golden_model/` | Metering accuracy golden model: 64 scenarios (PF × load × THD), double-precision Vrms/Irms/P/Q/S/Wh/THD, 11/11 self-tests, determinism N=3 → `identical: true` | ✅ |
| 6 | `00_spec_index.md` | This index | ✅ |

## Key numbers (Finish report data)

- **Requirements:** 60 (REQ-001…REQ-060)
- **Modules:** 17 (16 core + optional DMA): 10 REUSE, 5 CREATE, 1 BLACKBOX analog, 1 deferred CREATE
- **CREATE core blocks:** metering DSP (flagship), CP engine, clk/reset+PMU+INTC+boot, AXI→AHB bridge (fallback), AHB→APB bridge (fallback)
- **Reuse ratio:** 0.667 core (10/15); 0.625 with optional DMA (10/16)
  *(Opus §3.2 estimated 0.80 assuming wb2axip covered the AXI→AHB bridge;
  verification on 2026-08-19 showed wb2axip has no AHB bridge → both bridges
  reclassified CREATE-fallback. Deviation documented in manifest §5.)*
- **Memory map:** SRAM 0x0000_0000 (16 kB) | AXI→AHB window 0x4000_0000 |
  AHB: DSP 0x4000_0000, CAN 0x4000_1000, APB window 0x4000_2000 |
  APB: 12 × 4 kB slots (CP…SAR) | AXI sys regs 0x7F00_0000
- **IRQ map:** 16 sources aggregated to single picorv32 `irq`
- **Clock:** 40 MHz core (25 MHz fallback), external clock + divider v1, PLL optional
- **Golden model determinism:** identical=true, 3/3 runs, tests MD5
  `b35ac2cbe14b8a9055aa978a4fc23c27`, per-run logs with PID+timestamp

## Licence verification performed (2026-08-19, evidence in manifest)

| Source | Licence | Verified from |
|---|---|---|
| YosysHQ/picorv32 | ISC | GitHub API (license=ISC), language=Verilog |
| alexforencich/verilog-axi | MIT | GitHub API (license=MIT), language=Verilog |
| ZipCPU/wb2axip | Apache-2.0 | source headers + README; **no AHB bridge present** (flag) |
| freecores/can (OpenCores CAN) | LGPL-2.1+ | source file headers; **no LICENSE file at repo root** (flag) |
| efabless/EF_PWM32 | Apache-2.0 | EF_PWM32.v header; **not in IP index** (flag) |
| VLSIDA/OpenRAM | BSD-3-Clause | IP index (STRONG) |
| EF_UART/SPI/I2C/GPIO8/TMR32/WDT32 | Apache-2.0 | IP index (STRONG, silicon-proven) |

## Open questions / assumptions (detail in spec §16)

A1 EF_PWM32 index gap → register during reuse qualification
A2 OpenCores CAN: LGPL-2.1+ declared in headers, no root LICENSE → confirm for
   commercial path (thesis use fine)
A3 wb2axip lacks AHB bridge → bridges MOD-03/04 are CREATE fallback
A4 External ΔΣ ADC part TBD in architecture stage (interface kept generic)
A5 SPI-flash boot controller size ~1–2 k cells (MOD-15); UART-assisted boot
   fallback if timeline tight
A6 CP PWM duty mapping per IEC 61851-1 (B ≤5% idle, C 16–96%, D ~8%) — verify
   against current standard text in architecture stage
A7 Class-1 target with 0.5s analysis path; no legal-metrology claims

## Scope guardrails honoured

No Caravel (REQ-006) · pure Verilog-2001/2005 (REQ-013/014) · 3-tier AMBA with
tiering rule (REQ-021/022) · 40 MHz not 100 MHz (REQ-030) · external 16-bit
metering ADC, digital metrology on-die (REQ-036/037) · CAN REUSE not CREATE
(REQ-041) · CP engine CREATE (REQ-044) · OCPP/WiFi off-chip (REQ-053) ·
verified RTL + OpenLane sign-off + GLS, no tapeout (REQ-010/057) ·
uncertain-licence IP flagged with fallbacks (REQ-059).

## Handoff to next stage

Architecture stage consumes: 01_system_spec.md (REQs + module list + maps),
02_reuse_manifest.json (pinned sources + fallbacks), 03_traceability_matrix.md
(config keys), 04_blackbox_register.md (pin-exact analog/SRAM contracts),
golden_model/ (accuracy reference + determinism proof).
