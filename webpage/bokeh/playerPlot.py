#----- Author: Nick Konz -----#

from bokeh.layouts import column, row, widgetbox, gridplot
from bokeh.models import CustomJS, ColumnDataSource, Dropdown, Slider, Button, BoxZoomTool, Range1d, BoxSelectTool, LassoSelectTool, Select, CheckboxGroup
from bokeh.plotting import Figure, output_file, show, save, curdoc
from bokeh.transform import linear_cmap
from bokeh.models.tools import HoverTool
from bokeh.palettes import Viridis256
from bokeh.events import MouseEnter

import numpy as np

output_file("playerPlot.html")

x = []
y = []
players = []

srcData = ColumnDataSource(data=dict(x = x, y = y, players = players))


# create the scatter plot
TOOLS="pan,wheel_zoom,reset"

p = Figure(tools=TOOLS, plot_width=600, plot_height=600, min_border=10, min_border_left=50,
           toolbar_location="above",
           title="Player Data",
           active_scroll='wheel_zoom', 
           active_drag = "pan"
           )
p.background_fill_color = "#fafafa"

r = p.scatter(source = srcData, x='x', y='y', size=10, color="red", alpha=0.6)

p.add_tools(HoverTool(tooltips=[("Player name", "@players"), ("x", "@x"), ("y", "@y")]))


#JS callbacks

callbackPlot = CustomJS(args=dict(srcData=srcData, p=p, xaxis=p.xaxis[0], yaxis=p.yaxis[0]), code="""
    p.reset.emit();

    let result = createPlayerPlotData();

    let players_result = result[0];
    let x_result = result[1];
    let y_result = result[2];

    let players = [];
    let x = [];
    let y = []; 
    
    var dataData = srcData.data;

    dataData['players'] = [];
    dataData['x'] = [];
    dataData['y'] = [];

    players = dataData['players'];
    x = dataData['x'];
    y = dataData['y'];

    for (let i = 0; i < x_result.length; i++){
        players[i] = players_result[i];
        x[i] = x_result[i];
        y[i] = y_result[i];
    }

    dataData['players'] = players;
    dataData['x'] = x;
    dataData['y'] = y;

    xaxis.axis_label = playerPlotAxes[0];
    yaxis.axis_label = playerPlotAxes[1];

    srcData.change.emit();   
    p.change.emit();
""")

callbackUpdateHAxis = CustomJS(code="""
    playerPlotAxes[0] = this.value;
""")

callbackUpdateVAxis = CustomJS(code="""
    playerPlotAxes[1] = this.value;
""")

#widgets


hOptions = ["KO Counts per Player", "Win Counts per Player", "Damage Done per Player"]
vOptions = ["KO Counts per Player", "Win Counts per Player", "Damage Done per Player"]

hSelect = Select(title =    "Horizontal Data", 
                 options =  hOptions,   #list of options
                 value =   "KO Counts per Player" #default value  
                 )

vSelect = Select(title =    "Vertical Data", 
                 options =  vOptions,   #list of options
                 value =   "Win Counts per Player" #default value  
                 )

#layout

widgets = row(hSelect, vSelect)
layout = column(widgets, p)

curdoc().add_root(layout)
curdoc().title = "Player Plot"

#interactivity

p.js_on_event(MouseEnter, callbackPlot) #plot whichever axes are currently selected

hSelect.js_on_change('value', callbackUpdateHAxis)
vSelect.js_on_change('value', callbackUpdateVAxis)

hSelect.js_on_change('value', callbackPlot)
vSelect.js_on_change('value', callbackPlot)

#show(layout)
save(layout)