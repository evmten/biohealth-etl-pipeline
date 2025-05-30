import pandas as pd
import logging

def clean_life_expectancy(path="/opt/airflow/data/raw/life_expectancy.csv"):
    df = pd.read_csv(path)

    df = df[df["Sex"].isin(["M", "F"])]

    df_total = (
        df.groupby(["Country", "Year"], as_index=False)
        .agg({"LifeExpectancy": "mean"})
    )
    df_total["Sex"] = "T"
    
    df = pd.concat([df, df_total], ignore_index=True)
    df = df[df["Sex"] == "T"]

    iso3_to_name = {
        "AUS": "Australia", "AUT": "Austria", "BEL": "Belgium", 
        "CAN": "Canada", "CHL": "Chile", "COL": "Colombia","CRI": "Costa Rica", 
        "CZE": "Czech Republic", "DNK": "Denmark", "EST": "Estonia",
        "FIN": "Finland", "FRA": "France", "DEU": "Germany", "GRC": "Greece", 
        "HUN": "Hungary", "ISL": "Iceland", "IRL": "Ireland", "ISR": "Israel", "ITA": "Italy",
        "JPN": "Japan", "LVA": "Latvia", "LTU": "Lithuania", "LUX": "Luxembourg",
        "MEX": "Mexico", "NLD": "Netherlands", "NZL": "New Zealand", "NOR": "Norway",
        "POL": "Poland", "PRT": "Portugal", "SVK": "Slovakia", "SVN": "Slovenia",
        "KOR": "South Korea", "ESP": "Spain", "SWE": "Sweden", "CHE": "Switzerland", 
        "TUR": "Turkey", "GBR": "United Kingdom", "USA": "USA"
    }

    df["Country"] = df["Country"].map(iso3_to_name).fillna(df["Country"])
    df["Year"] = df["Year"].astype(int)
    df = df[df["Year"]==2022]
    df = df[df["Sex"] == "T"]

    df = df[["Country", "Year", "LifeExpectancy"]]

    return df

def clean_air_quality(path="/opt/airflow/data/raw/air_quality_partial.json"):
    df = pd.read_json(path)

    df = df[["Country", "Aqius", "Main_pollutant"]]
    df.rename(columns={
        "Country": "Country",
        "Aqius": "AirQualityIndex",
        "Main_pollutant": "MainPollutant"
    }, inplace=True)
    
    df["Country"] = df["Country"].replace({"USA": "United States"})

    return df

def clean_health_expenditure(path="/opt/airflow/data/raw/health_expenditure.csv"):
    df = pd.read_csv(path)
    logging.info(f"Sample:\n{df.head(3)}")
    return df

def transform_data(df_life, df_air, df_spending):
    logging.info("Starting data transformation...")

    df_life = clean_life_expectancy()
    df_air = clean_air_quality()
    df_spending = clean_health_expenditure()

    common = set(df_life["Country"]) & set(df_air["Country"]) & set(df_spending["Country"])
    print("Common countries:", sorted(common))
    print("Missing from life:", sorted(set(df_spending["Country"]) - set(df_life["Country"])))
    print("Missing from air:", sorted(set(df_spending["Country"]) - set(df_air["Country"])))


    df_merged = pd.merge(df_life, df_spending, on=["Country", "Year"], how="inner")
    df_merged.to_csv("/opt/airflow/data/cleaned/merged_life_spending.csv", index=False)

    df_final = pd.merge(df_merged, df_air, on=["Country"], how="inner")

    logging.info(f"Final dataset shape: {df_final.shape}")
    logging.info(f"Sample:\n{df_final.head(3)}")

    df_final.to_csv("/opt/airflow/data/cleaned/merged_health_data.csv", index=False)

    return df_final