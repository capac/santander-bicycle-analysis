# /usr/bin/env python3

from pathlib import Path
from itertools import islice
import os
import numpy as np
import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, Select


# load data from CSV file
home = os.environ['HOME']
data_dir = Path(home) / 'Programming/data/s2ds-project-data'
avg_weekdays_sum_diff_df = pd.read_csv(data_dir /
                                       'avg_weekday_sum_diff_merc_coord.csv',
                                       index_col='Date')


# group elements of list in tuples of four elements each for
# sum, difference, latitude and longitude (in Mercator coords)
def station_chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


# return a list of dictionaries, each one of which has time as key and
# a dictionary as value with sum_flux, diff_flux, lat and long values
def bike_flux(flux_df):
    bike_flux_list = []
    for row in flux_df.itertuples():
        sum_flux, diff_flux, lat, long = list(
            map(tuple, zip(*station_chunk(row[1:], 4))))
        sum_flux = np.array(sum_flux)/1e2
        diff_flux = np.array(diff_flux)/1e2
        bike_flux_list.append(
            {row[0]: {'sum_flux': sum_flux, 'diff_flux': diff_flux,
                      'lat': lat, 'long': long}})
    return bike_flux_list


# time interval dictionary with hour interval as
# key and list index for data dictionary and value
bike_flux_list = bike_flux(avg_weekdays_sum_diff_df)
time_interval_dict = {time_interval: bike_flux_list.index(interval_data) for interval_data
                      in bike_flux_list for time_interval in interval_data.keys()}

# drop down hour selector
hour_interval_selector = Select(title='Hour interval',
                                options=list(time_interval_dict.keys()),
                                value='00:00:00')
hour_interval_selector.on_change('value', lambda attr, old, new: update())

# minimum traffic flux slider
flux_slider = Slider(start=0,
                     end=30000,
                     value=0,
                     step=10,
                     title='Minimum Total Traffic (in units of hundreds)')
flux_slider.on_change('value', lambda attr, old, new: update())


def select_time():
    selected = bike_flux_list
    hour_interval = time_interval_dict[hour_interval_selector.value]
    min_flux = flux_slider.value/1e2

    selected_df = pd.DataFrame(
        selected[hour_interval][hour_interval_selector.value])
    print(selected_df['sum_flux'])
    selected_df = selected_df[selected_df['sum_flux'] >= min_flux]

    print('Hour interval =', hour_interval)
    print('Min flux =', min_flux)

    return selected_df


# source data dict
source = ColumnDataSource(
    data=dict(long=[], lat=[], sum_flux=[], diff_flux=[]))


def update():
    df = select_time()

    source.data = dict(
        long=df['long'],
        lat=df['lat'],
        sum_flux=df['sum_flux'],
        diff_flux=df['diff_flux']
    )
