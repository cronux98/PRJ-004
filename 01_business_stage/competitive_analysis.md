# PRJ-004 (NEW) — Competitive Analysis: 3-Layer Census per Candidate
Model: deepseek-v4-flash | Date: 2026-08-19 | Stage: 01_business_stage

Layer definitions: (1) COMMERCIAL products (Malaysia + global, MYR/USD prices),
(2) ACADEMIC + fabricated silicon, (3) OPEN-SOURCE RTL. T1/T2 citations required per spec cell;
T4/T5-only claims labeled HYPOTHESIS. Prices converted at ~4.2 MYR/USD where noted.

---

## CANDIDATE-A: BanjirSense-MY — community flood early-warning node SoC

### Layer 1: Commercial products
| Product | Price | Coverage | Network dependency | Source/Tier |
|---|---|---|---|---|
| RAK LoRaWAN water-level sensor (RAK7204-class) | USD 234-254 (~RM980-1,070) | point level | LoRaWAN gateway + network | store.rakwireless.com [S10|T1] |
| Milesight EM500-SWL submersible | USD ~504 (~RM2,120) | point level | LoRaWAN | store.mcci.com [S11|T1] |
| Alibaba LoRaWAN level sensors | USD 70-415 | point level | LoRaWAN | alibaba.com [S12|T4] HYPOTHESIS on quality/MTBF |
| JPS/NADMA national warning (sirens, PRABN telemetry) | govt budget | area/basin level | JPS network | nadma.gov.my [S07|T2], water.gov.my [S09|T1] |
| DIY Arduino + JSN-SR04T flood node | RM50-150 | point | none (local buzzer/app) | Shopee [S39|T5], PSA thesis (T5) |
| **Our node** | **RM129-149** | point + local mesh | none (mesh peers) | — |

Gap read: every commercial node is 1.5-7x our ceiling and requires LoRaWAN infrastructure fees;
JPS warning is basin/area-level, not community-level. The gap is price + community granularity
+ no-network-fee operation [S07|T2, S08|T2].

### Layer 2: Academic + fabricated silicon
- "Development of a smart sensing unit for LoRaWAN-based IoT flood monitoring and warning
  system" — peer-reviewed, built for Malaysian conditions, but a module-level prototype, NOT an
  SoC and NOT a product [S13|T2, ScienceDirect Results in Engineering 2023].
- NaFFWS implementation papers (Springer, 2019-2020) — system-level forecasting for east-coast
  catchments; telemetry is procured, not fabricated locally [S08|T2].
- No fabricated silicon for community flood nodes found in open literature (T2/T3 scan).
- Conclusion: academic layer validates the application but not the SoC claim — our
  single-die node SoC is a first (HYPOTHESIS, T5 — verified only by absence of evidence).

### Layer 3: Open-source RTL
- No open Sub-GHz FSK/OOK transceiver RTL in pure Verilog found. LoRa PHY exists as GNU Radio
  software (gr-lora_sdr [S46|T5], SDR-LoRa [S35|T2]) — SDR, not synthesizable RTL.
- IP index (~/.hermes_workspace/IP/index.md, T1) contains zero wireless entries across 54 blocks
  (fabric, CPU, mem, periph, sec, soc domains only).
- OpenRAM/Ibex/pulp-axi (all STRONG, T1) give the digital spine; the radio must be CREATED.

---

## CANDIDATE-B: JagaCare-MY — elderly aging-in-place health & safety monitor SoC

### Layer 1: Commercial products
| Product | Price | Capability | Malaysia presence | Source/Tier |
|---|---|---|---|---|
| Apple Watch (fall detection, SOS) | RM1,700+ | full smartwatch | strong | apple.com (T1) — price from public MY store (T1) |
| Generic fall-detection watches | USD 100-200 (~RM420-840) | fall alert + SOS | via marketplaces | seniorsmobility.org [S18|T3] |
| SOS pendants (433MHz/GSM) | RM60-250 | button alert | marketplaces | marketplace scan (T4/T5) |
| CorriCare (MY) — activity/fall stream to portal | subscription | non-wearable sensors | local company | corricare.com.my [S20|T4] |
| SmartPeep (SG/AU/MY) — AI camera fall detection | subscription | camera, cloud AI | regional | smartpeep.ai [S20|T4] |
| I'm Alive (MY) — daily check-in app | free | app only | local | imalive.co [S20|T4] |
| nRF52840-based wearables (reference hardware) | module RM40-90 | BLE SoC baseline | global | nordicsemi.com [S36|T1] |
| **Our device** | **RM139-149** | on-device fall/health DSP, BLE-class radio, open RTL | local silicon | — |

Gap read: the affordable middle is app-only (free, passive) or dumb pendants; smart devices are
either premium watches (RM1,700+) or cloud-AI subscriptions with privacy concerns. Our gap:
one-time RM139 device, on-device detection, no cloud video, local support [S18|T3, S20|T4].

### Layer 2: Academic + fabricated silicon
- Fall-detection algorithms are mature in literature (IMU threshold/ML pipelines — T2 general
  body of work; cited via the device class in [S18|T3]).
- Academic BLE/baseband implementations exist (FPGA-level, T2/T3); no fabricated sky130
  2.4GHz GFSK transceiver found in open literature (T5 absence-based HYPOTHESIS).
- Conclusion: algorithm layer is solved; silicon layer (esp. 2.4GHz analog) is the open risk.

### Layer 3: Open-source RTL
- No pure-Verilog BLE PHY/link layer of production quality in open source (SDR implementations
  only) [S35|T2]. BLE stacks exist as software (Zephyr, NimBLE — T1 ecosystem), which run on
  OUR SoC once the radio exists.
- IP index has no radio or DSP-accelerator entries (T1) — both must be CREATED (GFSK baseband +
  link, feature-extraction DSP).

---

## CANDIDATE-C: EVCore-MY — smart EV AC-charger controller SoC

### Layer 1: Commercial products
| Product | Price | Role | Source/Tier |
|---|---|---|---|
| AC wallbox 7kW (complete charger) | RM3,000-5,900 | system | mgmalaysia.com [S25|T4] |
| AC wallbox installed | RM2,800-7,000 | system | trexon.my [S26|T4] |
| OCPP 4G/WiFi comms module (retrofit) | RM150-300 class | controller comms | module vendor [S45|T4] |
| NXP/TI/ST EVSE reference designs (MCU+AFE) | chip-set level, USD 5-20 | controller silicon | vendor ref. designs (T1 — vendor catalog pricing class) HYPOTHESIS on MY pricing |
| ESP32-based open OCPP boards (community) | RM80-150 | hobby/commercial-lite | marketplace (T4/T5) |
| **Our controller module** | **RM99-149** | full EVSE controller + metering + OCPP-ready | — |

Gap read: complete chargers are RM3k+ (system market — ours is the module inside, RM99-149);
imported OCPP modules anchor the retrofit price at RM150-300; no Malaysia-designed open EVSE
controller silicon exists (T4/T5 scan). The wedge: open-silicon controller at module price
with metering + CP + CAN on one die [S28|T3, S45|T4].

### Layer 2: Academic + fabricated silicon
- EVSE control-pilot and metering research is extensive (T2 body of work on CP signaling,
  IEC 61851 compliance).
- CAN controller and metering DSP are textbook-class digital IP — repeatedly fabricated in
  130nm-class ASICs (T2 general literature; absence of a specific open sky130 EVSE SoC noted).
- Conclusion: no fabricated academic EVSE controller SoC found for Malaysia (T5 absence-based
  HYPOTHESIS) — the thesis contribution is open, Malaysia-first integration.

### Layer 3: Open-source RTL
- IP index: no CAN controller, no metrology DSP, no EVSE-specific block (T1).
- Open CAN 2.0B controller RTL candidates exist in the wider open-source ecosystem (T5 —
  unvetted, not in our index; mark PARTIAL/CREATE decision at spec stage).
- OCPP software stacks are open (OpenOCPP etc. — T1/T3 ecosystem), which run on our CPU.
- Everything else reuses STRONG index blocks: cv32e40p, pulp-axi, OpenRAM, SPI/UART/I2C/PWM
  (T1).

---

## Cross-candidate differentiation summary (vs all 3 layers)
| Candidate | vs Commercial | vs Academic | vs Open RTL |
|---|---|---|---|
| A | 1.5-7x cheaper, no network fees, community granularity | first single-die node (paper-only today) | first open Sub-GHz radio RTL (none exists) |
| B | one-time price vs RM1,700+ watches and cloud-AI subscriptions; privacy-first | silicon layer novel (algorithms mature) | first open BLE-class baseband + DSP accel |
| C | open silicon vs imported modules; metering+CP+CAN on one die | Malaysia-first integration (blocks textbook) | first open EVSE controller SoC in index |

Moat hypothesis (labeled HYPOTHESIS, T5): the CREATE-IP (radio PHY/MAC for A-B, CAN+metering
for C) is the durable asset — it is portable across IoT verticals and absent from the open
ecosystem [S35|T2 confirms absence for radios].
