---
model: deepseek-v4-flash
provider: deepseek
stage: 01_business_stage
project: PRJ-004 (NEW)
date: 2026-08-19
---

# PRJ-004 (NEW) — Market Validation: 5 Questions, Risk Matrix, Verdicts
Scoring chain (evidence -> normalized -> composite -> verdict) lives in
candidates_scores.json; this file is the per-candidate validation layer.
Validation question set applied identically to all candidates; every answer is cited.

---

## CANDIDATE-A: BanjirSense-MY — community flood early-warning node SoC

### 5 validation questions
1. **Is the problem real, long-standing, and unsolved in Malaysia?** YES. Flood losses are
   recurring and quantified: RM6.1B (Dec 2021) [S03|T1, S01|T2], RM933.4M (2024) [S04|T1],
   RM636.9M (2025) [S05|T2]; World Bank flags rising climate-driven costs [S06|T2]. Existing
   warning is basin/area-level (NaFFWS [S08|T2], JPS sirens [S07|T2]) with no affordable
   community-level sensing.
2. **Is there a credible buyer/payer channel for the DEVICE?** YES. (a) Community/individual:
   M40/T20 urban households in flood-prone areas (avg income RM8,479/mo [S40|T2]); (b) govt:
   JPS/NADMA/state agencies running NaFFWS expansion [S09|T1, S08|T2] plus RM25M 2025 repair
   allocation [S42|T5]; (c) schools/condos/SMEs as institutional buyers.
3. **Can the device retail < RM150 with a survivable margin?** YES (marginal). BOM model
   RM82-116 at RM129 retail (SoC RM15-18, ultrasonic RM20-30 [S39|T5], battery/solar RM12-18,
   PCB RM12-15, enclosure RM15-20); on-die radio removes the LoRa module cost that pushes
   commercial nodes to USD 234+ [S10|T1]. Margin 15-35% — volume + govt pilots de-risk.
4. **Can the SoC be built on sky130 with Verilog-2005 + AMBA 3-tier + analog/SRAM?** YES with
   one named risk. Digital spine fully proven (Ibex idx#13, pulp-axi idx#18, OpenRAM idx#25,
   peripherals idx#32-41; all T1). Analog (SAR ADC, comparator, LDO, PLL) designable on sky130
   [S34|T1]. 3-tier AMBA justified by CPU+DMA masters and streaming sensor/radio datapaths.
   RF front-end on sky130 NOT silicon-proven (T5 hypothesis) — mitigation: in-house digital
   baseband + external RF front-end module fallback [baseline_metrics.json].
5. **Are regulatory/ecosystem hurdles bounded?** YES. SIRIM Type Approval (MCMC label) is the
   known path, 2-6 months [S37|T3]; 433/915MHz SRD band; no medical certification; national
   semiconductor policy (NIMP 2030/NSS [S38|T3]) supports local silicon.

### Risk matrix
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| RF front-end not tapeout-ready on sky130 | MED | HIGH | External RF FE module v1; in-house digital PHY is the deliverable anyway |
| Community adoption slower than model | MED | MED | Govt pilots (JPS/NADMA), schools, condo channel; B2G before B2C |
| BOM creep vs RM150 ceiling | MED | MED | On-die radio removes module cost; enclosure tiering (pole vs wall) |
| LoRaWAN ecosystem lock-in by buyers | LOW | MED | Mesh works standalone; optional LoRa module attach via SPI |
| SIRIM/band-plan delays | LOW | LOW | 433MHz SRD established; budget 2-6 months [S37|T3] |

### Verdict: PASS — composite 72.15 (>= 70), no dimension < 40, all 5 validation questions YES.
Failing metrics: none.

---

## CANDIDATE-B: JagaCare-MY — elderly aging-in-place health & safety monitor SoC

### 5 validation questions
1. **Is the problem real, long-standing, and unsolved in Malaysia?** YES. Malaysia crosses
   15%-aged (60+) in 2030 [S15|T1, S14|T2] — inside the 4-year window; 2.6M aged 65+ today
   [S14|T2]. Care-giver shortage and aging-in-place demand are standing national policy topics
   [S16|T1]. Device market: affordable middle (one-time, privacy-first, on-device) is empty —
   free app check-ins vs RM1,700+ watches vs cloud-AI subscriptions [S18|T3, S20|T4].
2. **Is there a credible buyer/payer channel?** YES. Urban M40/T20 adult children of elderly
   parents (1.2-1.5M households modeled from [S40|T2] + [S14|T2]); care homes and NGOs as
   institutional channel; MOH digital-health direction (FHIR HIN [S19|T2]) opens future
   data-interop pull.
3. **Can the device retail < RM150 with a survivable margin?** YES (tight). Wearable BOM
   RM63-85 at RM139 retail (SoC RM17-20, IMU RM8-12, PPG RM10-15, battery RM8-10, strap/PCB/
   enclosure RM20-28). Price band validated by fall-watch market USD 100-200 [S18|T3]. Margin
   30-45% at volume; hub+wearable bundle (RM99+RM139) improves ACV.
4. **Can the SoC be built on sky130 with Verilog-2005 + AMBA 3-tier + analog/SRAM?** YES with
   the hardest RF risk of the three. Digital core proven (Ibex, OpenRAM, peripherals — T1);
   DSP accelerator is standard Verilog; PPG ADC path designable [S34|T1]. 2.4GHz GFSK analog
   front-end is NOT silicon-proven on sky130 (T5) — mitigation: external BLE RF FE + in-house
   baseband/link (CREATE core preserved) [S35|T2 confirms no open RTL alternative].
5. **Are regulatory/ecosystem hurdles bounded?** YES with a marketing constraint. SIRIM Type
   Approval required (radio) [S37|T3]; non-medical positioning avoids MDA registration —
   validated as a standing constraint in market_requirements.md (WON'T v1).

### Risk matrix
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| 2.4GHz RF FE on sky130 infeasible | HIGH | HIGH | External RF FE module; in-house digital baseband/link remains the CREATE asset |
| Smartwatch substitution (Apple/Huawei) | MED | HIGH | Price (RM139 vs RM1,700+) + elderly-first UX + local support + privacy story |
| Medical-claims regulatory trap | MED | HIGH | Non-medical marketing; no MDA claims; monitor-not-diagnose positioning |
| BOM creep in wearable form factor | MED | MED | Module reuse across hub+wearable; strap tiering |
| Trust/adoption by elderly users | MED | MED | Family-gateway UX (adult children buy, parents wear); local MY languages |

### Verdict: PASS — composite 70.85 (>= 70), no dimension < 40, all 5 validation questions YES.
Failing metrics: none (weakest dimensions: competition & gap 62, technical feasibility 65,
unit economics 65 — all above the 40 floor; named as watch-items).

---

## CANDIDATE-C: EVCore-MY — smart EV AC-charger controller SoC

### 5 validation questions
1. **Is the problem real, long-standing, and unsolved in Malaysia?** YES. Charging gap is
   quantified: 3,600 public points end-2024 vs 10,000 target end-2025 [S24|T2]; targets
   "a long way off" per Roland Berger [S24|T2]. BEV base growing 40-70%/yr [S21|T1, S22|T2].
   The controller-silicon gap: no Malaysia-designed open EVSE controller SoC; imports
   dominate [S45|T4, market scan].
2. **Is there a credible buyer/payer channel?** YES. (a) MY charger OEMs (wallbox makers,
   RM2,800-7,000 systems [S25|T4, S26|T4]) need controller modules; (b) CPOs (ChargEV 196->501
   points [S44|T3], Gentari, JomCharge) need OCPP-compliant AC points; (c) retrofit market for
   existing dumb chargers (OCPP modules RM150-300 anchor [S45|T4]).
3. **Can the device retail < RM150 with a survivable margin?** YES. Module BOM RM75-105 at
   RM139 retail (SoC RM18-22, WiFi module RM25-35, power RM10-15, PCB RM12-18, relay/CT
   RM10-15); margin 25-45%. Undercuts imported OCPP modules (RM150-300) [S45|T4].
4. **Can the SoC be built on sky130 with Verilog-2005 + AMBA 3-tier + analog/SRAM?** YES —
   highest confidence of the three: no on-die RF (WiFi external, pre-certified). All digital
   blocks proven (cv32e40p idx#15 @100MHz, OpenRAM 64kB idx#25, fabrics idx#18, peripherals —
   T1); CAN controller + metrology DSP are textbook Verilog-2001; metering ADC + CP analog
   designable on sky130 [S34|T1]. 3-tier AMBA justified: CPU+DMA masters, metering/display
   streaming on AHB, control on APB.
5. **Are regulatory/ecosystem hurdles bounded?** YES. MS IEC 61851 (Type 2 CP) + OCPP 1.6/
   2.0.1 conformance via OCA ecosystem [S28|T3]; SIRIM covered by pre-certified WiFi module +
   local OEM channel [S37|T3]; legal metrology avoided (non-billing v1); aligns with NIMP
   2030/NSS semiconductor strategy [S38|T3].

### Risk matrix
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Global chip vendors (NXP/TI/ST) squeeze pricing | MED | HIGH | Open-silicon + local support + module-level integration; target MY OEMs, not global |
| OCPP conformance cost/time | MED | MED | OCA certification path [S28|T3]; start with OCPP 1.6J (broad installed base) |
| WiFi module cost erodes margin | MED | MED | Pre-certified module at volume; later in-house BLE/Sub-GHz pairing radio |
| Charger safety standards (IEC 61851) compliance burden | MED | MED | CP analog per standard; partner OEMs own system-level certification |
| Charging-market consolidation | LOW | MED | Diversify: metering IP reusable for smart meters/solar inverters |

### Verdict: PASS — composite 71.60 (>= 70), no dimension < 40, all 5 validation questions YES.
Failing metrics: none.

---


## CANDIDATE-D: AgriCore-MY — solar fertigation/irrigation controller SoC for paddy & vegetable smallholders

### 5 validation questions
1. **Is the problem real, long-standing, and unsolved in Malaysia?** YES. Rice SSR misses every
   target: 75% by 2025 "increasingly unlikely" [S48|T2], 13MP wants 80% [S47|T2], BERNAS handed an
   80% SSL mission [S49|T2]; yields stagnate vs input costs and weather [S50|T2]. Smallholders lack
   affordable fertigation automation (imports USD ~408+ [S52|T4]; Netafim entering the segment [S51|T3]).
2. **Is there a credible buyer/payer channel for the DEVICE?** YES (weak). FAMA/MADA/KADA co-op
   channels and MAFI B2G programs exist, but the primary buyer is a price-sensitive smallholder —
   the weakest payer in the Malaysian economy (market_fit 60 reflects this).
3. **Can the device retail < RM150 with a survivable margin?** MARGINAL — BOM RM85-123 at RM129-149
   leaves 10-30%; probe cost can erase it (unit_economics 58). Treated as not-YES for PASS purposes.
4. **Can the SoC be built on sky130 with Verilog-2005 + AMBA 3-tier + analog/SRAM?** YES. All digital
   proven (Ibex idx#13, OpenRAM idx#25, peripherals — T1); EC/pH high-Z AFE + 12-bit SAR + MPPT
   designable [S34|T1]; radio reuses Candidate-A Sub-GHz IP. 3-tier AMBA justified (CPU/DMA masters,
   sensor streaming on AHB, control on APB).
5. **Are regulatory/ecosystem hurdles bounded?** YES. SIRIM only if radio enabled [S37|T3]; no agri
   certification for a controller; distribution, not regulation, is the ecosystem risk.

### Risk matrix
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Smallholder price sensitivity | HIGH | HIGH | Probe-optional kit, co-op bulk buying, B2G subsidies |
| Distribution/trust | MED | HIGH | FAMA/MADA/KADA channels; extension-officer training |
| Probe reliability at low cost | MED | HIGH | Probe-agnostic AFE; sensor-grade guide; warranty tiering |
| Netafim low-end squeeze | MED | MED | Open RTL + local support + no-subscription mesh |
| Yield uplift must be proven | MED | HIGH | UTHM greenhouse data [S53|T2] + pilot plots before scale claims |

### Verdict: FAIL — composite 67.20 (< 70 floor), no dimension < 40 (min 58), validation Q3 not fully YES.
Failing metrics: market_fit_size 60, unit_economics 58. Watch-item, not dead end — B2G-anchored model could flip it.

---

## CANDIDATE-E: SolarSync-MY — residential solar self-consumption optimizer & monitor SoC

### 5 validation questions
1. **Is the problem real, long-standing, and unsolved in Malaysia?** YES. NEM Rakyat quota fully
   taken up (May 2025, SEDA data) [S56|T3]; 1.75GW rooftop base [S59|T4]; owners lack a brand-agnostic
   way to see solar-vs-consumption and shift loads (inverter apps closed [T5 analysis]; EMS RM1,000+
   [S60|T4]; imports measure-only [S61|T4]).
2. **Is there a credible buyer/payer channel?** YES. SEDA-certified installer channel attaches at
   install; e-commerce DIY retrofit for the 1.75GW base [S58|T1, S59|T4].
3. **Can the device retail < RM150 with a survivable margin?** YES. BOM RM56-82 at RM139 (SoC
   RM15-18, 2x CT RM10-15, relay RM8-12, PSU RM8-12, PCB/enclosure RM15-25); margin 30-50%.
4. **Can the SoC be built on sky130 with Verilog-2005 + AMBA 3-tier + analog/SRAM?** YES — easiest
   silicon in batch 2: metering DSP shared with Candidate-C (proven design), 2x 16-bit oversampled
   ADC + zero-cross analog designable [S34|T1]; no RF on-die v1. 3-tier AMBA justified (CPU/DMA
   masters, metrology streaming on AHB, control on APB).
5. **Are regulatory/ecosystem hurdles bounded?** YES. No radio v1 = minimal SIRIM [S37|T3]; CT
   metering explicitly non-billing (legal metrology avoided); installer ecosystem is the rail.

### Risk matrix
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Inverter apps get better | MED | HIGH | We actuate (relay), they only display; brand-agnostic + offline |
| CT accuracy disputes | MED | MED | Metering-grade accumulation, non-billing positioning, per-unit calibration |
| Installer channel concentration | MED | MED | Multi-EPC white-label + direct e-commerce |
| Sub-GHz module adds SIRIM time | LOW | LOW | v1 display/wired; module optional; SIRIM path known [S37|T3] |
| Smart-meter AMI absorbs use-case | LOW | MED | AMI gives data, not actuation — optimizer function survives |

### Verdict: PASS — composite 71.45 (>= 70), no dimension < 40, all 5 validation questions YES.
Failing metrics: none (weakest: competition & gap 60 — crowded at the edges, empty in the middle).

---

## CANDIDATE-F: HazeGuard-MY — indoor air quality + CO2 monitor SoC calibrated to Malaysia's API

### 5 validation questions
1. **Is the problem real, long-standing, and unsolved in Malaysia?** YES. Aug 2026 haze: 11-12
   stations unhealthy, Serian API 204 [S63|T2]; official API network is outdoor-only and sparse;
   indoor exposure (schools/homes) unmeasured [S67|T2]; school CO2 monitors demanded since 2021
   [S66|T3]; haze returns every dry season [S65|T3].
2. **Is there a credible buyer/payer channel?** YES. M40/T20 urban households (RM8,479/mo [S40|T2]);
   school/kindergarten bulk via MOE-linked procurement; SME/office channel.
3. **Can the device retail < RM150 with a survivable margin?** YES (two-SKU). PM-only RM99 (BOM
   RM60-80, margin 20-40%); +CO2 RM149 (BOM RM95-130, margin 13-35%). CO2 SKU is thin but the PM SKU
   carries the floor.
4. **Can the SoC be built on sky130 with Verilog-2005 + AMBA 3-tier + analog/SRAM?** YES. The hard
   measurement heads (laser PM, NDIR CO2) are commodity external sensors; the SoC does fusion,
   Malaysia-API calibration, display, and mesh — all proven digital blocks (Ibex, OpenRAM, peripherals
   T1) plus trivial analog. 3-tier AMBA justified (sensor streaming on AHB, control on APB).
5. **Are regulatory/ecosystem hurdles bounded?** YES. SIRIM only if radio enabled [S37|T3]; no
   mandatory consumer IAQ certification; NRES/DOE API network is the natural calibration partner.

### Risk matrix
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| CO2 sensor cost squeezes margin | MED | HIGH | PM-only RM99 SKU; CO2 premium SKU; volume pricing |
| Commodity import flood (Xiaomi/Aqara) | MED | HIGH | Local API calibration + mesh + school channel + open RTL |
| Sensor accuracy disputes | MED | MED | Cross-calibration vs DOE stations during haze events; publish data |
| Haze seasonality = lumpy demand | MED | MED | School-year procurement calendar; CO2/ventilation use-case year-round |
| API scale changes | LOW | LOW | Calibration table is firmware-updatable |

### Verdict: PASS — composite 70.90 (>= 70), no dimension < 40, all 5 validation questions YES.
Failing metrics: none (weakest: unit economics 60 — CO2 SKU margin).

---

## CANDIDATE-G: HomeEye-MY — privacy-first smart video doorbell SoC

### 5 validation questions
1. **Is the problem real, long-standing, and unsolved in Malaysia?** YES. Doorbells start RM552
   [S70|T4], systems RM1-2k [S71|T4], all foreign-cloud with subscriptions; no <RM150 local-first,
   no-subscription, PDPA-friendly option exists.
2. **Is there a credible buyer/payer channel?** YES. M40/T20 urban households; e-commerce + local
   security integrators (who today bundle imports [S71|T4]).
3. **Can the device retail < RM150 with a survivable margin?** MARGINAL — BOM RM96-134 at RM139-149
   (camera RM25-35, WiFi RM25-35, PSRAM RM8-12, SoC RM18-22, PSU/PCB/enclosure RM20-30) leaves 3-30%;
   survivable only at volume with component tiering (unit_economics 54). Treated as not-YES for PASS
   purposes.
4. **Can the SoC be built on sky130 with Verilog-2005 + AMBA 3-tier + analog/SRAM?** YES with the
   hardest CREATE of the batch: low-res vision accelerator on 100MHz-class core + external PSRAM;
   camera via DVP module. Feasible, ambitious (technical_feasibility 64).
5. **Are regulatory/ecosystem hurdles bounded?** YES. Pre-certified WiFi module covers SIRIM [S37|T3];
   PDPA alignment is a selling point; firmware security is budgeted scope, not a blocker.

### Risk matrix
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Margin squeeze vs RM150 ceiling | HIGH | HIGH | Component tiering; white-label volume; revisit price floor |
| Vision accelerator complexity | HIGH | HIGH | v1 = motion + PIR + low-res person; cloud-optional ID later |
| Ring/Eufy brand gravity | MED | HIGH | Local-first privacy + no-subscription + open RTL; different buyer |
| WiFi module certification | MED | MED | Pre-certified module covers SIRIM |
| Firmware security burden | MED | HIGH | Signed boot, encrypted local storage, OTA as first-class scope |

### Verdict: FAIL — composite 66.60 (< 70 floor), no dimension < 40 (min 54), validation Q3 not fully YES.
Failing metrics: unit_economics 54, technical_feasibility 64. Watch-item — flips if component prices keep falling or a B2B anchor order lands.

---

## CANDIDATE-H: AquaPulse-MY — aquaculture pond brain SoC (DO/temp/pH AFE, aeration, auto-feeder)

### 5 validation questions
1. **Is the problem real, long-standing, and unsolved in Malaysia?** YES. USD 1B production value
   (2023) [S74|T1], RM11.55B trade [S75|T2], 392.4kt brackishwater output [S76|T1]; DO crashes kill
   ponds overnight; tools are industrial imports (OxyGuard class [S78|T1]) or handheld meters
   [S79|T5]; no <RM150 multi-param pond controller exists.
2. **Is there a credible buyer/payer channel?** YES (small). 10-25k intensively-managed ponds via
   DOF-linked co-ops and aquaculture suppliers; the device SAM (RM0.7-1.8M) is the smallest of the
   batch (market_fit 55).
3. **Can the device retail < RM150 with a survivable margin?** MARGINAL — galvanic DO probe RM40-70
   can breach the ceiling (BOM RM110-168); DO-probe-optional kit (BOM RM85-118) keeps margins
   20-45% (unit_economics 58). Treated as not-YES for PASS purposes.
4. **Can the SoC be built on sky130 with Verilog-2005 + AMBA 3-tier + analog/SRAM?** YES. High-Z probe
   AFE + 12-bit SAR + MPPT + zero-cross designable [S34|T1]; digital spine proven; radio from
   Candidate-A. Sensor chemistry stays in external probes.
5. **Are regulatory/ecosystem hurdles bounded?** YES. SIRIM radio path known [S37|T3]; DOF extension
   channel exists; no aquaculture-device certification burden.

### Risk matrix
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Probe cost + lifetime | HIGH | HIGH | Probe-optional SKU; probe-agnostic AFE; volume sourcing |
| Small device market in MYR | MED | HIGH | IP portability (agri D + industrial water) is the exit valve |
| Farmer trust/tech adoption | MED | MED | DOF extension channels; demo ponds; harvest-saved pilots |
| OxyGuard price-drop | LOW | MED | Their cost structure cannot follow to RM149 |
| Pond-side ruggedization | MED | MED | IP65 enclosure; surge protection on relay lines |

### Verdict: FAIL — composite 66.75 (< 70 floor), no dimension < 40 (min 55), validation Q3 not fully YES.
Failing metrics: market_fit_size 55, unit_economics 58. Watch-item — strongest candidate to resurrect with a B2B/co-op anchor.

---

## CANDIDATE-I: ParkIQ-MY — in-ground parking occupancy sensor SoC for municipalities

### 5 validation questions
1. **Is the problem real, long-standing, and unsolved in Malaysia?** YES. KL motorists spend 25
   min/day searching [S80|T3]; Penang's ANPR enforcement was halted after 7,000-10,000 violations/
   month [S81|T2] — the data layer is missing; imports price at USD 100-300/bay [S83|T1, S84|T1].
2. **Is there a credible buyer/payer channel?** YES (slow). Municipal tenders (12-18 month cycles),
   private lot operators, PSP-style app operators [S82|T3]; the halted ANPR budgets are the wedge.
3. **Can the device retail < RM150 with a survivable margin?** YES. BOM RM53-75 at RM129-149 (SoC
   RM15-18, magnetometer RM8-12, battery RM10-15, potting/PCB RM12-18, radio RM8-12); margin 40-60%.
4. **Can the SoC be built on sky130 with Verilog-2005 + AMBA 3-tier + analog/SRAM?** YES. Magnetometer
   is a commodity I2C part; deep-sleep PMU + wake comparator designable [S34|T1]; 5-year battery is a
   power-budget design problem, not a silicon risk; radio from Candidate-A.
5. **Are regulatory/ecosystem hurdles bounded?** YES. SIRIM radio path known [S37|T3]; MAMPU
   procurement is slow but standardized; privacy-by-design (no plates) avoids the ANPR backlash.

### Risk matrix
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Municipal procurement cycles | MED | HIGH | Pilot-first strategy; private lot operators as fast channel |
| Imported-sensor price war | MED | MED | Open RTL + local support + no-subscription mesh; TCO story |
| In-ground deployment failure modes | MED | HIGH | Surface-mount option; potting quality; field-replacement design |
| Radio coexistence in dense bays | MED | MED | Mesh TDMA from Candidate-A PHY; channel planning kit |
| ANPR-style political backlash | LOW | HIGH | Position as data-for-drivers, never enforcement; no identity data |

### Verdict: FAIL — composite 68.90 just below the 70 floor; no dimension < 40 (min 60); all 5 validation
questions answer YES but the composite rule (>= 70) is not met — weakest dimensions (market 62,
competition 60, differentiation 64) sit below batch-1 passing candidates.
Failing metrics: market_fit_size 62, competition_gap 60, differentiation_novelty 64. One anchor municipal tender flips it.

---

## CANDIDATE-J: BusSafe-MY — school-bus child-presence safety SoC (tag + hub sweep protocol)

### 5 validation questions
1. **Is the problem real, long-standing, and unsolved in Malaysia?** YES — fatal and current. 5-year-
   old died after ~5h in a Johor school van (Apr 2025) [S86|T2]; 4-year-old heatstroke death in a car
   (Oct 2025) [S89|T2]; Gerik crash (Jun 2025) [S90|T5]. GPS trackers give location, not presence
   [S91|T3]; car-native systems don't fit vans or budgets [S93|T1]; academic prototypes are papers
   [S92|T2].
2. **Is there a credible buyer/payer channel?** YES. Regulation is the demand generator: Johor set
   van SOPs right after the death [S87|T2]; APAD/JPJ already mandate GPS for buses (compliance
   budget lines exist) [S91|T3]; operators, private schools, and state transport departments buy.
3. **Can the device retail < RM150 with a survivable margin?** YES. Hub BOM RM61-87 at RM139 (margin
   37-56%); tags BOM RM12-18 at RM19-29 (margin 30-55%); RM250-450 total per van.
4. **Can the SoC be built on sky130 with Verilog-2005 + AMBA 3-tier + analog/SRAM?** YES — highest
   feasibility of the batch. Seat AFE is comparators + SAR ADC (sky130); radio reuses Candidate-A
   Sub-GHz digital PHY with external RF FE; all digital blocks proven (IP index T1). 3-tier AMBA
   justified (tag-sweep streaming on AHB, control on APB).
5. **Are regulatory/ecosystem hurdles bounded?** YES — regulation HELPS here. SIRIM radio path known
   [S37|T3]; SOP mandates + APAD/JPJ framework are tailwinds, not burdens.

### Risk matrix
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Operator cost resistance | MED | HIGH | Regulation-driven demand (SOPs [S87|T2]); RM250-450 vs one death's liability; insurance discounts |
| Tag loss/durability | MED | MED | Sub-RM5 tag economics; seat-sensor fallback works without tags |
| False alarms erode trust | MED | HIGH | Sweep protocol with driver-confirm step; per-vehicle sensitivity tuning |
| Mandate may not arrive | MED | MED | Johor SOPs already exist [S87|T2]; sell to liability-aware operators + parents |
| Radio coexistence on buses | LOW | MED | Short-range FSK burst; Candidate-A PHY with TDMA |

### Verdict: PASS — composite 73.20 (>= 70), no dimension < 40, all 5 validation questions YES.
Failing metrics: none. Strongest batch-2 candidate and new overall top scorer across all 10.

---

## Aggregate (all 10)
| Rank | Candidate | Composite | Verdict | Position |
|---|---|---|---|---|
| 1 | **CANDIDATE-J: BusSafe-MY** — school-bus child-presence SoC | **73.20** | PASS | LOW-POWER (tag/hub) |
| 2 | CANDIDATE-A: BanjirSense-MY — flood early-warning node SoC | 72.15 | PASS | LOW-POWER |
| 3 | CANDIDATE-C: EVCore-MY — EV charger controller SoC | 71.60 | PASS | HIGH-PERFORMANCE |
| 4 | CANDIDATE-E: SolarSync-MY — solar self-consumption optimizer SoC | 71.45 | PASS | HIGH-PERFORMANCE |
| 5 | CANDIDATE-F: HazeGuard-MY — indoor AQI/CO2 monitor SoC | 70.90 | PASS | LOW-POWER |
| 6 | CANDIDATE-B: JagaCare-MY — elderly aging-in-place monitor SoC | 70.85 | PASS | LOW-POWER |
| 7 | CANDIDATE-I: ParkIQ-MY — parking occupancy sensor SoC | 68.90 | FAIL | LOW-POWER |
| 8 | CANDIDATE-D: AgriCore-MY — fertigation controller SoC | 67.20 | FAIL | LOW-POWER |
| 9 | CANDIDATE-H: AquaPulse-MY — aquaculture pond brain SoC | 66.75 | FAIL | LOW-POWER |
| 10 | CANDIDATE-G: HomeEye-MY — video doorbell SoC | 66.60 | FAIL | HIGH-PERFORMANCE |

- Recommended winner across all 10: **CANDIDATE-J BusSafe-MY (73.20)** — live regulatory moment
  (Johor SOPs after the 2025 van death [S86|T2, S87|T2]), highest batch-2 feasibility (Sub-GHz radio
  IP reused from A), healthy margins (hub 37-56%, tags 30-55%), reusable tag/hub IP. Batch-1 winner
  A (72.15) remains co-finalist on problem scale (RM0.6-6B/yr flood losses) and govt co-buyer channel.
- All ten verdicts are derivable bottom-to-top from candidates_scores.json (evidence -> normalized
  score -> weighted composite -> PASS/FAIL); composite math verified programmatically.
- Batch-2 FAILs (D 67.20, G 66.60, H 66.75, I 68.90) have no dimension below 40 — they are honest
  composites under the 70 floor and remain watch-items, not dead ends.
- Every verdict is a binary PASS/FAIL per the scoring rule; no graded/qualified verdicts exist in this stage.
