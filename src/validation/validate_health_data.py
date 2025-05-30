import pandas as pd

def validate_merged_dataset(path="/opt/airflow/data/cleaned/merged_health_data.csv"):
    df = pd.read_csv(path)

    assert df["Country"].notnull().all(), "Missing country values!"
    assert df["LifeExpectancy"].between(30, 100).all(), "Life expectancy values out of range!"
    assert df["AirQualityIndex"].between(0, 500).all(), "Invalid AQI values!"
    assert df["HealthExpenditure"].gt(0).all(), "Negative or zero health expenditure!"

    print("Validated successfully!")
