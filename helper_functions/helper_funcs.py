# /usr/bin/env python3

from pathlib import Path
from itertools import islice
import os
import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, Button
from bokeh.models.widgets import Slider, Select
from bokeh.layouts import layout, widgetbox
from bokeh.io import curdoc


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


# scale factor for scale visualization of data points
scale_factor = 1e2

# return a list of dictionaries, each one of which has time as key and
# a dictionary as value with sum_flux, diff_flux, lat and long values


def bike_flux(flux_df):
    bike_flux_list = []
    for row in flux_df.itertuples():
        sum_flux, diff_flux, lat, long = list(
            map(tuple, zip(*station_chunk(row[1:], 4))))
        sum_flux = np.array(sum_flux)/scale_factor
        diff_flux = np.array(diff_flux)/scale_factor
        bike_flux_list.append(
            {row[0]: {'sum_flux': sum_flux, 'diff_flux': diff_flux,
                      'lat': lat, 'long': long}})
    return bike_flux_list


# time interval dictionary with hour interval as
# key and list index for data dictionary and value
bike_flux_list = bike_flux(avg_weekdays_sum_diff_df)
time_interval_dict = {time_interval: bike_flux_list.index(interval_data) for interval_data
                      in bike_flux_list for time_interval in interval_data.keys()}


def select_time():
    selected = bike_flux_list
    hour_interval = time_interval_dict[hour_interval_selector.value]
    min_flux = flux_slider.value/scale_factor

    selected_df = pd.DataFrame(
        selected[hour_interval][hour_interval_selector.value])
    # print(selected_df['sum_flux'])
    selected_df = selected_df[selected_df['sum_flux'] >= min_flux]

    # print('Hour interval =', hour_interval)
    # print('Min flux =', min_flux)

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


def animate_update():
    time_interval_list = list(time_interval_dict.keys())
    next_time_interval = time_interval_list[time_interval_list.index(
        hour_interval_selector.value) + 1]
    if next_time_interval == time_interval_list[-1]:
        next_time_interval = time_interval_list[0]
    hour_interval_selector.value = next_time_interval


callback_id = None


def animate():
    global callback_id
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        callback_id = curdoc().add_periodic_callback(animate_update, 350)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(callback_id)


# drop down hour selector
hour_interval_selector = Select(title='Hour interval',
                                options=list(time_interval_dict.keys()),
                                value='00:00:00')
hour_interval_selector.on_change('value', lambda attr, old, new: update())

# minimum traffic flux slider
flux_slider = Slider(start=0,
                     end=40000,
                     value=0,
                     step=10,
                     width=100,
                     align='start',
                     title='Lower Limit to Traffic Flux (in units of hundreds)')
flux_slider.on_change('value', lambda attr, old, new: update())

# hourly drop down and minimum flux selector
hour_inputs = widgetbox(hour_interval_selector, sizing_mode='scale_width')
slider_input = widgetbox(flux_slider, sizing_mode='scale_width')

# video time lapse button
button = Button(label='► Play',
                width=60,
                sizing_mode='scale_width',
                name='Traffic Time Lapse',
                align='end')
button.on_click(animate)
