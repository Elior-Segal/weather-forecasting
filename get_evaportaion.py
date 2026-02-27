# # import os
# # import requests
# #
# # base_url = "http://www.bom.gov.au/web01/ncc/www/climatology/evaporation/"
# # months = [
# #     "jan", "feb", "mar", "apr", "may", "jun",
# #     "jul", "aug", "sep", "oct", "nov", "dec"
# # ]
# #
# # output_dir = "evaporation_grids"
# # os.makedirs(output_dir, exist_ok=True)
# #
# # for m in months:
# #     filename = f"evap{m}.zip"
# #     url = base_url + filename
# #     print(url)
# #
# import numpy as np
# #
# #
# # def read_ascii_grid(path):
# #     with open(path, "r") as f:
# #         header = {}
# #         for _ in range(6):
# #             key, value = f.readline().split()
# #             header[key.lower()] = float(value)
# #
# #         data = np.loadtxt(f)
# #
# #     # unpack header
# #     ncols = int(header["ncols"])
# #     nrows = int(header["nrows"])
# #     xll = header["xllcorner"]
# #     yll = header["yllcorner"]
# #     cellsize = header["cellsize"]
# #     nodata = header["nodata_value"]
# #
# #     # replace NODATA with NaN
# #     data = np.where(data == nodata, np.nan, data)
# #
# #     return data, ncols, nrows, xll, yll, cellsize
# #
# #
# import matplotlib.pyplot as plt
#
# # data, ncols, nrows, xll, yll, cellsize = read_ascii_grid(
# #     r'C:\Users\Elior\PycharmProjects\DataScienceWorkshop\evaporation_grids\evapjun\evapjun.txt')
# #
# # extent = [
# #     xll,
# #     xll + ncols * cellsize,
# #     yll,
# #     yll + nrows * cellsize
# # ]
# #
# # plt.figure(figsize=(10, 6))
# # plt.imshow(
# #     np.flipud(data),
# #     extent=extent,
# #     origin="lower"
# # )
# # plt.colorbar(label="Grid value")
# # plt.xlabel("Longitude")
# # plt.ylabel("Latitude")
# # plt.title("Grid visualization")
# # plt.show()
# #
# #
# # def value_at_location(lon, lat, data, xll, yll, cellsize):
# #     """
# #     Returns the grid value nearest to (lon, lat)
# #     """
# #     col = int((lon - xll) / cellsize)
# #     row = int((lat - yll) / cellsize)
# #
# #     # grid row 0 is the TOP row → flip
# #     row = data.shape[0] - 1 - row
# #
# #     if (
# #             row < 0 or row >= data.shape[0] or
# #             col < 0 or col >= data.shape[1]
# #     ):
# #         return np.nan
# #
# #     return data[row, col]
# #
# #
# # val = value_at_location(
# #     lon=140.0,
# #     lat=-30.0,
# #     data=data,
# #     xll=xll,
# #     yll=yll,
# #     cellsize=cellsize
# # )
# #
# # print(val)
#
#
# from collections import namedtuple
#
# Grid = namedtuple(
#     "Grid",
#     ["data", "ncols", "nrows", "xll", "yll", "cellsize"]
# )
#
# import numpy as np
#
# def read_ascii_grid_filelike(f):
#     header = {}
#     for _ in range(6):
#         key, value = f.readline().split()
#         header[key.lower()] = float(value)
#
#     ncols = int(header["ncols"])
#     nrows = int(header["nrows"])
#     xll = header["xllcorner"]
#     yll = header["yllcorner"]
#     cellsize = header["cellsize"]
#     nodata = header["nodata_value"]
#
#     data = np.loadtxt(f)
#     data[data == nodata] = np.nan
#
#     return Grid(data, ncols, nrows, xll, yll, cellsize)
#
#
# import zipfile
# import io
#
# def load_ascii_grids_from_zip(zip_path):
#     grids = {}
#
#     with zipfile.ZipFile(zip_path) as z:
#         for name in z.namelist():
#             with z.open(name) as f:
#                 # text wrapper is required for np.loadtxt
#                 text_f = io.TextIOWrapper(f)
#                 grids[name] = read_ascii_grid_filelike(text_f)
#
#     return grids
#
#
# grids = load_ascii_grids_from_zip(r"C:\Users\Elior\PycharmProjects\DataScienceWorkshop\evaporation_grids\evap.zip")
#
#
#
# grid: Grid = grids['evapapr.txt']
#
# extent = [
#     grid.xll,
#     grid.xll + grid.ncols * grid.cellsize,
#     grid.yll,
#     grid.yll + grid.nrows * grid.cellsize
# ]
#
# plt.figure(figsize=(10, 6))
# plt.imshow(
#     np.flipud(grid.data),
#     extent=extent,
#     origin="lower"
# )
# plt.colorbar(label="Grid value")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.title("Grid visualization")
# plt.show()
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
    # unfortunately the site blocks automatic requests,
    # so we need to manually download them into evaporation_grids_zips folder
    base_url = "http://www.bom.gov.au/web01/ncc/www/climatology/evaporation/"

    output_dir = EVAPORATION_ZIPS_FOLDER
    os.makedirs(output_dir, exist_ok=True)

    for m in months:
        filename = f"evap{m}.zip"
        url = base_url + filename
        print(url)


def extract_evaporation():
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
