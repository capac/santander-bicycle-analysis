from pathlib import Path
from itertools import islice
import warnings
import os
import re
import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.tile_providers import get_provider
from pyproj import Proj, transform

# ignore chained assignment warnings
# pd.set_option('mode.chained_assignment', None)
# pd.options.display.max_columns = None

# ignore FutureWarning and DeprecationWarning messages
[warnings.filterwarnings("ignore", category=alert)
 for alert in [FutureWarning, DeprecationWarning]]

# load data
home = os.environ['HOME']
data_dir = Path(home) / 'Programming/data/s2ds-project-data'
avg_weekdays_sum_diff_df = pd.read_csv(
    data_dir / 'Average_Weekday_Sum_Difference.csv', index_col='Date')

# bokeh output
output_file("tile.html")
tile_provider = get_provider('CARTODBPOSITRON')

# coordinate transformation
inProj = Proj(init='epsg:4326')
outProj = Proj(init='epsg:3857')


def toWebMerc(long, lat):
    xwm, ywm = transform(inProj, outProj, long, lat)
    return (xwm, ywm)


station_id_list = [re.search(r'(?<=Latitude_)\d{1,3}', file).group(
    0) for file in avg_weekdays_sum_diff_df.filter(regex=r'^Latitude', axis=1).columns]
lat_long_df = avg_weekdays_sum_diff_df.filter(
    regex=r'^Latitude|^Longitude', axis=1)

station_id_index_list = [i for i, item in enumerate(
    avg_weekdays_sum_diff_df.columns.to_list()) if re.search(r'^Latitude', item)]

for station_id_index, station_id in zip(station_id_index_list, station_id_list):
    selection_df = lat_long_df.filter(regex=rf'_{station_id}$', axis=1)
    mercLong, mercLat = toWebMerc(
        selection_df.iloc[0, 1], selection_df.iloc[0, 0])
    avg_weekdays_sum_diff_df.insert(station_id_index, column='Merc_Lat_' +
                                    station_id, value=[mercLat for x in range(selection_df.shape[0])])
    avg_weekdays_sum_diff_df.insert(station_id_index+1, column='Merc_Long_' +
                                    station_id, value=[mercLong for x in range(selection_df.shape[0])])
    avg_weekdays_sum_diff_df.drop(
        ['Latitude_'+station_id, 'Longitude_'+station_id], axis=1, inplace=True)


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
    p.circle(x='long', y='lat', size='sum_flux', fill_color='royalblue', fill_alpha=0.5, source=flux_source)
    tooltips = [('Total traffic', '@sum_flux')]
    break

p.add_tools(HoverTool(tooltips=tooltips))
show(p)
