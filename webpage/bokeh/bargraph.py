#----- Author: Nick Konz -----#

from bokeh.layouts import column, row, widgetbox
from bokeh.models import CustomJS, ColumnDataSource, Slider, Button, BoxZoomTool, Range1d
from bokeh.plotting import figure, output_file, show, save
from bokeh.transform import linear_cmap

import numpy as np

output_file("bargraphSmash.html")

players = ['BEEF', 'Tomato', 'postmabone', 'curt']
wincounts = [75, 56, 69, 24]

src = ColumnDataSource(data=dict(players = players, wincounts = wincounts))

# sorting the bars means sorting the range factors
sorted_players = sorted(players, key=lambda x: wincounts[players.index(x)])

p = figure(x_range=sorted_players, plot_height=350, title="Win Counts per Player",
           toolbar_location=None, tools="")

p.vbar(source = src, x='players', top='wincounts', width=0.9, fill_color=linear_cmap('wincounts', 'Viridis256', 0, max(wincounts)))

p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)