from ingestion.ingest import fetch_data
from transformation.transform import transform_data
import logging

logging.basicConfig(level=logging.INFO)

def main():
    fetch_data()
    transform_data()

if __name__ == "__main__":
    main()