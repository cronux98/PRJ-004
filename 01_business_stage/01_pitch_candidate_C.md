# CANDIDATE-C: EVCore-MY — The RM139 Smart EV-Charger Controller SoC for Malaysia's Build-Out
*Funding-style pitch | PRJ-004 Stage 0 | model: deepseek-v4-flash | 2026-08-19*

---

## 1. Problem (Malaysia-specific, with the news hook)

Malaysia's EV transition is real: **14,766 BEVs and 30,796 hybrids** were registered in 2024
(MAA), 46,403 xEV units per MITI, with BYD (39%) and Tesla (24%) leading (JPJ data). The
government's Low Carbon Mobility Blueprint demands **10,000 public charge points by end-2025
(9,000 AC, 1,000 DC)** — and at end-2024 Malaysia had just **3,600**, a gap Roland Berger
calls "a long way off" (EV Charging Index 2025). ChargEV grew 196->501 points (+155%); the
build-out is accelerating — but every charger needs a **smart controller**, and Malaysia
imports all of them.

The unsolved problem is in the middle of the bill of materials: an AC wallbox costs
**RM2,800-7,000 installed** (MG Malaysia, Trexon) yet its brain — the OCPP-compliant
controller with energy metering, control-pilot (CP) signaling, and connectivity — is an
imported chip-set or a generic ESP32 board, with closed firmware, no local support, and
retrofit modules pricing at RM150-300. Malaysian charger OEMs have no open, affordable,
locally-designed controller silicon. NIMP 2030 and the National Semiconductor Strategy say
Malaysia should design chips; EV charging is the fastest-growing market to prove it.

## 2. Market & size (device, not system)

| Segment | 4-yr units | Price | Market |
|---|---|---|---|
| TAM: home AC charger installs + public AC build-out + retrofit of dumb chargers | 80k-150k modules | RM99-149 | RM8-22M |
| SAM: MY charger OEMs + CPOs + retrofit (urban-centric) | 50k-80k | RM99-149 | RM5-12M |

Anchors: complete AC chargers RM2,800-7,000 (system market, RM30-70M/yr); commodity OCPP
4G/WiFi retrofit modules RM150-300 — our module at RM99-149 **undercuts the retrofit
alternative while adding metering + CP + CAN on one die**. BEV base growing 40-70%/yr means
the home-charging need compounds every year of the window.

## 3. Solution & SoC architecture sketch

EVCore-MY: a **high-performance MCU-class controller SoC** on SkyWater 130nm for AC (Type 2)
EV chargers — metering DSP, control-pilot analog, CAN, and OCPP-ready connectivity, sold as
a RM139 controller module to charger OEMs and retrofitters.

```
  CT/voltage --- 2x 16-bit oversampled ADC (sky130 analog) --+-- AHB streaming --+
  Control Pilot (CP) --- PWM gen + comparator (sky130 analog)-+                    |
  CAN 2.0B (CREATE) --- AHB slave                             |                    v
  Display --- SPI (ip-005-spi-host) + PWM (ip-005-timer-pwm) -+-- APB <---- cv32e40p @100MHz --+-> SRAM 64kB (OpenRAM)
  WiFi module (external, pre-certified) --- SPI/UART ----+     (AXI4-Lite + DMA)                  (AXI4-Lite)
  RTC/tamper/flash --- APB peripherals -------------------+
```
- **AXI4-Lite**: cv32e40p CPU + DMA + 64kB dual-bank SRAM (multi-master).
- **AHB**: streaming — metrology datapath (sinc filter + energy accumulation, CREATE),
  display DMA, CAN data path.
- **APB**: control — CP PWM config, GPIO, timers, watchdog, PMU, UART debug, I2C EEPROM,
  WiFi module control.
- **Analog**: PLL (24MHz->100MHz), LDO, 16-bit oversampled metering ADC, comparator + PWM
  for IEC 61851 CP signaling.
- **High-performance story**: 100MHz core runs the full OCPP 1.6J/2.0.1 stack + metering +
  display concurrently — headroom for ISO 15118 later. No on-die RF: WiFi via pre-certified
  external module (fastest regulatory path).
- **Pure Verilog-2001/2005**; CREATE: CAN 2.0B controller (no index entry), metrology DSP,
  CP engine, RTC/tamper. REUSE: cv32e40p, pulp-axi, OpenRAM, SPI/UART/I2C, timers/PWM,
  GPIO, PMU (IP index, STRONG).

## 4. Why now

- The **10,000-point target is being missed — the gap is the market**: every AC point built
  and every dumb charger retrofitted needs a controller through 2026-2030.
- xEV sales grow 40-70%/yr: home charging stops being a luxury and becomes infrastructure.
- NETR (net-zero 2050, 45% GHG cut by 2030) keeps charging build-out a national policy
  priority with budget behind it.
- NIMP 2030/NSS: a Malaysian EVSE SoC is a flagship "Malaysia designs silicon" story.

## 5. Competition & moat

- Commercial: NXP/TI/ST EVSE reference designs (imported chip-sets), commodity OCPP modules
  (RM150-300, closed firmware), ESP32 hobby boards (not certifiable-grade).
- Academic: CP/metering research is mature; **no fabricated Malaysian EVSE controller SoC**
  in open literature.
- Open source: **no CAN controller, no metrology DSP in our IP index** (verified gap); OCPP
  software stacks are open (OpenOCPP class) and run on our CPU.
- **Moat**: open-silicon EVSE controller with metering + CP + CAN on one die, local support,
  OCPP-conformance path — built for MY OEMs who today import boards. The metering DSP +
  CAN IP are reusable in smart meters, solar inverters, and industrial controls (secondary
  markets that de-risk the EV bet).

## 6. Business model & unit economics

- Sell controller modules (RM139) to charger OEMs (white-label) + retrofit kits; CPO
  partnership for public AC points; licensing of metering/CAN IP later.
- BOM at RM139: SoC RM18-22 + WiFi module RM25-35 + power RM10-15 + PCB RM12-18 + relay/CT
  RM10-15 = **RM75-105; 25-45% margin**. Prototype: MPW shuttle (chipIgnite-class, ~USD 10k) or free Google MPW — outside the thesis scope.
- Margin model survives at RM139 because v1 keeps WiFi off-die (module cost is the trade for
  certification speed); in-house BLE/Sub-GHz pairing radio (reusing Candidates A/B IP) later
  cuts it further.

## 7. Risks & mitigations

- **Global chip vendors squeeze pricing** (MED/HIGH): open silicon + module-level
  integration + local OEM channel; Malaysia-first, not global-first.
- **OCPP conformance cost/time** (MED/MED): start OCPP 1.6J (largest installed base); OCA
  certification path is documented; partner OEMs absorb system-level certs.
- **WiFi module erodes margin** (MED/MED): volume pricing; later in-house short-range radio.
- **IEC 61851 safety compliance burden** (MED/MED): CP analog per standard; OEM partners own
  charger-level certification; our module targets the controller layer.
- **Charging-market consolidation** (LOW/MED): metering/CAN IP diversifies into smart meters
  and solar inverters.

## 8. The Ask

RM 1.8M for: first silicon (~RM60k) + OCPP 1.6J certification + 2,000-module pilot with a
Malaysian charger OEM + production tooling + SIRIM certification. The thesis is Malaysia's
first open EVSE controller SoC; the company rides the policy-mandated build-out that is
already 6,400 charge points behind target. Four years: 60k+ modules, RM8M+ SAM, and the
chip at the heart of Malaysia's own charging infrastructure.

*Composite 71.60/100 — PASS.*
