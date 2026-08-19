# PRJ-004 (NEW) — Market Requirements: MoSCoW per Candidate + IP Mapping
Model: deepseek-v4-flash | Date: 2026-08-19 | Stage: 01_business_stage

Baselines referenced from baseline_metrics.json (every metric reconciled there).
IP references are IP/index.md line items (T1 evidence, idx# = index row).

---

## Common hard constraints (owner, non-negotiable)
- Full SoC on sky130, high-performance OR low-power positioning.
- 3-tier AMBA hierarchy AXI4-Lite -> AHB -> APB with genuine multi-master streaming+control.
- Pure Verilog-2001/2005. Zero SystemVerilog/VHDL.
- Retail < RM150. Target M40/T20 urban (KL/Selangor/Penang/JB) + nationwide potential.
- Wireless where it strengthens the idea — in-house CREATE if no qualifying block exists.
- Baseline: Ibex-class CPU 25kGE @ 100MHz (idx#13), cv32e40p 40kGE (idx#15), pulp-axi (idx#18),
  OpenRAM (idx#25), Caravel user area 3.1x3.8mm (baseline_metrics.json, T1).

---

## CANDIDATE-A: BanjirSense-MY (flood early-warning node; LOW-POWER)

### MoSCoW
| Priority | Requirement | Value/Constraint | Evidence |
|---|---|---|---|
| MUST | Sub-GHz mesh radio (433/915MHz FSK), digital baseband + MAC in-house | packet engine + duty-cycled listen; no LoRaWAN fees | corpus S35 (T2 gap), S43 (T1) |
| MUST | Multi-channel 12-bit SAR ADC (8ch, 100kSPS) for ultrasonic/level + rain + battery | sky130 analog (T1/T5) | baseline_metrics.json |
| MUST | Wake-on-comparator deep sleep <10uA @1.8V; solar/battery power path | low-power positioning | baseline_metrics.json (target) |
| MUST | 32kB SRAM (OpenRAM) + DMA streaming of sensor/radio FIFOs | AXI4-Lite: CPU+DMA; AHB: streaming; APB: control | IP index idx#25, #18 |
| MUST | Retail RM129-149 (< RM150) | BOM <= RM90 | candidates_scores.json A-UE |
| SHOULD | Ultrasonic capture engine (waterproof JSN-SR04T-class, 20-600cm) | reuse ip-005-ultrasonic | IP index idx#45 |
| SHOULD | Local alarm + siren driver + GPIO alert bus | per-community alerting | S07 (T2) |
| SHOULD | UART/I2C debug + field flash; solar charge controller logic | ops | IP index idx#33, #31 |
| COULD | Rain-gauge counter, temperature, battery health telemetry | sensor richness | — |
| WON'T (v1) | LoRaWAN/GPS on-die (module attach option only) | scope control | — |

### IP mapping (IP/index.md rows)
- REUSE: lowrisc-ibex (13), pulp-axi (18), vlsida-openram (25), ip-005-spi-host (32),
  ip-005-uart (33), fossi-ef-gpio8 (39), fossi-ef-tmr32 (40), fossi-ef-wdt32 (41),
  ip-005-interrupt-ctrl (55), ip-005-power-mgr (54), ip-005-ultrasonic (45), ip-003-i2c (31).
- PARTIAL: PLL + LDO + SAR ADC + comparator (sky130 analog — design to spec; no index entry).
- CREATE: Sub-GHz FSK PHY + packet engine + mesh MAC (digital, Verilog-2001) — no open
  equivalent (S35 T2); ADC-capture DMA engine; wake/event manager; RF front-end (analog, high
  risk -> external FE fallback documented in baseline_metrics.json).

---

## CANDIDATE-B: JagaCare-MY (elderly aging-in-place monitor; LOW-POWER)

### MoSCoW
| Priority | Requirement | Value/Constraint | Evidence |
|---|---|---|---|
| MUST | 2.4GHz GFSK (BLE-class) baseband + link layer in-house; external RF FE fallback | wearable link to hub/phone | S35 (T2), S36 (T1) |
| MUST | 4ch 12-bit SAR ADC @50kSPS for PPG bio path + battery | sky130 analog | baseline_metrics.json |
| MUST | IMU interface (SPI) + on-device fall/activity DSP accelerator (feature extract + threshold/ML) | privacy-first, no cloud | S20 (T4) competitors are cloud |
| MUST | Deep sleep <20uA; RTC wake; low duty-cycle link events | low-power positioning | baseline_metrics.json (target) |
| MUST | 32kB SRAM + DMA streaming (ADC/IMU -> DSP -> radio) | 3-tier AMBA as candidate A | IP index |
| MUST | Retail RM139-149; home hub option RM99 | BOM wearable <= RM85 | candidates_scores.json B-UE |
| SHOULD | SOS button + audio alert path (buzzer/voice via PWM) | safety UX | S18 (T3) |
| SHOULD | PPG heart-rate (or HRV) with motion-artifact rejection | health value | — |
| SHOULD | UART/I2C/GPIO debug + field update; battery gauge (fuel gauge PARTIAL) | ops | IP index |
| COULD | Sub-GHz link to home hub (in-house, reuse A's radio IP) | hub mode | reuse story |
| WON'T (v1) | Medical-device certification claims; cloud video | MDA avoidance | S37 (T3) |

### IP mapping
- REUSE: lowrisc-ibex (13), pulp-axi (18), vlsida-openram (25), ip-005-spi-host (32),
  ip-005-uart (33), ip-003-i2c (31), fossi-ef-gpio8 (39), fossi-ef-tmr32 (40),
  fossi-ef-wdt32 (41), ip-005-interrupt-ctrl (55), ip-005-power-mgr (54).
- PARTIAL: PLL, LDO, SAR ADC, comparator, battery gauge (sky130 analog); PPG AFE (analog
  instrumentation amp + PGA — CREATE-class analog, or external AFE module v1).
- CREATE: 2.4GHz GFSK baseband + link layer (digital), DSP accelerator (FFT + feature
  extraction + classifier), PPG AFE control engine; RF front-end analog (high risk ->
  external FE fallback).

---

## CANDIDATE-C: EVCore-MY (smart EV AC-charger controller; HIGH-PERFORMANCE MCU class)

### MoSCoW
| Priority | Requirement | Value/Constraint | Evidence |
|---|---|---|---|
| MUST | cv32e40p-class CPU @ 100MHz (high-performance positioning) | 40kGE | IP index idx#15 |
| MUST | CAN 2.0B controller (CREATE/PARTIAL — open candidates unvetted T5) | vehicle/BMS/aux comms | IP index has none (T1) |
| MUST | Energy metering: 2x 16-bit oversampled ADC + metrology DSP (sinc filter, energy accumulation) | non-billing-grade v1 | baseline_metrics.json |
| MUST | Control Pilot (CP) analog: PWM generation + comparator level detect (IEC 61851 Type 2) | MS IEC 61851 | S28 (T3) |
| MUST | 64kB SRAM dual-bank + DMA for metering/display streaming | 3-tier AMBA | IP index |
| MUST | OCPP-ready: WiFi via external pre-certified module (SPI/UART), stack on-CPU | OCPP 1.6/2.0.1 | S28 (T3) |
| MUST | Retail RM99-149 module | BOM <= RM105 | candidates_scores.json C-UE |
| SHOULD | LCD/LED display control (SPI + PWM); relay + contactor drivers | UX + safety | — |
| SHOULD | RTC + tamper detection; flash for config/OCPP identity | ops | — |
| SHOULD | UART debug, I2C EEPROM, GPIO expansion | ops | IP index |
| COULD | In-house BLE/Sub-GHz app-pairing radio (reuse A/B radio IP) | app ecosystem | reuse story |
| WON'T (v1) | ISO 15118 PLC; DC fast-charging; on-die WiFi; billing-grade legal metrology | scope control | — |

### IP mapping
- REUSE: openhw-cv32e40p (15), pulp-axi (18), vlsida-openram (25), ip-005-spi-host (32),
  ip-005-uart (33), ip-003-i2c (31), ip-005-timer-pwm (50), fossi-ef-gpio8 (39),
  fossi-ef-tmr32 (40), fossi-ef-wdt32 (41), ip-005-interrupt-ctrl (55), ip-005-power-mgr (54).
- PARTIAL: PLL, LDO, SAR ADC, comparator (sky130 analog); CAN controller (open T5 candidates —
  decide CREATE vs vetted PARTIAL at spec stage).
- CREATE: metrology DSP (sinc + accumulate), CP PWM/level engine (digital control of analog),
  16-bit oversampled metering ADC path (analog), RTC, tamper logic.

---

## Technical constraints (all candidates, reconciled with baseline_metrics.json)
1. Clock: 24MHz xtal -> PLL -> 50-100MHz core (A/B at 50MHz low-power; C at 100MHz).
2. Memory: 32kB (A,B) / 64kB (C) SRAM via OpenRAM or sky130_sram_macros; sizes listed in
   baseline_metrics.json memory_baselines.
3. Die: fit 3.1x3.8mm Caravel-class user area (9-12mm2), 37-40 pads incl. analog pins.
4. Analog: 12-bit SAR (A/B), 16-bit oversampled metering (C), comparator, LDO, PLL — sky130
   primitives; RF front-end external-module fallback for A/B v1.
5. Power targets: sleep <10uA (A), <20uA (B), <50uA (C); active 5-15mW @50MHz (T5 targets).
6. Bus: AXI4-Lite (CPU, DMA, SRAM) -> AHB (streaming datapaths) -> APB (control regs);
   multi-master justified by CPU + DMA engines per candidate.
7. Verilog-2001/2005 only; all CREATE blocks written to that standard; reused blocks audited
   for SV-free RTL before integration.
8. Prototype: chipIgnite USD 9,750 (T1) or free Google MPW (T1); SIRIM Type Approval budgeted
   for radio variants (T3).
