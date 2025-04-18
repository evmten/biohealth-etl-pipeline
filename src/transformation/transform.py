import pandas as pd
import logging

def clean_life_expectancy(path="data/raw/life_expectancy.csv"):
    df = pd.read_csv(path)
    # Optional: map ISO country codes to full names
    iso3_to_name = {...}
    df["Country"] = df["Country"].map(iso3_to_name)
    # Optional: average over sex or select only 'T' (total)
    return df


def clean_air_quality(path="data/raw/air_quality_partial.json"):
    df = pd.read_json(path)
    # Rename or clean country names if needed
    return df


def clean_health_spending(path="data/raw/health_expenditure.csv"):
    df = pd.read_csv(path)
    # Melt year columns into rows
    df = df.melt(id_vars="Location", var_name="Year", value_name="HealthExpenditure")
    df.rename(columns={"Location": "Country"}, inplace=True)
    return df


def transform_data(df_life=None, df_air=None, df_spending=None):
    logging.info("Starting data transformation...")

    if df_life is None:
        df_life = clean_life_expectancy()

    if df_air is None:
        df_air = clean_air_quality()

    if df_spending is None:
        df_spending = clean_health_spending()

    # Merge on Country + Year (adjust based on what's available)
    # Example: group air quality to one row per country?
    
    df_final = df_life.merge(df_spending, on=["Country", "Year"], how="inner")
    df_final = df_final.merge(df_air, on="Country", how="inner")

    logging.info(f"Final merged shape: {df_final.shape}")
    df_final.to_csv("data/cleaned/merged_health_data.csv", index=False)

    return df_final
