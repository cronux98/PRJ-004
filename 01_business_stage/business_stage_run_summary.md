# PRJ-004 (NEW) — Stage 0 Business Analysis Run Summary
Model: deepseek-v4-flash | Date: 2026-08-19 | Stage: 01_business_stage

## Mission
Generate 3 candidate full-SoC product ideas for Malaysia, research them online, score each
bottom-to-top (evidence -> normalized -> weighted composite -> PASS/FAIL), and present all
three as funding-style pitches. Winner becomes a brand-new masters thesis SoC.

## Candidates & composites (derivable from candidates_scores.json)
| Rank | Candidate | Composite | Verdict | Position |
|---|---|---|---|---|
| 1 | **CANDIDATE-A: BanjirSense-MY** — community flood early-warning node SoC | **72.15** | PASS | LOW-POWER |
| 2 | CANDIDATE-C: EVCore-MY — smart EV AC-charger controller SoC | 71.60 | PASS | HIGH-PERFORMANCE |
| 3 | CANDIDATE-B: JagaCare-MY — elderly aging-in-place monitor SoC | 70.85 | PASS | LOW-POWER |

**Recommended winner: CANDIDATE-A BanjirSense-MY.** Strongest Malaysia-specific unsolved
problem (recurring floods: RM6.1B 2021 / RM933M 2024 / RM637M 2025 — DOSM), cleanest
CREATE-wireless-in-house claim (Sub-GHz FSK digital PHY, no open RTL exists), credible
govt/community co-buyer channel (JPS/NADMA pilots, M40/T20 households), highest IP-ability.
C is the closest runner-up (best silicon feasibility — no RF on-die); B passes but carries
the hardest 2.4GHz RF risk and the most crowded competitive field. All three verdicts are
bottom-to-top derivable; no dimension of any candidate scores below 40.

## Deliverables (absolute paths)
1. /home/smdadmin/hermes_workspace/projects/PRJ-004/v0/01_business_stage/research_corpus.json
   — 46 tiered sources (S01-S46), learnings, 4 resolved contradictions, validation gaps
2. /home/smdadmin/hermes_workspace/projects/PRJ-004/v0/01_business_stage/domain_report.md
   — Malaysia policy/demographic hooks, segmented device-vs-system markets, field cross-checks
3. /home/smdadmin/hermes_workspace/projects/PRJ-004/v0/01_business_stage/competitive_analysis.md
   — 3-layer census (commercial/academic/open-RTL) with T1/T2 cites per spec cell
4. /home/smdadmin/hermes_workspace/projects/PRJ-004/v0/01_business_stage/baseline_metrics.json
   — sky130A PPA + economics baselines, tiered, field-corroborated
5. /home/smdadmin/hermes_workspace/projects/PRJ-004/v0/01_business_stage/market_requirements.md
   — MoSCoW per candidate + IP mapping to IP/index.md rows + technical constraints
6. /home/smdadmin/hermes_workspace/projects/PRJ-004/v0/01_business_stage/market_validation.md
   — 5 cited validation questions per candidate, risk matrices, PASS/FAIL verdicts, YAML header
7. /home/smdadmin/hermes_workspace/projects/PRJ-004/v0/01_business_stage/business_stage_run_summary.md
   — this file
8. /home/smdadmin/hermes_workspace/projects/PRJ-004/v0/01_business_stage/candidates_scores.json
   — bottom-to-top metric model (evidence -> scores -> composite -> verdict)
9. /home/smdadmin/hermes_workspace/projects/PRJ-004/v0/01_business_stage/01_pitch_candidate_A.md
   /home/smdadmin/hermes_workspace/projects/PRJ-004/v0/01_business_stage/01_pitch_candidate_B.md
   /home/smdadmin/hermes_workspace/projects/PRJ-004/v0/01_business_stage/01_pitch_candidate_C.md
   — funding-style pitches (<= 8 KB each)

## SELF_VALIDATION: PASS — 7-gate checklist
| # | Gate | Result | Evidence |
|---|---|---|---|
| 1 | All 9 deliverables exist, non-empty, valid | PASS | stat + JSON lint clean; pitch sizes 6.7-6.8 KB (< 8 KB) |
| 2 | Real web research with fetchable sources; no fabricated numbers | PASS | 46 sources with URLs in research_corpus.json; key figures extracted from live pages (DOSM via CNA RM6.1B; Roland Berger 3,600 vs 10,000; MPRH 15.3% by 2030; RAK USD 234-254) |
| 3 | Source tiers enforced (T1/T2 for numerics + gap claims) | PASS | tier per source; T4/T5-only claims labeled HYPOTHESIS (e.g., sky130 RF FE) |
| 4 | Bottom-to-top scoring chain derivable | PASS | candidates_scores.json: raw evidence (cited) -> normalized -> weighted composite -> PASS/FAIL; composite math printed per candidate |
| 5 | Device vs system market segmentation | PASS | domain_report.md section 3: TAM/SAM in MYR for the DEVICE; system markets given as context only |
| 6 | Inversion analysis (what makes it FAIL) | PASS | risk matrices in market_validation.md + "validation_gaps" in corpus + RF hypotheses labeled |
| 7 | Hard constraints honored | PASS | sky130 full SoC; AMBA 3-tier justified per candidate (AXI4-Lite/AHB/APB placement in pitches); Verilog-2001/2005 CREATE story; retail < RM150 with BOM models; M40/T20 targeting; zero claude/opus used (deepseek-v4-flash only); no external auditor; no kanban sub-tasks; no git push; absolute paths; other stage dirs untouched |

## Integrity notes
- Every verdict is a binary PASS per the scoring rule; no graded/qualified verdicts exist in
  this stage.
- market_requirements.md metrics reconcile with baseline_metrics.json (clock, SRAM, die,
  power, BOM, prototype cost).


================================================================
## BATCH 2 (2026-08-19) — 7 MORE CANDIDATES (D..J) — TOTAL 10
================================================================

## Mission
Extend the PRJ-004 Stage 0 candidate set from 3 to 10 with 7 NEW full-SoC product ideas for
Malaysia, across distinct sectors, same methodology (recursive deep-research, Comprehensive mode,
source tiers T1-T5, bottom-to-top scoring) and same hard constraints (sky130 full SoC, AMBA 3-tier,
pure Verilog-2001/2005, retail < RM150, novel/meaningful improvement, wireless CREATE in-house).
Batch-1 candidates A/B/C and their files (domain_report.md, competitive_analysis.md,
baseline_metrics.json, market_requirements.md, research_corpus.json) were NOT modified.

## New candidates & composites (batch 2; derivable from candidates_scores.json)
| Rank (all 10) | Candidate | Composite | Verdict | Sector |
|---|---|---|---|---|
| 1 | **J: BusSafe-MY** — school-bus child-presence SoC (tag + hub sweep) | **73.20** | PASS | Kids' safety / school transport |
| 4 | E: SolarSync-MY — solar self-consumption optimizer SoC | 71.45 | PASS | Solar / energy management |
| 5 | F: HazeGuard-MY — indoor AQI/CO2 monitor SoC | 70.90 | PASS | Air quality / public health |
| 7 | I: ParkIQ-MY — in-ground parking occupancy sensor SoC | 68.90 | FAIL | Smart parking / traffic |
| 8 | D: AgriCore-MY — fertigation controller SoC | 67.20 | FAIL | Agriculture / food security |
| 9 | H: AquaPulse-MY — aquaculture pond brain SoC | 66.75 | FAIL | Aquaculture |
| 10 | G: HomeEye-MY — privacy-first video doorbell SoC | 66.60 | FAIL | Home security |

No domain overlap with A (flood/weather), B (elderly care), C (EV charging). All 10 candidates
span 10 distinct sectors. Batch-2 FAILs are honest composites below the 70 floor (all dimensions
>= 40) — the model discriminates; they remain watch-items.

## Updated top-10 ranking (all candidates)
1. CANDIDATE-J BusSafe-MY 73.20 (NEW RECOMMENDED WINNER) | 2. CANDIDATE-A BanjirSense-MY 72.15 |
3. CANDIDATE-C EVCore-MY 71.60 | 4. CANDIDATE-E SolarSync-MY 71.45 | 5. CANDIDATE-F HazeGuard-MY 70.90 |
6. CANDIDATE-B JagaCare-MY 70.85 | 7. CANDIDATE-I ParkIQ-MY 68.90 | 8. CANDIDATE-D AgriCore-MY 67.20 |
9. CANDIDATE-H AquaPulse-MY 66.75 | 10. CANDIDATE-G HomeEye-MY 66.60

## Recommended winner ACROSS ALL 10: CANDIDATE-J BusSafe-MY (73.20)
Live regulatory moment (Johor van SOPs after the April 2025 child death; APAD/JPJ GPS mandate
already in place), highest batch-2 feasibility (Sub-GHz radio IP reused from Candidate-A, no exotic
analog), healthy margins (hub 37-56%, tags 30-55%), and a reusable tag/hub IP pair. Batch-1 winner
A (72.15) remains co-finalist on problem scale (recurring floods, RM0.6-6B/yr losses) and govt
co-buyer channel — the race is close, decided by timing (J) vs problem scale (A).

## Research stats (batch 2)
- 36 live web searches across 7 candidate domains (agri, solar, air quality, home security,
  aquaculture, parking, kids safety) + 6 full-page fetches (curl) for primary numbers.
- 43 new tiered sources (S47-S93 range): T1 x7 (FAO, DOSM, SEDA, MyCC, OxyGuard, Oz Robotics,
  OmniWOT, Magna), T2 x12 (NST, Bernama, MalaysianReserve, Frontiers x2, Malay Mail haze, UKM,
  UTHM, The Vibes, The Star, FMT heatstroke), T3 x12 (KLPropertyTalk, FMT haze/ANPR, SoyaCincau,
  Accio, KATSANA, ProductNation, MIDA, Rakyat Post, Netafim launch, breathe-safe), T4 x8 (Solartech,
  TransitionZero, SOLARMAN, Amazon, Alibaba, ITC, inteligentnidum, Xiaomi), T5 x4 (Shopee DO meters,
  Wikipedia Gerik, labeled models). Batch-1 corpus sources reused where applicable (S27 NETR,
  S29/S31 prototype economics, S34 sky130 PDK, S37 SIRIM, S38 NIMP, S40 income).
- Key live-web figures: Serian API 204 (Malay Mail, Aug 2026); NEM Rakyat quota fully taken up
  (KLPropertyTalk, May 2025); Johor van death ~5h (The Vibes, May 2025); Penang ANPR halt +
  7-10k violations/mo (FMT, Aug 2026); 13MP SSR targets 80% rice / 98% fisheries (NST, Aug 2025);
  aquaculture ~USD 1B (FAO, 2023); Xiaomi Xiaomo doorbell RM552.40 (ProductNation).

## Batch-2 source table (id | tier | claim (short) | URL)
- S47 | T2 | 13MP targets: rice SSR 80%, fisheries 98%, vegetables 79% | https://www.nst.com.my/news/nation/2025/08/1254036/kpkm-boost-self-sufficiency-rice-fisheries-livestock-under-13mp
- S48 | T2 | 75% rice SSR by 2025 increasingly unlikely | https://themalaysianreserve.com/2025/04/14/malaysia-faces-uphill-battle-to-boost-rice-self-sufficiency/
- S49 | T2 | BERNAS to strengthen 80% rice SSL mission (Sep 2025) | https://www.bernama.com/en/news.php?id=2471897
- S50 | T2 | Paddy industry governance/tech-adoption review | https://www.frontiersin.org/journals/sustainable-food-systems/articles/10.3389/fsufs.2023.1093605/full
- S51 | T3 | Netafim GrowSphere FLEX smallholder fertigation launch (Aug 2026) | https://www.global-agriculture.com/crop-protection/orbia-netafim-launches-growsphere-flex-to-scale-digital-farming-for-smallholders-and-mid-sized-farmers/
- S52 | T4 | Alibaba hydroponic/fertigation controllers ~USD 408 | https://www.alibaba.com/showroom/hydroponic-controller-ph-ec.html
- S53 | T2 | UTHM smart fertigation system for chili greenhouses | https://publisher.uthm.edu.my/periodicals/index.php/rpmme/article/view/16807
- S54 | T4 | ITC Water C3000 irrigation/fertigation controller | https://www.itc.es/products/water-c3000/
- S55 | T1 | MyCC paddy & rice industry public report | https://www.mycc.gov.my/sites/default/files/pdf/newsroom/MyCC_Paddy+and+Rice+Industry+in+Malaysia+(Public+Report)_(ENG).pdf
- S56 | T3 | NEM Rakyat rooftop solar quota fully taken up (May 2025, SEDA data) | https://www.klpropertytalk.com/2025/05/residential-rooftop-solar-quota-under-net-energy-metering-fully-taken-up/
- S57 | T4 | NEM Rakyat quota +100MW to 600MW | https://solartech.com.my/news/great-news-government-increases-nem-rakyat-quota-by-100mw/
- S58 | T1 | SEDA NEM FAQ (official program documentation) | https://www.seda.gov.my/misc/frequently-asked-questions/net-metering-nem-faq/
- S59 | T4 | MY rooftop solar ~1.75GW, 80% in Selangor/Johor/Kedah/Penang (TransitionZero) | https://www.linkedin.com/posts/transitionzero_the-malaysian-government-has-long-viewed-activity-7404819817918111744-_ZkN
- S60 | T4 | SOLARMAN EMH-2 home energy management system | https://www.solarmanpv.com/
- S61 | T4 | Amazon 16-circuit home energy monitor (USD 50-150 class) | https://www.amazon.com/Energy-Monitor-Real-Time-Electricity-Metering/dp/B0D1QR8S3B
- S63 | T2 | Aug 2026 haze: 11-12 stations unhealthy, Serian API 204; MetMalaysia >90% Super El Nino chance | https://www.malaymail.com/news/malaysia/2026/08/12/haze-hits-malaysia-as-12-air-monitoring-stations-record-unhealthy-api-readings/231096
- S65 | T3 | FMT: the haze is back, and will return again (Jul 2025) | https://www.freemalaysiatoday.com/category/leisure/2025/07/26/the-haze-is-back-and-will-return-again
- S66 | T3 | Experts call for compulsory CO2 monitors in schools (2021) | https://www.freemalaysiatoday.com/category/nation/2021/10/30/thwart-covid-in-school-make-co2-monitors-compulsory-say-experts
- S67 | T2 | UKM Sabah study: school indoor pollutants vs children's respiratory symptoms | https://repoemc.ukm.my/items/977e8623-cfc1-43d1-9d3c-5c539ca5810a
- S68 | T3 | Qingping air quality monitor USD ~150 | https://breathesafeair.com/air-quality-monitors/
- S70 | T4 | ProductNation: Xiaomi Youpin Xiaomo video doorbell from RM552.40 | https://productnation.co/my/28309/best-wireless-doorbell-malaysia/
- S71 | T4 | Smart home security system prices in MY RM1,000-2,000 | https://inteligentnidum.com/smart-home-security-system-price-in-malaysia/
- S72 | T3 | MIDA/Statista: MY smart home automation revenue USD 51.26M (2020) vs USD 4.16M (2015) | https://www.mida.gov.my/de/smart-homes-for-smart-living/
- S74 | T1 | FAO: 2023 MY aquaculture production value ~USD 1B | https://openknowledge.fao.org/bitstreams/e94b8125-5fd7-4d8b-853b-f0af398995c4/download
- S75 | T2 | Frontiers 2025: fish/seafood trade RM7.5B (2017) -> RM11.55B (2022) | https://www.frontiersin.org/journals/sustainable-food-systems/articles/10.3389/fsufs.2025.1545263/full
- S76 | T1 | DOSM: brackishwater aquaculture 392.4k t (2024) | https://www.dosm.gov.my/portal-main/release-content/selected-agricultural-indicators-malaysia-2024
- S77 | T3 | ~90% of farmed shrimp in MY is P. vannamei | https://www.researchgate.net/publication/390516074_Antimicrobial_Resistance_in_Malaysian_Shrimp_Aquaculture_and_Strategies_to_Reduce_Its_Occurrence
- S78 | T1 | OxyGuard Atlantic DO monitor/controller (industrial class) | https://globalaquaculturesupply.com/atlantic-dissolved-oxygen-monitor-controller/
- S79 | T5 | Shopee MY: handheld DO meters (RM200-600 class) | https://shopee.com.my/YAGO-Dissolved-Oxygen-Meter-Bluetooth-App-Connectivity-High-Precision-Water-Quality-Monitor-Aquaculture-Pond-Water-Monitoring-Portable-DO-Meter-i.102577476.52551595426
- S80 | T3 | Asia Mobiliti/BCG: KL motorists 25 min/day searching for parking | https://asiamobiliti.com/smart-technology-of-private-parking-lots-in-malaysia/
- S81 | T2 | FMT: Penang halts ANPR parking system; 7,000-10,000 violations/month (Aug 2026) | https://www.freemalaysiatoday.com/category/nation/2026/08/08/penang-govt-orders-immediate-halt-of-hot-anpr-parking-system
- S82 | T3 | SoyaCincau: Penang Smart Parking app launch (Aug 2019) | https://soyacincau.com/2019/08/19/penang-smart-parking-system-app/
- S83 | T1 | Oz Robotics LW009-SM LoRaWAN in-ground parking sensor | https://ozrobotics.com/shop/lorawan-in-ground-parking-sensor/
- S84 | T1 | OmniWOT ParkNode Gen1 in-ground LoRaWAN sensor | https://omniwot.com/product/parknode-gen1-parking-sensor/
- S85 | T3 | Accio: LoRa smart parking 2026 trends (USD 100-300 import class) | https://www.accio.com/business/lora-smart-parking
- S86 | T2 | The Vibes: 5-year-old dies after ~5h in Johor school van (May 2025) | https://www.thevibes.com/articles/news/107672/five-year-old-boy-dies-after-being-left-in-school-van-for-nearly-five-hours
- S87 | T2 | The Star: Johor sets van/bus guidelines after the death (May 2025) | https://www.thestar.com.my/news/nation/2025/05/22/johor-sets-guidelines-on-school-vans-buses-after-death-of-five-year-old
- S88 | T3 | Rakyat Post: parents reject RM100,000 settlement (Jul 2025) | https://www.therakyatpost.com/news/malaysia/2025/07/31/boy-dies-in-school-van-parents-reject-rm100000-settlement-demand-justice/
- S89 | T2 | FMT: girl, 4, dies of heatstroke left in car, Gua Musang (Oct 2025) | https://www.freemalaysiatoday.com/category/nation/2025/10/21/girl-4-dies-of-heatstroke-after-left-in-car
- S90 | T5 | Wikipedia: 2025 Gerik bus crash, 15 students killed | https://en.wikipedia.org/wiki/2025_Gerik_bus_crash
- S91 | T3 | KATSANA: APAD/JPJ ICOP GPS requirements for buses | https://www.katsana.com/gps-tracker-for-bus/
- S92 | T2 | UTHM: child presence detection car alarm using GSM (research) | https://publisher.uthm.edu.my/periodicals/index.php/ritvet/article/view/208/1068
- S93 | T1 | Magna interior sensing / child presence detection (car-native) | https://www.magna.com/products/electrical-electronics/adas-automated-driving/interior-sensing

## SELF_VALIDATION (batch 2): PASS — 7-gate checklist
| # | Gate | Result | Evidence |
|---|---|---|---|
| 1 | All deliverables exist, non-empty, valid | PASS | 7 pitch files (candidate_04..10/01_pitch_candidate_*.md) + candidates_scores.json (10 candidates, JSON lint clean) + market_validation.md (10 sections) + run summary; pitch sizes 6.5-7.7 KB (< 8 KB); composite math recomputed programmatically for all 10 |
| 2 | Real web research with fetchable sources; no fabricated numbers | PASS | 43 new sources with URLs in the table above; key figures fetched from live pages (Serian API 204; NEM Rakyat quota taken up; Johor van death; Penang ANPR halt; FAO USD 1B; 13MP SSR targets) |
| 3 | Source tiers enforced (T1/T2 for numerics + gap claims) | PASS | tier per source; T4/T5-only claims labeled (e.g., TransitionZero 1.75GW T4, Shopee DO prices T5, Wikipedia Gerik T5); TAM/SAM models explicitly labeled 'model' |
| 4 | Bottom-to-top scoring chain derivable | PASS | candidates_scores.json: evidence -> normalized -> weighted composite -> PASS/FAIL for all 10; composite_math printed per candidate; independent recompute clean |
| 5 | Device vs system market segmentation | PASS | per-pitch TAM/SAM tables in MYR for the DEVICE; system markets (agri inputs, solar installs, parking platforms, fleet tracking) given as context only |
| 6 | Inversion analysis (what makes it FAIL) | PASS | risk matrices per candidate in market_validation.md; FAIL candidates have explicit failing metrics + MARGINAL validation answers (D/G/H unit economics, I composite floor); no hidden assumptions |
| 7 | Hard constraints honored | PASS | sky130 full SoC; AMBA 3-tier justified per pitch (AXI4-Lite/AHB/APB placement); Verilog-2001/2005 CREATE stories (no SV); retail < RM150 with BOM models; 10 distinct sectors; zero overlap with A/B/C; deepseek-v4-flash only (no claude/opus); no kanban sub-tasks; no git push; batch-1 protected files untouched (domain_report.md, competitive_analysis.md, baseline_metrics.json, market_requirements.md, research_corpus.json) |

## Integrity notes (batch 2)
- Every verdict is a binary PASS/FAIL per the scoring rule; no graded/qualified verdicts exist in this stage (grep-checked).
- Every numeric and gap claim carries a tiered source (S47-S93) or an explicit 'model' label.
- Batch-1 files A/B/C sections in candidates_scores.json and market_validation.md preserved
  byte-identical; batch-2 evidence lives in per-candidate JSON entries, pitches, and this summary.
