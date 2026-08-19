# CANDIDATE-J: BusSafe-MY — The RM139 School-Bus Child-Presence Safety SoC for Malaysia's Van Tragedy Moment
*Funding-style pitch | PRJ-004 Stage 0 batch-2 | model: deepseek-v4-flash | 2026-08-19*

---

## 1. Problem (Malaysia-specific, with the news hook)

2025 was Malaysia's year of the forgotten child. On 30 April 2025 a five-year-old
kindergarten pupil was left unattended for nearly five hours inside a school van in Taman
Bukit Indah, Johor, and died; police detained the 56-year-old driver [S86|T2]. The state
government responded with new van guidelines and SOPs [S87|T2]; the family rejected a
RM100,000 settlement offer [S88|T3]. In October 2025 a four-year-old girl died of heatstroke
after being left in a car in Gua Musang [S89|T2]. And in June 2025, 15 university students
died in the Gerik bus crash [S90|T5], reopening the national argument about school-transport
safety. The pattern: **the checklists exist; the enforcement of the final "sweep the bus"
check does not.**

The unsolved problem is mechanical and human: a driver or attendant must walk the aisle and
verify every seat is empty after every trip. Fatigue, distraction, and a sleeping child
defeat that check — repeatedly, fatally. Existing products are GPS trackers (KATSANA-style,
APAD/JPJ-ICOP compliant [S91|T3]) that tell you where the bus is, not whether a child is
still in it; US car child-presence systems (Magna interior sensing [S93|T1]) are built for
cars, not vans, and cost far above RM150; Malaysian academic prototypes exist on paper
(UTHM GSM child-presence alarm [S92|T2]). There is no affordable, bus-native system that
automatically sweeps the vehicle, alarms on a child left behind, and works offline — no
subscription, no smartphone requirement for the driver.

## 2. Market & size (device, not system)

| Segment | 4-yr units | Price | Market |
|---|---|---|---|
| TAM: licensed school buses + vans (25-35k vehicles, labeled industry estimate) + institutional vans | 20k-40k systems | hub RM139 + tags RM19-29 | RM4-11M |
| SAM: van/bus operators in Johor/KL/Selangor/Penang under new SOP pressure + private schools | 10k-20k systems | hub RM139 + 10-20 tags | RM2-6M |

Anchors: the Johor death [S86|T2] triggered SOP mandates [S87|T2] — regulation is the
demand generator; GPS trackers are already APAD/JPJ-mandated for buses [S91|T3] (the wiring
and channel exist); US car-presence systems prove the feature but not the price [S93|T1];
vehicle-fleet estimate is a labeled model. Device market segmented from the RM50-200/yr
fleet-tracking subscription market.

## 3. Solution & SoC architecture sketch

BusSafe-MY: a **two-die product family on SkyWater 130nm** — a van-mounted hub SoC and a
coin-cell tag SoC — doing automatic child-presence sweep, driver checklist, and alarm.

```
TAG (child seat card, RM19-29):  Sub-GHz FSK burst SoC + coin cell — motion + presence beacon
HUB (driver console, RM139):     Sub-GHz FSK mesh (CREATE, reuse Candidate-A radio IP) --- AHB stream --+
  seat-sensor AFE (seat pressure, 8ch comparator/ADC, sky130 analog) ----------------------------------+  |
  buzzer + driver display (segment LCD, SPI) + relay (door interlock) --------------------- APB <-- Ibex RV32IMC @50MHz --+-> SRAM 32kB (OpenRAM)
  GPS + GSM module (external, optional) --- UART (KATSANA-style tracking [S91|T3])             (AXI4-Lite + DMA)
  temperature sensor (cabin heat alarm) --- I2C
```
- **AXI4-Lite**: Ibex CPU + DMA + 32kB SRAM.
- **AHB**: streaming — tag-sweep datapath (presence scan algorithm), seat-sensor FIFO,
  mesh packets.
- **APB**: control — AFE config, display, buzzer/relay, RTC, PMU, UART/GPS.
- **Analog**: 8ch seat-pressure comparator/ADC AFE, LDO, battery comparator, cabin-temp
  sense. Radio is digital baseband (from Candidate-A) + external RF front-end.
- **Low-power story**: hub runs on vehicle power with battery backup; tags sleep <5µA and
  beacon once per sweep — 2-year coin-cell life.
- **The sweep protocol (CREATE)**: after ignition-off or driver-card removal, the hub
  queries all tags + seat sensors; any child presence → 90dB buzzer + door interlock +
  SMS/GSM alert; the driver cannot close the trip without a confirmed empty sweep.
- **Pure Verilog-2001/2005**; CREATE: presence-sweep protocol, seat-sensor AFE, tag
  baseband (tiny FSK burst); REUSE: Ibex, pulp-axi, OpenRAM, SPI/I2C/UART, timers, PMU (IP
  index STRONG); radio IP from Candidate-A.

## 4. Why now

- The Johor death [S86|T2] and its SOP response [S87|T2] created a regulatory moment —
  guidelines are being written NOW, and devices that operationalize them ride the wave.
- Gua Musang heatstroke death [S89|T2] keeps child-in-vehicle safety in the national
  headlines through 2025-2026.
- APAD/JPJ already mandate GPS tracking for buses [S91|T3] — the compliance infrastructure
  and budget line exist; child-presence is the obvious next mandate.
- Gerik [S90|T5] keeps school-transport safety a standing national topic.
- The buyer is emotional and institutional at once: parents, operators, and state
  governments all want this to exist.

## 5. Competition & moat

- Commercial: KATSANA-class GPS trackers (location only [S91|T3]), US car child-presence
  (Magna [S93|T1] — cars, not vans, high cost), generic Chinese van monitors (no presence
  sweep, no local support).
- Academic: UTHM GSM child-presence alarm prototype [S92|T2] — a paper, not a product.
- Open source: no open-silicon child-presence system; sweep protocol + tag baseband absent
  from IP index (verified gap).
- **Moat**: bus-native sweep (seats + tags + driver checklist) at RM139 hub + RM19-29 tags;
  offline (no subscription); the Sub-GHz tag/hub pair is reusable for pets, logistics,
  event badges; regulatory tailwind (SOP mandates) is a moat no import can match locally.

## 6. Business model & unit economics

- Hub RM139 + tags RM19-29 each (10-20 per bus) sold to van/bus operators, private
  schools, and state transport departments (B2G); insurance-partner bundling later.
- Hub BOM at RM139: SoC RM15-18 + display RM10-15 + buzzer/relay RM8-12 + seat AFE parts
  RM8-12 + enclosure/PCB RM20-30 = **RM61-87; 37-56% margin**. Tag BOM RM12-18 at RM19-29
  (tiny PCB + coin cell RM3-5 + SoC RM8-10) = 30-55% margin.
- Prototype: USD 9,750 chipIgnite or free Google MPW [S29|T1, S31|T1].

## 7. Risks & mitigations

- **Operator cost resistance** (MED/HIGH): regulation-driven demand (SOPs [S87|T2]);
  RM250-450 total per van vs one death's liability; insurance discounts.
- **Tag loss/durability** (MED/MED): $0.50 tags economics; seat-sensor fallback works
  without tags.
- **False alarms erode trust** (MED/HIGH): sweep protocol with driver-confirm step;
  sensitivity tuning per vehicle.
- **Mandate may not arrive** (MED/MED): Johor SOPs already exist [S87|T2]; sell to
  liability-aware operators and parents (school channel) regardless.
- **Radio coexistence on buses** (LOW/MED): short-range FSK burst; reuse Candidate-A PHY
  with TDMA.

## 8. The Ask

RM 1.5M for: first silicon (~RM60k) + 3,000-vehicle pilot across Johor/KL operators under
the new SOP regime + SIRIM certification + insurance-partner pilot (premium discount
study). The thesis is Malaysia's first open-silicon child-presence system; the company
turns a national grief moment into a mandated safety standard. Four years: 15k+ systems,
RM3M+ SAM, and the tag/hub IP that every fleet in ASEAN will eventually need.

*Composite 73.20/100 — PASS. Strongest batch-2 candidate: live regulatory moment, highest
feasibility (radio IP reuse), healthy margins. New overall top scorer across all 10.*
