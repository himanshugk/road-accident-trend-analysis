"""
Data Export Module.
Writes verified DataFrames to data/cleaned/*.csv with full provenance.
"""

import os
import pandas as pd
from typing import Dict

CLEANED_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cleaned")

def export_cleaned_data(dfs: Dict[str, pd.DataFrame]) -> Dict[str, str]:
    os.makedirs(CLEANED_DIR, exist_ok=True)
    paths = {}
    for name, df in dfs.items():
        file_path = os.path.join(CLEANED_DIR, f"{name}.csv")
        df.to_csv(file_path, index=False)
        paths[name] = file_path
    return paths
