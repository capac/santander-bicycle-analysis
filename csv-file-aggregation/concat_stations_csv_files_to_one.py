# Import CSV files into PostgreSQL database

import pandas as pd
import os, csv
from pathlib import Path
from time import time

# start time
t0 = time()

# data directory
home = os.environ['HOME']
bike_data_dir = Path(home) / 'Programming/s2ds-project/S2DS2016 Starting Data/bike_data/cycle-parking-2015'
print(f'Bicycle data directory: {bike_data_dir}')
bike_files = list(bike_data_dir.glob('**/*.csv'))

# list of column headers
columns_list = ['X', 'Y', 'CPUniqueID', 'Correct_as_of', 'Station_Name', 'Cycle_parking_present_', 'Any_Cycle_parking_within_statio', 'Location_number', 'Number_of_parking_spaces', 'Type_updated', 'Type', 'Location', 'Rough_distance_from_closest_sta', 'Covered_by', 'Covered','Secure_cycle_storage_available', 'Secure_storage_type', 'Pump_and_repair_facilities', 'Photo_Hyperlink', 'Lat__MapInfo_', 'Long__MapInfo_']

# Check to see if CSV files all have the same headers
for i, bike_file in enumerate(bike_files):
    with open(bike_file, newline='', encoding='ISO-8859-1') as csvfile:
        reader=list(csv.reader(csvfile))
        if sorted(reader[0]) != sorted(columns_list):
            print(f'Check: {bike_file}')

# Convert datetimes to custom format in each dataframe
tmp_df_list=[]
date_columns = ['Correct_as_of']
for i, bike_file in enumerate(bike_files):
    tmp_df=pd.read_csv(bike_file, encoding='ISO-8859-1', low_memory=False)
    for col in date_columns:
        tmp_df[col]=pd.to_datetime(tmp_df[col], format=r'%b-%d', errors='raise', exact=False)
    tmp_df_list.append(tmp_df)
    if i % 2 == 0:
        print(f'Number of CSV files processed: {i}')
print(f'Total number of CSV files: {i}')

# Concatenate dataframes
journeys_df=pd.concat(tmp_df_list, axis=0, ignore_index=True)

# Ratio of rows that have at least one NAN
print(
    f'Ratio of rows that have at least one NA: {journeys_df.isna().any(axis=1).sum()/journeys_df.isna().all(axis=1).shape[0]:.3f}')

# Convert dtype to boolean
for col in ['Cycle_parking_present_', 'Any_Cycle_parking_within_statio', 'Covered', 'Secure_cycle_storage_available', 'Pump_and_repair_facilities']:
    journeys_df[col]=journeys_df[col].astype('bool')

# Convert dtype to int
for col in ['Location_number', 'Number_of_parking_spaces']:
    journeys_df[col]=journeys_df[col].astype('int32')

# Print column dtypes
for col in columns_list:
    print(f'Columns: {col}, dtype: {journeys_df[col].dtypes}')

# Save file to CSV
print(f'Saving to CSV')
journeys_df.to_csv('stations.csv')
print(f'Time elapsed: {time() - t0:.2f} seconds')
