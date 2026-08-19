# CANDIDATE-G: HomeEye-MY — The RM149 Privacy-First Smart Video Doorbell SoC
*Funding-style pitch | PRJ-004 Stage 0 batch-2 | model: deepseek-v4-flash | 2026-08-19*

---

## 1. Problem (Malaysia-specific, with the news hook)

Malaysia's smart-home market is growing off a small base — home-automation revenue was
forecast at USD 51M (2020) after quintupling from USD 4.2M (2015) [S72|T3] — and home
security is the leading application. But the device that guards the front door is a
foreign, cloud-first product: name-brand video doorbells start at RM552 (Xiaomi Youpin
Xiaomo [S70|T4]) and climb past RM700 for Ring/Eufy class, while "complete" local security
systems run RM1,000-2,000 [S71|T4]. Every one of them ships video to a foreign cloud, often
behind a subscription, and none is built or supported in Malaysia.

The unsolved problem is the price/privacy corner: a Malaysian family wants to see who is at
the door — without paying RM600+, without a monthly plan, and without their doorstep footage
leaving the country. PDPA and the 2024 data-breach headlines have made local data a selling
point, yet no Malaysian-made, open-silicon, local-first video doorbell exists. The
technology to build one (camera module + WiFi + MCU) is commodity; the silicon that fuses
them into a <RM150, on-device-detection, cloud-optional product is not.

## 2. Market & size (device, not system)

| Segment | 4-yr units | Price | Market |
|---|---|---|---|
| TAM: urban landed + condo households (KL/Selangor/Penang/JB) adopting smart security | 150k-300k | RM139-149 | RM21-45M |
| SAM: M40/T20 households buying their first smart doorbell, privacy-motivated | 80k-150k | RM139-149 | RM11-22M |

Anchors: doorbell price band RM552+ for name brands [S70|T4]; system market RM1-2k [S71|T4];
smart-home growth trend [S72|T3]; M40/T20 income anchor [S40|T2]. Device market segmented
from the RM1-2k installed-security system market.

## 3. Solution & SoC architecture sketch

HomeEye-MY: a **single-die video-doorbell SoC** on SkyWater 130nm — camera interface,
on-device person/motion detection accelerator, audio, and WiFi-via-module, sold as a
RM139-149 doorbell with local storage and cloud-optional mode.

```
  Camera module (DVP, external OV5640-class) --- camera I/F + line buffer --+-- AHB streaming --+
  Mic/speaker --- I2S + audio codec I/F ------------------------------------+                    |
  PIR + button --- GPIO/wake -----------------------------------------------+-- APB <-- cv32e40p @100MHz --+-> SRAM 64kB + ext PSRAM (QSPI)
  WiFi module (external, pre-certified) --- SDIO/SPI + UART -----------------+     (AXI4-Lite + DMA)
  Vision accelerator (CREATE: motion + person detection, low-res) --- AHB master
```
- **AXI4-Lite**: CPU + DMA + SRAM/PSRAM (multi-master).
- **AHB**: streaming — camera line buffers, vision-accelerator datapath, audio FIFOs,
  WiFi packets.
- **APB**: control — camera config, audio codec, PIR/button, PMU, watchdog, GPIO.
- **Analog**: LDO, PLL, audio codec AFE (or external codec), battery comparator.
- **High-performance story**: 100MHz core + dedicated vision accelerator keeps person
  detection on-device (no cloud round-trip for the core function); frames to PSRAM,
  thumbnails/events to local flash.
- **Privacy-first story**: factory-default local mode — video never leaves the home unless
  the owner opts in; PDPA-aligned by construction.
- **Pure Verilog-2001/2005**; CREATE: vision accelerator (motion + person), camera I/F,
  audio I/F; REUSE: CPU, pulp-axi, OpenRAM, SPI/I2C/UART/I2S, timers, PMU (IP index STRONG).

## 4. Why now

- Smart-home adoption curve is steepening [S72|T3]; security is the #1 category.
- Privacy is a marketable feature now: PDPA enforcement + cloud-breach fatigue favor
  local-first hardware.
- Component costs (camera, WiFi modules) have fallen enough to make RM149 plausible for
  the first time.
- NIMP 2030/NSS [S38|T3] favors locally designed silicon; a Malaysian security device is a
  flagship story.

## 5. Competition & moat

- Commercial: Ring/Eufy (RM600-800, subscription, foreign cloud), Xiaomi (RM552+ [S70|T4]),
  local system integrators bundling imports (RM1-2k [S71|T4]).
- Academic: embedded vision is mature; **no fabricated Malaysian open video-doorbell SoC**.
- Open source: no open-silicon vision pipeline for doorbells; CMSIS/OpenCV-class software
  exists but needs a CPU too weak at this power/price.
- **Moat**: local-first privacy (PDPA story) + no subscription + open RTL + local support;
  vision accelerator IP is reusable in cameras, access control, retail analytics.

## 6. Business model & unit economics

- RM139-149 via e-commerce + ISP/home-security installer channel; cloud-optional
  (no subscription); B2B white-label for local security companies.
- BOM at RM139-149: SoC RM18-22 + camera module RM25-35 + WiFi module RM25-35 + PSRAM
  RM8-12 + PSU/PCB/enclosure RM20-30 = **RM96-134; 3-30% margin** — the tightest in batch 2;
  every component is a price negotiation.
- Prototype: USD 9,750 chipIgnite or free Google MPW [S29|T1, S31|T1].

## 7. Risks & mitigations

- **Margin squeeze vs RM150 ceiling** (HIGH/HIGH): component-tiering (2MP camera v1,
  e-ink-less), white-label volume; revisit price floor if BOM cannot hit RM134.
- **Vision accelerator complexity** (HIGH/HIGH): v1 = motion + PIR + person-at-low-res on
  dedicated datapath; cloud-optional person ID later; honest schedule buffer.
- **Ring/Eufy brand gravity** (MED/HIGH): local-first privacy + no-subscription + open RTL
  is a different buyer; do not fight on features.
- **WiFi module certification** (MED/MED): pre-certified module covers SIRIM [S37|T3].
- **Firmware security burden** (MED/HIGH): signed boot, encrypted local storage, OTA —
  budgeted as first-class scope, not an afterthought.

## 8. The Ask

RM 1.6M for: first silicon (~RM60k) + 5,000-unit pilot with two Malaysian security
integrators + WiFi/SIRIM certification + security hardening audit (signed boot, encrypted
storage). The thesis is Malaysia's first open-silicon video-doorbell SoC; the company
sells privacy as the product and silicon as the moat.

*Composite 66.60/100 — FAIL (below 70 floor: unit economics 54, technical feasibility 64).
Honest verdict: the <RM150 video-doorbill BOM is survivable only at volume; the vision
accelerator is the hardest CREATE in batch 2. Watch-item — revisit if component prices keep
falling or if a B2B anchor order materializes.*
