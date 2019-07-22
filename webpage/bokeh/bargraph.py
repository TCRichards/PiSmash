#----- Author: Nick Konz -----#

from bokeh.layouts import column, row, widgetbox
from bokeh.models import CustomJS, ColumnDataSource, Slider, Button, BoxZoomTool, Range1d
from bokeh.plotting import Figure, output_file, show, save
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
           title="Stats Per Player", tools = "xpan, xwheel_zoom",
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

callbackWin = CustomJS(args=dict(src=src, p=p, x_range=p.x_range, axis=p.yaxis[0]), code="""

    p.reset.emit();

    let result = createWinBars();
    let players_result = result[0];
    let wincounts_result = result[1];

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
        counts[i] = wincounts_result[i];
    }

    data['players'] = players;
    data['counts'] = counts;

    axis.axis_label = "Win count";

    src.change.emit();   
    p.change.emit();
""")

callbackKO = CustomJS(args=dict(src=src, p=p, x_range=p.x_range, axis=p.yaxis[0]), code="""

    p.reset.emit();

    let result = createKOBars();
    let players_result = result[0];
    let KOcounts_result = result[1];

    x_range.factors = players_result;

    var data = src.data;

    data['players'] = [];
    data['counts'] = [];

    players = data['players']
    counts = data['counts']

    for (let i = 0; i < players_result.length; i++){
        players[i] = players_result[i];
        counts[i] = KOcounts_result[i];
    }

    data['players'] = players;
    data['counts'] = counts;

    axis.axis_label = "KO count";

    src.change.emit();
    p.change.emit();   

""")

callbackDamPerc = CustomJS(args=dict(src=src, p=p, x_range=p.x_range, axis=p.yaxis[0]), code="""

    p.reset.emit();

    let result = createDamPercBars();
    let players_result = result[0];
    let damPercCounts_result = result[1];

    x_range.factors = players_result;

    var data = src.data;

    data['players'] = [];
    data['counts'] = [];

    players = data['players']
    counts = data['counts']

    for (let i = 0; i < players_result.length; i++){
        players[i] = players_result[i];
        counts[i] = damPercCounts_result[i];
    }

    data['players'] = players;
    data['counts'] = counts;

    axis.axis_label = "Total damage percentage";

    src.change.emit();
    p.change.emit();   

""")

# layout & callback setup

p.js_on_event(MouseEnter, callbackWin)

buttonWin = Button(label = "Show Win Count (default)", button_type = "primary")
buttonWin.js_on_click(callbackWin)

buttonKO = Button(label = "Show KO Count", button_type = "primary")
buttonKO.js_on_click(callbackKO)

buttonDamPerc = Button(label = "Show Total Damage Percentages", button_type = "primary")
buttonDamPerc.js_on_click(callbackDamPerc)

p.xgrid.grid_line_color = None
p.y_range.start = 0

buttons = column(buttonWin, buttonKO, buttonDamPerc)

layout = row(buttons, p)

#show(layout)
save(layout)