# CANDIDATE-F: HazeGuard-MY — The RM139 Indoor Air Quality + CO2 Monitor SoC for Haze Season
*Funding-style pitch | PRJ-004 Stage 0 batch-2 | model: deepseek-v4-flash | 2026-08-19*

---

## 1. Problem (Malaysia-specific, with the news hook)

The haze is not a weather report — it is a recurring public-health event with a live 2026
chapter. In August 2026, 11-12 Malaysian air-monitoring stations recorded unhealthy API
readings and Serian (Sarawak) peaked at **API 204** (very unhealthy) as transboundary smoke
from Sumatra/Kalimantan fires hit the west coast and Borneo [S63|T2]. MetMalaysia warns of a
**>90% chance of a "Super El Nino" by year-end** that could rival 1997-98 [S63|T2]. The
pattern is standing: FMT's July 2025 headline says it plainly — "The haze is back, and will
return again" [S65|T3].

The unsolved problem is that Malaysia's official API network measures **outdoor** air at a
handful of stations — but Malaysians spend 90% of their time **indoors**, and the classrooms,
offices, and bedrooms where children and the elderly breathe are unmeasured. Malaysian
school studies already link indoor pollutants to children's respiratory symptoms (Sabah,
24 classrooms, 332 pupils [S67|T2]), and experts have been calling for compulsory classroom
CO2 monitors since the pandemic [S66|T3]. The monitors that exist are imported and priced
for the top of the market: IQAir-class devices above RM1,000, Qingping at USD ~150 [S68|T3],
Xiaomi/Aqara at RM250-450. There is no <RM150 device that speaks Malaysia's API language,
works in a classroom without a phone, and links a whole school or kampung on a local mesh.

## 2. Market & size (device, not system)

| Segment | 4-yr units | Price | Market |
|---|---|---|---|
| TAM: urban households in haze-affected states (KL/Selangor/JB/Penang/Kuching) + schools + SMEs | 150k-300k | RM129-149 | RM19-45M |
| SAM: M40/T20 urban homes + school/kindergarten bulk (MOE-linked) | 80k-150k | RM129-149 | RM10-22M |

Anchors: recurring unhealthy-API events [S63|T2]; school IAQ evidence [S67|T2]; expert calls
for compulsory CO2 monitors [S66|T3]; competitor price band USD 150+ [S68|T3]; M40/T20
household income RM8,479/mo [S40|T2] — RM129 is 1.5% of one month's income.

## 3. Solution & SoC architecture sketch

HazeGuard-MY: a **single-die indoor AQI monitor SoC** on SkyWater 130nm — PM2.5 laser-sensor
interface, CO2 sensor link, on-device AQI fusion calibrated to Malaysia's API, display,
and Sub-GHz mesh, sold as a RM129-149 monitor with a school-bulk mode.

```
  PM2.5 laser sensor (PMS5003-class, UART) -----------+-- AHB streaming --+
  CO2 sensor (SCD40-class, I2C, external) ------------+                    |
  Temp/humidity --- I2C ------------------------------+-- APB <---- Ibex RV32IMC @50MHz --+-> SRAM 32kB (OpenRAM)
  LCD/segment display --- SPI + PWM -------------------+   (AXI4-Lite + DMA)
  Sub-GHz FSK mesh (CREATE, reuse Candidate-A radio IP) -- AHB packet FIFO
  Buzzer/LED alert --- GPIO
```
- **AXI4-Lite**: Ibex CPU + DMA + 32kB SRAM.
- **AHB**: streaming — sensor capture FIFOs, AQI fusion datapath, mesh packets.
- **APB**: control — sensor config, display, GPIO alert, RTC, PMU.
- **Analog**: LDO, 12-bit SAR ADC (temp/light aux), comparator (wake); the hard
  measurement heads (laser particle counter, NDIR CO2) are commodity external sensors —
  the SoC's job is fusion, calibration, alerting, and networking.
- **Low-power story**: mains/USB powered; battery backup 8h; mesh relay lets one gateway
  serve a whole classroom block — no WiFi credentials, no subscription.
- **Malaysia-API alignment**: on-device conversion to Malaysia's API scale (0-500) with
  haze-season calibration offsets — a local-first feature imported units lack.
- **Pure Verilog-2001/2005**; CREATE: AQI fusion engine, API-calibration table, mesh
  relay; REUSE: Ibex, pulp-axi, OpenRAM, SPI/I2C/UART, timers, PMU (IP index STRONG);
  radio IP from Candidate-A.

## 4. Why now

- Live news hook: August 2026 unhealthy-API event, Serian 204 [S63|T2]; haze returns every
  dry season [S65|T3].
- Super El Nino warning for year-end 2026 [S63|T2] — the worst haze years follow El Nino.
- Post-Covid IAQ awareness made CO2 monitors a known school ask [S66|T3]; Malaysian school
  IAQ evidence is published [S67|T2].
- 13MP/health-policy attention on air quality; NRES owns API monitoring — a natural B2G
  channel for a denser indoor network.

## 5. Competition & moat

- Commercial: IQAir (RM1,000+), Qingping (USD ~150 [S68|T3]), Xiaomi/Aqara (RM250-450,
  cloud-app dependent), PurpleAir (USD ~300, US AQI).
- Academic: Malaysian school IAQ studies exist [S67|T2] — measurement, not products.
- Open source: no open-silicon AQI monitor; no open Malaysia-API calibration layer.
- **Moat**: Malaysia-API calibration + local-language alerts + mesh (classroom block, one
  gateway) + open RTL; school-bulk economics (MOE/procurement channel); mesh IP shared
  with Candidates A/D/J — one radio, four products.

## 6. Business model & unit economics

- PM2.5+temp/humidity monitor at RM99; +CO2 version at RM149; school packs (10+ units +
  one mesh gateway) via B2G/B2S; e-commerce retail.
- BOM PM-only RM60-80 (SoC RM15-18 + PMS5003 RM35-45 + PSU/PCB/enclosure RM20-30) = margin
  ~20-40% at RM99; +CO2 adds RM40-60 (SCD40-class) → BOM RM95-130 at RM149, margin 13-35% —
  tight but survivable; PM-only SKU protects the floor.
- Prototype: USD 9,750 chipIgnite or free Google MPW [S29|T1, S31|T1].

## 7. Risks & mitigations

- **CO2 sensor cost squeezes margin** (MED/HIGH): PM-only RM99 SKU; CO2 as premium SKU;
  volume pricing on SCD40-class.
- **Commodity import flood (Xiaomi/Aqara)** (MED/HIGH): local calibration + mesh + school
  channel + open RTL — compete on system value, not spec sheet.
- **Sensor accuracy disputes** (MED/MED): cross-calibration against DOE reference stations
  during haze events; publish accuracy data.
- **Haze seasonality = lumpy demand** (MED/MED): school-year procurement calendar; sell
  year-round on CO2/ventilation use-case.
- **API scale changes** (LOW/LOW): calibration table is firmware-updatable.

## 8. The Ask

RM 1.3M for: first silicon (~RM60k) + 10,000-unit pilot across 100 KL/Selangor schools and
kampung clinics + DOE cross-calibration program + SIRIM certification. The thesis is
Malaysia's first open-silicon air-quality SoC; the company is the indoor half of the
national API story — the half that is unmeasured today.

*Composite 70.90/100 — PASS. Weakest dimension: unit economics (60) — CO2 SKU margin is
thin; the PM-only SKU carries the floor.*
