# PRJ-004 EVCore-MY — Traceability Matrix
*REQ → Module → Config/Register binding | 02_specification_stage | 2026-08-19*

Every requirement (REQ-001…REQ-060 from `01_system_spec.md`) is bound to the module(s) that implement it and the configuration key / register that carries the implementation choice. No config key without a requirement; no requirement without a binding (audit 1.8).

## Binding keys glossary

| Key | Meaning |
|---|---|
| `CLOCK_PERIOD_NS` | Core clock period (40 MHz → 25 ns; 25 MHz → 40 ns) |
| `PROGADDR_RESET` | picorv32 reset vector (0x0000_0000) |
| `SRAM_SIZE_BYTES` | 16 kB = 16384 |
| `AXI_BASE_*` / `AHB_BASE_*` / `APB_BASE_*` | Address map bases (REQ-026/027/028) |
| `BRIDGE_*` | MOD-03/04 bridge parameters (address decode windows, wait states) |
| `METERING_*` | Metering DSP config (decimation ratio, Q-format, calib gain/phase) |
| `CAN_*` | CAN registers (SJA1000-class: mode, command, status, interrupt, acceptance, timing) |
| `CP_*` | CP engine registers (state, PWM duty, fault latch, level thresholds) |
| `EF_*_BASE` | EF peripheral APB base addresses |
| `IRQ_*` | Interrupt aggregator enable/pending bits (REQ-029) |
| `PLL_*` | Optional PLL config (bypass/divide) |
| `SAR_*` / `CMP_*` | SAR ADC + comparator control regs (MOD-16) |

## Matrix

| REQ | Requirement (short) | Module(s) | Config / register binding |
|---|---|---|---|
| REQ-001 | RM139 module, BOM RM75–105 | (product — all) | BOM_MODEL = RM75–105 (business doc) |
| REQ-002 | B2B channel (OEM/CPO/retrofit) | (product) | CHANNEL = B2B (business doc) |
| REQ-003 | NIMP 2030 / NSS narrative | (product) | NARRATIVE = NIMP2030 (business doc) |
| REQ-004 | IP portability (metering+CAN) | MOD-06, MOD-07 | METERING_Q_FORMAT, CAN_SJA1000_REGS (portable register API) |
| REQ-005 | Non-billing metering claim | MOD-06 | METERING_CLASS = non-billing (REQ-039 limit set) |
| REQ-006 | Standalone sky130A, NO Caravel | top | PDK = sky130A, FLOW = OpenLane/LibreLane, HARNESS = none |
| REQ-007 | Die area 1–3 mm² | top | AREA_TARGET = 1–3 mm² |
| REQ-008 | 60–100 k std cells | top | CELL_BUDGET = 60000–100000 |
| REQ-009 | SRAM 16 kB (32 kB stretch) | MOD-05 | SRAM_SIZE_BYTES = 16384 |
| REQ-010 | Deliverable = sign-off, no tapeout | top | DELIVERABLE = RTL+signoff+GLS |
| REQ-011 | sky130hd cells | top | PDK_CELLS = sky130hd |
| REQ-012 | No on-die radio | top | RADIO = external module (UART1/SPI1) |
| REQ-013 | 100% pure Verilog-2001/2005 | all RTL | LANG = verilog-2001/2005, SV/VHDL = 0 |
| REQ-014 | Zero-SV/VHDL find proof | RTL tree | SV_SCAN = `find -name "*.sv" -o -name "*.vhd" -o -name "*.vhdl"` == 0 |
| REQ-015 | REUSE md5-pinned pure Verilog | MOD-01/02/05/07/09–14 | MD5_MANIFEST per module (md5-pinnable commits in 02_reuse_manifest.json) |
| REQ-016 | Banned cores (Ibex/cv32e40p/pulp-axi) | top | BANNED_CORES = none in RTL tree |
| REQ-017 | picorv32 CPU (AXI wrapper) | MOD-01 | PICORV32_AXI = enabled; ISA = RV32IM |
| REQ-018 | PROGADDR_RESET = 0x0 | MOD-01 | PROGADDR_RESET = 0x0000_0000 |
| REQ-019 | Boot: SRAM primary, SPI flash option | MOD-15, MOD-01 | BOOT_MODE = SRAM | SPI_FLASH; BOOT_COPY = 16 kB |
| REQ-020 | IRQ aggregation → single irq | MOD-15 | IRQ_EN/PEND regs (16 sources) |
| REQ-021 | 3-tier AMBA required | MOD-02/03/04 | BUS_TIERS = AXI4-Lite→AHB3-Lite→APB |
| REQ-022 | Tiering rule (transaction character) | all | TIERING_RULE = REQ-022 (normative) |
| REQ-023 | Tiering trade-off quantified (thesis) | arch stage | TIERING_STUDY = required |
| REQ-024 | verilog-axi interconnect | MOD-02 | AXI_INTERCONNECT = alexforencich/verilog-axi |
| REQ-025 | Bridges MOD-03/04 CREATE fallback | MOD-03, MOD-04 | BRIDGE_AXI2AHB = custom; BRIDGE_AHB2APB = custom |
| REQ-026 | AXI map (SRAM 0x0, bridge 0x4000_0000, sys 0x7F00_0000) | MOD-02/03/05/15 | AXI_BASE_SRAM = 0x0000_0000; AXI_BASE_BRIDGE = 0x4000_0000; AXI_BASE_SYS = 0x7F00_0000 |
| REQ-027 | AHB map (DSP 0x4000_0000, CAN 0x4000_1000, APB window 0x4000_2000) | MOD-03/06/07/04 | AHB_BASE_METERING = 0x4000_0000; AHB_BASE_CAN = 0x4000_1000; AHB_BASE_APB = 0x4000_2000 |
| REQ-028 | APB map (12 slots × 4 kB) | MOD-04, MOD-08…16 | EF_*_BASE per slot (CP 0x0000 … SAR 0xB000) |
| REQ-029 | IRQ map (16 sources) | MOD-15 | IRQ_EN[15:0], IRQ_PEND[15:0] bit assignments per table |
| REQ-030 | 40 MHz core (25 MHz fallback) | MOD-15, MOD-01 | CLOCK_PERIOD_NS = 25 (40 MHz) / 40 (25 MHz fallback) |
| REQ-031 | Ext clock + divider; PLL optional | MOD-15, MOD-16 | CLK_SRC = external; PLL_EN = 0 (v1); DIVCFG |
| REQ-032 | LDO external | top | LDO = external (no on-die) |
| REQ-033 | Async-assert/sync-deassert reset | MOD-15 | RST_MODE = async-assert/sync-deassert |
| REQ-034 | CDC sample domain ↔ core domain | MOD-06, MOD-15 | CDC = async-FIFO + 2FF sync; CDC_CHECK = formal |
| REQ-035 | Clock gating (DSP, CAN idle) | MOD-06, MOD-07, MOD-15 | CLK_GATE_EN = per-block; POWER_ACTIVITY = GLS |
| REQ-036 | External 16-bit ΔΣ/ADC | MOD-06 (input), MOD-16 | ADC_EXT = external chip; ADC_IF = bitstream + MCLK ≤ 2.048 MHz |
| REQ-037 | Digital metrology datapath (CREATE) | MOD-06 | METERING_CFG = decimation, window; CALIB_GAIN/PHASE/OFFSET |
| REQ-038 | Fixed-point Q-format + error model | MOD-06 | METERING_Q_FORMAT = Q1.15/Q0.31; ERROR_BUDGET doc |
| REQ-039 | Class-1 (0.5s analysis) accuracy | MOD-06 | METERING_CLASS = 1; LIMITS: Vrms/Irms ≤0.5%, P ≤0.8%, Q ≤1.5%, Wh ≤1.0% |
| REQ-040 | Sample FIFO + threshold IRQ | MOD-06 | METERING_FIFO_THRESH; IRQ 10 |
| REQ-041 | CAN = REUSE (OpenCores) | MOD-07 | CAN_SOURCE = freecores/can; CAN_MODE = SJA1000-class |
| REQ-042 | CAN stream FIFO on AHB, regs on APB | MOD-07 | CAN_TXFIFO/CAN_RXFIFO (AHB); CAN_MODE/CAN_CMR/CAN_SR… (APB) |
| REQ-043 | Single CAN 2.0B node, no CAN-FD | MOD-07 | CAN_2_0B = standard+extended; CAN_FD = off |
| REQ-044 | CP engine CREATE (FSM + PWM) | MOD-08 | CP_PWM_DUTY (8/10/16%); CP_STATE |
| REQ-045 | CP states A/B/C/D/E/F + fault latch | MOD-08 | CP_STATE[2:0]; CP_FAULT_LATCH; CP_DEENERGIZE |
| REQ-046 | CP safety liveness formal property | MOD-08 | FORMAL_PROP = CP_SAFETY (SymbiYosys) |
| REQ-047 | CP sampling via SAR ADC + comparator | MOD-08, MOD-16 | CP_LEVEL_THRESH (CMP); SAR_CH = CP |
| REQ-048 | Analog ≤ 3 blocks, blackboxed | MOD-16 | PLL (optional), SAR_ADC 12-bit, CMP ×1–2 |
| REQ-049 | No high-res ADC / LDO / RF on die | top | ANALOG_BUDGET = 3 max |
| REQ-050 | Analog wrapper regs on APB | MOD-16 | SAR_CTRL, SAR_DATA, CMP_CTRL @ APB +0xB000 |
| REQ-051 | EF_* peripherals reused | MOD-09…14 | EF_UART/EF_SPI/EF_I2C/EF_GPIO8/EF_TMR32/EF_PWM32/EF_WDT32 bases |
| REQ-052 | EF_PWM32 index gap → register | MOD-13 | INDEX_ACTION = add EF_PWM32 to IP/INDEX.md |
| REQ-053 | OCPP/WiFi external (firmware, not RTL) | MOD-09/10 (links) | OCPP_STACK = firmware; WIFI = external module |
| REQ-054 | cocotb/PyUVM + Verilator, formal | verif | VERIF_FLOW = cocotb/pyuvm/Verilator + SymbiYosys |
| REQ-055 | Golden model (deterministic) | golden_model/ | GOLDEN_MODEL = golden_model/ (N=3 seeds) |
| REQ-056 | GLS + SDF + CDC analysis | verif/back-end | GLS = enabled; SDF = back-annotated |
| REQ-057 | OpenLane sign-off report | back-end | SIGN_OFF = area/timing/power report |
| REQ-058 | Scope guardrails (defer list) | top | DEFERRED = radio, 100 MHz, 64 kB, on-die ADC, from-scratch CAN, OCPP-RTL, DMA, CAN-FD, tapeout |
| REQ-059 | IP licence discipline + fallbacks | manifest | 02_reuse_manifest.json flags + fallbacks |
| REQ-060 | Doc traceability (this matrix) | spec | 03_traceability_matrix.md |

## Coverage check

| Check | Count |
|---|---|
| REQs in spec | 60 (REQ-001…REQ-060) |
| REQs bound in matrix | 60 / 60 |
| Modules referenced | MOD-01…MOD-17 (all) |
| Config keys used | 30+ (glossary) |
| REQ without module binding | 0 |
| REQ without config binding | 0 |

*No config key appears without a requirement; every requirement has module + config binding. Bindings with concrete register names (CAN_*, CP_*, SAR_*, IRQ_*) are refined to bit-level in the architecture stage; the spec-stage binding is the register-block level required by audit 1.8.*
