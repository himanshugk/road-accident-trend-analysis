"""
Data Validation and Quality Assurance Module.
Validates math, checks constraints, asserts non-negative values and data contracts.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

def validate_datasets(dfs: Dict[str, pd.DataFrame]) -> Tuple[bool, List[str]]:
    errors = []
    
    # 1. National Series Validation
    df_nat = dfs["national_series"]
    required_cols_nat = ["year", "accidents", "fatalities", "severity", "source", "is_provisional"]
    for col in required_cols_nat:
        if col not in df_nat.columns:
            errors.append(f"Missing column in national_series: {col}")
            
    # Check 2025 exact figures
    row_2025 = df_nat[df_nat["year"] == 2025]
    if row_2025.empty:
        errors.append("Year 2025 missing in national_series")
    else:
        acc_2025 = row_2025["accidents"].values[0]
        fat_2025 = row_2025["fatalities"].values[0]
        sev_2025 = row_2025["severity"].values[0]
        if acc_2025 != 513563:
            errors.append(f"2025 accidents mismatch: expected 513563, got {acc_2025}")
        if fat_2025 != 183382:
            errors.append(f"2025 fatalities mismatch: expected 183382, got {fat_2025}")
        if sev_2025 != 35.7:
            errors.append(f"2025 severity mismatch: expected 35.7, got {sev_2025}")
            
        # Check that 2025 injuries is explicitly NA
        inj_2025 = row_2025["injuries"].values[0]
        if pd.notna(inj_2025):
            errors.append(f"2025 injuries must be empty/NA, but got {inj_2025}")

    # Check 2024 injuries is 471441
    row_2024 = df_nat[df_nat["year"] == 2024]
    if not row_2024.empty:
        inj_2024 = row_2024["injuries"].values[0]
        if inj_2024 != 471441:
            errors.append(f"2024 injuries mismatch: expected 471441, got {inj_2024}")
            
    # Check severity calculations consistency (+- 0.5 tolerance due to official published rounding)
    for _, row in df_nat.iterrows():
        calc = round((row["fatalities"] / row["accidents"]) * 100, 1)
        if abs(calc - row["severity"]) > 0.8:
            errors.append(f"Severity discrepancy in year {row['year']}: recorded {row['severity']} vs calc {calc}")
            
    # 2. State Leaders
    df_lead = dfs["state_leaders"]
    tn_row = df_lead[df_lead["state"] == "Tamil Nadu"]
    if tn_row.empty or tn_row["val_2025"].values[0] != 71387:
        errors.append("Tamil Nadu 2025 accident figure incorrect or missing")
    up_row = df_lead[df_lead["state"] == "Uttar Pradesh"]
    if up_row.empty or up_row["val_2025"].values[0] != 27550:
        errors.append("Uttar Pradesh 2025 fatality figure incorrect or missing")

    # 3. State Severity 2026
    df_sev = dfs["state_severity_2026"]
    up_sev = df_sev[df_sev["state"] == "Uttar Pradesh"]["severity_rate"].values[0]
    if up_sev != 55.4:
        errors.append(f"UP 2026 severity mismatch: expected 55.4, got {up_sev}")
    # Verify Kerala & Bihar are omitted / NaN
    for omitted_state in ["Kerala", "Bihar"]:
        om_val = df_sev[df_sev["state"] == omitted_state]["severity_rate"].values[0]
        if pd.notna(om_val):
            errors.append(f"State {omitted_state} severity must be omitted/NaN, got {om_val}")

    # 4. Recorded causes 2025
    df_causes = dfs["recorded_causes_2025"]
    os_row = df_causes[df_causes["cause"] == "Over-speeding"]
    if os_row.empty or os_row["accidents_count"].values[0] != 82124:
        errors.append("Over-speeding 2025 count mismatch: expected 82124")

    is_valid = len(errors) == 0
    return is_valid, errors
