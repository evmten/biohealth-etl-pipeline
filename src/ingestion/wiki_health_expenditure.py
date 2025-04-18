import pandas as pd
import logging

def fetch_health_expenditure_data():
    logging.info("Scraping health expenditure per capita from Wikipedia...")

    url = "https://en.wikipedia.org/wiki/List_of_countries_by_total_health_expenditure_per_capita"

    try:
        tables = pd.read_html(url)
        
        # Check which table looks right (usually table 0 or 1)
        df = tables[0]
        logging.info(f"Scraped table with shape: {df.shape}")
        logging.info("Sample:\n" + str(df.head(3)))
        # oecd_countries = df["Location"].unique()
        # df_spending = fetch_health_expenditure_data()
        
        return df

    except Exception as e:
        logging.error(f"Health expenditure scraping failed: {e}")
        return None

