# import logging

# def fetch_data():
#     logging.info("Fetching data... (stub)")

import pandas as pd
import logging
import os

def fetch_data():
    logging.info("Loading OECD health data from local CSV...")
    
    file_path = os.path.join("data", "raw", "oecd_health_stats.csv")
    
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Loaded dataset with shape: {df.shape}")
        logging.info("Sample:\n" + str(df.head(3)))
        return df
    except Exception as e:
        logging.error(f"Failed to load CSV: {e}")
        return None
