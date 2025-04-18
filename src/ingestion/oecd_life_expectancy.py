import requests
import logging
import pandas as pd
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()


def fetch_life_expectancy_data():
    logging.info("Fetching air quality data from OECD API...")

    url = f"https://sdmx.oecd.org/public/rest/data/OECD.CFE.EDS,DSD_REG_HEALTH@DF_HEALTH,/A.CTRY.CHE+USA+GBR+TUR+SWE+ESP+SVN+SVK+PRT+POL+NOR+NZL+NLD+MEX+LUX+LTU+LVA+KOR+JPN+ITA+ISR+IRL+HUN+ISL+GRC+DEU+FRA+FIN+EST+DNK+CZE+CRI+COL+CHL+CAN+BEL+AUS+AU1+AU2+AU3+AU4+AU5+AU6+AU7+AU8+AUT+AT11+AT111+AT112+AT113+AT12+AT121+AT122+AT123+AT124+AT125+AT126+AT127+AT13+AT130+AT21+AT211+AT212+AT213+AT22+AT221+AT222+AT223+AT224+AT225+AT226+AT31+AT311+AT312+AT313+AT314+AT315+AT32+AT321+AT322+AT323+AT33+AT331+AT332+AT333+AT334+AT335+AT34+AT341+AT342..LFEXP..M+F.Y?startPeriod=2020&dimensionAtObservation=AllDimensions"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.content)

        ns = {'generic': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic'}

        records = []
        for obs in root.findall('.//generic:Obs', ns):
            keys = {v.attrib['id']: v.attrib['value'] for v in obs.find('generic:ObsKey', ns)}
            value = obs.find('generic:ObsValue', ns).attrib['value']
            record = {
                'Country': keys.get('REF_AREA'),
                'Year': keys.get('TIME_PERIOD'),
                'Sex': keys.get('SEX'),
                'LifeExpectancy': float(value)
            }
            records.append(record)

        df = pd.DataFrame(records)
        logging.info(f"Parsed life expectancy records: {df.shape}")
        logging.info(f"Sample:\n{df.head(3)}")
        logging.info(f"Countries:\n{df['Country'].unique()}")        
        
        return df

    except Exception as e:
        logging.error(f"OECD XML parse failed: {e}")
        return None