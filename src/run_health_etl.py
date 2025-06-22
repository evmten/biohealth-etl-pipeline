import logging
import json
import time
import pandas as pd

import os
import sys
# Add src folder to Python path (for Airflow)
sys.path.append('/opt/airflow/src')

# Import data fetching and transformation modules
from ingestion.oecd_life_expectancy import fetch_life_expectancy_data
from ingestion.airvisual_air_quality import fetch_air_quality_data
from ingestion.wiki_health_expenditure import fetch_health_expenditure_data
from transformation.transform_health_data import transform_data
from config.cities import cities

logging.basicConfig(level=logging.INFO)

# Fetch and store life expectancy data
df_life = fetch_life_expectancy_data()

os.makedirs("/opt/airflow/data/raw", exist_ok=True)
df_life.to_csv("/opt/airflow/data/raw/life_expectancy.csv", index=False)

# Fetch air quality data with rate limiting
air_quality_results = []
batch_size = 5
sleep_after_batch = 65

for i, loc in enumerate(cities):
    logging.info(f"Requesting data for {loc['city']}, {loc['country']} ({i+1}/{len(cities)})")
    result = fetch_air_quality_data(loc["city"], loc["state"], loc["country"])

    if (i + 1) % batch_size == 0:
        logging.info("Reached batch limit, sleeping to respect API rate limits...")
        time.sleep(sleep_after_batch)

    if result:
        air_quality_results.append(result)

# Save air quality and city metadata
with open("/opt/airflow/data/raw/air_quality_partial.json", "w", encoding="utf-8") as f:
    json.dump(air_quality_results, f, indent=4, ensure_ascii=False)

with open("/opt/airflow/data/raw/countries_cities.json", "w", encoding="utf-8") as f:
    json.dump(cities, f, indent=4, ensure_ascii=False)

# Load air quality and health expenditure data
df_air = pd.DataFrame(air_quality_results)
df_spending = fetch_health_expenditure_data()
df_spending.to_csv("/opt/airflow/data/raw/health_expenditure.csv", index=False)
df_spending = pd.read_csv("/opt/airflow/data/raw/health_expenditure.csv")

# Transform and merge datasets
transform_data(df_life, df_air, df_spending)