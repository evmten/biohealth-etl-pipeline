"""
This script fetches life expectancy, air quality, and health expenditure data,
transforms it and saves the merged dataset for further use
"""

import logging
import json
import time
import pandas as pd

from ingestion.oecd_life_expectancy import fetch_life_expectancy_data
from ingestion.airvisual_air_quality import fetch_air_quality_data
from ingestion.wiki_health_expenditure import fetch_health_expenditure_data
from transformation.transform_health_data import transform_data
from config.cities import cities

logging.basicConfig(level=logging.INFO)

def main():

    # Fetch and save life expectancy data
    df_life = fetch_life_expectancy_data()
    df_life.to_csv("../data/raw/life_expectancy.csv", index=False)
    
    air_quality_results = []
    batch_size = 5
    sleep_after_batch = 65  # seconds

    # Fetch air quality data in batches to respect API rate limits
    for i, loc in enumerate(cities):
        logging.info(f"Requesting data for {loc['city']}, {loc['country']} ({i+1}/{len(cities)})")

        result = fetch_air_quality_data(loc["city"], loc["state"], loc["country"])

        # Pause after every 5 requests
        if (i + 1) % batch_size == 0:
            logging.info("Reached batch limit, sleeping to respect API rate limits...")
            time.sleep(sleep_after_batch)
        else:
            if result:
                air_quality_results.append(result)

    # Save fetched air quality data    
    with open("../data/raw/air_quality_partial.json", "w", encoding="utf-8") as f:
        json.dump(air_quality_results, f, indent=4, ensure_ascii=False)

    df_air = pd.DataFrame(air_quality_results)
    print(df_air.head())

    # Save cities metadata
    with open("../data/raw/countries_cities.json", "w", encoding="utf-8") as f:
        json.dump(cities, f, indent=4, ensure_ascii=False)

    df_spending = fetch_health_expenditure_data()
    
    transform_data(df_life, df_air, df_spending)

if __name__ == "__main__":
    main()