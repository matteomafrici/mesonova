> **Source:** drive-2026-10-20, `Launch System Requirements Check List.xlsx` | **Author:** Ümran Demirci | **Date:** 2026-10-17 00:12:43 | *converted with openpyxl - generated, do not edit*

## Sheet: Requirements Matrix

| OPTION 1  |  AIR-LAUNCHED SOUNDING ROCKET / LAUNCH SYSTEMS |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| IDENTIFICATION | Category | Requirement  & Description | Target or Limit | Unit | Verification Method | Department | Status |
| MIS-001 | Mission | Design an air-launched sounding rocket for in-situ mesospheric measurements | Air launch; mesospheric in-situ measurements | Mandatory | Mission concept and design review | Systems | Not Started |
| MIS-002 | Mission | Carry a single- or multi-instrument scientific payload | One or more instruments | Mandatory | Payload manifest / architecture | Payload | Not Started |
| PER-001 | Performance | Scientific payload mass shall not exceed 250 kg | ≤ 250 | kg | Mass budget / instrument datasheets | Payload | Not Started |
| PER-002 | Performance | Rocket apogee shall be between 110 and 125 km | 110–125 | km | Trajectory simulation | Trajectory | Not Started |
| PER-003 | Performance | Rocket gross lift-off/release mass shall not exceed 1750 kg | ≤ 1750 | kg | Integrated mass budget | Propulsion & Mass | Not Started |
| SCI-001 | Science | Payload shall acquire useful data while crossing 70–100 km altitude | 70–100 | km | Measurement timeline + trajectory | Payload & Trajectory | Not Started |
| SCI-002 | Science | Total useful measurement time in 70–100 km region shall be quantified | Quantify; no minimum specified | s | Trajectory and instrument duty-cycle analysis | Payload & Trajectory | Not Started |
| SCI-003 | Science | Scientific payload mass and volume shall be derived from literature / existing instrument baselines | Literature-backed mass and volume | kg / m³ | Cited instrument comparison | Payload | Not Started |
| SCI-004 | Science | Allowable payload acceleration and thermal environment shall be derived from selected payload | Instrument-specific limits | g / °C | Manufacturer / scientific source review | Payload & Structures | Not Started |
| SCI-005 | Science | Vehicle shall provide at least 20% margin relative to maximum allowable payload acceleration | ≥ 20% acceleration margin | % | Load history vs defined margin convention | Structures & Trajectory | Not Started |
| AIR-001 | Aircraft | Design team shall select a fully compatible carrier aircraft | Selected and compatible | — | Aircraft interface / capacity trade-off | Aircraft & Operations | Not Started |
| AIR-002 | Aircraft | Effects of release conditions on performance and trajectory shall be investigated | Release altitude/speed/attitude sensitivity | — | Parametric trajectory cases | Aircraft & Trajectory | Not Started |
| REC-001 | Recovery | Scientific payload shall be reusable | Reusable payload | — | Recovery concept and reuse assessment | Recovery | Not Started |
| SAF-001 | Safety | Ground impact of payload shall satisfy casualty risk below 10^-4 | < 1E-4 | risk | Risk assessment / landing footprint | Recovery & Safety | Not Started |
| ARC-001 | Architecture | Launch vehicle stages shall be expendable | Expendable stages | — | Configuration and staging review | Propulsion & Mass | Not Started |
| OPS-001 | Operations | Carrier aircraft, launch/recovery area, technologies and operating countries shall respect realistic technology-access and geopolitical constraints | Documented feasible choices | — | Operational feasibility assessment | Aircraft & Operations | Not Started |
| TEC-001 | Technology | Design shall rely primarily on high-TRL technologies with only minor developments | High TRL / minor development | TRL | Technology readiness matrix | Systems | Not Started |
| TEC-002 | Technology | Minor developments (AD2) shall be quantified | Quantify AD2 | — | Development assessment | Systems | Not Started |
| CST-001 | Cost | Project cost is not a design driver; no budget constraint is imposed | No imposed budget limit | — | Document as design assumption | Systems | Not Started |
| ANA-001 | Analysis | Perform preliminary configuration selection and baseline identification | Trade-off and baselines | — | Concept trade-off / cited baseline review | Systems | Not Started |
| ANA-002 | Analysis | Perform requirements analysis and functional analysis | Requirements + functional architecture | — | Matrices and functional diagram | Systems | Not Started |
| ANA-003 | Analysis | Perform mass sizing and staging analysis | Mass budget + staging trade-off | kg | Sizing model / stage architecture | Propulsion & Mass | Not Started |
| ANA-004 | Analysis | Perform aerodynamic and stability analyses | Drag + stability assessment | — | Aerodynamic model / CG-CP assessment | Aerodynamics | Not Started |
| ANA-005 | Analysis | Perform trajectory analysis | Trajectory simulation | — | Time histories + apogee | Trajectory | Not Started |
| ANA-006 | Analysis | Perform structural assessment | Preliminary loads and sizing | — | Structural calculations | Structures | Not Started |
| ANA-007 | Analysis | Perform recovery analysis | Recovery design | — | Descent / landing assessment | Recovery | Not Started |
| ANA-008 | Analysis | Perform uncertainty analysis | Sensitivity / uncertainty assessment | — | Parameter variation results | Reliability | Not Started |

## Sheet: Team Dashboard

| REQUIREMENTS  |  TEAM DASHBOARD |  |
|---|---|
| Metric | Value |
| Total requirements | 27 |
| Verified | 0 |
| In progress | 0 |
| Blocked | 0 |
| Completion rate | 0 |
| HOW TO USE |  |
| 1. Assign each requirement to one team member by editing Suggested Owner. |  |
| 2. Update Status as the team progresses; dashboard values update automatically. |  |
| 3. Add source URLs, evidence and verification results to your own project documentation. |  |
| 4. Values labelled Direct are taken from the provided Option 1 assignment. |  |
| 5. Verification methods and suggested owners are team planning proposals, not professor-prescribed. |  |
| 6. The assignment does not set a minimum measurement time or a fixed number of stages. |  |
| SOURCE: Launch Systems 2026–27 Project Assignment, Option 1, page 1. |  |

## Sheet: Assumptions & Decisions

| DESIGN ASSUMPTIONS & OPEN DECISIONS |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| ID | Topic | Decision / Question | Current Assumption | Evidence / Reference | Owner | Status |
| D-01 | Science | Which mesospheric phenomenon and instruments? |  |  | Payload | Open |
| D-02 | Aircraft | Which carrier aircraft and release conditions? |  |  | Aircraft | Open |
| D-03 | Configuration | Single-stage or multi-stage? |  |  | Propulsion | Open |
| D-04 | Propulsion | Which available high-TRL motor? |  |  | Propulsion | Open |
| D-05 | Recovery | How is scientific payload recovered and reused? |  |  | Recovery | Open |
| D-06 | Operations | Where can aircraft release and payload recovery be conducted? |  |  | Operations | Open |
| D-07 | Measurement | What is useful measurement time based on instrument operation? |  |  | Payload | Open |
| D-08 | Margin | How will 20% acceleration margin be defined and verified? |  |  | Structures | Open |
