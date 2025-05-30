🌍 Health Data Pipeline
A Data Engineering project that builds a scalable data pipeline to collect, transform, and store global health-related data. It demonstrates key data engineering concepts like API integration, web scraping, ETL workflows, data validation, orchestration with Airflow, and database loading.

📊 Project Overview
This project integrates three health data sources into a single SQLite database for analysis and reporting:

✅ Life Expectancy: Fetched from OECD API (XML)
✅ Air Quality: Collected from the IQAir API (JSON)
✅ Health Expenditure: Scraped from Wikipedia (HTML)

The pipeline is orchestrated with Apache Airflow using Docker, and the data is loaded into SQLite. The final dataset merges life expectancy, air quality index, and health spending per country.

🛠️ Tools & Technologies
Python 3.11

Apache Airflow 2.8.0 (Dockerized)

SQLite (via sqlite3)

Docker & Docker Compose

APIs: OECD API (XML), IQAir API (JSON)

Web Scraping: pandas.read_html for Wikipedia

Pytest (for testing)

Pandas (ETL and transformation)

JSON, CSV, SQL (data formats)

🌐 Data Sources & APIs
Source	Type	Description
OECD API	XML	Life expectancy by country (2020+)
IQAir API (AirVisual)	JSON (REST)	Air quality index per city
Wikipedia	Web page	Health expenditure per capita

🏗️ Architecture Overview
plaintext
Copy
+-----------------------+
|       Airflow DAGs     |
| (health & validation)  |
+-----------------------+
          |
          v
+-----------------------+
|   Data Ingestion      |
| - OECD API (XML)      |
| - IQAir API (JSON)    |
| - Wikipedia (HTML)    |
+-----------------------+
          |
          v
+-----------------------+
| Data Transformation   |
| - Cleaning            |
| - Aggregation         |
| - Merging datasets    |
+-----------------------+
          |
          v
+-----------------------+
| Data Storage (SQLite) |
| - Raw tables          |
| - Cleaned dataset     |
+-----------------------+
🚀 How to Run the Project
Prerequisites
✅ Install Docker and Docker Compose
✅ Get an IQAir API Key and set it in a .env file:

bash
Copy
# .env file (root folder)
IQAIR_API_KEY=your_api_key_here
Step-by-Step Guide
1️⃣ Clone the repo

bash
Copy
git clone https://github.com/your-username/health-data-pipeline.git
cd health-data-pipeline
2️⃣ Start Airflow containers

bash
Copy
docker-compose up --build
3️⃣ Trigger the pipeline DAG

Go to http://localhost:8080 (Airflow UI)

Trigger health_data_pipeline → This will:

Fetch data from APIs

Save raw data

Transform and merge datasets

Store results in SQLite

4️⃣ Validate Data

The pipeline triggers validate_health_data DAG automatically for validation checks.

5️⃣ Run SQLite queries (optional)

Use a SQLite viewer or run:

bash
Copy
python src/load_to_sqlite.py
6️⃣ Run Tests

bash
Copy
pytest tests/test_transform.py
🧪 Testing Instructions
Run the tests after the DAG completes:

bash
Copy
pytest tests/test_transform.py
Tests include:
✅ Data transformation logic (life expectancy, air quality, health spending)
✅ Database connection and data integrity (SQLite)
