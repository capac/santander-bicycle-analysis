# Import CSV files into PostgreSQL database

import pandas as pd
import os, csv
from pathlib import Path
from time import time

# start time
t0 = time()

# data directory
home = os.environ['HOME']
bike_data_dir = Path(home) / 'Programming/s2ds-project/S2DS2016 Starting Data/bike_data'
bike_files = list(bike_data_dir.glob('**/*.csv'))
print(f'Bicycle data directory: {bike_data_dir}')

# list of column headers
columns_list=['Rental Id', 'Duration', 'Bike Id', 'End Date', 'EndStation Id', 'EndStation Name', 'Start Date', 'StartStation Id', 'StartStation Name']

# Check to see if CSV files all have the same headers
for i, bike_file in enumerate(bike_files):
    with open(bike_file, newline='', encoding='ISO-8859-1') as csvfile:
        reader=list(csv.reader(csvfile))
        if sorted(reader[0]) != sorted(columns_list):
            print(f'Check: {bike_file}')

# Convert datetimes to custom format in each dataframe
tmp_df_list=[]
for i, bike_file in enumerate(bike_files):
    tmp_df=pd.read_csv(bike_file, encoding='ISO-8859-1', low_memory=False)
    for col in ['End Date', 'Start Date']:
        tmp_df[col]=pd.to_datetime(
            tmp_df[col], format=r'%d/%m/%Y %H:%M', errors='raise', exact=False)
    tmp_df_list.append(tmp_df)
    if i % 10 == 0:
        print(f'Number of CSV files processed: {i}')
    print(f'Total number of CSV files: {i}')

# Concatenate dataframes
journeys_df=pd.concat(tmp_df_list, axis=0, ignore_index=True)

# Are the 'Unnamed' columns made up entirely of NANs?
unnamed_cols=['Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11']
for col in unnamed_cols:
    print(f'Column: {col}, NANs: {journeys_df[col].isna().all()}')

# Drop last three Unnamed columns
journeys_df.drop(unnamed_cols, axis=1, inplace=True)

# Ratio of rows that have at least one NAN
print(
    f'Ratio of rows that have at least one NA: {journeys_df.isna().any(axis=1).sum()/journeys_df.isna().all(axis=1).shape[0]:.3f}')

# Drop rows that have at least one NAN
journeys_df.dropna(how='any', inplace=True, axis=0)
print(f'Dropped NANs')

# Remove rows where 'StartStation Id' = 'Tabletop1'
journeys_df=journeys_df.loc[~(journeys_df['StartStation Id'] == 'Tabletop1')]

# Convert dtype from float to int
for col in ['Rental Id', 'Duration', 'Bike Id', 'EndStation Id', 'StartStation Id']:
    journeys_df[col]=journeys_df[col].astype('int32')

# Ratio of rows that have at least one NAN
print(
    f'Ratio of rows that have at least one NA: {journeys_df.isna().any(axis=1).sum()/journeys_df.isna().all(axis=1).shape[0]:.3f}')

# Print column dtypes
for col in columns_list:
    print(f'Columns: {col}, dtype: {journeys_df[col].dtypes}')

# Save file to CSV
print(f'Saving to CSV')
journeys_df.to_sql('journeys.csv')
print(f'Time elapsed: {time() - t0:.2f} seconds')
