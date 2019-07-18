#----- Author: Nick Konz -----#

from bokeh.layouts import column, row, widgetbox
from bokeh.models import CustomJS, ColumnDataSource, Slider, Button, BoxZoomTool, Range1d
from bokeh.plotting import Figure, output_file, show, save
from bokeh.transform import linear_cmap

import numpy as np

output_file("bargraphSmash.html")


#example data for testing only
#players = ['BEEF', 'Thomato', 'postmabone', 'curt', 'LONG']
#counts = [75, 56, 69, 24, 101]

players = []
counts = []

src = ColumnDataSource(data=dict(players = players, counts = counts))

# sorting the bars means sorting the range factors
#sorted_players = sorted(players, key=lambda x: counts[players.index(x)])

p = Figure(plot_height = 400, plot_width = 600, x_range=players, 
           x_axis_label = 'player name',
           y_axis_label = '',
           title="Stats per player", tools = "xpan, xwheel_zoom",
           active_scroll='xwheel_zoom', active_drag = "xpan")

p.xaxis.axis_label_text_font_size = "14pt"
p.yaxis.axis_label_text_font_size = "14pt"

#try:
#    p.vbar(source = src, x='players', top='wincounts', width=0.9, fill_color=linear_cmap('wincounts', 'Viridis256', 0, max(wincounts)))
#except ValueError: #this just happens because on page load, data isn't loaded so the plotting gets grumpy
#    p.vbar(source = src, x='players', top='wincounts', width=0.9, fill_color=linear_cmap('wincounts', 'Viridis256', 0, 0))

p.vbar(source = src, x='players', top='counts', width=0.9)
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

    axis.axis_label = "Win Count";

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

    axis.axis_label = "KO Count";

    src.change.emit();
    p.change.emit();   
""")


# layout

buttonWin = Button(label = "Show Win Count (Default)", button_type = "primary")
buttonWin.js_on_click(callbackWin)

buttonKO = Button(label = "Show KO Count", button_type = "primary")
buttonKO.js_on_click(callbackKO)

p.xgrid.grid_line_color = None
p.y_range.start = 0

buttons = row(buttonWin, buttonKO)

layout = column(buttons, p)

#show(layout)
save(layout)