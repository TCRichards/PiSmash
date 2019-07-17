#----- Author: Nick Konz -----#

from bokeh.layouts import column, row, widgetbox
from bokeh.models import CustomJS, ColumnDataSource, Slider, Button, BoxZoomTool, Range1d
from bokeh.plotting import figure, output_file, show, save
from bokeh.transform import linear_cmap

import numpy as np

output_file("bargraphSmash.html")


#example data for testing only
players = ['BEEF', 'Thomato', 'postmabone', 'curt']
wincounts = [75, 56, 69, 24]

src = ColumnDataSource(data=dict(players = players, wincounts = wincounts))

# sorting the bars means sorting the range factors
sorted_players = sorted(players, key=lambda x: wincounts[players.index(x)])

p = figure(plot_height = 400, plot_width = 600, x_range=sorted_players, 
           x_axis_label = 'player name',
           y_axis_label = 'Win count',
           title="Win count per player", tools = "xpan, xwheel_zoom",
           active_scroll='xwheel_zoom', active_drag = "xpan")

p.vbar(source = src, x='players', top='wincounts', width=0.9, fill_color=linear_cmap('wincounts', 'Viridis256', 0, max(wincounts)))

# JS callbacks

callback_plot = CustomJS(args=dict(src=src, p=p, axis=p.xaxis[0], x_range=p.x_range), code="""


   
""")


# layout
button_plot = Button(label = "Generate Plot", button_type = "primary")

button_plot.js_on_click(callback_plot)

p.xgrid.grid_line_color = None
p.y_range.start = 0

buttons = row(button_plot)

layout = column(buttons, p)

show(layout)
save(layout)