# CANDIDATE-D: AgriCore-MY — The RM139 Solar Fertigation Controller SoC for Malaysia's Rice Bowl
*Funding-style pitch | PRJ-004 Stage 0 batch-2 | model: deepseek-v4-flash | 2026-08-19*

---

## 1. Problem (Malaysia-specific, with the news hook)

Malaysia's rice self-sufficiency ratio (SSR) is stuck below two-thirds while every policy
target misses. The 75% SSR goal for 2025 is "increasingly unlikely" [S48|T2]; the 13th
Malaysia Plan (2026-2030) now targets 80% for rice, 79% for vegetables [S47|T2]; and BERNAS
has been handed an explicit "strengthen the 80% rice SSL mission" [S49|T2]. Yields are
stagnating against rising input costs and unpredictable weather [S50|T2], and the paddy and
rice industry's own competition watchdog flags declining yields and unregulated services
[S55|T1].

The unsolved problem sits at the farm gate: Malaysia's ~200,000 paddy and vegetable
smallholders (MADA/KADA granary zones + FAMA-linked veggie clusters) cannot afford the
automation that lifts yield. Commercial fertigation controllers — the class that meters
fertilizer into irrigation water — start at USD ~408 (Alibaba hydroponic controllers
[S52|T4]) and climb to Netafim-scale systems. Netafim's August 2026 launch of GrowSphere
FLEX, a digital fertigation controller explicitly aimed at smallholders and mid-sized
farmers [S51|T3], proves global vendors now see this exact buyer — but their price, cloud
dependency, and import channel keep them out of reach of a Malaysian smallholder farming
RM2-3k/ha. There is no <RM150, offline-first, solar-powered controller that a chili or paddy
farmer can buy once, install with a local co-op, and run without a subscription.

## 2. Market & size (device, not system)

| Segment | 4-yr units | Price | Market |
|---|---|---|---|
| TAM: paddy + vegetable smallholder plots suitable for fertigation retrofits (granary + veg clusters) | 30k-60k | RM129-149 | RM4-9M |
| SAM: MADA/KADA paddy zones + FAMA vegetable clusters + contract farms with co-op distribution | 15k-30k | RM129-149 | RM2-4.5M |

Anchors: food-security policy spending is rising (13MP SSR targets [S47|T2]); a commercial
controller is USD ~408+ [S52|T4] and Netafim's smallholder push [S51|T3] validates the
segment; device market is deliberately segmented from the RM-billions agri-input system
market (fertilizer, irrigation systems).

## 3. Solution & SoC architecture sketch

AgriCore-MY: a **single-die, solar-powered fertigation/irrigation controller SoC** on
SkyWater 130nm — EC/pH/moisture probe AFE, pump/valve PWM, Sub-GHz mesh, sold as a RM129-149
solar controller kit (probe-optional).

```
  EC/pH probes --- high-Z AFE + 12-bit SAR ADC 2ch (sky130 analog) --+-- AHB streaming --+
  Soil moisture --- comparator/ADC --------------------------------------------------+   |
  Solar panel --- MPPT charge controller (sky130 analog) --- PMU -------------------+   |
  Pump/valve --- PWM drivers + relay logic (ip-005-timer-pwm) --- APB <-- Ibex RV32IMC @50MHz --+-> SRAM 32kB (OpenRAM)
  Sub-GHz FSK mesh (CREATE, reuse Candidate-A radio IP) --- AHB packet FIFO             (AXI4-Lite + DMA)
  RS485/UART --- fertigation pump link --- APB
```
- **AXI4-Lite**: Ibex CPU + DMA + 32kB SRAM (multi-master).
- **AHB**: streaming — EC/pH capture FIFO, mesh packet FIFO, dosing-schedule datapath.
- **APB**: control — probe AFE gain/offset, PWM/valve config, RTC, PMU, UART/RS485, GPIO.
- **Analog**: MPPT solar charger, LDO, 12-bit SAR ADC with high-impedance EC/pH input,
  comparator (battery/wake).
- **Low-power story**: solar + battery; 2-minute duty cycle; deep sleep <15µA; mesh relay
  without gateway — a 10-acre plot covered by one node.
- **Pure Verilog-2001/2005**; CREATE: dosing/scheduling engine, probe AFE control, MPPT
  control; REUSE: Ibex, pulp-axi, OpenRAM, SPI/UART/I2C, timers/PWM, PMU (IP index STRONG);
  radio PHY/MAC reuses Candidate-A's in-house Sub-GHz IP (or external LoRa module option).

## 4. Why now

- The 13MP window (2026-2030) explicitly funds food security: 80% rice SSR target [S47|T2]
  and BERNAS's 80% SSL mission [S49|T2] create government attention and co-op channels.
- El Nino risk (MetMalaysia: >90% chance of a strong event by year-end, could rival
  1997-98 [S63|T2]) makes water/fertigation efficiency a live 2026 concern.
- Netafim's smallholder entry [S51|T3] validates demand at the exact price band we attack
  from below.
- Labor shortage + aging farmers: automation is the only way the SSR targets get met.

## 5. Competition & moat

- Commercial: Netafim (GrowSphere FLEX, cloud, USD-scale [S51|T3]), Alibaba hydroponic
  controllers ~USD 408 [S52|T4], ITC Water C3000 class [S54|T4] — all >RM1k locally.
- Academic: smart fertigation systems for Malaysian chili greenhouses are proven
  (UTHM [S53|T2]) — papers, not products.
- Open source: no open-silicon fertigation controller exists; no EC/pH AFE in our IP index
  (verified gap).
- **Moat**: offline-first solar controller at ~1/5 the imported price; open RTL; mesh
  without subscription; probe-agnostic AFE (works with cheap hobby-grade probes); dosing +
  probe AFE IP reusable in aquaculture (Candidate-H), pool control, industrial dosing.

## 6. Business model & unit economics

- Kit RM129-149 (controller + 2 valves + moisture probe; EC/pH probes optional) via
  FAMA/co-op channels + e-commerce; B2G pilots via MAFI/KPKM programs.
- BOM at RM129-149: SoC RM15-18 + EC/pH probes RM25-40 + solenoid valves RM15-25 + solar/
  battery RM15-20 + PCB/enclosure RM15-20 = **RM85-123; 10-30% margin** — thin, driven by
  probe cost; probe-optional starter kit protects the price point.
- Prototype: USD 9,750 chipIgnite or free Google MPW [S29|T1, S31|T1].

## 7. Risks & mitigations

- **Smallholder price sensitivity** (HIGH/HIGH): probe-optional kit, co-op bulk buying,
  B2G subsidies — hardware at cost, service via mesh network value.
- **Distribution/trust** (MED/HIGH): FAMA/MADA/KADA channel partnerships; extension-officer
  training kits.
- **Probe reliability at low cost** (MED/HIGH): probe-agnostic AFE; sensor-grade guide;
  warranty tiering.
- **Netafim low-end squeeze** (MED/MED): open RTL + local support + no-subscription mesh is
  the wedge they cannot copy without a Malaysian presence.
- **Yield uplift must be proven** (MED/HIGH): UTHM greenhouse data [S53|T2] + pilot plots
  before scale claims.

## 8. The Ask

RM 1.2M for: first silicon (~RM60k) + 2,000-kit pilot across two MADA districts and one FAMA
vegetable cluster + probe-qualification lab + co-op training program + SIRIM certification.
The thesis is Malaysia's first open-silicon agri controller; the company rides the 13MP
food-security budget that is already paying for everything except the chip.

*Composite 67.20/100 — FAIL (below 70 floor: market 60, unit economics 58). Honest verdict:
the problem is national policy, but smallholder hardware margins are brutal at RM150. Keep as
watch-item; revisit with a B2G-anchored business model.*
