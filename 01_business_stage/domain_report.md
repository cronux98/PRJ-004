# PRJ-004 (NEW) — Stage 0 Domain Report: Malaysia Market Context
Model: deepseek-v4-flash | Date: 2026-08-19 | Stage: 01_business_stage

Source convention: [Sxx|tier] -> research_corpus.json; T1 vendor/official, T2 peer-reviewed/standards,
T3 reputable secondary, T4 vendor PR, T5 community. Every numeric claim is cited.

---

## 1. National policy & structural context (the hooks)

1.1 **NIMP 2030 + National Semiconductor Strategy (NSS)** — Malaysia's E&E policy is shifting from
packaging/test to IC design and manufacturing; the government is actively courting local silicon
design capability [S38|T3]. A Malaysia-designed SoC thesis + product aligns with this push and is a
fundable/presentable story at national level.

1.2 **NETR (National Energy Transition Roadmap)** — net-zero by 2050 ambition; 45% GHG-intensity
reduction vs 2005 by 2030; low-carbon mobility (EV) is one of the six flagship levers [S27|T2].
Directly feeds Candidate C (EV charging) and indirectly A (climate adaptation).

1.3 **12th Malaysia Plan / MyDIGITAL** — digital-infrastructure and smart-city agendas continue;
flood resilience spending (NaFFWS) and digital health (MOH FHIR HIN since 2022) are both
operational programs [S08|T2, S19|T2].

1.4 **Climate & flood policy** — World Bank warned in 2025 that Malaysia's flood losses are rising
with climate change; 8 fatalities in the 2025 NE-monsoon season alone [S06|T2]. Flood management
is a permanent national budget line: RM25M was allocated in 2025 for immediate East-Malaysia
repairs after floods [S42|T5].

## 2. Demographic & structural trends (verified)

2.1 **Aging (Candidate B)**
- Aged 60+ = 7.9% (2010) -> projected 15.3% by 2030 — one of the fastest ageing trajectories
  globally (DOSM 2016 via MPRH) [S15|T1].
- 2.6M Malaysians aged 65+ = 7.7% of 34.1M (2024, DOSM via Malay Mail) [S14|T2].
- Malaysia becomes "aged nation" (65+ >= 20%) by 2048 (MOF) [S16|T1] — the 2026-2030 window
  covers the "ageing nation" 2030 crossing exactly.
- Contradiction resolved: "ageing nation 2030" (60+ >= 15%) vs "aged nation 2048" (65+ >= 20%)
  are different thresholds — both official, both cited [corpus.contradictions[0]].

2.2 **Flood exposure (Candidate A)**
- Dec 2021: RM6.1B losses (~0.4% GDP), 11 states, 60 districts, ~50 dead, ~400k evacuated
  [S01|T2, S02|T2, S03|T1].
- 2024 annual monsoon: RM933.4M [S04|T1]; 2025: RM636.9M [S05|T2].
- Recurrence is annual (Nov-Mar NE monsoon) and intensifying per World Bank [S06|T2].

2.3 **EV adoption (Candidate C)**
- 2024 TIV: 14,766 BEV + 30,796 hybrids (MAA) [S21|T1]; 46,403 xEV units per MITI [S22|T2].
- BYD 39.3% / Tesla 23.6% share of 2024 EV registrations (JPJ data) [S23|T3].
- Charging infrastructure: 3,600 public points at end-2024 vs 10,000 target end-2025; +153%
  growth in 2024; 30% DC share [S24|T2]. ChargEV alone grew 196 -> 501 points [S44|T3].

2.4 **Household income (affordability anchor for all three)**
- Average household income RM8,479/month (2022, DOSM HIES) [S40|T2]; B40 threshold RM5,249;
  M40 band RM5,250-11,819 [S40|T2]. Urban M40/T20 (KL/Selangor/Penang/JB) can absorb RM100-150
  safety/health/energy devices; the <RM150 ceiling is a mass-market sweet spot, not a luxury item.

## 3. Segmented market sizing (device vs system — strict separation)

Method: bottom-up unit modeling anchored to official statistics; every model labeled "model".
No official Malaysia device-market figures exist for these niches (stated as a gap).

### Candidate A — community flood early-warning node
| Segment | Units (4-yr) | Unit price | Market |
|---|---|---|---|
| TAM: flood-prone communities nationwide (kampung, sekolah, condo basement, road underpass, riverbank) | 300k-500k | RM129-149 | RM40-70M |
| SAM: urban (KL/Selangor/Penang/JB) + govt pilots (JPS/NADMA/MDAs) + schools | 100k-150k | RM129-149 | RM13-22M |
| System market (context, NOT device): national flood warning infra (NaFFWS, telemetry) | n/a | n/a | RM100M+ over program life [S08|T2, S09|T1] |
Anchor prices: RAK LoRaWAN level sensor USD 234-254 [S10|T1]; Milesight USD 504 [S11|T1];
Alibaba low-end USD 70-415 [S12|T4]. Our node (no network fee, local mesh) at RM129-149 undercuts
the entire commercial stack.

### Candidate B — elderly aging-in-place monitor
| Segment | Units (4-yr) | Unit price | Market |
|---|---|---|---|
| TAM: 3.6M aged 60+ (2026e); family + institutional care demand | 300k-500k devices | RM139-149 | RM40-70M |
| SAM: urban M40/T20 families w/ elderly parents (1.2-1.5M households) at 8-12% adoption | 100k-180k | RM139-149 | RM14-27M |
| System market (context): Malaysia patient-monitoring devices USD 403M (2024) -> USD 648M (2032) [S17|T4] | n/a | n/a | — |
Anchor: fall watches USD 100-200 [S18|T3]; app-only competitors free [S20|T4].

### Candidate C — smart EV AC-charger controller module
| Segment | Units (4-yr) | Unit price | Market |
|---|---|---|---|
| TAM: home AC charger installs (BEV base growing 40-70%/yr) + public AC points build-out + retrofit | 80k-150k modules | RM99-149 | RM8-22M |
| SAM: MY charger OEMs + CPOs + retrofit market, urban-centric | 50k-80k | RM99-149 | RM5-12M |
| System market (context): AC wallbox RM2,800-7,000 installed [S25|T4, S26|T4]; 10,000-point national build-out [S24|T2] | n/a | n/a | RM30-70M/yr |
Anchor: commodity OCPP 4G/WiFi modules RM150-300 [S45|T4] — we undercut.

## 4. Field cross-checks (what the numbers must survive)

4.1 **Prototype cost** — USD 9,750 chipIgnite full-SoC on SKY130 (vendor FAQ [S29|T1]) corroborated
by trade press [S30|T3]; free path via Google open MPW [S31|T1]. A thesis budget can fund first
silicon; volume economics then scale on mature 130nm.

4.2 **Sky130 capability** — Caravel-class SoCs run ~50MHz in 3.1x3.8mm user area with 37 pads
[S32|T1]; sky130B ships 1-2kB SRAM macros with OpenRAM for larger arrays [S33|T3]; analog
primitives for PLL/LDO/ADC/comparator are in the open PDK [S34|T1]. IP index confirms STRONG
reusable RISC-V cores, AXI fabric, SRAM, and peripherals (IP/index.md, T1).

4.3 **Wireless gap** — no production-grade pure-Verilog BLE or Sub-GHz transceiver RTL exists in
open source; LoRa PHY exists only as SDR software (gr-lora_sdr, SDR-LoRa) [S35|T2, S46|T5]. This
is the core CREATE-IP thesis for A and B — and the honest risk: sky130 RF front-end is not
silicon-proven (hypothesis, T5), mitigated by external RF front-end + in-house digital baseband.

4.4 **Regulatory** — SIRIM Type Approval (MCMC label) is mandatory for all radio devices; Mode B
2-6 months [S37|T3]. Non-medical positioning avoids MDA registration for B. EVSE additionally
touches MS IEC 61851 (CP signaling) and OCPP conformance [S28|T3] — handled via local OEM
partners in C.

4.5 **Income reality check** — RM129-149 retail = 1.5-1.8% of average monthly household income
[RM8,479, S40|T2] — consistent with impulse/consideration purchase for M40/T20 urban households.

## 5. Cross-checks between domains (contradiction hygiene)

- Flood losses: 2021 exceptional (RM6.1B) vs annual RM0.6-1B — pitches use annual as baseline,
  2021 as motivation ceiling [corpus.contradictions[1]].
- EV counts: BEV-only (14,766) vs xEV (46,403) vs charge points (3,600 vs 10,000 target) — each
  used with its own scope label [corpus.contradictions[2], [3]].
- Aging: 2030 vs 2048 thresholds — resolved as definitional [corpus.contradictions[0]].

## 6. Domain verdict

All three domains are genuine, cited, recurring Malaysian problems with a 2026-2030 window:
floods (A) = quantified annual losses + govt spending + coarse existing warning; aging (B) =
deterministic demographics + national policy attention; EV charging (C) = policy-mandated
build-out missing targets. Device-level markets are modest (RM5-70M) but real, and every
candidate undercuts its commercial substitute on price while adding an open-silicon
differentiator. Full scoring in candidates_scores.json.
