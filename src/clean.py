"""
Data Cleaning and Formatting Module.
Normalises column names, ensures strict typing, preserves provenance and tags derivations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

def clean_national_series(data: list) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df["year"] = df["year"].astype(int)
    df["accidents"] = pd.to_numeric(df["accidents"], errors="coerce").astype(int)
    df["fatalities"] = pd.to_numeric(df["fatalities"], errors="coerce").astype(int)
    # injuries can have None/NaN for 2025
    df["injuries"] = pd.to_numeric(df["injuries"], errors="coerce").astype("Int64")
    df["severity"] = df["severity"].astype(float)
    df["yoy_accidents_pct"] = df["yoy_accidents_pct"].astype(float)
    df["yoy_fatalities_pct"] = df["yoy_fatalities_pct"].astype(float)
    df["source"] = df["source"].astype(str)
    df["is_provisional"] = df["is_provisional"].astype(bool)
    df["derivation_note"] = df["derivation_note"].astype(str)
    return df

def clean_state_leaders(data: list) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df["state"] = df["state"].astype(str)
    df["metric"] = df["metric"].astype(str)
    df["val_2024"] = df["val_2024"].astype(int)
    df["val_2025"] = df["val_2025"].astype(int)
    df["yoy_pct"] = df["yoy_pct"].astype(float)
    df["national_share_2025_pct"] = df["national_share_2025_pct"].astype(float)
    df["source"] = df["source"].astype(str)
    df["is_provisional"] = df["is_provisional"].astype(bool)
    return df

def clean_state_severity_2026(data: list) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df["state"] = df["state"].astype(str)
    df["severity_rate"] = pd.to_numeric(df["severity_rate"], errors="coerce")
    df["period"] = df["period"].astype(str)
    df["source"] = df["source"].astype(str)
    df["status"] = df["status"].astype(str)
    return df

def clean_recorded_causes(data: list) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df["cause"] = df["cause"].astype(str)
    df["accidents_count"] = df["accidents_count"].astype(int)
    df["pct_of_total"] = df["pct_of_total"].astype(float)
    df["source"] = df["source"].astype(str)
    df["is_provisional"] = df["is_provisional"].astype(bool)
    return df

def clean_all(raw_data_dict: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    return {
        "national_series": clean_national_series(raw_data_dict["national_series"]),
        "state_leaders": clean_state_leaders(raw_data_dict["state_leaders"]),
        "state_severity_2026": clean_state_severity_2026(raw_data_dict["state_severity_2026"]),
        "recorded_causes_2025": clean_recorded_causes(raw_data_dict["recorded_causes_2025"])
    }
