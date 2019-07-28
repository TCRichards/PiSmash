#----- Author: Nick Konz -----#

from bokeh.layouts import column, row, widgetbox
from bokeh.models import CustomJS, ColumnDataSource, Slider, Button, BoxZoomTool, Range1d, Select
from bokeh.plotting import Figure, output_file, show, save, curdoc
from bokeh.transform import linear_cmap
from bokeh.models.tools import HoverTool
from bokeh.palettes import Viridis256
from bokeh.events import MouseEnter

import numpy as np

output_file("bargraphSmash.html")

#initial plot

players = []
counts = []

src = ColumnDataSource(data=dict(players = players, counts = counts))

p = Figure(plot_height = 400, plot_width = 600, x_range=players, 
           x_axis_label = 'Player name',
           y_axis_label = '',
           title="Stats Per Player", 
           tools = "xpan, xwheel_zoom, reset",
           active_scroll='xwheel_zoom', active_drag = "xpan")

p.title.text_font_size = "18pt"
p.xaxis.axis_label_text_font_size = "12pt"
p.yaxis.axis_label_text_font_size = "12pt"


#try:
#    p.vbar(source = src, x='players', top='counts', width=0.9, fill_color=linear_cmap('counts', 'Viridis256', 0, max(counts)))
#except ValueError: #this just happens because on page load, data isn't loaded so the plotting gets grumpy
#    p.vbar(source = src, x='players', top='counts', width=0.9, fill_color=linear_cmap('counts', 'Viridis256', 0, 0))

p.vbar(source = src, x='players', top='counts', width=0.9)

# tools
p.add_tools(HoverTool(tooltips=[("Player name", "@players"), ("Count", "@counts")]))


# JS callbacks

callbackPlot = CustomJS(args=dict(src=src, p=p, x_range=p.x_range, axis=p.yaxis[0]), code="""

    p.reset.emit();

    let result = createBars();
    let players_result = result[0];
    let counts_result = result[1];

    x_range.factors = players_result;

    players = [];
    counts = [];

    var data = src.data;

    data['players'] = [];
    data['counts'] = [];

    players = data['players']
    counts = data['counts']

    for (let i = 0; i < players_result.length; i++){
        players[i] = players_result[i];
        counts[i] = counts_result[i];
    }

    data['players'] = players;
    data['counts'] = counts;

    axis.axis_label = barGraphAxis;

    src.change.emit();   
    p.change.emit();
""")

callbackAxis = CustomJS(code="""
    barGraphAxis = this.value;
""")

# layout
options = ["KO Counts per Player", "Win Counts per Player", "Damage Done per Player"]

select = Select(title =    "Data Category", 
                 options =  options,   #list of options
                 value =   "KO Counts per Player" #default value  
                 )

p.xgrid.grid_line_color = None
p.y_range.start = 0

widgets = row(select)

layout = column(widgets, p)

curdoc().add_root(layout)
curdoc().title = "Bar Graph"

#interactivity

p.js_on_event(MouseEnter, callbackPlot) #plot whichever axes are currently selected

select.js_on_change('value', callbackAxis)
select.js_on_change('value', callbackPlot)

#show(layout)
save(layout)