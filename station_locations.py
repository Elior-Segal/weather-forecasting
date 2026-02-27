import numpy as np
import pandas as pd

from stations_parser import df as stations_df

locations_name = ['Adelaide', 'Albany', 'Albury', 'AliceSprings', 'BadgerysCreek', 'Ballarat', 'Bendigo', 'Brisbane',
                  'Cairns', 'Canberra', 'Cobar', 'CoffsHarbour', 'Dartmoor', 'Darwin', 'GoldCoast', 'Hobart',
                  'Katherine', 'Launceston', 'Melbourne', 'MelbourneAirport', 'Mildura', 'Moree', 'MountGambier',
                  'MountGinini', 'Newcastle', 'Nhil', 'NorahHead', 'NorfolkIsland', 'Nuriootpa', 'PearceRAAF',
                  'Penrith', 'Perth', 'PerthAirport', 'Portland', 'Richmond', 'Sale', 'SalmonGums', 'Sydney',
                  'SydneyAirport', 'Townsville', 'Tuggeranong', 'Uluru', 'WaggaWagga', 'Walpole', 'Watsonia',
                  'Williamtown', 'Witchcliffe', 'Wollongong', 'Woomera']


#
# def get_station_information(location):
#     location_stations = stations_df[stations_df.site_norm.apply(lambda s: s.startswith(location.upper()))]
#
#     airport = location_stations[location_stations.site_norm.str.contains("AIRPORT")]
#     if airport.empty:
#
#         time_coherent = location_stations[
#             (location_stations.start < 2007) & ((location_stations.end > 2017) | (location_stations.end.isna()))]
#         if time_coherent.empty:
#             return location_stations.iloc[0]
#         else:
#             return time_coherent.loc[time_coherent.start.idxmax()]
#     else:
#         return airport.iloc[0]
#
#
# locations = {location: get_station_information(location) for location in locations_name}
# loc_to_lat_lon = {location: (np.float32(station_info.lat), np.float32(station_info.lon)) for location, station_info in locations.items()}


def get_station_information(location):
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

# old = {'Adelaide': (np.float32(-34.9524), np.float32(138.5196)),
#  'Albany': (np.float32(-34.9414), np.float32(117.8022)),
#  'Albury': (np.float32(-36.0663), np.float32(146.953)),
#  'AliceSprings': (np.float32(-23.7951), np.float32(133.889)),
#  'BadgerysCreek': (np.float32(-33.8969), np.float32(150.7281)),
#  'Ballarat': (np.float32(-37.5174), np.float32(143.7791)),
#  'Bendigo': (np.float32(-36.7411), np.float32(144.3274)),
#  'Brisbane': (np.float32(-27.3915), np.float32(153.13)),
#  'Cairns': (np.float32(-16.8681), np.float32(145.7444)),
#  'Canberra': (np.float32(-35.3049), np.float32(149.2014)),
#  'Cobar': (np.float32(-31.5388), np.float32(145.7964)),
#  'CoffsHarbour': (np.float32(-30.3189), np.float32(153.1162)),
#  'Dartmoor': (np.float32(-28.0636), np.float32(115.1903)),
#  'Darwin': (np.float32(-12.4239), np.float32(130.8925)),
#  'GoldCoast': (np.float32(-27.939), np.float32(153.4283)),
#  'Hobart': (np.float32(-42.8339), np.float32(147.5033)),
#  'Katherine': (np.float32(-14.4747), np.float32(132.3051)),
#  'Launceston': (np.float32(-41.5397), np.float32(147.2033)),
#  'Melbourne': (np.float32(-37.6654), np.float32(144.8329)),
#  'MelbourneAirport': (np.float32(-37.6654), np.float32(144.8329)),
#  'Mildura': (np.float32(-34.2358), np.float32(142.0867)),
#  'Moree': (np.float32(-29.4898), np.float32(149.8471)),
#  'MountGambier': (np.float32(-37.8221), np.float32(140.7593)),
#  'MountGinini': (np.float32(-35.5293), np.float32(148.7721)),
#  'Newcastle': (np.float32(-33.0814), np.float32(151.6521)),
#  'Nhil': (np.float32(-36.3093), np.float32(141.6486)),
#  'NorahHead': (np.float32(-33.2814), np.float32(151.5766)),
#  'NorfolkIsland': (np.float32(-29.0582), np.float32(167.954)),
#  'Nuriootpa': (np.float32(-34.4709), np.float32(138.9991)),
#  'PearceRAAF': (np.float32(-31.6669), np.float32(116.0189)),
#  'Penrith': (np.float32(-33.758), np.float32(150.7054)),
#  'Perth': (np.float32(-31.9275), np.float32(115.9764)),
#  'PerthAirport': (np.float32(-31.9275), np.float32(115.9764)),
#  'Portland': (np.float32(-38.3148), np.float32(141.4705)),
#  'Richmond': (np.float32(-20.7001), np.float32(143.1137)),
#  'Sale': (np.float32(-38.1016), np.float32(147.1398)),
#  'SalmonGums': (np.float32(-32.9869), np.float32(121.6239)),
#  'Sydney': (np.float32(-33.9278), np.float32(151.17)),
#  'SydneyAirport': (np.float32(-33.9278), np.float32(151.17)),
#  'Townsville': (np.float32(-19.2483), np.float32(146.7661)),
#  'Tuggeranong': (np.float32(-35.4184), np.float32(149.0937)),
#  'Uluru': (np.float32(-25.3602), np.float32(131.0196)),
#  'WaggaWagga': (np.float32(-35.1071), np.float32(147.3636)),
#  'Walpole': (np.float32(-34.9769), np.float32(116.7286)),
#  'Watsonia': (np.float32(-37.7), np.float32(145.0833)),
#  'Williamtown': (np.float32(-32.7298), np.float32(152.0254)),
#  'Witchcliffe': (np.float32(-34.0281), np.float32(115.1042)),
#  'Wollongong': (np.float32(-34.2625), np.float32(150.8752)),
#  'Woomera': (np.float32(-31.1558), np.float32(136.8054))}
#
#
# for k in old:
#     print(k)
#     print(old[k])
#     print(loc_to_lat_lon[k])
#     print(((old[k][0] - loc_to_lat_lon[k][0])**2+(old[k][1] - loc_to_lat_lon[k][1])**2)**0.5)
#     print()
#
#
# from collections import defaultdict
# d = defaultdict(list)
#
# for loc, lat in loc_to_lat_lon.items():
#     d[lat].append(loc)
#
# for a in d.values():
#     if len(a) > 1:
#         print(a)
