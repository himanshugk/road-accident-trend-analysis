"""
Derivations and Analytical Calculations Module.
Derives daily/hourly rates, 5-year CAGR, percentage shares, and back-solve arithmetic.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

def derive_national_metrics(df_national: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes key summary rates for 2025:
    - 1,407 accidents/day, 502 deaths/day, 59 accidents/hour, 21 deaths/hour
    - 5-year growth 2021 vs 2025: accidents +24.5%, deaths +19.1%
    """
    row_2025 = df_national[df_national["year"] == 2025].iloc[0]
    row_2021 = df_national[df_national["year"] == 2021].iloc[0]
    
    acc_2025 = row_2025["accidents"]
    fat_2025 = row_2025["fatalities"]
    
    acc_2021 = row_2021["accidents"]
    fat_2021 = row_2021["fatalities"]
    
    # Standard calendar year = 365 days, 8760 hours
    days = 365.0
    hours = 365.0 * 24.0
    
    accidents_per_day = round(acc_2025 / days)
    deaths_per_day = round(fat_2025 / days)
    accidents_per_hour = round(acc_2025 / hours)
    deaths_per_hour = round(fat_2025 / hours)
    
    accidents_5yr_growth_pct = round(((acc_2025 - acc_2021) / acc_2021) * 100, 1)
    fatalities_5yr_growth_pct = round(((fat_2025 - fat_2021) / fat_2021) * 100, 1)
    
    return {
        "accidents_2025": int(acc_2025),
        "fatalities_2025": int(fat_2025),
        "severity_2025": float(row_2025["severity"]),
        "accidents_per_day": int(accidents_per_day),
        "deaths_per_day": int(deaths_per_day),
        "accidents_per_hour": int(accidents_per_hour),
        "deaths_per_hour": int(deaths_per_hour),
        "accidents_5yr_growth_pct": float(accidents_5yr_growth_pct),
        "fatalities_5yr_growth_pct": float(fatalities_5yr_growth_pct)
    }

def add_derived_columns(cleaned_dfs: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    df_nat = cleaned_dfs["national_series"].copy()
    
    # Calculate Lakh representations
    df_nat["accidents_lakh"] = (df_nat["accidents"] / 100000.0).round(2)
    df_nat["fatalities_lakh"] = (df_nat["fatalities"] / 100000.0).round(2)
    
    # Daily averages
    df_nat["accidents_per_day"] = (df_nat["accidents"] / 365.0).round(1)
    df_nat["deaths_per_day"] = (df_nat["fatalities"] / 365.0).round(1)
    
    # Recalculated severity (killed per 100 accidents) to check consistency
    df_nat["calc_severity"] = ((df_nat["fatalities"] / df_nat["accidents"]) * 100.0).round(1)
    
    cleaned_dfs["national_series"] = df_nat
    return cleaned_dfs
