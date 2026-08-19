# CANDIDATE-I: ParkIQ-MY — The RM129 In-Ground Parking Occupancy Sensor SoC for Malaysian Municipalities
*Funding-style pitch | PRJ-004 Stage 0 batch-2 | model: deepseek-v4-flash | 2026-08-19*

---

## 1. Problem (Malaysia-specific, with the news hook)

Malaysian cities are parked in a data vacuum. KL motorists spend an average of **25 minutes
a day hunting for parking** (BCG study via Asia Mobiliti [S80|T3]) — time, fuel, and
congestion that bay-level sensing would remove. Municipalities have tried enforcement-first
tech and it backfired publicly: Penang launched its Penang Smart Parking app in 2019
[S82|T3], then in August 2026 was forced to **halt its ANPR "hot" enforcement system** after
it recorded **7,000-10,000 violations a month** and triggered a political backlash [S81|T2].
The lesson municipalities are learning the hard way: you cannot police your way out of a
parking shortage — you have to show drivers where the empty bays are.

The unsolved problem is the sensor layer. Real occupancy data needs one device per bay, and
today those devices are imported: LoRaWAN in-ground geomagnetic sensors (Oz Robotics
LW009-SM [S83|T1], OmniWOT ParkNode [S84|T1]) typically price at USD 100-300 each [S85|T3
context], before gateway, platform, and subscription fees. A Malaysian city council
deploying 10,000 bays faces a 7-figure ringgit bill and a foreign supply chain. There is no
<RM150, Malaysia-designed, open-silicon bay sensor with a 5-year battery, no subscription,
and a mesh that works without cellular fees.

## 2. Market & size (device, not system)

| Segment | 4-yr units | Price | Market |
|---|---|---|---|
| TAM: on-street + lot bays in KL/Penang/JB/Shah Alam/Putrajaya/Melaka (30-60k bay estimate, labeled model) | 20k-40k | RM129-149 | RM2.6-6M |
| SAM: municipal pilots + PSP-style app operators + private lot operators | 10k-25k | RM129-149 | RM1.3-3.7M |

Anchors: KL 25-min search cost [S80|T3]; Penang enforcement failure [S81|T2]; incumbent
sensors USD 100-300 [S83|T1, S84|T1]; bay-count estimate is a labeled model (no official
published count). Device market segmented from the RM10-50M system market (apps, platforms,
ANPR fleets).

## 3. Solution & SoC architecture sketch

ParkIQ-MY: a **single-die, battery-first parking sensor SoC** on SkyWater 130nm —
3-axis magnetometer fusion, wake-on-event, Sub-GHz mesh, 5-year battery, sold as a RM129-149
in-ground/on-surface sensor for municipalities.

```
  3-axis magnetometer (external, I2C) --- wake-on-event I/F --+-- AHB streaming --+
  Temperature/aux --- ADC (sky130 analog) -------------------+                    |
  Sub-GHz FSK mesh (CREATE, reuse Candidate-A radio IP) -----+-- APB <-- Ibex RV32IMC @25-50MHz --+-> SRAM 16-32kB (OpenRAM)
  Battery + PMU (sky130 analog) --- deep-sleep domains -----------------------------------+  (AXI4-Lite + DMA)
```
- **AXI4-Lite**: Ibex CPU + DMA + SRAM (small — this is a leaf node).
- **AHB**: streaming — magnetometer FIFO, occupancy-decision datapath, mesh packets.
- **APB**: control — sensor config, PMU/wake domains, RTC, UART debug.
- **Analog**: LDO, battery comparator, wake-on-event comparator, temp ADC. No RF on-die
  v1 (Sub-GHz module option) or in-house FSK PHY from Candidate-A for the full-IP version.
- **Low-power story**: the entire design is a power budget — <10µA sleep, 20ms wake to
  classify occupancy (magnetometer + optional PIR/ultrasonic fusion), mesh beacon 5s duty;
  **5-year CR2032-class battery life** is the spec that wins municipal tenders.
- **Pure Verilog-2001/2005**; CREATE: magnetometer-fusion occupancy classifier,
  wake-on-event logic, mesh sync; REUSE: Ibex, OpenRAM, I2C/SPI/UART, timers, PMU (IP index
  STRONG); radio IP from Candidate-A.

## 4. Why now

- The August 2026 Penang ANPR halt [S81|T2] is a live policy vacuum: enforcement-only
  failed; the alternative (bay-level data) is the obvious next move — municipal budgets
  were already allocated for the halted system.
- PSP app has 6+ years of user base [S82|T3] — it needs sensors to fulfill its "locate
  empty bays" promise.
- LoRaWAN mesh economics make a no-subscription municipal network credible.
- Smart-city frameworks at federal (KPKT) and state levels fund exactly this category.

## 5. Competition & moat

- Commercial: Oz Robotics LW009-SM [S83|T1], OmniWOT ParkNode [S84|T1], China NB-IoT/LoRa
  sensors (USD 70-200 [S85|T3]) — all imported, gateway+platform dependent.
- Academic: occupancy-detection algorithms are mature; **no fabricated Malaysian parking
  sensor SoC**.
- Open source: no open-silicon parking sensor; magnetometer-fusion + wake-on-event absent
  from IP index (verified gap).
- **Moat**: <RM150 vs USD 100-300 imports; no-subscription mesh; 5-year battery spec;
  open RTL + local support + MAMPU-friendly procurement; low-power wake-on-event IP
  reusable across every battery sensing node (Candidates A/D/F/J).

## 6. Business model & unit economics

- RM129-149/sensor to municipalities (tender) and private lot operators; gateway + mesh
  software as B2G service; white-label for Malaysian smart-city integrators.
- BOM at RM129-149: SoC RM15-18 + magnetometer RM8-12 + battery RM10-15 + potting/PCB
  RM12-18 + radio parts RM8-12 = **RM53-75; 40-60% margin** — the best unit economics in
  batch 2 after E.
- Prototype: USD 9,750 chipIgnite or free Google MPW [S29|T1, S31|T1].

## 7. Risks & mitigations

- **Municipal procurement cycles** (MED/HIGH): 12-18 month tenders; pilot-first strategy;
  private lot operators as the fast channel.
- **Imported-sensor price war** (MED/MED): open RTL + local support + no-subscription mesh
  beat commodity price-on-paper; total-cost-of-ownership story.
- **In-ground deployment failure modes** (MED/HIGH): surface-mount option (LW009-SM style
  [S83|T1]), potting quality program, field-replacement design.
- **Radio coexistence in dense bays** (MED/MED): mesh TDMA from Candidate-A PHY; channel
  planning kit for councils.
- **ANPR-style political backlash** (LOW/HIGH): positioning is data-for-drivers, never
  enforcement; privacy by design (no plates, no identity).

## 8. The Ask

RM 1.2M for: first silicon (~RM60k) + 5,000-sensor pilot with one municipal council
(Penang Island or MBPP successor program) + battery-life qualification (accelerated aging)
+ SIRIM certification. The thesis is Malaysia's first open-silicon parking sensor; the
company sells the data layer that every smart-parking app has been missing since 2019.

*Composite 68.90/100 — FAIL (just below the 70 floor: market fit 62, competition & gap 60,
differentiation 64). Honest verdict: excellent unit economics and feasibility, but the
sensor space is crowded with imports and municipal procurement is slow. Watch-item — one
anchor municipal tender flips it to PASS.*
