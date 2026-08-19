# EVCore-MY — Safety Architecture (Control-Pilot, Metering, Product Framing)
## PRJ-004 / v0 / 03_architecture_stage / 05_safety_architecture.md

*Version 1.0 | 2026-08-19 | Architecture stage — derived from `01_ARCHITECTURE.md` (§5 clock/reset,
§7 IRQ map, §8.8 MOD-08 CP engine, §8.14 MOD-14 WDT, §9 CP safety architecture, §13 A6
resolution), `02_specification_stage/01_system_spec.md` (REQ-005, REQ-033, REQ-044…REQ-047,
REQ-055), `02_memory_map.json` (IRQ map, MOD-08/MOD-14/MOD-15 slots), and
`04_blackbox_register.md` (BB-02/BB-03 sensing contracts).*

*Purpose: thesis-level safety architecture for the EVSE control-pilot (CP) path and the
metering datapath — the two functions whose failure modes reach outside the die. This document
is explicitly NOT a certification artefact (REQ-005: non-billing, non-certified product
framing; see §6). It defines the mechanisms, the failure analysis, the formal targets, and the
product-level framing that the thesis (Chapters 5 and 7) will build on.*

---

## 0. Safety scope and principles

Three layers of safety-relevant functionality exist in EVCore-MY:

1. **CP path (MOD-08 + MOD-16 + MOD-14 + MOD-15)** — the IEC 61851-1 control pilot is the
   only signal path that can instruct an EV to draw power. Its safety analysis is the core of
   this document (REQ-044…REQ-047, REQ-046 formal target).
2. **Metering path (MOD-06)** — energy statistics integrity: calibration control, tamper
   detection, and the error-budget discipline already specified in `01_ARCHITECTURE.md` §8.6
   and `04_architecture_model.md`. Non-billing (REQ-005), so the analysis is integrity- and
   tamper-focused, not legal-metrology-focused.
3. **Product/system framing (external)** — the silicon provides mechanisms; the *system*
   (external contactor/relay, RCD/GFCI, wiring, enclosure) provides the certified safety
   layers. §6 states the boundary.

**Guiding principles applied throughout:**

- **Never-energise-in-fault is a structural property, not a firmware promise.** The
  architecture makes the dangerous condition (charging duty while in state A/fault)
  *unrepresentable* in the duty-generation cone, so no firmware bug, register corruption, or
  FSM glitch can produce it without also violating a single always-block property that formal
  tools can prove (REQ-046).
- **Two independent safety nets:** (a) the CP FSM's own hardware fault latch (firmware-
  independent), and (b) the SoC watchdog (MOD-14) + PMU reset/brown-out (MOD-15) as the
  system-level recovery net. Neither depends on the other.
- **Fail-safe defaults:** reset state of every safety-relevant flop is the *safe* state
  (state A, PWM output disabled, fault latch clearable only by explicit firmware action);
  clock loss and power loss drive the CP output to the de-energized level by construction
  (§3.5).
- **Every claim is traced to a REQ or explicitly carried as an architecture decision.**
  No safety property is silently assumed (constraint 13 discipline applied to safety).

---

## 1. IEC 61851-1 control-pilot state machine — safety analysis

### 1.1 State definitions and duty map (REQ-044/045, A6 resolved)

States and the canonical duty map per `01_ARCHITECTURE.md` §8.8 (REQ-045 adopted over
REQ-044's inconsistent single-percentage figures — A6):

| State | Meaning (REQ-045) | CP voltage | PWM duty (architecture-canonical, A6) | Charging duty? |
|---|---|---|---|---|
| A | No vehicle connected | 12 V | **off** (duty don't-care, PWM disabled) | NO |
| B | Vehicle connected, not charging | 12 V | **≤ 5%** (idle) | NO |
| C | Charging, ventilation not required | 12 V | **16–96%** (current-encoding range) | YES |
| D | Charging with ventilation | 12 V | **~8%** (ventilation signalling) | YES* |
| E | Fault — no CP / shorted pilot | < 6 V / 0 V detect | **off** (de-energized) | NO |
| F | Fault — pilot line failure | 0 V | **off** (de-energized) | NO |

\* D is a charging state with a ventilation constraint; its ~8% duty is still a "charging
duty" in the safety-property sense (the vehicle may draw power), so the never-energise
property treats C and D as the energized set: **charging range = {16–96%} ∪ {~8%}**.

**Duty map decision (A6, carried from §13 of ARCHITECTURE.md):** B ≤5%, C 16–96%, D ~8%.
REQ-045 is canonical because it alone can represent C's current-encoding range; REQ-044's
"8% D / 10% C / 16% B" figures are superseded. RTL stage must implement the REQ-045 map;
firmware writes duty values, and the FSM's state-gated mux enforces the state↔duty pairing
hardware-wise.

### 1.2 State transition table (architecture-level; bit-level is RTL-stage)

| From | Event (sensed) | To | Action | Safety note |
|---|---|---|---|---|
| A | CP level rises to connected threshold (comparator + SAR ADC cross-check) | B | PWM on at idle duty (≤5%) | No power flow yet |
| B | Duty raised to charging range by firmware per vehicle request | C or D | PWM duty → 16–96% (C) or ~8% (D) | **Energization** — only legal from B, only via explicit firmware intent (state moves to C/D) |
| C | Ventilation requirement signalled (aux input / firmware) | D | Duty → ~8% | |
| D | Ventilation cleared | C | Duty → 16–96% | |
| any of A–D | CP level fault: no CP / 0 V / below threshold | E or F | **PWM off, `CP_FAULT_LATCH` set, IRQ 11** | Never-energise: transition target is a fault state, duty forced off |
| any of A–D | Watchdog timeout / brown-out / reset | A (reset default) | whole SoC resets; CP PWM output disabled by reset state | System-level net (§4) |
| E/F | Firmware explicit clear (`CP_FAULT_CLEAR` write + re-validation of CP line) | A | Latch cleared, state re-enters A | No automatic E/F→B/C/D path — ever. Re-energization requires a full A→B→C/D sequence |

**Deliberate absence:** there is NO transition from E/F directly to B/C/D. The only exit from
a latched fault is clear-and-revalidate through A. This single design rule eliminates the
classic "fault glitch re-energizes" class of failures at the state-machine level.

### 1.3 Fault sources and sensing (REQ-047)

| Fault | Primary sensor | Secondary cross-check | Latency target (architecture) |
|---|---|---|---|
| CP line open / no CP (state E) | Comparator 0 (CP level detect, BB-03) | SAR ADC CP channel (BB-02) | ≤ 1 line-cycle of CP sampling (~20 ms @ 50 Hz; comparator is continuous) |
| CP short / 0 V (state F) | Comparator 0 + SAR ADC | — | same |
| Threshold drift / sensing disagreement | SAR ADC vs comparator disagree > margin | firmware arbitration via IRQ 12/13 | detected within one control-loop tick (IRQ-driven, §7) |
| PWM duty corruption (register glitch) | **structural** — duty mux gated by state register (§1.4) | firmware reads back duty | n/a — prevented by construction |
| FSM corruption (unreachable state) | **structural** — one-hot/encoded state with safe default | firmware state readback | n/a — unreachable encodings decode to A (safe) |

**Sampling architecture note:** the comparator is continuous (registered output, BB-03
contract) and drives the CP FSM directly — the *hardware* fault path does not wait for
firmware or for the SAR ADC. The SAR ADC provides the *independent* amplitude cross-check for
threshold validation and tamper/aging detection (BB-02 contract, MOD-16 channel select). This
is deliberate redundancy: comparator = fast, coarse, hardware; SAR ADC = slow, precise,
firmware-visible.

### 1.4 Never-energise-in-fault — structural guarantee (REQ-046, formal target)

The safety property: **`state ∈ {A, E, F} → duty ∉ charging range ({16–96%} ∪ {~8%})`**.

Architecture makes this checkable-by-construction (`01_ARCHITECTURE.md` §9):

- The PWM duty-generation datapath is **gated by the registered FSM state** — the duty value
  emitted on the CP PWM pin is selected by a mux whose select is the state register itself,
  not by a separately-computed enable bit that firmware could set independently.
- Therefore the pair `(state, duty)` is structurally coupled: to violate the property, a
  failure must corrupt the state register AND the duty mux in a coordinated way — a
  single-cone property for formal tools: `always (state==A || state==E || state==F) → duty_not_charging`.
- **Formal target (RTL stage, SymbiYosys BMC + induction):** prove the property over the full
  FSM, including the reset state (reset defaults: state=A, duty=off), the fault-latch path,
  and all unreachable-state decodings (unreachable codes decode to A). REQ-046 names this as
  thesis Chapter 5; the cone is deliberately small (§9 of ARCHITECTURE.md).
- **Never-energise is also the reset contract:** on ANY reset source (§4.3), the CP output
  pin is driven to the de-energized level by the reset value of the duty flop and the pad
  configuration (CP PWM pad has a defined pull/level in reset, §3.5). No clock is required to
  hold the de-energized state — the output is reset-controlled, not FSM-controlled, during
  reset.

### 1.5 Failure modes and effects (FMEA-lite, CP path)

| Failure | Effect | Detection | Net | Severity |
|---|---|---|---|---|
| FSM stuck in C with duty 16–96% after vehicle disconnect | pilot continues to signal charging to a disconnected cable | CP level drops to A-level → comparator fault path → E/F + latch | HW fault path (firmware-independent) | High — but bounded: disconnect always changes CP level, which the comparator senses continuously |
| Firmware hang mid-charging (duty left at 96%) | no state change, charging continues | MOD-14 WDT not fed → timeout → reset → state A, duty off | WDT (independent of CP FSM) | Medium (system recovers to safe state; charging session lost) |
| Comparator 0 stuck (fails to detect fault) | fault not latched via fast path | SAR ADC cross-check disagrees with comparator over N consecutive samples → firmware declares fault | redundant sensor | Medium (redundancy covers it) |
| Duty register single-bit upset in state C | duty changes within C's legal range (e.g. 40%→90%) | firmware duty readback + bounds check; WDT coverage | firmware + WDT | Low (still within charging range; over-current protection is external contactor/RCD) |
| Duty register upset targeting charging range from state A | **blocked by construction** | n/a — property holds structurally | structural (§1.4) | Eliminated by design |
| XOSC fails / clock loss | PWM stops; CP signal disappears | PMU brown-out/clock-fail detect → reset (IRQ 14) | MOD-15 + reset net | Low (fails safe: no clock → no PWM → de-energized) |
| `rst_n_core` release metastability | undefined FSM start | prevented: 2FF async-assert/sync-deassert synchronizer (REQ-033, §5.2 of ARCHITECTURE.md) | MOD-15 | Eliminated by design |

Severity is rated relative to the *system* context: the SoC never carries load current itself
— the external relay/contactor + RCD/GFCI are the certified protection layers (§6). The
silicon's job is to not *command* energization unsafely, which the structural property
guarantees.

---

## 2. Watchdog coupling (MOD-14 + MOD-15 + MOD-08)

### 2.1 Two-net architecture (deliberate, not layered)

| Net | Owner | Covers | Action on trip |
|---|---|---|---|
| **Net 1 — CP fault latch (hardware, firmware-independent)** | MOD-08 FSM + comparator path | CP line faults, state/latch corruption | PWM off + fault latch + IRQ 11 *without* CPU involvement |
| **Net 2 — SoC watchdog** | MOD-14 WDT32 + MOD-15 | firmware hang, CPU lock-up, register corruption | WDT timeout → (IRQ 8) → SoC reset → all flops to defined safe state (state A, duty off) |

Net 1 does not depend on the CPU, the bus, or firmware — it is the comparator→FSM→PWM pin
path, a pure hardware loop with a registered latch. Net 2 does not depend on the CP FSM — it
is the firmware-feeding-WDT loop with a hardware reset sink. The two nets share only the reset
distribution tree (MOD-15), whose correctness is guaranteed by the reset synchronizer design
(REQ-033).

### 2.2 WDT configuration and coupling rules (architecture-level)

- **Feed contract:** firmware must feed MOD-14 (`WDT_FEED` at APB `0x9000`, §10 of
  ARCHITECTURE.md) within the configured window. Window is configurable (EF_WDT32 native);
  architecture sets the *default* window to ≥ 4× the worst-case control-loop period so a busy
  but healthy loop never trips, and ≤ the CP-state-hold time that would be unsafe if
  firmware died mid-transition (RTL stage computes exact values from the loop budget).
- **WDT timeout action:** timeout asserts the SoC reset net (async-assert, sync-deassert
  through MOD-15) AND raises IRQ 8 before reset so firmware can log the cause (reset cause
  register in MOD-15 PMU block, `BOOT_STATUS`-adjacent).
- **Boot-time WDT:** enabled by firmware immediately after boot-copy release (before the
  first CP energization is possible); the reset default of the WDT enable is *on-with-long-
  window* so a bricked boot still resets into the safe state.
- **CP-state/WDT coupling rule:** the CP FSM is *not* allowed to enter state C or D while the
  WDT is disabled or in its reset default state — the enable bit for charging-duty
  generation is ANDed with WDT-arm status (a small hardware gate in MOD-08, part of the
  state-gated cone so it stays formal-checkable). This closes the "WDT disabled + firmware
  glitch energizes" hole.

### 2.3 PMU brown-out (MOD-15) as the third net

`PGOOD` from the external LDO (REQ-032) is monitored by MOD-15; brown-out/undervoltage asserts
the same reset net (async path, no clock needed) and raises IRQ 14. This covers the power-
supply failure class that neither Net 1 nor Net 2 can see. Reset cause register distinguishes
POR / WDT / brown-out / external for firmware and for the thesis safety writeup.

---

## 3. Metering tamper and calibration lock (MOD-06)

### 3.1 Calibration integrity (REQ-038/039/055; non-billing framing REQ-005)

- Calibration registers (`CALIB_GAIN` Q2.14, `CALIB_PHASE`/`CALIB_OFFSET` Q1.31, MOD-06 AHB
  in-band, `0x4000_0000`) are the only path that changes metering gain/phase/offset.
- **Calibration lock (architecture decision):** a `CALIB_LOCK` bit in the MOD-06 control
  register group. While set, calibration registers are read-only (writes ignored, error
  status set). Unlocking requires a two-step sequence: write `CALIB_LOCK=0` then re-write
  the calibration value in the same access window — a software-only gate, deliberately *not*
  a secret (no security claims in scope), sufficient against accidental/erroneous writes.
  RTL stage decides exact lock semantics (sticky-until-reset recommended).
- **Production-calibration flow (architecture-level):** calibration happens at module
  production against a reference meter; the golden model provides the reference-comparison
  methodology (`04_architecture_model.md` §6); the lock is set after calibration trim. No
  on-die non-volatile storage exists (no flash on die; NVM would be an added analog block —
  out of the ≤3 budget, REQ-048), so calibration constants live in the external SPI NOR
  flash image and are loaded by firmware at boot before the lock is set. A tampered flash
  image is a firmware/product issue, not an RTL one — flagged, not solved here.
- **Error-budget separation:** the primary 64-scenario golden comparison runs with
  calibration at unity (`04_architecture_model.md` §6 step 6) so DSP accuracy and calibration
  residual are measured separately; calibration residual is budgeted ≤0.01%
  (`01_ARCHITECTURE.md` §8.6 table). Tamper analysis must not blur that separation.

### 3.2 Tamper detection (statistics integrity; thesis-level)

Because metering is non-billing (REQ-005), "tamper" here means *defeating the charging
statistics* (e.g., charging while bypassing the meter, or manipulating accumulated Wh). The
architecture provides detection hooks, not enforcement:

| Indicator | Sensor/datapath | Detection | Output |
|---|---|---|---|
| Current without CP state C/D | MOD-06 Irms > threshold while CP state ∉ {C, D} | firmware comparison (reads both registers) | `TAMPER_EVENT` log + CAN/OCPP telemetry flag |
| Wh discontinuity (reset/rollover anomalies) | `WH_ACCUM_REG` + reset cause (MOD-15) | firmware watches reset cause + counter monotonicity | log + flag |
| Calibration register write while locked | MOD-06 lock logic | sticky error/status bit | log + flag |
| CP level/PWM mismatch (state C signalled, no PWM duty in range) | MOD-08 status vs MOD-06 P | firmware cross-check | log + flag |
| Sensing drift (aging): SAR ADC vs comparator disagreement over hours | MOD-16 both paths | firmware trend analysis on IRQ 12/13 deltas | maintenance flag (not tamper per se) |

All tamper outputs are **statistics-integrity flags**, not enforcement actions (no disconnect
authority in the silicon — the external contactor is product-level). REQ-005 keeps this
honest: the thesis claims tamper *detection* hooks, never billing-grade metering.

---

## 4. System-level safety nets and recovery

### 4.1 Reset sources → safe-state convergence

| Source | Async? | IRQ | Result |
|---|---|---|---|
| POR / external `ext_rst_n` | yes | — | full reset → state A, duty off |
| Brown-out (PGOOD loss, MOD-15) | yes | 14 | full reset |
| WDT timeout (MOD-14) | no (sync path) | 8 | full reset |
| Firmware soft reset (MOD-15 register) | no | — | full reset (or CP-only reset option, RTL-stage choice) |

Every source converges to the same reset distribution (§5.2 of ARCHITECTURE.md: async-assert/
sync-deassert 2FF), and every flop has a defined reset state (REQ-033) — the CP PWM output's
reset value is the de-energized level (§1.4). Recovery from any source therefore lands in
state A with the pilot de-energized; re-energization requires the full A→B→C/D sequence and
firmware re-validation of the CP line.

### 4.2 Fault escalation path (IRQ map, `02_memory_map.json`)

| IRQ | Source | Escalation |
|---|---|---|
| 11 | CP engine (state change, fault latch) | firmware: read `CP_FAULT_LATCH`, log, notify OCPP (UART1), hold state; do NOT clear until CP line validated |
| 13 | Comparator zero-cross/level edge | firmware: CP state re-evaluation, zero-cross for PF/phase calib hooks |
| 12 | SAR ADC conversion done | firmware: CP amplitude cross-check, aux sense |
| 8 | WDT timeout | firmware: log reset cause, clean reboot |
| 14 | PMU brown-out/status | firmware: log, safe shutdown |
| 9 | CAN bus error | firmware: bus-off recovery per SJA1000-class state |

The IRQ aggregation (MOD-15, IRQ_EN/IRQ_PEND, single line into picorv32 `irq[3]`) is
level-sensitive with write-1-to-clear (§7 of ARCHITECTURE.md) — a stuck source cannot be lost
while enabled, and the CP fault latch (IRQ 11) remains pending until firmware explicitly
handles it, so a missed interrupt cannot silently clear a fault.

### 4.3 CP pad behavior during reset/clock loss

- During reset: CP PWM output driven to de-energized level by the flop reset value; pad
  configured as output with defined level (not high-Z) so the pilot line is *actively* held
  safe, not floating.
- Clock loss (XOSC fail): PWM generator stops; output holds last driven level only until the
  PMU clock-fail/brown-out net asserts reset (async path, no clock needed) which forces the
  de-energized level. If the die loses both clocks and power, the external relay/RCD layer
  (§6) is the ultimate net. Architecture-level: the window between clock loss and reset
  assertion is bounded by the PMU clock-fail detect (RTL-stage: detect on 2 missing edges,
  assert reset); the pilot line is then de-energized. A held-high PWM in that window is
  bounded to ≤ a few ms and covered by the product-level contactor timing (not certification-
  relevant at thesis level, but documented).

---

## 5. Formal verification targets (carried to RTL stage, REQ-046/054/056)

| Property | Tool | Scope | Architecture-provided enabler |
|---|---|---|---|
| **P1 (never-energise):** `state ∈ {A,E,F} → duty ∉ {16–96% ∪ ~8%}` | SymbiYosys BMC + induction | MOD-08 full FSM + duty mux + reset | single-cone state-gated mux (§1.4) |
| **P2 (fault latch persistence):** `CP_FAULT_LATCH` set → cannot clear except explicit `CP_FAULT_CLEAR`; no E/F→B/C/D transition exists | SymbiYosys | MOD-08 FSM | transition table excludes E/F→B/C/D (§1.2) |
| **P3 (reset convergence):** every reset source → state A ∧ duty off within K cycles | SymbiYosys | MOD-08 + MOD-15 reset net | defined reset states (REQ-033) |
| **P4 (WDT-arm gating):** `state ∈ {C,D} → wdt_armed` (charging requires armed WDT) | SymbiYosys | MOD-08 + MOD-14 arm signal | hardware AND gate in the state-gated cone (§2.2) |
| P5 (CDC sanity, REQ-034/056): no metastability propagation at the ΔΣ ADC boundary | formal CDC (SymbiYosys/SLEC-class) | MOD-06 input path | 2FF + async FIFO structure (§5.3 of ARCHITECTURE.md) |

P1–P4 are the safety chapter (Chapter 5) evidence; P5 is the RTL→silicon chapter (Chapter 7)
item. All are scoped to single-cone or small-FSM size so the formal budget is thesis-
practical. No conditional verdicts: if any property fails at RTL stage, the fix is a design
change (re-gating), not a waiver — consistent with §G.8 of the workflow (no CONDITIONAL PASS).

---

## 6. B2B product safety framing (thesis-level, NOT certification)

The EVCore-MY safety architecture is **silicon mechanism + product framing**, explicitly not
a certification artefact:

| Layer | Owner | What it provides | Certification role |
|---|---|---|---|
| This SoC (RTL + analog) | thesis project | structural never-energise (P1–P4), fault latch, WDT nets, tamper hooks, defined reset states | input evidence for product safety case; NOT a certified safety element (no IEC 61508/ISO 26262 claims) |
| External contactor/relay + RCD/GFCI | product (OEM partner) | disconnects load on overcurrent/earth fault regardless of SoC state | certified protection layer (IEC 60364 / product standards) |
| CP interface conformance | product (OEM partner) | IEC 61851-1 electrical compliance of the pilot circuit (voltage levels, impedances, cabling) | product certification (e.g., CE/UKCA/SIRIM for EVSE) |
| WiFi/OCPP module | external pre-certified module (REQ-053) | communication; OCA conformance is product-phase | partner absorbs system-level certification (REQ-053) |
| Metering claims | none | REQ-005: non-billing framing; no legal-metrology claims anywhere in the project | explicitly excluded (no MID/STQC-type certification) |

**What the thesis claims (and what it does not):**
- CLAIMS: a structural safety property (P1) that is formally provable at RTL stage, a
  redundant fault-detection architecture (comparator fast path + SAR cross-check), a two-net
  watchdog design, and a documented failure-mode analysis of the CP path.
- DOES NOT CLAIM: compliance with any safety standard, certification-ready CP electronics,
  billing-grade metering, or any SIL/ASIL rating. Every document in this stage uses "safety"
  in the engineering-mechanism sense; §6 of this document is the explicit boundary statement
  that keeps the thesis honest (REQ-005).

**B2B angle:** the OEM/CPO buyers (REQ-002) receive a documented safety-mechanism package
(this document + formal proofs at RTL stage) that de-risks their own product certification —
the silicon provides the mechanisms, the partner provides the certified layers. That is the
commercial framing; no certification claim is implied by it.

---

## 7. REQ trace for this document

| REQ | Where satisfied |
|---|---|
| REQ-005 | §0, §3.2, §6 (non-billing framing throughout) |
| REQ-033 | §1.4, §4.1 (reset sync, defined reset states) |
| REQ-044 | §1.1 (CP engine states, 1 kHz PWM — duty map per A6) |
| REQ-045 | §1.1 (states A–F, duty ranges canonical) |
| REQ-046 | §1.4, §5 P1 (never-energise structural + formal target) |
| REQ-047 | §1.3 (SAR ADC + comparator CP sensing) |
| REQ-048/049 | §6 note, sensing-only analog (no high-res ADC claims) |
| REQ-054 | §5 (formal scope for SymbiYosys) |
| REQ-055 | §3.1 (calibration discipline vs golden model) |
| REQ-056 | §5 P5 (CDC formal carried) |
| REQ-020/029 | §4.2 (IRQ escalation path via aggregator) |
| REQ-051 (MOD-14 WDT) | §2 (watchdog nets) |

---

## 8. Open items carried to RTL stage

1. **Exact WDT window values** (default window vs control-loop budget, §2.2) — RTL stage computes from the firmware loop measurement.
2. **`CALIB_LOCK` semantics** (sticky-until-reset vs per-window) — RTL-stage choice, architecture fixes the locked/read-only behavior.
3. **PMU clock-fail detect threshold** (edges before reset assert, §4.3) — RTL-stage parameter; the async reset path itself is fixed.
4. **Formal proofs P1–P4** (SymbiYosys) — RTL-stage deliverables (REQ-054), architecture fixes only the cones.
5. **CP-only reset option** (MOD-15 soft reset scoping, §4.1) — RTL-stage decision; full reset remains the default.
6. **Tamper heuristics** (thresholds for Irms-without-C, drift analysis windows, §3.2) — firmware/product stage, hooks only in RTL.

---

*End of safety architecture. Scope: CP path safety (IEC 61851-1 states, never-energise
structural property P1, fault latch, two watchdog nets), metering calibration-lock + tamper
hooks (non-billing), reset convergence, formal targets P1–P5, and the thesis-level B2B product
safety framing with an explicit non-certification boundary. All REQ-044…REQ-047 and REQ-046's
formal target are satisfied at architecture level; proofs are RTL-stage deliverables.*
