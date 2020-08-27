# /usr/bin/env python3

from bokeh.plotting import figure
from bokeh.models import LinearColorMapper, HoverTool, Div, ColorBar
from bokeh.tile_providers import get_provider
from bokeh.layouts import layout
from bokeh.io import curdoc
from bokeh.core.validation import silence
from bokeh.core.validation.warnings import MISSING_RENDERERS
from coordinate_transformation.to_web_merc import toWebMerc
from helper_functions.helper_funcs import hour_inputs, slider_input, source, update, animate, button

# silence unnecessary warnings for color_bar_plot
silence(MISSING_RENDERERS, True)

# bokeh output HTML file
tile_provider = get_provider('CARTODBPOSITRON')

# base HTML web page for Bokeh visualization
homepage = Div(text=open('traffic_plot.html').read(), width=800)

# London longitude and latitude GPS coordinate range
london_x_range = (-0.25, 0.015)
london_y_range = (51.436, 51.568)
merc_lower_left = toWebMerc(london_x_range[0], london_y_range[0])
merc_upper_right = toWebMerc(london_x_range[1], london_y_range[1])

# tooltips on dats point hoverover
tooltips = [('Total traffic', '@sum_flux{0,0.00}'),
            ('Net flux', '@diff_flux{0,0.00}'),
            ('Station name', '@station_name{safe}')]

# icons in tool bar
toolbox = ['pan', 'wheel_zoom', 'box_zoom', 'save', 'reset']

# update data to show initial data points at 00:00:00 on the plot
update()

# range bounds supplied in web mercator coordinates
plot = figure(x_range=(merc_lower_left[0], merc_upper_right[0]),
              y_range=(merc_lower_left[1], merc_upper_right[1]),
              x_axis_type="mercator",
              y_axis_type="mercator",
              x_axis_label='Longitude',
              y_axis_label='Latitude',
              title='Average Weekday Public Bicycle Traffic in London UK',
              toolbar_location='below',
              tools=toolbox,
              toolbar_sticky=False,
              width=950,
              height=750)
plot.add_tile(tile_provider)
plot.add_tools(HoverTool(tooltips=tooltips))

# color bar
color_mapper = LinearColorMapper(palette='Turbo256',
                                 low=-3e1,
                                 high=3e1)

color_bar = ColorBar(color_mapper=color_mapper,
                     label_standoff=12,
                     border_line_color=None,
                     title_text_align='left',
                     location=(0, 0))


color_bar_plot = figure(title="Net Traffic Flux",
                        title_location="right",
                        height=750,
                        width=120, 
                        toolbar_location=None,
                        min_border=0,
                        outline_line_color=None)

color_bar_plot.add_layout(color_bar, 'right')
color_bar_plot.title.align = "center"

# data points
plot.circle(x='long',
            y='lat',
            size='sum_flux',
            fill_color={'field': 'diff_flux', 'transform': color_mapper},
            fill_alpha=0.5,
            source=source)

# main plot layout
plot_layout = layout([[homepage],
                      [plot, color_bar_plot],
                      [hour_inputs, slider_input, button]])

# attaches layout to current document
curdoc().add_root(plot_layout)
curdoc().title = 'Bicycle Traffic in London UK'
