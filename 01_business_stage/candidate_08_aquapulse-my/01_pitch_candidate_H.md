# CANDIDATE-H: AquaPulse-MY — The RM149 Aquaculture Pond Brain SoC (Monitor + Aeration + Auto-Feeder)
*Funding-style pitch | PRJ-004 Stage 0 batch-2 | model: deepseek-v4-flash | 2026-08-19*

---

## 1. Problem (Malaysia-specific, with the news hook)

Malaysia's aquaculture sector is a RM-billion industry run on paddles and guesswork.
Production value reached nearly **USD 1 billion in 2023** (FAO [S74|T1]); fish-and-seafood
trade value grew from RM7.5B (2017) to **RM11.55B (2022)** [S75|T2]; brackishwater
aquaculture alone produced **392.4 thousand tonnes in 2024** [S76|T1]; and ~90% of farmed
shrimp is the high-value vannamei species [S77|T3]. The 13MP even targets a 98% fisheries
self-sufficiency ratio [S47|T2].

The unsolved problem is at pond level: a farmer's two most expensive risks are dissolved
oxygen crashes (a single overnight DO drop kills a whole pond of shrimp) and feeding
mismatches. The tools are imported and priced for industrial farms: OxyGuard-class DO
monitor/controllers [S78|T1] run to thousands of ringgit, mid-range options are handheld
meters (RM200-600 class on Shopee [S79|T5]), and nobody sells a <RM150 pond controller that
reads DO/temp/pH, switches the aerator when oxygen dips, and runs an auto-feeder — all
offline, solar-powered, no subscription. Malaysia's 40,000+ registered fish farmers and
thousands of shrimp-pond operators have no locally designed, open-silicon pond brain.

## 2. Market & size (device, not system)

| Segment | 4-yr units | Price | Market |
|---|---|---|---|
| TAM: commercial shrimp + freshwater fish ponds (Selangor, Johor, Sabah, Perak, Kedah clusters) | 10k-25k | RM139-149 | RM1.4-3.7M |
| SAM: intensively-managed ponds (aeration + feeding already in use) with co-op/DOF channel | 5k-12k | RM139-149 | RM0.7-1.8M |

Anchors: USD 1B production value [S74|T1]; RM11.55B trade [S75|T2]; 392.4kt brackishwater
output [S76|T1]; competitor controllers at OxyGuard-class prices [S78|T1]; DO meters
RM200-600 [S79|T5]. Device market deliberately segmented from the RM-billions production
value — this is a per-pond tool, not a share of harvest value.

## 3. Solution & SoC architecture sketch

AquaPulse-MY: a **single-die pond controller SoC** on SkyWater 130nm — DO/temp/pH probe
AFE, aeration relay logic, auto-feeder scheduler, Sub-GHz mesh, solar-powered, sold as a
RM139-149 pond kit.

```
  DO probe (galvanic, external) --- high-Z AFE + 12-bit SAR ADC (sky130 analog) --+-- AHB streaming --+
  pH/temp probes --- high-Z AFE + ADC -------------------------------------------------------------+  |
  Aeration relay (1HP class) --- zero-cross + relay driver ------------------------------------------+-- APB <-- Ibex RV32IMC @50MHz --+-> SRAM 32kB (OpenRAM)
  Auto-feeder motor --- PWM (ip-005-timer-pwm) ------------------------------------------------------+      (AXI4-Lite + DMA)
  Solar + battery --- MPPT charge + PMU (sky130 analog) ----------------------------------------------+
  Sub-GHz FSK mesh (CREATE, reuse Candidate-A radio IP) --- AHB packet FIFO
```
- **AXI4-Lite**: Ibex CPU + DMA + 32kB SRAM.
- **AHB**: streaming — probe capture FIFOs, feeding-schedule datapath, mesh packets.
- **APB**: control — AFE gain/offset, relay/PWM config, RTC, PMU, UART debug.
- **Analog**: high-impedance probe AFE (pH/ORP/DO), 12-bit SAR ADC, MPPT solar charger,
  LDO, zero-cross comparator. Sensor chemistry (galvanic DO, glass pH) stays in the probe —
  the silicon reads it.
- **Low-power story**: solar + battery; 30s duty cycle; deep sleep <15µA; mesh relay
  covers a whole pond farm without gateway fees or network subscriptions.
- **Pure Verilog-2001/2005**; CREATE: probe AFE control + DO-threshold aeration logic,
  feeding scheduler, MPPT control; REUSE: Ibex, pulp-axi, OpenRAM, SPI/UART/I2C, timers/
  PWM, PMU (IP index STRONG); radio IP from Candidate-A; probe AFE shared with
  Candidate-D (agri).

## 4. Why now

- 13MP food-security window: 98% fisheries SSR target [S47|T2] puts aquaculture on the
  policy radar with budget.
- Disease pressure + biofloc/intensification trends make DO automation the standard
  practice, not a luxury [S77|T3].
- Labor shortage: one controller replaces nightly pond checks.
- El Nino/drought risk [S63|T2] raises water-quality stakes (higher temps = lower DO).

## 5. Competition & moat

- Commercial: OxyGuard monitor/controllers (industrial, RM-thousands [S78|T1]), handheld
  DO meters (RM200-600 [S79|T5]), imported IoT pond kits (no local support).
- Academic: pond monitoring research is mature; **no fabricated Malaysian open pond SoC**.
- Open source: no open-silicon aquaculture controller; DO/pH AFE absent from our IP index
  (verified gap).
- **Moat**: pond brain (monitor + aerate + feed) at 1/10 the OxyGuard price; offline solar
  mesh without subscription; probe-agnostic (fits cheap galvanic DO probes); AFE + dosing
  IP shared with Candidate-D — one analog core, agri + aquaculture markets.

## 6. Business model & unit economics

- Pond kit RM139-149 (controller + relays + feeder motor; DO probe optional at cost) via
  DOF-linked co-ops, aquaculture suppliers, e-commerce.
- BOM at RM149: SoC RM15-18 + galvanic DO probe RM40-70 + pH probe RM15-25 + feeder motor
  RM10-15 + solar/battery RM15-20 + PCB/enclosure RM15-20 = **RM110-168** — probe cost can
  breach the ceiling; DO-probe-optional kit (BOM RM85-118) keeps margins at 20-45%.
- Prototype: USD 9,750 chipIgnite or free Google MPW [S29|T1, S31|T1].

## 7. Risks & mitigations

- **Probe cost + lifetime** (HIGH/HIGH): probe-optional SKU; probe-agnostic AFE; volume
  probe sourcing.
- **Small device market in MYR** (MED/HIGH): realistic TAM is RM1.4-3.7M — fine for a
  thesis, thin for a company; IP portability (D + industrial water) is the exit valve.
- **Farmer trust/tech adoption** (MED/MED): DOF extension channels, demo ponds, "watch it
  save one harvest" pilots.
- **OxyGuard price-drop** (LOW/MED): their cost structure cannot follow to RM149.
- **Pond-side ruggedization** (MED/MED): IP65 enclosure, surge protection on relay lines.

## 8. The Ask

RM 1.1M for: first silicon (~RM60k) + 1,000-pond pilot across Selangor/Johor shrimp and
Perak freshwater clusters + probe-qualification + SIRIM certification. The thesis is
Malaysia's first open-silicon aquaculture SoC; the company sells the thing that saves a
pond overnight — for the price of one dead harvest's insurance.

*Composite 66.75/100 — FAIL (below 70 floor: market fit 55, unit economics 58). Honest
verdict: real problem, proven feasibility, but the device market is small and probe costs
strain RM150. Watch-item — strongest candidate to resurrect with a B2B/co-op anchor.*
