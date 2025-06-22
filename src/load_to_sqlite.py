import pandas as pd
import sqlite3
import os
import json

csv_path = "../data/cleaned/merged_health_data.csv"
db_path = "../data/health_data.db"
table_name = "health_data"

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found at {csv_path}")

# Load merged data
df = pd.read_csv(csv_path)

conn = sqlite3.connect(db_path)

# Load and store raw datasets
df_life_raw = pd.read_csv("../data/raw/life_expectancy.csv")
df_life_raw.to_sql("raw_life_expectancy", conn, if_exists="replace", index=False)

with open("../data/raw/air_quality_partial.json", encoding="utf-8") as f:
    air_data = json.load(f)
df_air_raw = pd.DataFrame(air_data)
df_air_raw.to_sql("raw_air_quality", conn, if_exists="replace", index=False)


df_spending_raw = pd.read_csv("../data/raw/health_expenditure.csv")
df_spending_raw.to_sql("raw_health_expenditure", conn, if_exists="replace", index=False)

# Store merged data
df_merged_health_data = pd.read_csv("../data/cleaned/merged_health_data.csv")
df_merged_health_data.to_sql("merged_health_data", conn, if_exists="replace", index=False)

# Store main table
df.to_sql(table_name, conn, if_exists="replace", index=False)

print(f"Successfully loaded {len(df)} rows into '{table_name}' table in '{db_path}'")

print(df.head())

# Top 5 countries by life expectancy
print("\n Top 5 countries by life expectancy:")
query = """
    SELECT Country, LifeExpectancy
    FROM health_data
    ORDER BY LifeExpectancy DESC
    LIMIT 5;
    """

df_top5_life = pd.read_sql_query(query, conn)
print(df_top5_life)


# Top 5 countries by health expenditure
print("\n Top 5 countries by health expenditure:")
query = """
    SELECT Country, HealthExpenditure
    FROM merged_health_data
    ORDER BY HealthExpenditure DESC
    LIMIT 5;
    """

df_top5_expediture = pd.read_sql_query(query, conn)
print(df_top5_expediture)


# Top 5 countries with high air pollution and high spending
print("\n Top 5 countries with high air pollution and high spending:")
query = """
    SELECT Country, AirQualityIndex, HealthExpenditure
    FROM merged_health_data
    ORDER BY AirQualityIndex DESC
    LIMIT 5;
    """

df_top5_pollution_expediture = pd.read_sql_query(query, conn)
print(df_top5_pollution_expediture)


# Top 5 countries with the best air quality (lowest AQI)
print("\n Top 5 countries with the best air quality (lowest AQI):")
query = """
    SELECT Country, AirQualityIndex
    FROM merged_health_data
    ORDER BY AirQualityIndex ASC
    LIMIT 5;
    """

df_top5_air_quality = pd.read_sql_query(query, conn)
print(df_top5_air_quality)


# Count of records for each table
print("\n Count of records for life expectancy table:")
query = """
    SELECT COUNT(*) FROM raw_life_expectancy;
    """

df_records_life_expectancy = pd.read_sql_query(query, conn)
print(df_records_life_expectancy)

print("\n Count of records for air quality table:")
query = """
    SELECT COUNT(*) FROM raw_air_quality;
    """

df_records_air_quality = pd.read_sql_query(query, conn)
print(df_records_air_quality)

print("\n Count of records for health expenditure table:")
query = """
    SELECT COUNT(*) FROM raw_health_expenditure;
    """

df_records_health_expenditure = pd.read_sql_query(query, conn)
print(df_records_health_expenditure)


print("\n Preview sample records:")
query = """
    SELECT * FROM raw_air_quality LIMIT 5;
    """

df_samples_air_quality = pd.read_sql_query(query, conn)
print(df_samples_air_quality)

print("\n Compare raw vs clean: countries present in raw but missing from final:")
query = """
    SELECT DISTINCT Country FROM raw_health_expenditure
    EXCEPT
    SELECT DISTINCT Country FROM merged_health_data;
    """

df_raw_vs_clean = pd.read_sql_query(query, conn)
print(df_raw_vs_clean)

conn.close()