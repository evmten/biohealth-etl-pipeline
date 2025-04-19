import logging
import json
import time
import pandas as pd

import os
import sys
sys.path.append('/opt/airflow/src')

from ingestion.oecd_life_expectancy import fetch_life_expectancy_data
from ingestion.airvisual_air_quality import fetch_air_quality_data
from ingestion.wiki_health_expenditure import fetch_health_expenditure_data
from transformation.transform import transform_data


logging.basicConfig(level=logging.INFO)

# Fetch life expectancy
df_life = fetch_life_expectancy_data()

os.makedirs("/opt/airflow/data/raw", exist_ok=True)
df_life.to_csv("/opt/airflow/data/raw/life_expectancy.csv", index=False)

# Cities for air quality
cities = [
    {"city": "Canberra", "state": " ACT", "country": "Australia"},
    {"city": "Vienna", "state": "Vienna", "country": "Austria"},
    {"city": "Brussels", "state": "Brussels Capital", "country": "Belgium"},
    {"city": "Toronto", "state": "Ontario", "country": "Canada"},
    {"city": "Santiago", "state": "Santiago Metropolitan", "country": "Chile"},
    {"city": "Bogota", "state": "Bogota D.C.", "country": "Colombia"}, 
    {"city": "San Jose", "state": "San Jose", "country": "Costa Rica"},
    {"city": "Prague", "state": "Praha", "country": "Czech Republic"},
    {"city": "Copenhagen", "state": "Capital Region", "country": "Denmark"},
    {"city": "Tallinn", "state": "Harjumaa", "country": "Estonia"},
    {"city": "Helsinki", "state": "Uusimaa", "country": "Finland"},
    {"city": "Paris", "state": "Ile-de-France", "country": "France"},
    {"city": "Berlin", "state": "Berlin", "country": "Germany"},
    {"city": "Athens", "state": "Attica", "country": "Greece"},
    {"city": "Budapest", "state": "Central Hungary", "country": "Hungary"},
    {"city": "Reykjavik", "state": "Capital Region", "country": "Iceland"},
    {"city": "Dublin", "state": "Leinster", "country": "Ireland"},
    {"city": "Jerusalem", "state": "Jerusalem", "country": "Israel"},
    {"city": "Rome", "state": "Latium", "country": "Italy"},
    {"city": "Tokyo", "state": "Tokyo", "country": "Japan"},
    {"city": "Riga", "state": "Riga", "country": "Latvia"}, 
    {"city": "Vilnius", "state": "Vilnius", "country": "Lithuania"},
    {"city": "Luxembourg", "state": "District de Luxembourg", "country": "Luxembourg"},
    {"city": "Mexico City", "state": "Mexico City", "country": "Mexico"},
    {"city": "Amsterdam", "state": "North Holland", "country": "Netherlands"},
    {"city": "Auckland", "state": "Auckland", "country": "New Zealand"},
    {"city": "Oslo", "state": "Oslo", "country": "Norway"},
    {"city": "Warsaw", "state": "Mazovia", "country": "Poland"},
    {"city": "Lisbon", "state": "Lisbon", "country": "Portugal"},
    {"city": "Bratislava", "state": "Bratislava", "country": "Slovakia"}, 
    {"city": "Ljubljana", "state": "Osrednjeslovenska", "country": "Slovenia"},
    {"city": "Seoul", "state": "Seoul", "country": "South Korea"},
    {"city": "Madrid", "state": "Madrid", "country": "Spain"},
    {"city": "Stockholm", "state": "Stockholm", "country": "Sweden"},
    {"city": "Bern", "state": "Bern", "country": "Switzerland"},
    {"city": "Istanbul", "state": "Istanbul", "country": "Turkey"},
    {"city": "London", "state": "England", "country": "United Kingdom"},
    {"city": "Washington D.C.", "state": "District of Columbia", "country": "USA"}
]

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

# Save air quality JSON
with open("/opt/airflow/data/raw/air_quality_partial.json", "w", encoding="utf-8") as f:
    json.dump(air_quality_results, f, indent=4, ensure_ascii=False)

# Save countries info
with open("/opt/airflow/data/raw/countries_cities.json", "w", encoding="utf-8") as f:
    json.dump(cities, f, indent=4, ensure_ascii=False)

df_air = pd.DataFrame(air_quality_results)
df_spending = fetch_health_expenditure_data()

# Transform and save final dataset
transform_data(df_life, df_air, df_spending)
