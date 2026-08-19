# CANDIDATE-E: SolarSync-MY — The RM139 Solar Self-Consumption Optimizer SoC for Malaysia's Quota-Starved Rooftop Boom
*Funding-style pitch | PRJ-004 Stage 0 batch-2 | model: deepseek-v4-flash | 2026-08-19*

---

## 1. Problem (Malaysia-specific, with the news hook)

Malaysia's residential solar demand now outruns the policy plumbing. In May 2025 the NEM
Rakyat rooftop-solar quota **was fully taken up** — SEDA's data showed every megawatt
allocated [S56|T3], forcing the government to add another 100MW to reach 600MW [S57|T4].
Installed rooftop capacity is estimated at 1.75GW, 80% concentrated in Selangor, Johor,
Kedah and Penang [S59|T4]. The NETR (net-zero 2050, 45% GHG-intensity cut by 2030 [S27|T2])
keeps the pipeline open — yet every new solar household hits the same wall:

A rooftop array generates when the sun shines, but the household consumes in the evening.
NEM credits are capped and shrinking; the owner cannot see, in real time, which loads to
shift. The answer today is a **closed per-brand inverter app** (free but useless across
brands), a **RM1,000+ energy-management system** (SOLARMAN EMH-2 class [S60|T4]), or an
**imported CT-clamp monitor** (USD 50-150 on Amazon [S61|T4]) with no local support and no
optimization — it measures, it doesn't act. Malaysia has no <RM150, brand-agnostic,
offline-first device that clamps onto the mains, shows solar-vs-consumption live, and
switches the water heater or pool pump to the sunny hours automatically. That is the device
that makes a 4kW rooftop pay.

## 2. Market & size (device, not system)

| Segment | 4-yr units | Price | Market |
|---|---|---|---|
| TAM: solar households + retrofit monitors (NEM Rakyat 600MW ~ 60-100k homes/yr pipeline + existing 1.75GW base [S59|T4]) | 60k-120k | RM139-149 | RM8-18M |
| SAM: urban KL/Selangor/Penang/Johor installs via SEDA-certified installer channel + e-commerce | 40k-80k | RM139-149 | RM6-12M |

Anchors: quota exhaustion [S56|T3] = demand signal; 1.75GW installed base [S59|T4] = retrofit
market; competitor monitors USD 50-150 [S61|T4]; NETR policy keeps growth in the window
[S27|T2]. Device segmented from the RM10-30k system market (panels + inverter).

## 3. Solution & SoC architecture sketch

SolarSync-MY: a **high-performance metering-class SoC** on SkyWater 130nm — 2-channel CT
energy metering DSP, load-shift relay control, display, and a Sub-GHz/BLE link, sold as a
RM139 clamp-on optimizer.

```
  Mains CT x2 --- 2x 16-bit oversampled ADC (sky130 analog) --+-- AHB streaming --+
  Relay (load shift: heater/pool pump) --- driver + zero-cross --+                 |
  LCD/e-ink --- SPI (ip-005-spi-host) --------------------------+-- APB <---- Ibex/cv32e40p @100MHz --+-> SRAM 64kB (OpenRAM)
  Sub-GHz FSK mesh / BLE-class link (CREATE, reuse A/B radio IP) -+                    (AXI4-Lite + DMA)
  RTC --- APB
```
- **AXI4-Lite**: CPU + DMA + 64kB SRAM (multi-master).
- **AHB**: streaming — metrology datapath (sinc filter + energy accumulation, CREATE,
  shares Candidate-C's metering DSP), display DMA, link packets.
- **APB**: control — CT ADC config, relay driver, RTC, UART debug, GPIO.
- **Analog**: PLL, LDO, 2x 16-bit oversampled metering ADC, zero-cross comparator.
- **High-performance story**: 100MHz core runs energy math + forecasting + relay policy in
  real time; metering-grade accumulation without billing claims (legal metrology avoided).
- **Low-power story**: mains-powered (no battery); <1W device; optional solar-harvest
  backup via PMU.
- **Pure Verilog-2001/2005**; CREATE: metering DSP (shared with C), load-shift scheduler,
  zero-cross relay engine; REUSE: CPU, pulp-axi, OpenRAM, SPI/UART/I2C, timers, PMU (IP
  index STRONG). No RF on-die v1 (optional Sub-GHz module) — fastest regulatory path.

## 4. Why now

- NEM Rakyat quota exhaustion [S56|T3] and the +100MW top-up [S57|T4] prove demand
  outruns supply — every new install is a monitor/optimizer attach.
- NETR 45%-by-2030 target keeps rooftop solar a funded national priority [S27|T2].
- Electricity tariff pressure + solar feed-in value falling → self-consumption optimization
  (not generation) becomes the homeowner's lever.
- Solar installers need a margin-adding, brand-agnostic accessory; none exists at RM139.

## 5. Competition & moat

- Commercial: SOLARMAN EMH-2 (RM1,000+ class [S60|T4]), GEO Minim and Amazon CT monitors
  (USD 50-150, measure-only, no local support [S61|T4]), per-brand inverter apps (free,
  closed, brand-locked).
- Academic: energy metering is mature; **no fabricated Malaysian open metering SoC**.
- Open source: metering DSP absent from our IP index (verified gap); solar apps exist but
  run on imported hardware.
- **Moat**: the same metering DSP serves Candidate-C (EVSE), smart meters, and industrial
  submetering — one IP, three markets; brand-agnostic (works with ANY inverter); offline
  (no subscription, no cloud dependency); open RTL + local support; installer-channel pull.

## 6. Business model & unit economics

- RM139 via SEDA-certified installers (bundled at install) + e-commerce DIY; B2B white-label
  for solar EPCs; metering IP licensing later.
- BOM at RM139: SoC RM15-18 + 2x CT RM10-15 + relay RM8-12 + PSU RM8-12 + PCB/enclosure
  RM15-25 = **RM56-82; 30-50% margin** — the healthiest unit economics of batch 2.
- Prototype: USD 9,750 chipIgnite or free Google MPW [S29|T1, S31|T1].

## 7. Risks & mitigations

- **Inverter apps get better** (MED/HIGH): we act (relay), they only show; brand-agnostic
  and offline are durable advantages.
- **CT accuracy disputes** (MED/MED): metering-grade accumulation, clearly non-billing
  positioning; calibration per unit.
- **Installer channel concentration** (MED/MED): multi-EPC white-label + direct e-commerce.
- **Sub-GHz module adds SIRIM time** (LOW/LOW): v1 wired/display-only + optional module;
  SIRIM path known [S37|T3].
- **Smart-meter rollout (AMI) absorbs the use-case** (LOW/MED): AMI gives data, not
  actuation — the relay/optimizer function survives.

## 8. The Ask

RM 1.4M for: first silicon (~RM60k) + 5,000-unit pilot with two SEDA-certified installer
networks + SIRIM certification + metering-accuracy qualification lab. The thesis is
Malaysia's first open metering/optimizer SoC; the company attaches to every rooftop the
quota race is about to build. Four years: 60k+ units, RM8M+ SAM, and metering IP that also
feeds the EVSE and smart-meter plays.

*Composite 71.45/100 — PASS. Weakest dimension: competition & gap (60) — crowded at the
edges, empty in the middle where we sit.*
