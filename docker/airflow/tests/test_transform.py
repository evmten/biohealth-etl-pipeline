import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import pandas as pd
from pathlib import Path
from transformation.transform import clean_life_expectancy, clean_air_quality, clean_health_expenditure

def test_life_expectancy_transform():
    path = Path("data") / "raw" / "life_expectancy.csv"
    # df = pd.read_csv(path)
    df = clean_life_expectancy(path)
    assert isinstance(df, pd.DataFrame)
    assert "Country" in df.columns
    assert "LifeExpectancy" in df.columns
    assert df["Year"].nunique() == 1 and df["Year"].iloc[0] == 2022

def test_air_quality_transform():
    path = Path("data") / "raw" / "air_quality_partial.json"
    # df = pd.read_csv(path)
    df = clean_air_quality(path)
    assert isinstance(df, pd.DataFrame)
    assert "AirQualityIndex" in df.columns
    assert df["AirQualityIndex"].dtype in [int, float]

def test_health_expenditure_transform():
    path = Path("data") / "raw" / "health_expenditure.csv"
    # df = pd.read_csv(path)
    df = clean_health_expenditure(path)
    assert isinstance(df, pd.DataFrame)
    assert "HealthExpenditure" in df.columns
    assert df["Year"].nunique() == 1 and df["Year"].iloc[0] == 2022
