import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv() # Load API key from .env file

def fetch_air_quality_data(city, state, country):
    
    # API request URL
    api_key = os.getenv("IQAIR_API_KEY")
    url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Extract pollution data
        pollution = data['data']['current']['pollution']
        logging.info(
            f"{city}, {country} — AQI (US): {pollution['aqius']}, Main: {pollution['mainus']}"
        )
        
        return {
            "City": city,
            "Country": country,
            "Aqius": pollution["aqius"],
            "Main_pollutant": pollution["mainus"]
        }

    except Exception as e:
        logging.error(f"Failed to fetch air data for {city}, {country}: {e}")
        return None
