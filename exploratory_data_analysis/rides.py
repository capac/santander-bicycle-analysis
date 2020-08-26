# /usr/bin/env python3

from matplotlib.pyplot import minorticks_off
import pandas as pd
import numpy as np
import os
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from pathlib import Path
from time import time

t0 = time()
home = os.environ['HOME']
data_dir = Path(home) / 'Programming/data/s2ds-project-data'

# connect to SQLite DB on laptop
flow_journey_db = data_dir / 'journey-data_2019-2020.db'
con = sqlite3.connect(flow_journey_db)
query = '''SELECT * FROM rides_count'''
cursor = con.execute(query)
journey_results = cursor.fetchall()
bike_df = pd.DataFrame(journey_results, columns=[
                       x[0] for x in cursor.description])

# date index
dates = pd.date_range(
    start=bike_df['Date'].iloc[0], end=bike_df['Date'].iloc[-1], freq='1D')

# convert to datetime and filter on date index
bike_df['Date'] = pd.to_datetime(bike_df['Date'], format=r'%Y-%m-%d')
filter_ = bike_df['Date'].isin(dates)

# scatter plot
days = bike_df['Date'].loc[filter_]
rides = bike_df['Num_Rides'].loc[filter_]
fig, axes = plt.subplots(figsize=(8, 6))
axes.scatter(days, rides/1e4, alpha=0.6, marker='o', s=40,
             color='dodgerblue', edgecolor='k')

yaxis_limits = axes.yaxis.get_data_interval()
yaxis_limits = [yaxis_limits[0]-0.25, yaxis_limits[1]+0.25]

# London tube strikes, in tuples with years, months and days
# complete_london_tube_strike_list = [(2012, 12, 26), (2014, 2, 4), (2014, 2, 5), (2014, 2, 6), (2014, 4, 28), (2014, 4, 29), (2014, 4, 30), (2014, 8, 22), (2014, 8, 23), (2014, 12, 1), (2015, 7, 8), (2015, 7, 9), (2015, 8, 5), (2015, 8, 6)]
# for dt in [(2012, 12, 26), (2014, 2, 6), (2014, 4, 30), (2014, 8, 23), (2014, 12, 1), (2015, 7, 9), (2015, 8, 6)]:
#     axes.vlines(datetime(*dt), yaxis_limits[0], yaxis_limits[1], linestyle=':')
#     axes.annotate('Tube strike', xy=(datetime(*dt)-timedelta(20), axes.yaxis.get_data_interval()
#                                      [0] + 5), ha='left', va='bottom', rotation=90, size=7, color='k')
# print(axes.yaxis.__dir__())

# format the ticks
months = mdates.MonthLocator()  # every month
weeks = mdates.WeekdayLocator()  # every weekday

# draw ticks
month_fmt = mdates.DateFormatter(r'%Y-%m')
axes.xaxis.set_major_formatter(month_fmt)
axes.xaxis.set_minor_locator(weeks)
axes.xaxis_date()

# round to nearest month
datemin = np.datetime64(days.iloc[0], 'D')
datemax = np.datetime64(days.iloc[-1], 'D') + np.timedelta64(1, 'D')
axes.set_xlim(datemin, datemax)
axes.set_ylim(yaxis_limits[0], yaxis_limits[1])

# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
axes.set_xticks([], minor=True)
fig.autofmt_xdate()

# set axes labels
axes.set_xlabel('Dates', fontsize=12)
axes.set_ylabel('Rides per day (in units of 10,000)', fontsize=12)
axes.set_title(
    f'Total number of rides per day from {days.min():%Y-%m-%d} to {days.max():%Y-%m-%d}', fontsize=14)
# fig.tight_layout()
# axes.grid(linestyle=':')
print(f'Time elapsed: {time() - t0:.2f} seconds')
plt.show()
