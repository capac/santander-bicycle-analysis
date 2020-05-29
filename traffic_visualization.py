# /usr/bin/env python3

from pathlib import Path
from itertools import islice
import os
import re
import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.tile_providers import get_provider
from coordinate_transformation.to_web_merc import toWebMerc


# load data
home = os.environ['HOME']
data_dir = Path(home) / 'Programming/data/s2ds-project-data'
avg_weekdays_sum_diff_df = pd.read_csv(
    data_dir / 'avg_weekday_sum_diff_merc_coord.csv', index_col='Date')

# bokeh output
output_file("traffic_visualization.html")
tile_provider = get_provider('CARTODBPOSITRON')


# London GPS coordinate range
london_x_range = (-0.25, 0.015)
london_y_range = (51.436, 51.568)
merc_lower_left = toWebMerc(london_x_range[0], london_y_range[0])
merc_upper_right = toWebMerc(london_x_range[1], london_y_range[1])

# range bounds supplied in web mercator coordinates
p = figure(x_range=(merc_lower_left[0], merc_upper_right[0]),
           y_range=(merc_lower_left[1], merc_upper_right[1]),
           x_axis_type="mercator", y_axis_type="mercator", width=1000,
           height=800)
p.add_tile(tile_provider)


# group elements of list in tuples of four elements each
def station_chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


bike_flux_list = []
for row in avg_weekdays_sum_diff_df.itertuples():
    sum_flux, diff_flux, lat, long = list(
        map(tuple, zip(*station_chunk(row[1:], 4))))
    sum_flux = list(np.array(sum_flux)/3e1)
    bike_flux_list.append(
        {row[0]: {'sum_flux': sum_flux, 'diff': diff_flux,
                  'lat': lat, 'long': long}})


time_interval_list = [
    time for interval_data in bike_flux_list for time in interval_data.keys()]

for i, time in enumerate(time_interval_list):
    # print(bike_flux_list[i][time])
    # print(type(bike_flux_list[i][time]))
    flux_source = ColumnDataSource(data=bike_flux_list[i][time])
    p.circle(x='long', y='lat', size='sum_flux',
             fill_color='royalblue', fill_alpha=0.5, source=flux_source)
    tooltips = [('Total traffic', '@sum_flux')]
    break

p.add_tools(HoverTool(tooltips=tooltips))
show(p)
