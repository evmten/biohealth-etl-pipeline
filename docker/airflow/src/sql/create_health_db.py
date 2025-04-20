import sqlite3

# Connect (or create) database
conn = sqlite3.connect("data/health_data.db")
cursor = conn.cursor()

# Create table
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

# Optionally print confirmation
print("SQLite DB and table created successfully.")

# Close connection
conn.commit()
conn.close()