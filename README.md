🏥 Public Health Data Pipeline (ETL + Airflow + SQLite)
This project builds a local ETL pipeline that ingests, transforms, and loads public health data using Python, Airflow, and SQLite. It showcases essential data engineering skills such as orchestration, modular pipeline design, and validation.

🚀 Features
Modular Python ETL scripts

Airflow orchestration via Docker

Ingestion from API, CSV, and scraped sources

SQLite storage with raw and clean layers

Basic SQL analytics

Lightweight validation using pytest

📊 Architecture

📂 Project Structure
css
Copy
Edit
pipeline-project/
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── health_data.db
├── src/
│   ├── ingestion/
│   │   └── ingest.py
│   └── transformation/
│       └── transform.py
├── docker/
│   └── airflow/
│       ├── dags/
│       │   ├── health_pipeline_dag.py
│       │   ├── run_etl.py
│       │   └── validate_data.py
│       │   └── validate_pipeline_dag.py
│       └── tests/
│           └── test_transform.py
├── requirements.txt
└── README.md
📌 Data Sources
OECD API: Life expectancy data

IQAir API: Air quality index

Wikipedia (scraped): Health expenditure by country

🛠️ Tools & Tech

Tool	Purpose
Python	ETL logic
Pandas	Transformation
SQLite	Lightweight DB
Docker	Containerized Airflow
Apache Airflow	Orchestration & scheduling
Pytest	Basic data validation
🔁 Workflow Overview
Ingestion: Download data via API, CSV, and scraping

Transformation: Clean and harmonize datasets into one schema

Load: Save raw and cleaned data into SQLite

Orchestration: Run full pipeline using Airflow DAG

Validation: Basic checks with pytest

✅ Example Queries
sql
Copy
Edit
-- Top 5 countries by life expectancy
SELECT Country, LifeExpectancy
FROM health_data
ORDER BY LifeExpectancy DESC
LIMIT 5;

-- Compare raw vs clean datasets
SELECT DISTINCT Location
FROM raw_health_expenditure
EXCEPT
SELECT DISTINCT Country
FROM merged_health_data;
🧪 Running Tests
bash
Copy
Edit
cd docker/airflow
pytest tests/
🐳 Running Airflow
bash
Copy
Edit
cd docker
docker-compose up -d
Then open your browser at: http://localhost:8080
Login with your admin user and trigger the DAG.