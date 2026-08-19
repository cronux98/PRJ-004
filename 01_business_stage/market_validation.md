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

## Aggregate
- Recommended winner: **CANDIDATE-A BanjirSense-MY (72.15)** — strongest Malaysia-specific
  unsolved problem, cleanest CREATE-wireless-in-house story (Sub-GHz FSK), credible
  govt/community co-buyer channel, highest IP-ability. C (71.60) is close on feasibility;
  B (70.85) passes but carries the 2.4GHz RF risk and the most crowded competitive field.
- All three verdicts are derivable bottom-to-top from candidates_scores.json
  (evidence -> normalized score -> weighted composite -> PASS/FAIL).
- Every verdict is a binary PASS per the scoring rule; no graded/qualified verdicts exist in this stage.
