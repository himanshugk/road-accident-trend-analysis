# Project 10 — Road Accident Trend Analysis (MoRTH India)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io/)
[![Validation](https://img.shields.io/badge/Data%20Validation-100%25%20Passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

A comprehensive, production-grade, explainable analytical dashboard and data pipeline analyzing road accident frequency, fatalities, severity, and contributing causes across Indian states and national trends (2021–2025+).

Built for the **Government of India Hackathon Submission (Project 10)**.

---

## 🎯 Executive Summary & Mission

Road accidents in India constitute a major public safety and public health crisis. In 2025 alone, India recorded **513,563 road accidents** resulting in **183,382 deaths** — translating to **1,407 accidents and 502 fatalities every single day**, or **59 accidents and 21 deaths every hour**.

This project provides an auditable, end-to-end data engineering and visual analytics platform:
1. **Explainable Data Pipeline**: Ingests, normalizes, derives, and validates road safety indicators with 100% provenance tracking.
2. **Interactive Streamlit Dashboard**: Offers executive KPI cards, 5-year trend trajectory, state-level severity benchmarks, root cause breakdown, policy what-if simulator, and live data quality inspection.
3. **Strict Data Ethics**: Enforces absolute non-fabrication; missing indicators (such as 2025 injuries) are prominently acknowledged rather than synthesized.

---

## 🏗️ Repository Architecture

```
project10_road_accidents/
├── .streamlit/
│   └── config.toml             # Streamlit theme and layout configuration
├── data/
│   ├── raw/                    # Raw downloads and immutable feeds
│   ├── cleaned/                # Production CSVs consumed by the app
│   │   ├── national_series.csv
│   │   ├── state_leaders.csv
│   │   ├── state_severity_2026.csv
│   │   └── recorded_causes_2025.csv
│   └── metadata/               # Data catalogs and source schemas
├── docs/
│   ├── DATA_SOURCES.md         # Source audit log and verification links
│   ├── DATA_CLEANING.md        # Conflict resolution and arithmetic proofs
│   └── DECISIONS.md            # Architectural Decision Records (ADR)
├── notebooks/
│   └── 01_eda_and_cleaning.ipynb # Jupyter notebook with end-to-end proofs
├── pages/
│   ├── 1_📈_National_Trends.py # 2021-2025 National trajectory & severity
│   ├── 2_🗺️_State_Analysis.py  # Known leaders & 2026 severity ranking
│   ├── 3_⚠️_Cause_Breakdown.py # Traffic violations & reporting deficit
│   ├── 4_🎯_Policy_Simulator.py# Differentiating Feature: Intervention What-If
│   └── 5_🔍_Data_Inspector.py  # Differentiating Feature: Live Data Contract Audit
├── src/
│   ├── ingest.py               # Tier 1 discovery + Tier 2 seed ingest
│   ├── clean.py                # Schema normalization and type casting
│   ├── derive.py               # Daily/hourly rates and CAGR math
│   ├── validate.py             # Rule checks and integrity assertions
│   ├── export.py               # CSV serialization
│   └── pipeline.py             # Master orchestrator (python -m src.pipeline)
├── tests/
│   └── test_pipeline.py        # Automated test suite
├── app.py                      # Streamlit application entry point
├── requirements.txt            # Pinned dependencies
└── README.md                   # This document
```

---

## ⚡ Quickstart

### 1. Installation
Clone the repository and install dependencies:
```bash
cd project10_road_accidents
pip install -r requirements.txt
```

### 2. Run Data Pipeline
Re-run the ingestion, cleaning, derivation, and validation suite:
```bash
python -m src.pipeline
```

### 3. Run Automated Tests
```bash
python -m pytest tests/
```

### 4. Launch Interactive Dashboard
```bash
streamlit run app.py
```

---

## 📊 Key Analytical Findings (2021–2025)

1. **5-Year Growth**: Between 2021 and 2025, road accidents surged by **+24.5%** (from 4.12 lakh to 5.14 lakh) and fatalities rose by **+19.1%** (from 1.54 lakh to 1.83 lakh).
2. **Accident Severity Paradox**: National severity (deaths per 100 accidents) has slightly declined from 37.3 in 2021 to 35.7 in 2025, but state-level disparities are severe (Uttar Pradesh recorded 55.4 in early 2026, while Madhya Pradesh stood at 23.2).
3. **State Concentration**:
   - **Tamil Nadu** leads in accident frequency (71,387 accidents in 2025, ~13.9% of national total).
   - **Uttar Pradesh** records the highest fatalities (27,550 deaths in 2025, 15.0% of national total, up +14.2% YoY).
4. **Enforcement Deficit**: Over-speeding accounts for **82,124** recorded violations (15.99% of accidents), yet over **83%** of accident reports lack specific violation coding.

---

## 🌟 Differentiating Innovations

1. **Policy What-If Intervention Simulator** (`pages/4_🎯_Policy_Simulator.py`):
   Allows transport planners and police commissioners to model expected life savings under targeted speed enforcement, helmet/seatbelt crackdowns, and emergency response time improvements.
2. **Live Data Contract & Quality Inspector** (`pages/5_🔍_Data_Inspector.py`):
   Provides complete data transparency, mathematical checks, schema provenance, and allows auditors to download cleaned CSVs and inspect missing field policies directly from the browser.
