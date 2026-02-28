"""
This file Creates the solar_exposure.csv file which contains all the enriched solar exposure
"""

import os
import zipfile
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from .station_locations import locations

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
SUN_EXPOSURES_ZIPS_FOLDER = Path(os.path.join(DIR_PATH, "resources/sunshine/sun_exposures"))
SUN_EXPOSURES_FOLDER = Path(os.path.join(DIR_PATH, "resources/sunshine/sun_exposures_extracted"))
SUN_EXPOSURE_DF = os.path.join(DIR_PATH, "resources/sunshine/solar_exposure.csv")


def download_solar_exposures():
    """
    Based on the location names and information from station_locations file,
    Downloads from the australian weather site the full solar exposure information of all the locations
    @note Downloads the solar exposure compressed to the SUN_EXPOSURES_ZIPS_FOLDER directory
    """
    out_dir = SUN_EXPOSURES_ZIPS_FOLDER
    out_dir.mkdir(exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for location, info in tqdm(locations.items()):
        filename = f'{location}_sun_exposure.zip'
        if (out_dir / filename).exists():
            # assume already downloaded
            continue

        sun_exposure_url = f'https://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_stn_num={info['site']}'

        resp = requests.get(sun_exposure_url, headers=headers)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # find link containing the text
        link = soup.find("a", string="All years of data")

        if not link or not link.get("href"):
            print(location)
            print(f"Link not found on {sun_exposure_url}")
            continue

        zip_url = urljoin(sun_exposure_url, link["href"])
        print(f"Downloading: {zip_url}")

        zip_resp = requests.get(zip_url, headers=headers)
        zip_resp.raise_for_status()

        (out_dir / filename).write_bytes(zip_resp.content)


def extract_solar_exposures():
    """
    Extracts the solar zip files from the SUN_EXPOSURES_ZIPS_FOLDER directory to the SUN_EXPOSURES_FOLDER
    """
    # Configuration
    source_dir = SUN_EXPOSURES_ZIPS_FOLDER
    output_dir = SUN_EXPOSURES_FOLDER

    # Create the output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    # Iterate through all .zip files
    for zip_path in source_dir.glob('*.zip'):
        # Create a folder name based on the zip filename (e.g., 'a.zip' -> 'a')
        extract_to = output_dir / zip_path.stem

        print(f"Extracting {zip_path.name} to {extract_to}...")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)


def create_solar_exposure_df():
    """
    Combines all the solar exposure CSVs in SUN_EXPOSURES_FOLDER into one bug solar exposure csv
    @return: stores the combined csv to SUN_EXPOSURE_DF
    """
    solar_exposures_dfs = []
    for root, dirs, files in os.walk(SUN_EXPOSURES_FOLDER):
        for file in files:
            if not file.endswith(".csv"):
                continue
            file_path = os.path.join(root, file)
            location = os.path.split(root)[1][:-len("_sun_exposure")]

            solar_exposure_df = pd.read_csv(file_path)[['Year', 'Month', 'Day', 'Daily global solar exposure (MJ/m*m)']]
            solar_exposure_df["Date"] = pd.to_datetime(solar_exposure_df[['Year', 'Month', 'Day']]).dt.strftime(
                "%Y-%m-%d")
            solar_exposure_df = solar_exposure_df.drop(columns=['Year', 'Month', 'Day'])
            solar_exposure_df.rename(columns={'Daily global solar exposure (MJ/m*m)': 'solar_exposure'}, inplace=True)
            solar_exposure_df['Location'] = location

            solar_exposures_dfs.append(solar_exposure_df)

    df = pd.concat(solar_exposures_dfs)
    df.to_csv(SUN_EXPOSURE_DF)


if __name__ == '__main__':
    if not os.path.exists(SUN_EXPOSURE_DF):
        download_solar_exposures()
        extract_solar_exposures()
        create_solar_exposure_df()
