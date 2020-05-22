import pandas as pd
import os
from pathlib import Path
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool

# load data
home = os.environ['HOME']
data_dir = Path(home) / 'Programming/data/s2ds-project-data'
avg_weekdays_sum_diff_df = pd.read_csv(data_dir / 'Average_Weekday_Sum_Difference.csv')

