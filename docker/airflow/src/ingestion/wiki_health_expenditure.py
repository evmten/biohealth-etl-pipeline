import pandas as pd
import logging

def fetch_health_expenditure_data():
    logging.info("Scraping health expenditure per capita from Wikipedia...")

    url = "https://en.wikipedia.org/wiki/List_of_countries_by_total_health_expenditure_per_capita"

    try:
        tables = pd.read_html(url)
        df = tables[0]

        if "2022" not in df.columns:
            raise ValueError("2022 column not found in Wikipedia table.")
        df = df[["Location", "2022"]]
        
        df.rename(columns={"Location": "Country", "2022": "HealthExpenditure"}, inplace=True)

        logging.info(f"Scraped and filtered table shape: {df.shape}")
        logging.info("Sample:\n" + str(df.head(3)))

        # Add Year column to allow merging
        df["Year"] = 2022
        logging.info(f"Columns: {df.columns.tolist()}")
        
        return df

    except Exception as e:
        logging.error(f"Health expenditure scraping failed: {e}")
        return None


