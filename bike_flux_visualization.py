from pathlib import Path
from itertools import islice
import warnings
import os
import pandas as pd
from bokeh.plotting import figure, output_file, show
# from bokeh.models import ColumnDataSource, HoverTool
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


# range bounds supplied in web mercator coordinates
p = figure(x_range=(-80150.03, 48980.58), y_range=(6667414.22, 6749655.34),
           x_axis_type="mercator", y_axis_type="mercator", width=1000,
           height=800)
p.add_tile(tile_provider)


# group elements of list in tuples of four elements each
def station_chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


time_of_day_df = []
for row in avg_weekdays_sum_diff_df.itertuples():
    sum_flux, diff_flux, lat, long = list(
        map(tuple, zip(*station_chunk(row[1:21], 4))))
    time_of_day_df.append(
        {row[0]: {'sum': sum_flux, 'diff': diff_flux,
                  'lat': lat, 'long': long}})


# print(time_of_day_df[0])
long, lat = toWebMerc(time_of_day_df[0]['00:00:00']['long'][0],
                      time_of_day_df[0]['00:00:00']['lat'][0])
p.circle(x=[long], y=[lat], size=15, fill_color='orange', fill_alpha=0.8)

show(p)
