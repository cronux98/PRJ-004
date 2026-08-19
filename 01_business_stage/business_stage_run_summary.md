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
