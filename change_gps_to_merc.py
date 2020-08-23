# /usr/bin/env python3

import pandas as pd
from pathlib import Path
import os
import re
from coordinate_transformation.to_web_merc import toWebMerc

# load CSV data into Pandas dataframe
home = os.environ['HOME']
data_dir = Path(home) / 'Programming/data/s2ds-project-data'
avg_weekdays_sum_diff_df = pd.read_csv(
    data_dir / 'avg_weekend_sum_diff_station_name_2019_v2.csv', index_col='Date')

# list of tuple station IDs and index of station IDs
tuple_station_id_index_list = [(i, re.search(r'(?<=Latitude_)\d{1,3}', item).group(
    0)) for i, item in enumerate(avg_weekdays_sum_diff_df.columns.to_list()) if re.search(r'^Latitude', item)]

# add mercator columns to dataframe and drop GPS coordinates columns from dataframe
for station_id_index, station_id in tuple_station_id_index_list:
    selection_df = avg_weekdays_sum_diff_df.filter(regex=rf'(^Latitude|^Longitude)_{station_id}$', axis=1)
    mercLong, mercLat = toWebMerc(
        selection_df.iloc[0, 1], selection_df.iloc[0, 0])
    avg_weekdays_sum_diff_df.insert(station_id_index, column='Merc_Lat_' +
                                    station_id, value=[mercLat for x in range(selection_df.shape[0])])
    avg_weekdays_sum_diff_df.insert(station_id_index+1, column='Merc_Long_' +
                                    station_id, value=[mercLong for x in range(selection_df.shape[0])])
    avg_weekdays_sum_diff_df.drop(
        ['Latitude_'+station_id, 'Longitude_'+station_id], axis=1, inplace=True)

# save to CSV
avg_weekdays_sum_diff_df.to_csv(
    data_dir / 'avg_weekend_sum_diff_station_name_merc_coord_2019_v2.csv')
