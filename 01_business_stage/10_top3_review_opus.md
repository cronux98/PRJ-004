# PRJ-004 — Top-3 Candidate Review & #1 Perfection Plan (Opus)

*Independent architecture + business review | Stage 0 gate | reviewer model: claude-opus-4-8 | 2026-08-19*
*Inputs read: all 10 pitches (A–J), `candidates_scores.json`, `market_validation.md`.*
*Owner profile: masters student, **first-ever SoC**, sky130, pure Verilog-2005, 3-tier AMBA, retail < RM150.*

> **Note on scope of authority:** I read the scoring model as an *input* and then applied independent
> engineering judgment weighted for **this specific owner** — a junior engineer whose FIRST SoC has to
> survive a thesis timeline and a viva. That reweighting moves my ranking away from the raw composite
> order, and I explain exactly why below. The composite still appears next to every pick.

---

## 0. The one lens the business scoring under-weighted

The scoring model gives `technical_feasibility` a 20% weight (correctly, the single largest), but it then
hands **70–82** feasibility to candidates whose core CREATE block is a **from-scratch wireless PHY**
(A: Sub-GHz FSK PHY+MAC; B: 2.4 GHz GFSK/BLE-class; and by inheritance D/F/H/I/J, which all "reuse
Candidate-A's radio IP" that *does not exist yet*). For an experienced team with a proven RF flow that
is a fair score. For a **first-time** SoC designer it is not.

A digital radio baseband + MAC is, block-for-block, the **hardest digital IP in the entire batch** —
on par with G's vision accelerator. It bundles preamble detection, symbol-timing recovery / CDR, bit
slicing, data whitening, framing, CRC/FEC, and (for the mesh candidates) a TDMA/relay MAC — *plus* an
sky130 RF front-end that every pitch already flags as "NOT silicon-proven." Betting a first thesis on
that is the highest-variance choice available.

**Consequence for ranking:** I promote the two candidates whose silicon has **no RF PHY at all**
(C and E) and treat the radio-dependent top scorer (J) as an excellent-but-riskier #3. This is the
core place where my judgment diverges from the composite, and it is deliberate.

---

## 1. Top-3 Ranking (independent judgment)

| My rank | Candidate | Composite (verdict) | Business rank | Position |
|---|---|---|---|---|
| **#1** | **C — EVCore-MY** (EV AC-charger controller SoC) | **71.60 (PASS)** | 3 | High-performance |
| **#2** | **E — SolarSync-MY** (solar self-consumption optimizer SoC) | **71.45 (PASS)** | 4 | High-performance |
| **#3** | **J — BusSafe-MY** (school-bus child-presence safety SoC) | **73.20 (PASS)** | 1 | Low-power (tag/hub) |

Everything ranked 4–10 (A 72.15, F 70.90, B 70.85, I 68.90, D 67.20, H 66.75, G 66.60) is discussed in
§1.4 so the cut is defensible, not silent.

### 1.1 #1 — CANDIDATE-C: EVCore-MY — composite 71.60 (PASS)

*Smart EV AC-charger controller SoC: energy-metrology DSP + CAN 2.0B + IEC 61851 control-pilot + OCPP-ready host, WiFi via external pre-certified module.*

**Why it wins for THIS owner (and beats E and J):**

1. **It is the most *buildable* rich-thesis SoC in the batch — no RF, by design.** Pitch C's own
   architecture decision ("No on-die RF: WiFi via pre-certified external module") is the single best
   risk call across all ten pitches. The scoring rewarded it with the **joint-highest feasibility (82)**.
   Remove the radio and the remaining blocks (a metrology datapath, a CAN FSM, a PWM/comparator CP
   engine) are all *textbook, bounded, synthesizable digital* — exactly the difficulty band a first SoC
   should live in.

2. **It carries the deepest, most examinable thesis surface.** Mixed-signal energy metrology (sinc/CIC
   decimation, RMS, active/reactive power, energy accumulation, calibration + error analysis) is a
   genuine DSP contribution; the CAN 2.0B engine is a canonical protocol FSM ideal for coverage-driven
   and *formal* verification; the CP interface is a small safety FSM (IEC 61851). That is three distinct
   verification chapters plus a bus-architecture chapter — E gives ~two, J gives a thinner silicon story
   (its novelty is a *protocol*, not a datapath). More on this in §2.

3. **It is the strongest "industry demand NOW" story in the batch, and the most reusable IP.** EV
   charging sits at the intersection of *automotive + energy transition + national semiconductor policy*.
   Pitch C's own framing — "a Malaysian EVSE SoC is a flagship 'Malaysia designs silicon' story" under
   NIMP 2030 / NSS — is real: the Low Carbon Mobility Blueprint's 10,000-point target was missed
   (3,600 at end-2024), so the build-out demand persists for the entire thesis-to-market window. And the
   two CREATE blocks (**metering DSP + CAN**) have the widest secondary markets of any candidate: smart
   meters (TNB AMI), solar inverters (literally candidate E), motor drives, BMS, industrial control.

4. **Commercially it undercuts a real, priced incumbent with a real channel.** The device attacks the
   RM150–300 imported OCPP retrofit module from below at RM139 while adding metering + CP + CAN on one
   die (25–45% modelled margin). The buyer is a business (MY charger OEMs / CPOs — Gentari, JomCharge,
   ChargEV/TNB), not a price-sensitive consumer, which de-risks the "< RM150 with survivable margin"
   question that sinks D/G/H.

5. **It fails *gracefully* for a junior.** The one hard part — 16-bit metrology analog — can be
   **externalized** (external ΔΣ/ADC feeding the on-chip *digital* metrology DSP) without losing the
   thesis contribution. No other top candidate lets you excise its hardest block and *keep its novelty*.

*The knock (addressed in §3):* as pitched, C is over-scoped for a first SoC — cv32e40p @100 MHz, 64 kB
dual-bank SRAM, CAN listed as CREATE, on-die 16-bit metering ADC. §3 scopes every one of these down.

### 1.2 #2 — CANDIDATE-E: SolarSync-MY — composite 71.45 (PASS)

*Residential solar self-consumption optimizer: 2-channel CT metering DSP + load-shift relay, no RF v1.*

**Why #2 (and why it's the natural "de-risked sibling" of C):**

1. **It is the single most *completable* SoC in the batch.** Scoring gives it feasibility 82 tied with C,
   but E has *fewer* CREATE blocks — it is essentially "C minus CAN minus the CP safety FSM": a metering
   datapath + a zero-cross relay scheduler. If the timeline slips, E is the safe harbour.
2. **Best-in-class unit economics + cleanest regulatory path.** RM56–82 BOM at RM139 (30–50% margin,
   "healthiest of the batch after I/J"), no radio → minimal SIRIM, CT metering explicitly non-billing so
   legal metrology is avoided. The SEDA-certified installer channel is a ready-made distribution rail.
3. **Direct IP synergy with #1.** E and C *share the metering DSP*. Whichever you build first, the other
   becomes a fast follow-on — a strong story for "reusable open IP" and a de-risked Chapter-on-reuse.
4. **Rides NETR / rooftop-solar policy that is demonstrably supply-constrained** (NEM Rakyat quota fully
   taken up May 2025; +100 MW top-up to 600 MW). Demand is pinned by policy for the window.

**Why it sits *below* C:** lower novelty (its own weakest dimension, differentiation 65 — "globally
incremental; EMS products exist"), a thinner protocol/safety surface (no CAN, no standards FSM), and a
narrower "flagship national" narrative than EV. As a *thesis vehicle* it has less depth to fill chapters
and less to impress a viva; as a *product* it is arguably the safest. That trade is why it is #2, not #1
— and why I recommend building C's metering DSP such that E falls out almost for free.

### 1.3 #3 — CANDIDATE-J: BusSafe-MY — composite 73.20 (PASS, batch top scorer)

*School-bus child-presence safety: hub SoC + coin-cell tag SoC, presence-sweep protocol, seat-pressure AFE, Sub-GHz link, door interlock + alarm.*

**Why it stays in the top 3 despite my reweighting:**

1. **The best "why now" in the entire batch — regulation that *helps*.** The 2025 Johor school-van death
   and the SOPs written in direct response make this "the rare case where regulation HELPS the product"
   (its own validation note). Timing 80, and an emotionally + institutionally funded buyer (parents,
   operators, state transport departments; APAD/JPJ compliance budget lines already exist).
2. **Genuinely novel systems contribution.** The presence-sweep protocol (ignition-off → query
   tags + seat sensors → interlock/alarm until a confirmed-empty sweep) is a clean, publishable,
   patent-adjacent idea that nobody sells. Highest novelty of batch-2 (74) with a clear story.
3. **Its analog is trivial** (seat-pressure comparators + SAR ADC) and it has healthy margins
   (hub 37–56%, tags 30–55%) at a low absolute buyer cost (RM250–450/van).

**Why it drops from business-#1 to my #3 (the honest reasons):**

- **It is a two-die product** (hub + tag). Two chips = two floorplans, two verification environments, a
  wireless *link* to verify between them, and roughly double the physical-design learning curve. That is
  a lot for a *first* SoC.
- **Its silicon still needs the radio.** The pitch says "radio is digital baseband (from Candidate-A) +
  external RF FE" and "tag baseband (tiny FSK burst)" — i.e. the from-scratch PHY risk from §0 is still
  present, just smaller. To make J junior-safe you must externalize the transceiver *entirely* (COTS FSK
  module + COTS beacon tag for the thesis), at which point the taped-out silicon novelty shrinks to
  "seat-AFE + sweep FSM + interlock," which is thinner than C's metrology + CAN.
- **Composite ≠ thesis-fit.** J's 73.20 is driven by *market timing* and *margins*, not by silicon depth
  or first-SoC achievability — the two axes that matter most for this owner. It remains an outstanding
  *product* and a strong #3, and it is the pick to reach for if the owner specifically wants a
  safety/impact thesis over an energy/automotive one.

### 1.4 Why the rest didn't make the cut (brief, so the cut is defensible)

- **A — BanjirSense (72.15, business #2):** biggest problem scale (RM0.6–6 B/yr floods) and the
  highest-value IP (radio PHY), but it is the **RF-PHY-risk poster child** — long-range Sub-GHz mesh with
  peer relaying + an unproven sky130 RF front-end is the *worst* first-SoC fit in the batch. Superb
  candidate for a *second* project or a team with RF experience; too risky as a first thesis.
- **F — HazeGuard (70.90):** easiest analog (all hard sensors external) but its silicon is a "glorified
  sensor hub," and its headline novelty ("Malaysia-API calibration") is a *firmware table*, not silicon.
  Achievable but thesis-thin, and it still leans on the Candidate-A mesh for its moat.
- **B — JagaCare (70.85):** **hardest radio of all** (2.4 GHz GFSK, "the hardest of our three radios")
  plus the medical-claims regulatory trap. Highest-variance analog; wrong for a first SoC.
- **I — ParkIQ (68.90, FAIL):** excellent unit economics (40–60%) and a pure low-power design, but
  crowded by cheap imports, slow municipal procurement, and *still* radio-dependent. A fine low-power
  study, not a top-3 thesis.
- **D / H / G (67.20 / 66.75 / 66.60, FAIL):** margin-structurally weak at < RM150 (D probes, H DO
  probes, G camera+WiFi+PSRAM). G additionally carries the batch's hardest CREATE (vision accelerator).
  All honest watch-items, none a first-SoC thesis.

---

## 2. #1 Pick — Masters Thesis Lens (Candidate C, EVCore-MY)

### 2.1 The contribution / novelty claim (what you actually defend)

> **"An open-source, sky130-fabricable EV-charger (EVSE) controller SoC that integrates a digital
> energy-metrology datapath, a CAN 2.0B protocol engine, and an IEC 61851 control-pilot interface on a
> real 3-tier AMBA fabric — delivered as auditable, 100% pure-Verilog RTL and closed with a
> coverage-driven PyUVM/Verilator verification methodology — targeting Malaysia's EVSE controller
> localisation gap under NIMP 2030."**

This is a *masters-appropriate* novelty: **systems integration + open IP + a verification methodology +
a mixed-signal metrology analysis**, aimed at a documented national industrial gap. You are **not**
claiming a new metrology algorithm or a new CPU — and you should say so explicitly, because over-claiming
is what viva panels punish. The defensible "firsts" are: *first open-source sky130 EVSE controller*;
*first fully pure-Verilog integration of metering-DSP + CAN + CP on the open PDK*; and the
*coverage-closure result* on that integration.

### 2.2 Chapter → deliverable map

| Ch | Title | Core content | Evidence of thesis depth |
|---|---|---|---|
| 1 | Introduction | Malaysia EV build-out gap (3,600 vs 10,000 points), NIMP 2030/NSS, problem statement | Business framing from pitch C |
| 2 | Background & literature | EVSE (IEC 61851, OCPP 1.6J), energy metrology, RISC-V SoCs, open PDK/sky130, AMBA | Positions the "firsts" honestly |
| 3 | SoC architecture & bus design | 3-tier AMBA rationale, master/slave map, address map, CDC plan | **Bus-architecture trade-off study** (§2.3) |
| 4 | Energy-metrology datapath (flagship) | CIC/sinc decimation, Vrms/Irms, P/Q/S, Wh accumulation, calibration + fixed-point error model | **Quantitative accuracy analysis vs a golden reference model** |
| 5 | CAN 2.0B engine + CP/IEC 61851 FSM | Bit-stuffing, arbitration, CRC-15, error frames; CP PWM + state detect | **Formal verification** of the safety/liveness properties |
| 6 | Functional verification | Coverage-driven PyUVM/cocotb over Verilator; ABV/assertions; scoreboard | **Methodology chapter — aligns with your existing toolchain** |
| 7 | Physical implementation | OpenLane hardening on sky130: floorplan, timing/Fmax, area, power; GLS with SDF | **GLS + STA + power = real back-end depth, no tapeout needed** |
| 8 | Results & discussion | Metrology accuracy, coverage closure, Fmax/area/power, limitations, future work | Honest scope boundaries; roadmap |

### 2.3 Analysis angles that give it genuine depth

- **Bus-architecture trade-off (Ch 3):** quantify *why three buses and not one* — measure latency,
  throughput, and area/LUT cost of the metering stream on **AHB** vs forcing it onto **AXI4-Lite**, and
  register access on **APB** vs AHB. This turns the mandated "3-tier AMBA" constraint into a *result*,
  not a checkbox. Directly answers the most common viva jab ("why the complexity?").
- **Metrology accuracy analysis (Ch 4):** build a Python golden model; sweep power factor and load;
  report error vs a reference (e.g., the class of an ADE-series meter), quantization noise, and THD
  sensitivity. This is the chapter that makes it a real *engineering* thesis, not an integration report.
- **Formal verification (Ch 5):** the CP FSM ("never energise the pilot in State A / fault") and CAN
  bit-stuffing/arbitration are small enough to prove with open formal tools (SymbiYosys) — a
  high-value, high-credibility result on a safety-relevant block.
- **Low-power analysis (Ch 7):** clock-gating the metering datapath during idle, power-domain sketch,
  activity-based power from GLS. Even as a "high-performance" positioned part, a power chapter adds depth.
- **GLS + CDC (Ch 7):** run gate-level sim with back-annotated SDF and document what RTL sim hid
  (X-propagation, reset, CDC between the metering clock and the CPU clock). Examiners *love* this because
  it shows you understand the RTL→silicon gap.

### 2.4 What a viva examiner will probe (rehearse these)

1. "You mandated a 3-tier AMBA fabric — prove it earns its complexity vs a single AXI-Lite bus." → Ch 3 numbers.
2. "How do you validate metering accuracy with no silicon and no bench?" → golden-model + calibration + error budget (Ch 4).
3. "CAN arbitration and bit-stuffing corner cases — how did you know you covered them?" → functional-coverage closure + formal (Ch 5/6).
4. "Is 40 MHz enough to run OCPP + metering + CP concurrently?" → cycle budget / utilisation analysis; note OCPP is firmware.
5. "Why picorv32 and not Ibex/cv32e40p — what did pure-Verilog cost you?" → auditability/Verilator-fit vs microarch features; honest trade.
6. "What fails at tapeout that your RTL sim never showed?" → GLS/CDC/analog-integration answer (Ch 7).
7. "Your novelty is integration — defend that as a masters contribution." → open-IP + methodology + national-gap framing (§2.1).

---

## 3. #1 Pick — Junior-Engineer First-SoC Scope Plan (HARD constraints honoured)

**Design rule for the whole project: pure Verilog-2001/2005 only. Zero SystemVerilog, zero VHDL in any
synthesizable source.** (Verification in Python/cocotb/pyuvm is fine and encouraged — that is not RTL.)

### 3.1 Physical budget (standalone sky130 die via OpenLane, **no tapeout required**)

| Parameter | Recommendation | Rationale |
|---|---|---|
| Target platform | **Standalone sky130A die** via the OpenLane/LibreLane flow (no Caravel harness — owner decision 2026-08-19) | Full pad ring, own I/O; ~**1–3 mm²** die area is comfortable for this block count |
| Std-cell logic budget | **~60–100 k cells** (core + peripherals + metering DSP + CAN) | picorv32 ≈ 10–15 k; the rest is small |
| SRAM | **16 kB baseline** (8 × 2 kB OpenRAM 1-port), 32 kB stretch | SRAM dominates area — budget ~0.5–1 mm². Start at 16 kB |
| Total area target | **~1–3 mm² die** | Leaves margin for a first back-end pass |
| Clock | **40 MHz core** (25 MHz safe fallback; **cut the 100 MHz**) | sky130 closes 25–50 MHz easily; 100 MHz is a back-end fight |
| Analog custom blocks | **≤ 3**: 1 PLL (or ext-clock + divider), 1×12-bit SAR ADC (CP/aux), 1–2 comparators (CP level, zero-cross). **LDO external.** | Keep analog tiny; *externalise the 16-bit metering ADC* |
| Deliverable | **Verified RTL + OpenLane hardening report (area/timing/power) + GLS** | Thesis stops at sign-off analysis; silicon is out of scope |

### 3.2 Module list (sized for one thesis timeline: RTL → verification)

| # | Module | REUSE / CREATE | Bus attach | Pure-Verilog source / note |
|---|---|---|---|---|
| 1 | **picorv32** CPU (RV32I[M]) | REUSE | AXI4-Lite master | `picorv32.v` (YosysHQ) — native Verilog; has `picorv32_axi` AXI4-Lite wrapper |
| 2 | AXI4-Lite interconnect | REUSE | — | alexforencich **verilog-axi** (pure Verilog) |
| 3 | AXI-Lite→AHB bridge | REUSE | AXI4-Lite↔AHB | ZipCPU **wb2axip** family (pure Verilog, *formally verified* — thesis bonus) |
| 4 | AHB→APB bridge | REUSE | AHB↔APB | ZipCPU / small custom APB bridge |
| 5 | SRAM 16 kB | REUSE (compiled macro) | AXI4-Lite slave | OpenRAM sky130 macros + behavioural Verilog model for sim |
| 6 | **Metering DSP datapath** | **CREATE (flagship)** | AHB slave (stream in) | CIC/sinc decimation + Vrms/Irms + P/Q/S + Wh accumulate + calib |
| 7 | **CAN 2.0B controller** | **REUSE / port** (⚠ was CREATE) | AHB/APB | OpenCores Verilog CAN (SJA1000-class) — *reclassify from CREATE*; check licence |
| 8 | **Control-Pilot (CP) engine** | **CREATE (small)** | APB | 1 kHz PWM gen + CP state FSM (IEC 61851 A/B/C/D) + comparator sampling |
| 9 | UART (debug + WiFi module link) | REUSE | APB | Efabless `EF_UART` (Apache-2.0, Verilog) |
| 10 | SPI host (display / EEPROM) | REUSE | APB | `EF_SPI` (Verilog) |
| 11 | I2C (RTC / EEPROM) | REUSE | APB | `EF_I2C` (Verilog) |
| 12 | GPIO | REUSE | APB | `EF_GPIO8` (Verilog) |
| 13 | Timers / PWM | REUSE | APB | `EF_TMR32` / `EF_PWM32` (Verilog) |
| 14 | Watchdog | REUSE | APB | small custom or `EF_*` |
| 15 | Clock/reset + PMU regs | CREATE (small) | APB | clock-gating + reset synchroniser + power/status registers |
| 16 | *(optional)* 1-channel DMA | CREATE-lite / **defer** | AXI4-Lite master | Only if metering→SRAM copy becomes a CPU bottleneck; else CPU-copy |

**CREATE count = 3 core blocks** (Metering DSP, CP engine, clk/rst-PMU) + optional tiny DMA. Everything
else is REUSE. That is the right shape for a first SoC: **one deep flagship (metering), two small
CREATEs, a large well-supported REUSE base.**

### 3.3 Bus map — 3-tier AMBA kept **real but simple**

```
                 ┌──────────────┐
   picorv32 ─────► AXI4-Lite     │  TOP TIER (multi-master, low-latency)
   (AXI-Lite      │  interconnect│◄──── optional 1-ch DMA (master)
    master)       └──┬────────┬──┘
                     │        │
              SRAM 16kB      AXI-Lite→AHB bridge
             (AXIL slave)         │
                          ┌───────▼────────┐  MID TIER (streaming datapaths)
                          │   AHB-lite bus  │
                          │  ┌───────────┐  │
                          │  │Metering   │  │  ← CT/voltage samples (from EXTERNAL ADC)
                          │  │DSP (CREATE)│  │
                          │  └───────────┘  │
                          │  CAN 2.0B FIFO   │
                          └───────┬─────────┘
                             AHB→APB bridge
                                  │
                    ┌─────────────▼──────────────┐  LEAF TIER (control regs, slow)
                    │            APB bus           │
                    │ CP engine · UART · SPI · I2C │
                    │ GPIO · Timers/PWM · WDT · PMU│
                    └─────────────────────────────┘
```

- **AXI4-Lite** = CPU + (optional) DMA + SRAM — the only place you need multi-master + low latency.
- **AHB-lite** = the two *streaming* datapaths (metering samples, CAN frame FIFO). This is what justifies
  the mid tier — and it is exactly the measurement you turn into the Ch-3 trade-off result.
- **APB** = every slow control register (CP, peripherals, PMU). Trivial, cheap, and where 90% of the
  register map lives.

### 3.4 Clock & analog plan (sky130-friendly, small)

- **Clocks:** single 40 MHz core domain (25 MHz safe fallback) from an on-chip PLL fed by an external
  crystal — **or** skip the PLL entirely for v1 and divide an external clock (removes an analog block).
  One *slow* metering-sample clock domain if the external ADC streams on its own clock → document the
  **CDC** as a verification item (Ch 6/7).
- **Analog (keep to ≤ 3 custom blocks):** 1× **PLL** (optional), 1× **12-bit SAR ADC** for CP voltage /
  aux sense, 1–2× **comparator** (CP level detect, zero-cross). **LDO: use an external regulator** for
  v1. **Externalise the 16-bit metering ADC** (external ΔΣ modulator or ADC chip) — the SoC ingests the
  bitstream/samples and does the *digital* metrology; your flagship contribution is preserved with **zero
  custom high-res analog risk.** (On-chip ΔΣ is an explicit *future-work* stretch goal, not v1.)

### 3.5 Scope guardrails — what to explicitly DEFER / CUT

| Cut / defer | Why | Where it goes |
|---|---|---|
| On-die WiFi/RF | Never attempt RF on a first SoC | External pre-certified module (as pitch C already says) |
| 100 MHz clock | Back-end timing-closure trap on sky130 | Target 40 MHz; **report Fmax as a result** |
| 64 kB dual-bank SRAM | Area + complexity | 16 kB single bank (32 kB stretch) |
| On-chip 16-bit metering ADC | Custom high-res analog = highest analog risk | External ADC → on-chip digital metrology DSP |
| CAN as a from-scratch CREATE | Re-inventing a solved protocol | REUSE/port OpenCores Verilog CAN |
| OCPP 1.6J / ISO 15118 stacks | These are **firmware/host**, not silicon | Firmware on picorv32 / external host; out of RTL scope |
| Full descriptor DMA | Not needed at 40 MHz metering rates | CPU-copy; add 1-ch DMA only if measured to be a bottleneck |
| CAN-FD / TTCAN | Beyond v1 | Future work |
| **Tapeout** | Not required for the thesis | Stop at verified RTL + OpenLane sign-off + GLS |

### 3.6 Pure-Verilog corrections — FLAGGED cores and their replacements

The pitches (and several sketches) name **SystemVerilog** IP. Under the hard rule these **must be
replaced** before specification:

| ❌ Named in pitches (SystemVerilog) | Appears in | ✅ Pure-Verilog replacement |
|---|---|---|
| **Ibex** (lowRISC, SV) | A, B, D, F, H, I, J | **picorv32** (native Verilog; `picorv32_axi` AXI4-Lite wrapper). *SERV* (bit-serial, pure Verilog) if extreme area is wanted |
| **cv32e40p** (OpenHW, SV) | **C**, E, G | **picorv32** (RV32IM). Do **not** carry cv32e40p into the spec |
| **pulp-axi** (SV) | A, B, C, D, H, J | alexforencich **verilog-axi** (AXI4-Lite) + ZipCPU **wb2axip** AHB/APB bridges (all pure Verilog; wb2axip is *formally verified* → free thesis credibility) |
| CAN "CREATE" | C | OpenCores Verilog CAN (REUSE) — verify licence for any commercial path |
| OpenRAM macro | all | ✅ *Not* an SV issue — it is a compiled hard macro + behavioural Verilog sim model. Keep |
| `EF_*` peripherals (UART/SPI/I2C/GPIO/TMR/PWM) | all | ✅ Efabless Verilog (Apache-2.0) — keep as REUSE |

**Verification-flow note (matches your existing toolchain):** drive the DUT with **cocotb / pyuvm over
Verilator**. Verilator handles Verilog-2001/2005 cleanly, and this reuses the PyUVM+Verilator flow you
already run (tabbypy3 3.11 venv; venv-bin-first PATH). A **coverage-driven** verification result on the
CAN + metering integration is a legitimate thesis pillar and slots straight into Ch 6.

---

## 4. #1 Pick — Industry-Demand Relevance Lens (Candidate C)

**Why an EVSE controller SoC matters to the industry NOW:**

- **National semiconductor policy is the tailwind.** NIMP 2030 and the National Semiconductor Strategy
  explicitly push Malaysia *up the value chain* from assembly/test/packaging (ATP) into **IC design**. A
  locally-designed controller for a **policy-mandated domestic market** (EV charging) is precisely the
  "Malaysia designs silicon" flagship the policy asks for — a fundable, quotable thesis-to-industry story
  (MIDA/MITI, the Penang/Kulim/Selangor design ecosystem).
- **Energy transition + automotive convergence.** The Low Carbon Mobility Blueprint (10,000 charge
  points), NETR (net-zero 2050, 45% GHG-intensity cut by 2030), and 40–70%/yr xEV growth keep the
  build-out funded and *behind schedule* — demand persists across the entire 3–5-year window. CAN is the
  automotive/industrial backbone, so the IP is dual-use from day one.
- **Customers & channels (a real B2B chain, not consumer hope):** MY charger OEMs / wallbox makers
  (white-label the controller module), CPOs (Gentari, JomCharge, ChargEV/TNB), and retrofit installers
  undercutting the RM150–300 imported OCPP module. Later: **license the metering + CAN IP.**
- **3–5-year trajectory:** the charging gap compounds each year it is missed; localisation pressure
  (supply-chain resilience, NIMP) rises; the metering/CAN IP appreciates as EV + grid + industrial demand
  converge. This is a market that *grows into* the IP rather than one you must fight to enter.
- **Adjacent markets the IP extends into (the moat multiplier):** **smart meters** (TNB AMI), **solar
  inverters** (literally candidate E — same metering DSP), **industrial submetering**, **motor drives**,
  and **BMS** (CAN + sensing). One thesis, one open-IP core, five downstream markets — the strongest
  "IP portability" story of any candidate, and a natural multi-paper / future-work pipeline.

---

## 5. Final Recommendation + 3 Must-Do Changes

### Recommendation

**Build Candidate C — EVCore-MY, scoped down as in §3.** It is the batch's best *first-SoC thesis
vehicle*: the only rich-depth design with **no RF PHY** (the batch's dominant execution risk),
the deepest examinable surface (mixed-signal metrology + a CAN protocol FSM + a small IEC 61851 safety
FSM + a genuine 3-tier-AMBA trade-off study), the strongest **industry-demand-NOW** narrative (EV +
energy transition + NIMP 2030, with the widest reusable-IP footprint of any candidate), and a real B2B
channel that sidesteps the < RM150 consumer-margin trap. Keep **Candidate E (SolarSync)** as the
deliberately de-risked sibling — it *shares the metering DSP*, so it is your safety net and your obvious
follow-on. Reach for **Candidate J (BusSafe)** only if you specifically want a safety/impact thesis and
accept two-die + radio-externalisation scope.

### The perfected #1 pitch, in one paragraph

*EVCore-MY is an open-source, sky130-fabricable EV-charger controller SoC — the first pure-Verilog
integration of a digital energy-metrology datapath, a CAN 2.0B protocol engine, and an IEC 61851
control-pilot interface on a real 3-tier AMBA fabric (AXI4-Lite / AHB / APB) built around a picorv32
core at 40 MHz with 16 kB of OpenRAM SRAM. It ingests metering samples from an external ADC and computes
RMS, active/reactive power, and energy on-chip; it speaks CAN to the charger and CP to the vehicle; WiFi
and the OCPP 1.6J stack live off-die in firmware/module. Delivered as verified RTL closed with a
coverage-driven PyUVM/Verilator methodology and hardened through OpenLane for area/timing/power analysis
(no tapeout), it is a completable first SoC that doubles as Malaysia's flagship NIMP-2030 answer to an
imported RM150–300 controller — with metering + CAN IP that extends straight into smart meters, solar
inverters (EVCore's sibling SolarSync), and industrial control.*

### 3 must-do changes before writing the specification

1. **Excise every SystemVerilog core and lock a 100%-pure-Verilog IP BOM.** Replace **cv32e40p → picorv32**
   (AXI4-Lite wrapper), **pulp-axi → alexforencich verilog-axi + ZipCPU wb2axip** AHB/APB bridges, and
   **reclassify CAN from CREATE to REUSE** (OpenCores Verilog CAN). Write "zero SV/VHDL in synthesizable
   RTL" into the spec as a gating design rule, and pin the exact repos/licences.

2. **Externalise the high-resolution analog and re-anchor the contribution on the *digital* metrology
   datapath.** Move the 16-bit metering ADC off-die (external ΔΣ/ADC), cut **100 MHz → 40 MHz**,
   **64 kB → 16 kB**, single CAN node, and push OCPP/ISO-15118/WiFi to firmware/module. Name the
   **metering DSP** the flagship CREATE; CP engine + CAN port are the small secondary blocks. This is what
   turns C from "over-scoped as pitched" into "completable first SoC" without losing its novelty.

3. **Redefine the deliverable as verified RTL + OpenLane sign-off analysis (explicitly no tapeout), with
   coverage-driven PyUVM/Verilator verification named as a first-class thesis pillar.** Add the three
   depth chapters — **metering-accuracy analysis** (golden-model + error budget), **bus-architecture
   trade-off** (quantified AHB-stream vs single-bus), and **formal verification of the CP/CAN FSMs** — and
   fold the §3.5 defer-list into the spec as hard scope guardrails so the thesis can't quietly balloon.

---

*Reviewer: claude-opus-4-8. Basis: independent read of pitches A–J, `candidates_scores.json`,
`market_validation.md`. Ranking diverges from the raw composite by design — reweighted for a first-time
SoC designer on a thesis timeline (see §0). No other files were modified.*
