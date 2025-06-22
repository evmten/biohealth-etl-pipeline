import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("data/health_data.db")
cursor = conn.cursor()

# Create table if not already exists
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