# CANDIDATE-B: JagaCare-MY — The RM139 Aging-in-Place Monitor SoC for Malaysia's 2030
*Funding-style pitch | PRJ-004 Stage 0 | model: deepseek-v4-flash | 2026-08-19*

---

## 1. Problem (Malaysia-specific, with the news hook)

Malaysia becomes an **ageing nation in 2030** — the 60+ population crosses 15.3% (DOSM
projection; MPRH, 2017), and it is one of the fastest ageing transitions on the planet: 7.9%
(2010) to 15.3% (2030), a 20-year sprint that took France 115 years. Today there are already
**2.6 million Malaysians aged 65+ (7.7%)** (DOSM via Malay Mail, 2024), and the Finance
Minister warns Malaysia becomes an "aged nation" by 2048 (MOF, 2025). Every one of those
numbers has a family behind it.

The unsolved problem: **aging in place safely**. A mother lives alone in a flat in PJ; her
children work in Singapore. A fall happens — the golden hour passes before anyone knows.
Malaysia's answer today is either a **free check-in app** (I'm Alive), a **RM1,700+ smartwatch**
(Apple/Huawei fall detection), a **cloud-AI camera subscription** (SmartPeep, CorriCare), or a
**dumb SOS pendant** that requires the wearer to press a button. There is no affordable,
privacy-first, one-time-payment middle: a device that watches for falls itself, never sends
video to a cloud, and works in Bahasa Melayu, Mandarin, and Tamil. The care-giver shortage is
national policy; the technology middle is empty.

## 2. Market & size (device, not system)

| Segment | 4-yr units | Price | Market |
|---|---|---|---|
| TAM: 3.6M aged 60+ (2026e) + family/institutional care demand | 300k-500k | RM139-149 | RM40-70M |
| SAM: urban M40/T20 families with elderly parents (1.2-1.5M households, 8-12% adoption) | 100k-180k | RM139-149 | RM14-27M |

Anchors: quality fall-detection watches retail USD 100-200 globally (SeniorsMobility);
Malaysia's patient-monitoring device market is USD 403M (2024) growing 6.1% CAGR (Stellar MR);
M40/T20 households average RM8,479/mo income (DOSM 2022) — RM139 is 1.6% of one month's
income. System market (context): elderly-care services and monitoring subscriptions.

## 3. Solution & SoC architecture sketch

JagaCare-MY: a **single-die, low-power wearable/home monitor SoC** on SkyWater 130nm —
IMU + PPG bio-path + on-device fall/health DSP + 2.4GHz GFSK (BLE-class) radio, sold as a
RM139 wearable with a RM99 home hub.

```
  IMU (SPI) ------------> SPI host (ip-005-spi-host) --+-- AHB streaming ---+
  PPG AFE --- 12-bit SAR ADC 4ch (sky130 analog) ------+                    |
  SOS button/buzzer --- GPIO/PWM (fossi-ef-gpio8) --+                        v
  32kHz RTC ---- PMU (ip-005-power-mgr) --- APB <--- Ibex RV32IMC @50MHz --+-> SRAM 32kB (OpenRAM)
  2.4GHz GFSK link (CREATE: baseband+link; ext RF FE) --- AHB stream        (AXI4-Lite + DMA)
  DSP accelerator (CREATE: FFT + feature extract + fall classifier) --- AHB slave
```
- **AXI4-Lite**: Ibex CPU + DMA + 32kB SRAM (multi-master).
- **AHB**: streaming — ADC/PPG capture FIFO, IMU FIFO, DSP accelerator datapath, radio link
  packets.
- **APB**: control — radio config, AFE gain/offset, GPIO, timers, watchdog, PMU, I2C (PPG
  sensor), UART debug.
- **Analog**: PLL, LDO, 4ch 12-bit SAR ADC, comparator (battery/wake), PPG AFE path.
- **Low-power story**: deep sleep <20µA; RTC wake; duty-cycled link events (broadcast every
  30s, 0.3% duty); 14-day battery; on-device inference means no wake-for-cloud.
- **Privacy-first**: fall detection runs in silicon — no camera, no cloud video, data stays
  in the home hub. This is the differentiator.
- **Pure Verilog-2001/2005**; CREATE: 2.4GHz GFSK baseband + link layer (no open RTL exists),
  DSP accelerator, PPG AFE control. REUSE: Ibex, pulp-axi, OpenRAM, SPI/I2C/UART, timers,
  PMU (IP index, STRONG).

## 4. Why now

- The **2030 ageing-nation crossing happens inside this product's 4-year window** — the
  demographic clock is the hook, and it is deterministic.
- MOH's digital-health push (national FHIR Health Information Network since 2022) is
  building the interoperability rails our device can plug into.
- Care-worker shortage + aged-nation 2048 fiscal warnings (MOF) make aging-in-place a
  standing national policy topic — funded attention, not a fad.
- A Malaysian-designed elderly-monitor chip is a first: local language, local support,
  open RTL — no import.

## 5. Competition & moat

- Commercial: Apple/Huawei watches (RM1,700+, over-featured for seniors), generic fall
  watches (USD 100-200, no local support), app-only check-ins (free, passive), cloud-AI
  cameras (subscription, privacy-hostile), dumb pendants (no detection).
- Academic: fall-detection algorithms are mature; **silicon is not** — no fabricated sky130
  2.4GHz health-monitor SoC in open literature.
- Open source: **no production-grade pure-Verilog BLE/GFSK PHY** (verified gap; SDR software
  only). BLE stacks (Zephyr/NimBLE) run on our CPU once the radio exists.
- **Moat**: in-house GFSK baseband/link + on-device DSP pipeline — portable IP for every
  wearable/health vertical; open-silicon trust story (auditable, no surveillance); one-time
  price vs subscriptions.

## 6. Business model & unit economics

- Wearable RM139 + hub RM99 bundle via e-commerce, pharmacy chains, care-home NGOs; B2B
  white-label for care providers.
- BOM at RM139: SoC RM17-20 + IMU RM8-12 + PPG RM10-15 + battery RM8-10 + strap/PCB/enclosure
  RM20-28 = **RM63-85; 30-45% margin** at volume. Prototype: USD 9,750 chipIgnite or free
  Google MPW; die cost USD 1-3 at volume.
- Non-medical positioning keeps certification to SIRIM Type Approval only (radio) — no MDA
  medical-device registration burden.

## 7. Risks & mitigations

- **2.4GHz RF front-end on sky130 is the hardest of our three radios** (HIGH/MED): v1 ships
  with an external BLE RF front-end; the in-house digital baseband + link layer remains the
  CREATE deliverable and the moat.
- **Smartwatch substitution** (MED/HIGH): price (RM139 vs RM1,700+), elderly-first UX,
  local-language support, privacy — the children buy, the parents wear.
- **Medical-claims regulatory trap** (MED/HIGH): monitor-not-diagnose; no MDA claims; hub
  keeps data local.
- **BOM creep in wearables** (MED/MED): module reuse across wearable+hub; strap tiering.
- **Adoption by seniors** (MED/MED): family-gateway sales model; Bahasa Melayu/Mandarin/Tamil
  voice alerts.

## 8. The Ask

RM 1.5M for: first silicon (~RM60k) + 5,000-unit pilot with a Malaysian care-home group +
production tooling + SIRIM certification + firmware/UX for three languages. The chip is a
thesis; the company is the quiet insurance every Malaysian family will need before 2030.
Four years: 100k+ wearables, RM14M+ SAM, Malaysia's first open-silicon elderly monitor.

*Composite 70.85/100 — PASS (watch-items: competition 62, feasibility 65, unit economics 65).*
