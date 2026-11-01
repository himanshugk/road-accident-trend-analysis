import pytest
import pandas as pd
import numpy as np
from src.ingest import get_tier2_seed_data
from src.clean import clean_all
from src.derive import add_derived_columns, derive_national_metrics
from src.validate import validate_datasets

def test_pipeline_data_integrity():
    raw = get_tier2_seed_data()
    cleaned = clean_all(raw)
    derived = add_derived_columns(cleaned)
    is_valid, errors = validate_datasets(derived)
    assert is_valid, f"Validation failed: {errors}"

def test_2025_benchmark_rates():
    raw = get_tier2_seed_data()
    cleaned = clean_all(raw)
    derived = add_derived_columns(cleaned)
    metrics = derive_national_metrics(derived["national_series"])
    
    # 1,407 accidents/day, 502 deaths/day, 59 accidents/hour, 21 deaths/hour
    assert metrics["accidents_per_day"] == 1407
    assert metrics["deaths_per_day"] == 502
    assert metrics["accidents_per_hour"] == 59
    assert metrics["deaths_per_hour"] == 21
    
    # 5-year growth: accidents +24.5%, deaths +19.1%
    assert metrics["accidents_5yr_growth_pct"] == 24.5
    assert metrics["fatalities_5yr_growth_pct"] == 19.1

def test_no_fabrication_rules():
    raw = get_tier2_seed_data()
    cleaned = clean_all(raw)
    df_nat = cleaned["national_series"]
    
    # 2025 injury total must be None / NaN
    row_2025 = df_nat[df_nat["year"] == 2025].iloc[0]
    assert pd.isna(row_2025["injuries"]), "2025 injuries should never be fabricated"
    
    # 2024 injury total must be 471,441
    row_2024 = df_nat[df_nat["year"] == 2024].iloc[0]
    assert row_2024["injuries"] == 471441

def test_state_severity_2026_omissions():
    raw = get_tier2_seed_data()
    cleaned = clean_all(raw)
    df_sev = cleaned["state_severity_2026"]
    
    kerala_val = df_sev[df_sev["state"] == "Kerala"]["severity_rate"].values[0]
    bihar_val = df_sev[df_sev["state"] == "Bihar"]["severity_rate"].values[0]
    up_val = df_sev[df_sev["state"] == "Uttar Pradesh"]["severity_rate"].values[0]
    
    assert pd.isna(kerala_val)
    assert pd.isna(bihar_val)
    assert up_val == 55.4
