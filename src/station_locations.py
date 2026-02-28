"""
This file calculates the data locations' longitude and latitude based on the stations information file
loc_to_lat_lon is a dict: [location name] -> Tuple[latitude, longitude]
"""

import numpy as np
import pandas as pd

from .stations_parser import df as stations_df

locations_name = ['Adelaide', 'Albany', 'Albury', 'AliceSprings', 'BadgerysCreek', 'Ballarat', 'Bendigo', 'Brisbane',
                  'Cairns', 'Canberra', 'Cobar', 'CoffsHarbour', 'Dartmoor', 'Darwin', 'GoldCoast', 'Hobart',
                  'Katherine', 'Launceston', 'Melbourne', 'MelbourneAirport', 'Mildura', 'Moree', 'MountGambier',
                  'MountGinini', 'Newcastle', 'Nhil', 'NorahHead', 'NorfolkIsland', 'Nuriootpa', 'PearceRAAF',
                  'Penrith', 'Perth', 'PerthAirport', 'Portland', 'Richmond', 'Sale', 'SalmonGums', 'Sydney',
                  'SydneyAirport', 'Townsville', 'Tuggeranong', 'Uluru', 'WaggaWagga', 'Walpole', 'Watsonia',
                  'Williamtown', 'Witchcliffe', 'Wollongong', 'Woomera']


def get_station_information(location):
    """
    Given a location name,
    searches for possible rows in the stations information file based on the name and time of operation
    @param location: the location to query its information
    @return: the row of a likely appropriate row
    """
    location_stations = stations_df[stations_df.site_norm.apply(lambda s: s.startswith(location.upper()))]

    if 'Airport' in location:
        airport = location_stations[location_stations.site_norm.str.contains("AIRPORT")]
    else:
        airport = pd.DataFrame()
        location_stations = location_stations[~location_stations.site_norm.str.contains("AIRPORT")]

    if airport.empty:
        time_coherent = location_stations[
            (location_stations.start < 2007) & ((location_stations.end > 2017) | (location_stations.end.isna()))]
        if time_coherent.empty:
            return location_stations.iloc[0]
        else:
            return time_coherent.loc[time_coherent.start.idxmax()]
    else:
        return airport.iloc[0]


locations = {location: get_station_information(location) for location in locations_name}
loc_to_lat_lon = {location: (np.float32(station_info.lat), np.float32(station_info.lon)) for location, station_info in
                  locations.items()}