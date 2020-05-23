import pandas as pd
import os
from pathlib import Path
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.tile_providers import get_provider

# load data
home = os.environ['HOME']
data_dir = Path(home) / 'Programming/data/s2ds-project-data'
avg_weekdays_sum_diff_df = pd.read_csv(data_dir / 'Average_Weekday_Sum_Difference.csv')

# bokeh output
output_file("tile.html")
tile_provider = get_provider('OSM')

# range bounds supplied in web mercator coordinates
p = figure(x_range=(-89055.59, 40075.02), y_range=(6667414.22, 6749655.34), x_axis_type="mercator", y_axis_type="mercator", width=1000, height=800)
p.add_tile(tile_provider)

show(p)
