"""
This file bundles all the evaporation into one file
"""
import os
import zipfile
from pathlib import Path

EVAPORATION_ZIPS_FOLDER = "evaporation_grids_zips"
EVAPORATION_FOLDER = "evaporation_grids"
EVAPORATION_ZIP = "evap.zip"

months = [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
]


def print_evaporation_urls():
    """
    prints the 12 monthly average evaporation grids' links:

    unfortunately the site blocks automatic requests,
    so we need to manually download them into evaporation_grids_zips folder.
    (Otherwise this function would download them)
    """
    base_url = "http://www.bom.gov.au/web01/ncc/www/climatology/evaporation/"

    output_dir = EVAPORATION_ZIPS_FOLDER
    os.makedirs(output_dir, exist_ok=True)

    for m in months:
        filename = f"evap{m}.zip"
        url = base_url + filename
        print(url)


def extract_evaporation():
    """
    extracts the evaporation zips from EVAPORATION_ZIPS_FOLDER to EVAPORATION_FOLDER
    """
    # Configuration
    source_dir = Path(EVAPORATION_ZIPS_FOLDER)
    output_dir = Path(EVAPORATION_FOLDER)

    # Create the output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    # Iterate through all .zip files
    for zip_path in source_dir.glob('*.zip'):
        # Create a folder name based on the zip filename (e.g., 'a.zip' -> 'a')
        extract_to = output_dir / zip_path.stem

        print(f"Extracting {zip_path.name} to {extract_to}...")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)


def bundle_evaporation():
    """
    puts the 12 monthly average evaporation grids into one easy to use zip
    (The input directory is EVAPORATION_FOLDER and the output zip is EVAPORATION_ZIP)
    """
    source_dir = Path(EVAPORATION_FOLDER)
    output_zip = EVAPORATION_ZIP

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        # Use rglob('*') to find all files in all subdirectories
        for file_path in source_dir.rglob('*'):
            if file_path.is_file():
                # 'arcname' determines the name/path inside the zip.
                # Using file_path.name strips the subfolders (a/, b/, etc.)
                print(f"Adding: {file_path.name}")
                zip_ref.write(file_path, arcname=file_path.name)


if __name__ == '__main__':
    print_evaporation_urls()
    if os.listdir(EVAPORATION_ZIPS_FOLDER):
        extract_evaporation()
        bundle_evaporation()
