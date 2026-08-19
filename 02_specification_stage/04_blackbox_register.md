# PRJ-004 EVCore-MY — Blackbox Register: sky130 Analog + SRAM Stubs
*02_specification_stage | 2026-08-19 | blackbox for synthesis, dummy behavioural models for simulation*

This register defines every non-digital-CREATE macro the SoC instantiates, with pin-exact interfaces. These blocks are **blackboxes for synthesis** (no RTL inside; the OpenLane flow treats them as hard macros / don't-touch) and have **dummy behavioural models for simulation** (pure Verilog-2001, `ifdef SIMULATION`-gated where required). Per REQ-048 the analog budget is ≤ 3 custom blocks (PLL optional, SAR ADC, comparators); LDO is external; the 16-bit metering ADC is external (REQ-036).

---

## 1. BB-01 — OpenRAM 16 kB SRAM (MOD-05)

| Field | Value |
|---|---|
| Type | Compiled macro (VLSIDA/OpenRAM, BSD-3-Clause), 8 × 2 kB 1-port instances |
| Bus attach | AXI4-Lite slave via a small AXI→SRAM wrapper (wrapper = project RTL) |
| Synthesis role | BLACKBOX (macro views: GDS/LEF/liberty); wrapper is synthesizable RTL |
| Simulation role | Behavioural Verilog model (OpenRAM-generated `sram_1rw1r_..._sky130.v`-class model), `$readmemh` for boot image |
| md5 pin | OpenRAM generator commit + generated model md5 recorded in RTL manifest |

### Pin-exact interface (per 2 kB instance; wrapper aggregates 8)

```verilog
module sram_1rw_2kB_sky130 (
  input  wire        clk0,
  input  wire        csb0,      // active-low chip select
  input  wire        web0,      // active-low write enable
  input  wire [10:0] addr0,     // 2 kB -> 11-bit word address (32-bit words)
  input  wire [3:0]  wmask0,    // byte write mask
  input  wire [31:0] din0,
  output wire [31:0] dout0
);
```

**Model notes (sim):** combinational-read behavioural model with setup/hold assertion; write with byte mask; contents initialised from `firmware.hex` via `$readmemh` under `` `ifdef SIMULATION``; power/DFT pins omitted from the sim model (macro has them for sign-off).

---

## 2. BB-02 — 12-bit SAR ADC (MOD-16) — REQUIRED

| Field | Value |
|---|---|
| Type | sky130 analog macro (12-bit successive-approximation) |
| Purpose | CP voltage sampling + aux sense (REQ-047/048) |
| Synthesis role | BLACKBOX (analog macro, don't-touch) |
| Simulation role | Dummy behavioural model: configurable conversion latency, deterministic code→voltage mapping, optional noise injection off by default |
| Clock | SAR_CLK = core clock / N (N configurable, SAR_CLKDIV) |

### Pin-exact interface

```verilog
module sar_adc_12b_sky130 (
  input  wire        clk,       // SAR conversion clock (divided core clock)
  input  wire        rst_n,
  input  wire        start,     // pulse: start conversion
  input  wire [2:0]  chsel,     // channel select (CP, aux0, aux1, ...)
  input  wire        vref_ok,   // external reference-good status (product-level)
  output wire        busy,      // high during conversion
  output wire        eoc,       // end-of-conversion pulse
  output wire [11:0] dout,      // 12-bit result (unsigned, 0..4095)
  // analog pins (blackbox only)
  inout  wire        vin_p,     // analog input (pad)
  inout  wire        vrefp      // external reference (pad)
);
```

**Model notes (sim):** dummy model converts `vin_p` stimulus (analog value driven via a testbench real→code ramp) to `dout = floor(vin/ref * 4096)` with `busy` high for `SAR_LATENCY` clocks (default 16). No real analog modelling; noise/INL/DNL errors are parameters (default 0) for the metering error-budget testbench.

---

## 3. BB-03 — Comparator ×1–2 (MOD-16) — REQUIRED

| Field | Value |
|---|---|
| Type | sky130 analog comparator (2 instances: CP level detect, zero-cross) |
| Purpose | CP level detection thresholds + line zero-cross (REQ-047/048) |
| Synthesis role | BLACKBOX |
| Simulation role | Dummy model: `out = (vp - vn) > vth ? 1 : 0` with programmable threshold + hysteresis (params), no propagation delay |

### Pin-exact interface

```verilog
module cmp_sky130 (
  input  wire        clk,       // sampling clock (core clock)
  input  wire        rst_n,
  input  wire [1:0]  sel,       // instance select (0 = CP level, 1 = zero-cross)
  input  wire [11:0] vth,       // threshold code (compared against SAR-consistent scale)
  output wire        out,       // comparator output (registered)
  // analog pins (blackbox only)
  inout  wire        vp,        // positive input (pad)
  inout  wire        vn         // negative input (pad / internal ref)
);
```

**Model notes (sim):** registered output to avoid combinational loops in gate-level sim; hysteresis parameter `CMP_HYST` (default 8 codes) to mimic real comparator behaviour; edges generate IRQ 13 (zero-cross) / feed CP state detect.

---

## 4. BB-04 — PLL (MOD-16) — OPTIONAL, may be omitted for v1

| Field | Value |
|---|---|
| Type | sky130 PLL (analog) — OPTIONAL per REQ-031 |
| v1 default | **Not instantiated.** External clock + on-chip divider (DIVCFG) reaches 40 MHz / 25 MHz |
| Synthesis role | BLACKBOX if instantiated |
| Simulation role | Dummy model: `clk_out = clk_ref * M / D` with lock delay; `locked` asserted after `PLL_LOCK_CYCLES` (param, default 100) |

### Pin-exact interface (if instantiated)

```verilog
module pll_sky130 (
  input  wire        clk_ref,   // reference clock (external crystal/osc)
  input  wire        rst_n,
  input  wire        pll_en,
  input  wire [3:0]  mdiv,      // multiply
  input  wire [3:0]  ddiv,      // divide
  output wire        clk_out,
  output wire        locked
);
```

**Model notes (sim):** v1 flow runs with PLL absent (clock mux selects external ÷ divider). If instantiated later, the dummy model generates `clk_out` and `locked` with no jitter (jitter = 0 param default); CDC verification uses the two-clock behavioural model.

---

## 5. External macro interface — 16-bit ΔΣ metering ADC (off-chip, REQ-036)

Not a blackbox on die, but its digital interface is pinned here so the metering DSP (MOD-06) has a stable ingestion contract:

```verilog
// External ADC interface (pins, off-chip)
// Option A (bitstream): MCLK out (<= 2.048 MHz), DAT in (1-bit PDM/ΔΣ stream)
// Option B (word): MCLK out, SCLK out, DAT in (16-bit words, LSB-first or MSB-first per part)
module adc_ext_if (
  input  wire        clk_core,   // 40 MHz core
  input  wire        rst_n,
  output wire        mclk,       // ADC master clock out (e.g. 1.024 MHz)
  input  wire        dat,        // ADC data in (bitstream or serial words)
  // to MOD-06
  output wire        sample_valid,
  output wire [15:0] sample_data
);
```

**Model notes (sim):** behavioural driver in testbench generates ideal ΔΣ-bitstream/word streams from the golden-model waveforms (golden_model/); the DSP compares its fixed-point output against golden double-precision references (REQ-039, REQ-055).

---

## 6. Blackbox usage rules

1. **Synthesis:** every BB-* is a hard macro / don't-touch cell in the OpenLane config (`set_dont_touch`, macro placement via `MACROS` in config.tcl). No synthesis inside blackboxes.
2. **Simulation:** dummy models are pure Verilog-2001, instantiated only when `` `ifdef SIMULATION `` (or via a sim-only top). No SV/VHDL (REQ-013/014).
3. **Pin-exactness:** the pin names/widths above are contractual — the architecture stage may not rename them without updating this register (traceability: REQ-048/050 → MOD-16 → BB-02/03/04).
4. **Fallbacks:**
   - SAR ADC macro unavailable → external SAR chip over SPI + comparator-only CP sampling (manifest MOD-16 fallback).
   - PLL omitted → external clock + divider (default v1).
   - OpenRAM macro unavailable for a flow → behavioural model only is NOT enough for sign-off; escalate (macro is required for area/timing; model is sim-only).
5. **DFT:** scan not applied to analog macros; SRAM has DFT pins (test mode) used at sign-off, excluded from sim models.

---

*Blackboxes: BB-01 SRAM 16 kB, BB-02 SAR ADC, BB-03 comparator ×2, BB-04 PLL (optional). External: LDO (REQ-032), 16-bit metering ADC (REQ-036), WiFi module (REQ-053).*
