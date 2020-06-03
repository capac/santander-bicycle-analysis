# /usr/bin/env python3

from bokeh.plotting import figure
from bokeh.models import LinearColorMapper, HoverTool, Div, ColorBar
from bokeh.tile_providers import get_provider
from bokeh.layouts import layout, widgetbox
from bokeh.io import curdoc
from coordinate_transformation.to_web_merc import toWebMerc
from helper_functions.helper_funcs import flux_slider, hour_interval_selector, source, update

# bokeh output HTML file
tile_provider = get_provider('CARTODBPOSITRON')

# base HTML web page which contains Bokeh visualization plot
homepage = Div(text=open('traffic_visualization.html').read(), width=800)

# London GPS coordinate range
london_x_range = (-0.25, 0.015)
london_y_range = (51.436, 51.568)
merc_lower_left = toWebMerc(london_x_range[0], london_y_range[0])
merc_upper_right = toWebMerc(london_x_range[1], london_y_range[1])

tooltips = [('Total traffic', '@sum_flux{0,0.00}'), ('Net flux', '@diff_flux{0,0.00}')]

# update data to show initial data point on plot
update()

# range bounds supplied in web mercator coordinates
p = figure(x_range=(merc_lower_left[0], merc_upper_right[0]),
           y_range=(merc_lower_left[1], merc_upper_right[1]),
           x_axis_type="mercator",
           y_axis_type="mercator",
           title='Average Daily Public Bicycle Traffic in London UK',
           toolbar_location=None,
           tooltips=tooltips,
           width=950,
           height=750)
p.add_tile(tile_provider)
p.add_tools(HoverTool(tooltips=tooltips))

color_mapper = LinearColorMapper(palette='Turbo256',
                                 low=-6e2,
                                 high=6e2)

color_bar = ColorBar(color_mapper=color_mapper,
                     label_standoff=12,
                     border_line_color=None,
                     location=(0,0))

p.add_layout(color_bar, 'right')

p.circle(x='long',
         y='lat',
         size='sum_flux',
         fill_color={'field': 'diff_flux', 'transform': color_mapper},
         fill_alpha=0.5,
         source=source)

hour_interval_selector_input = widgetbox(hour_interval_selector)
flux_slider_input = widgetbox(flux_slider)

plot_layout = layout([[homepage], [p], [hour_interval_selector_input, flux_slider_input]])


curdoc().add_root(plot_layout)
curdoc().title = 'Bicycle Traffic in London UK'
