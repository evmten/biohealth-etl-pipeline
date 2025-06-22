import sys, os
import sqlite3
from pathlib import Path
import pandas as pd

# Define base path to data directory
BASE_PATH = Path(__file__).resolve().parent.parent / "data"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from transformation.transform_health_data import clean_life_expectancy, clean_air_quality, clean_health_expenditure

# Test cleaning of life expectancy data
def test_life_expectancy_transform():
    path = BASE_PATH / "raw" / "life_expectancy.csv"
    df = clean_life_expectancy(path)
    assert isinstance(df, pd.DataFrame)
    assert "Country" in df.columns
    assert "LifeExpectancy" in df.columns
    assert df["Year"].nunique() == 1 and df["Year"].iloc[0] == 2022
    assert df["LifeExpectancy"].notnull().all()
    assert len(df) > 25

# Test cleaning of air quality data
def test_air_quality_transform():
    path = BASE_PATH / "raw" / "air_quality_partial.json"
    df = clean_air_quality(path)
    assert isinstance(df, pd.DataFrame)
    assert "AirQualityIndex" in df.columns
    assert df["AirQualityIndex"].dtype in [int, float]
    assert len(df) > 25

# Test cleaning of health expenditure data
def test_health_expenditure_transform():
    path = BASE_PATH / "raw" / "health_expenditure.csv"
    df = clean_health_expenditure(path)
    assert isinstance(df, pd.DataFrame)
    assert "HealthExpenditure" in df.columns
    assert df["Year"].nunique() == 1 and df["Year"].iloc[0] == 2022
    assert set(df.columns) == {"Country", "HealthExpenditure", "Year"}
    assert len(df) > 25

# Test if data was loaded into SQLite successfully
def test_sqlite_load():
    conn = sqlite3.connect(str(BASE_PATH / "health_data.db"))
    df = pd.read_sql("SELECT * FROM health_data LIMIT 1", conn)
    assert not df.empty
    conn.close()