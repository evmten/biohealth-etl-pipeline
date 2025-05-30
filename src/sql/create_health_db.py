import sqlite3

conn = sqlite3.connect("data/health_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS health_data (
    Country TEXT,
    Year INTEGER,
    LifeExpectancy REAL,
    HealthExpenditure REAL,
    AirQualityIndex INTEGER,
    MainPollutant TEXT
)
""")

print("SQLite DB and table created successfully.")

conn.commit()
conn.close()