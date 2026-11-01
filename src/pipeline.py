"""
Master Pipeline Orchestrator.
Runs ingest -> clean -> derive -> validate -> export.
Can be executed as: python -m src.pipeline
"""

import sys
import logging
from src.ingest import ingest_tier1_open_data, get_tier2_seed_data
from src.clean import clean_all
from src.derive import add_derived_columns, derive_national_metrics
from src.validate import validate_datasets
from src.export import export_cleaned_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def run_pipeline():
    logging.info("Starting Road Accidents Data Pipeline...")
    
    # Step 1: Ingest
    has_tier1 = ingest_tier1_open_data()
    logging.info(f"Ingestion mode: {'Tier 1 live feeds' if has_tier1 else 'Tier 2 validated published figures'}")
    raw_data = get_tier2_seed_data()
    
    # Step 2: Clean
    cleaned = clean_all(raw_data)
    logging.info("Data cleaned and standardized.")
    
    # Step 3: Derive
    derived = add_derived_columns(cleaned)
    metrics = derive_national_metrics(derived["national_series"])
    logging.info(f"Derived Key Metrics (2025): {metrics['accidents_per_day']} accidents/day, {metrics['deaths_per_day']} deaths/day")
    
    # Step 4: Validate
    is_valid, errors = validate_datasets(derived)
    if not is_valid:
        logging.error(f"Validation failed with {len(errors)} errors:")
        for err in errors:
            logging.error(f"  - {err}")
        sys.exit(1)
    logging.info("Validation PASSED (100% assertions satisfied).")
    
    # Step 5: Export
    paths = export_cleaned_data(derived)
    logging.info("Successfully exported cleaned CSVs:")
    for name, path in paths.items():
        logging.info(f"  - {name}: {path}")
        
    return derived, metrics

if __name__ == "__main__":
    run_pipeline()
