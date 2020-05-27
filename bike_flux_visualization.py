from pathlib import Path
from itertools import islice
import warnings
import os
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool
from bokeh.tile_providers import get_provider
from pyproj import Proj, transform

# ignore FutureWarning messages
warnings.filterwarnings("ignore", category=FutureWarning)

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


def toWebMerc(lon, lat):
    xwm, ywm = transform(inProj, outProj, lon, lat)
    return (xwm, ywm)


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
        map(tuple, zip(*station_chunk(row[1:61], 4))))
    bike_flux_list.append(
        {row[0]: {'sum': sum_flux, 'diff': diff_flux,
                  'lat': lat, 'long': long}})


# print(bike_flux_list[32])
time_interval_list = [
    time for interval_data in bike_flux_list for time in interval_data.keys()]
# print(time_interval_list)

for i, time in enumerate(time_interval_list):
    coord_list_length = len(bike_flux_list[i][time]['lat'])
    for j in range(coord_list_length):
        long, lat = toWebMerc(bike_flux_list[i][time]['long'][j],
                              bike_flux_list[i][time]['lat'][j])
        p.circle(x=[long], y=[lat], size=bike_flux_list[i][time]
                 ['sum'][j]/3e1, fill_color='royalblue', fill_alpha=0.5)
    # flux_col = ColumnDataSource(bike_flux_list[i][time])
    tooltips = [('Total traffic', '''@{bike_flux_list[i][time]['sum']}''')]
    break

p.add_tools(HoverTool(tooltips=tooltips))
show(p)
