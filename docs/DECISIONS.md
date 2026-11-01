# ARCHITECTURAL DECISIONS & ASSUMPTION LOG (ADR)
**Project 10: Road Accident Trend Analysis (MoRTH India)**

## ADR-001: Data Ingestion Fallback Hierarchy
- **Context**: In hackathon and disconnected execution environments, `data.gov.in` endpoints require active API keys or return HTML wrappers rather than machine-readable CSVs.
- **Decision**: Implemented an automated 3-tier strategy. Ingest checks for raw cached dumps in `data/raw/`; when unavailable, it transitions cleanly to Tier 2 validated data reconstructed from official parliamentary replies without error or halt.
- **Impact**: 100% reproducible execution and offline resilience.

---

## ADR-002: Reconciling 2025 Provisional National Totals
- **Context**: An aggregator report published 5,13,474 accidents and 1,83,434 deaths, whereas the MoRTH reply in Lok Sabha stated 5,13,563 accidents and 1,83,382 deaths.
- **Decision**: Use the Lok Sabha reply figures (5,13,563 and 183,382). Document the discrepancy explicitly in `docs/DATA_CLEANING.md` and display a footnote on dashboard KPI cards.
- **Impact**: Upholds the highest standard of regulatory provenance.

---

## ADR-003: Non-Imputation of 2025 Injuries and Regional Granularity
- **Context**: Several dashboards attempt to interpolate missing indicators (like 2025 injured individuals or state-wide matrices) using linear regression or regional scaling.
- **Decision**: Strictly prohibit synthetic numbers. Missing 2025 injury total is rendered as `Pending Official Table` with explanatory notes. State-level analyses focus exclusively on verified reporting states.
- **Impact**: Eliminates statistical distortion and prevents misleading policy recommendations.

---

## ADR-004: Decoupling 2026 Severity Window from 2021–2025 Annual Totals
- **Context**: MoRTH released a partial state severity benchmark covering 1 Jan – 27 Jul 2026.
- **Decision**: Maintain `state_severity_2026` as a separate, distinct table with clear labelling. It is never merged or averaged with 2021–2025 full-calendar-year figures.
- **Impact**: Protects against temporal mismatch errors.

---

## ADR-005: Innovation Features Selection
- **Context**: Evaluation rubric mandates at least 2 differentiating features.
- **Decision**: 
  1. **Policy What-If Intervention Simulator**: Quantifies how targeted enforcement of over-speeding and helmet/seatbelt compliance could reduce annual fatalities and save lives.
  2. **Audit & Data Quality Inspector**: A dedicated interactive data contract verification view that inspects provenance, missing fields, derivation math, and validation flags live.
- **Impact**: Provides high utility for policymakers, analysts, and auditing authorities.
