#----- Author: Nick Konz -----#

from bokeh.layouts import column, row, widgetbox
from bokeh.models import CustomJS, ColumnDataSource, Slider, Button, BoxZoomTool, Range1d
from bokeh.plotting import Figure, output_file, show, save
from bokeh.transform import linear_cmap
from bokeh.models.tools import HoverTool
from bokeh.palettes import Viridis256
from bokeh.events import MouseEnter

import numpy as np

output_file("scatterSmash.html")

#initial plot


#KOs = [4, 5, 7]
#wins = [1, 2, 4]
#players = ['BEEF', 'Thomato', 'postmabone']

KOs = []
wins = []
players = []

src = ColumnDataSource(data=dict(KOs = KOs, wins = wins, players = players))

p = Figure(plot_height = 600, plot_width = 600, 
           x_axis_label = 'KO count (per player)',
           y_axis_label = 'Win count (per player)',
           title="KO count vs. Win count per player", tools = "pan, wheel_zoom",
           active_scroll='wheel_zoom', active_drag = "pan")

p.title.text_font_size = "18pt"
p.xaxis.axis_label_text_font_size = "12pt"
p.yaxis.axis_label_text_font_size = "12pt"

p.circle('KOs', 'wins', source=src, size=10, color="red", alpha=0.7)

# tools
p.add_tools(HoverTool(tooltips=[("Player name", "@players"), ("KOs", "@KOs"), ("Wins", "@wins")]))


# JS callbacks

callbackKOWin = CustomJS(args=dict(src=src, p=p), code="""

    p.reset.emit();

    let result = createWinBars();

    let players_result = result[0];
    let wins_result = result[1];

    result = createKOBars();
    let KOs_result = result[1];

    players = [];
    KOs = [];
    wins = [];

    var data = src.data;

    data['players'] = [];
    data['wins'] = [];
    data['KOs'] = [];

    players = data['players']
    KOs = data['KOs']
    wins = data['wins']


    for (let i = 0; i < players_result.length; i++){
        players[i] = players_result[i];
        wins[i] = wins_result[i];
        KOs[i] = KOs_result[i];
    }

    console.log(players,wins,KOs)

    data['players'] = players;
    data['wins'] = wins;
    data['KOs'] = KOs;

    src.change.emit();   
    p.change.emit();
""")

# layout & callbacks

p.js_on_event(MouseEnter, callbackKOWin)

buttonKOWin = Button(label = "KO counts vs. Win counts per player (default)", button_type = "primary")
buttonKOWin.js_on_click(callbackKOWin)

#p.xgrid.grid_line_color = None
#p.y_range.start = 0

buttons = row(buttonKOWin)

layout = column(buttons, p)

#show(layout)
save(layout)