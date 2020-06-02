# /usr/bin/env python3

from bokeh.models import ColumnDataSource, LinearColorMapper
from bokeh.plotting import figure, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Div, LinearColorMapper
from bokeh.tile_providers import get_provider
from bokeh.layouts import layout, widgetbox
from bokeh.io import curdoc
from coordinate_transformation.to_web_merc import toWebMerc
from helper_functions.helper_funcs import update, flux_slider, hour_interval_selector, source
import os

# bokeh output HTML file
tile_provider = get_provider('CARTODBPOSITRON')

# base HTML web page which contains Bokeh visualization plot
homepage = Div(text=open(os.path.join(os.getcwd(),
                                      'traffic_visualization.html')).read(), width=800)


# London GPS coordinate range
london_x_range = (-0.25, 0.015)
london_y_range = (51.436, 51.568)
merc_lower_left = toWebMerc(london_x_range[0], london_y_range[0])
merc_upper_right = toWebMerc(london_x_range[1], london_y_range[1])


tooltips = [('Total traffic', '@sum_flux'), ('Net flux', '@diff_flux')]

# range bounds supplied in web mercator coordinates
p = figure(x_range=(merc_lower_left[0], merc_upper_right[0]),
           y_range=(merc_lower_left[1], merc_upper_right[1]),
           x_axis_type="mercator",
           y_axis_type="mercator",
           title='Average Daily Public Bicycle Traffic in London UK',
           toolbar_location=None,
           tooltips=tooltips,
           width=1000,
           height=800)
p.add_tile(tile_provider)
p.add_tools(HoverTool(tooltips=tooltips))

color_mapper = LinearColorMapper(palette='Turbo256', low=-5e2, high=5e2)

p.circle(x='long',
         y='lat',
         size='sum_flux',
         fill_color={'field': 'diff_flux', 'transform': color_mapper},
         fill_alpha=0.5,
         source=source)

inputs=widgetbox(hour_interval_selector, flux_slider)

plot_layout=layout([[homepage], [inputs], [p]])

curdoc().add_root(plot_layout)
curdoc().title='Bicycle Traffic in London UK'


# TOOLS = 'pan,wheel_zoom,box_zoom,reset'
# p = figure(tools=TOOLS)

# x = np.linspace(-10, 10, 200)
# y = -x**2

# data_source = ColumnDataSource({'x': x, 'y': y})

# color_mapper = LinearColorMapper(palette='Magma256', low=min(y), high=max(y))

# specify that we want to map the colors to the y values,
# this could be replaced with a list of colors
# p.scatter(x, y, color={'field': 'y', 'transform': color_mapper})
