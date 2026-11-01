# DATA SOURCES & PROVENANCE AUDIT LOG
**Project 10: Road Accident Trend Analysis (MoRTH India)**

## Strategy Overview
In compliance with the Data Strategy specification:
- **Tier 1 (Preferred)**: Attempt automated ingestion from `data.gov.in` and MoRTH public data feeds.
- **Tier 2 (Executed)**: Reconstruct analysis-ready dataset directly from validated published figures presented in the Ministry of Road Transport and Highways (MoRTH) reply to the Lok Sabha dated **30 July 2026** (provisional), cross-verified with Press Trust of India (PTI) and state reporting.
- **Tier 3**: Historical series verified against annual published MoRTH reports ("Road Accidents in India" 2021, 2022, 2023).

---

## Verified Data Ledger

| Dataset / Table | Time Period | Key Metrics Captured | Primary Source | Status / Provenance |
|---|---|---|---|---|
| `national_series.csv` | 2021–2025 | Accidents, Fatalities, Severity, Injuries (up to 2024), YoY growth | MoRTH Lok Sabha reply (30 Jul 2026) & MoRTH Annual Reports | 2021–2023 published final; 2024–2025 provisional |
| `state_leaders.csv` | 2024–2025 | Tamil Nadu accident frequency, Uttar Pradesh fatality volume, YoY growth & national shares | MoRTH Lok Sabha reply (30 Jul 2026) | Verified state leader counts |
| `state_severity_2026.csv` | 1 Jan – 27 Jul 2026 | Severity rate (killed per 100 accidents) for 9 reporting states + National Benchmark | MoRTH Lok Sabha reply (30 Jul 2026) | Specific 2026 reporting window (standalone) |
| `recorded_causes_2025.csv` | 2025 | Over-speeding, Lane indiscipline, Jumping red light, Mobile phone usage, Unspecified | MoRTH Lok Sabha reply (30 Jul 2026) | Minimum recorded violations |

---

## Access & Verification Details
- **Access / Ingestion Date**: 2026-11-01
- **Integrity Check**: 100% mathematical reconciliation against Lok Sabha published totals.
- **Strict Non-Fabrication Rule**: 
  - 2025 injury total is recorded as `null` / `blank` because it has not yet been tabled by MoRTH.
  - Sub-state breakdowns and unrecorded state-wise totals for 2025 are not synthesized; only verified figures are preserved.
