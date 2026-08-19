# CANDIDATE-A: BanjirSense-MY — The RM129 Community Flood Early-Warning Node SoC
*Funding-style pitch | PRJ-004 Stage 0 | model: deepseek-v4-flash | 2026-08-19*

---

## 1. Problem (Malaysia-specific, with the news hook)

Malaysia floods every monsoon — and the losses are national accounting entries, not anecdotes:
**RM6.1 billion** in December 2021 (0.4% of GDP; ~50 dead; ~400,000 evacuated) (DOSM Special
Report via CNA, 2022), **RM933.4 million** in 2024, **RM636.9 million** in 2025 (DOSM via
Bernama, 2026). The World Bank warns these costs are rising with climate-driven rainfall
(Eco-Business, 2025). The 2025 northeast-monsoon season alone killed eight people before
March.

And yet the warning system is coarse. JPS's National Flood Forecasting and Warning System
(NaFFWS) works at **river-basin level** with 48-hour forecasts (Springer, 2019). KL residents
get an **area-level siren** (NADMA, 2026). A kampung beside a rising river, a condo basement,
a road underpass — the people who need minutes of warning get a basin forecast or a
neighbourhood siren, or nothing.

The gap is a **community-level, affordable, self-contained warning node** — the flood
equivalent of a smoke detector. It doesn't exist: every commercial node costs USD 234-504
(RAK, Milesight) and demands a LoRaWAN network subscription.

## 2. Market & size (device, not system)

| Segment | 4-yr units | Price | Market |
|---|---|---|---|
| TAM: flood-prone communities (kampung, sekolah, condo basement, underpass, riverbank) | 300k-500k | RM129-149 | RM40-70M |
| SAM: urban KL/Selangor/Penang/JB + govt pilots + schools | 100k-150k | RM129-149 | RM13-22M |

Anchors: RAK LoRaWAN level sensor USD 234-254 (vendor store); Milesight USD 504; Alibaba
low-end USD 70-415. Our node at RM129-149 is **1.5-7x cheaper with zero network fees**.
Buyers: M40/T20 households (average income RM8,479/mo, DOSM 2022), JPS/NADMA pilot programs,
schools, condo management. System market (context): national flood infra runs RM100M+.

## 3. Solution & SoC architecture sketch

BanjirSense-MY: a **single-die, low-power flood-warning node SoC** on SkyWater 130nm
(sky130) — MCU + sensor AFE + Sub-GHz mesh radio, powered by battery + solar, sold as a
RM129-149 device that installs on a pole in 10 minutes.

```
  ANT --- Sub-GHz FSK Radio (CREATE: PHY+MAC, 433/915MHz mesh)
                |   |-- RF front-end (external FE fallback v1; digital baseband in-house)
  Ultrasonic ---| 12-bit SAR ADC 8ch (sky130 analog) ---+
  Rain gauge ---|                                       |-- AHB streaming  --+
  Temp/battery --| Comparator wake (sky130 analog)      |                    |
                                                +------+                    v
  32kHz RTC ---- PMU (ip-005-power-mgr) --- APB <---- Ibex RV32IMC @50MHz --+-> SRAM 32kB (OpenRAM)
  Solar/batt --- LDO (sky130 analog)                                          (AXI4-Lite + DMA)
```
- **AXI4-Lite**: Ibex CPU + DMA + 32kB SRAM (multi-master).
- **AHB**: streaming datapaths — ADC capture FIFO, ultrasonic engine (reuse ip-005-ultrasonic),
  radio packet engine.
- **APB**: control registers — radio config, AFE, GPIO, timers, watchdog, PMU, UART/I2C debug.
- **Analog**: PLL (24MHz->50MHz), LDO, 12-bit SAR ADC, wake-on-comparator.
- **Low-power story**: deep sleep <10µA; wake on water-level comparator or duty-cycled radio
  listen (0.1%); solar/battery year-life. Mesh: nodes relay alarms peer-to-peer — no gateway,
  no subscription, no telco.
- **Pure Verilog-2001/2005**; CREATE blocks: FSK PHY+MAC (no open RTL exists — only SDR
  software), ADC-capture DMA, wake/event manager. REUSE: Ibex, pulp-axi, OpenRAM, SPI/UART/
  I2C, timers, PMU, ultrasonic capture (IP index, all STRONG).

## 4. Why now

- 2021's RM6.1B disaster made floods a permanent national conversation; annual losses recur
  (RM0.6-1B/yr) and the World Bank says they get worse.
- NaFFWS expansion + RM25M 2025 federal flood-repair allocation = government spending on
  flood sensing is rising now.
- Climate intensity (2024-2026 monsoon seasons, 8 deaths in 2025 season) = the news hook
  repeats every November-March, for free.
- NIMP 2030 + National Semiconductor Strategy: Malaysia wants locally designed silicon — a
  Malaysian flood SoC is exactly the story the policy asks for.

## 5. Competition & moat

- Commercial: RAK/Milesight LoRaWAN sensors (USD 234-504, network-dependent), JPS sirens
  (area-level), DIY Arduino nodes (hobby-grade).
- Academic: peer-reviewed LoRaWAN flood sensing for Malaysia (2023) — module prototype, not
  silicon, not a product.
- Open source: **no pure-Verilog Sub-GHz radio RTL exists** (verified gap; LoRa PHY exists
  only as GNU Radio software).
- **Moat**: the in-house FSK radio PHY + mesh MAC + wake-on-comparator low-power architecture.
  This IP is portable to every IoT vertical (agriculture, water, security) and is the first
  open radio RTL of its class. Open silicon + local support + no-network-fee operation is
  defensible against module assemblers for years.

## 6. Business model & unit economics

- Sell the node (RM129) and a 5-node community kit (RM599) via e-commerce + govt/school
  pilots; mesh firmware updates over-the-air.
- BOM at RM129 retail: SoC RM15-18 + ultrasonic sensor RM20-30 + battery/solar RM12-18 +
  PCB RM12-15 + enclosure RM15-20 + RF parts RM8-15 = **RM82-116 cost; 15-35% margin**,
  improving with volume (die cost USD 1-3 at 100k units; prototype USD 9,750 chipIgnite or
  free Google MPW).
- Margin model survives at RM129 only because the radio is on-die — no LoRa module (RM50+)
  and no network fees. B2G pilots de-risk volume.

## 7. Risks & mitigations

- **sky130 RF front-end not proven** (HIGH/MED): in-house digital baseband is the deliverable;
  v1 uses an external RF front-end module — same IP, same product story.
- **Adoption slower than model** (MED/MED): government pilot channel first (JPS/NADMA,
  schools), then community virality — flood season is the marketing engine.
- **BOM creep vs RM150 ceiling** (MED/MED): enclosure tiering, on-die radio, volume buys.
- **SIRIM Type Approval** (LOW/LOW): known 2-6 month path, 433/915MHz SRD band.

## 8. The Ask

RM 1.5M for: first silicon (chipIgnite/MPW, ~RM60k) + 1,000-node pilot in a flood-prone
Selangor/Kelantan district with a JPS/NADMA partner + production tooling + SIRIM
certification + team. The thesis SoC is the chip; the company is the mesh network that
turns RM129 into the community's cheapest insurance. Four years: 100k+ nodes, RM13M+ SAM,
and Malaysia's first open flood-warning silicon.

*Composite 72.15/100 — PASS. All evidence cited in research_corpus.json / candidates_scores.json.*
