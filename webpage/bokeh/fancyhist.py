#----- Author: Nick Konz -----#

from bokeh.layouts import column, row, widgetbox, gridplot
from bokeh.models import CustomJS, ColumnDataSource, Dropdown, Slider, Button, BoxZoomTool, Range1d, BoxSelectTool, LassoSelectTool, Select, CheckboxGroup
from bokeh.plotting import Figure, output_file, show, save, curdoc
from bokeh.transform import linear_cmap
from bokeh.models.tools import HoverTool
from bokeh.palettes import Viridis256
from bokeh.events import MouseEnter

import numpy as np

output_file("fancyhistSmash.html")

x = []
y = []

hhist = []
hzeros = []
hleft = []
hright = []

vhist = []
vzeros = []
vleft = []
vright = []

maxes = [1, 1]

#selection = ["Highest KO Count per Game (normalized)", "Highest Damage Done per Game (normalized)"]

srcData = ColumnDataSource(data=dict(x = x, y = y))
srcHist = ColumnDataSource(data=dict(hhist = hhist, hleft = hleft, hright = hright, hzeros = hzeros, vhist = vhist, vleft = vleft, vright = vright, vzeros = vzeros))
#srcSelection = ColumnDataSource(data=dict(selection = selection))

# create the scatter plot
TOOLS="pan,wheel_zoom,reset"

p = Figure(tools=TOOLS, plot_width=600, plot_height=600, min_border=10, min_border_left=50,
           toolbar_location="above",
           title="Linked Histograms of Game Data",
           active_scroll='wheel_zoom', 
           active_drag = "pan"
           )
p.background_fill_color = "#fafafa"

p.select(BoxSelectTool).select_every_mousemove = False
p.select(LassoSelectTool).select_every_mousemove = False

r = p.scatter(source = srcData, x='x', y='y', size=6, color="#3A5785", alpha=0.6)

p.add_tools(HoverTool(tooltips=[("x", "@x"), ("y", "@y")]))

# create the horizontal histogram

#hhist, hedges = np.histogram(x, bins=20)
#hzeros = np.zeros(len(hedges)-1)
#hmax = max(hhist)*1.1

LINE_ARGS = dict(color="#3A5785", line_color=None)

ph = Figure(toolbar_location=None, plot_width=p.plot_width, plot_height=200, x_range=p.x_range,
            y_range=(-maxes[0], maxes[0]), min_border=10, min_border_left=50, y_axis_location="right")
ph.xgrid.grid_line_color = None
ph.yaxis.major_label_orientation = np.pi/4
ph.background_fill_color = "#fafafa"

ph.quad(source = srcHist, bottom=0, left="hleft", right="hright", top="hhist", color="white", line_color="#3A5785")
hh1 = ph.quad(source = srcHist, bottom=0, left="hleft", right="hright", top="hzeros", alpha=0.5, **LINE_ARGS)
hh2 = ph.quad(source = srcHist, bottom=0, left="hleft", right="hright", top="hzeros", alpha=0.1, **LINE_ARGS)

# create the vertical histogram

#vhist, vedges = np.histogram(y, bins=20)
#vzeros = np.zeros(len(vedges)-1)
#vmax = max(vhist)*1.1

pv = Figure(toolbar_location=None, plot_width=200, plot_height=p.plot_height, x_range=(-maxes[1], maxes[1]),
            y_range=p.y_range, min_border=10, y_axis_location="right")
pv.ygrid.grid_line_color = None
pv.xaxis.major_label_orientation = np.pi/4
pv.background_fill_color = "#fafafa"

pv.quad(source = srcHist, left=0, bottom="vleft", top="vright", right="vhist", color="white", line_color="#3A5785")
vh1 = pv.quad(source = srcHist, left=0, bottom="vleft", top="vright", right="vzeros", alpha=0.5, **LINE_ARGS)
vh2 = pv.quad(source = srcHist, left=0, bottom="vleft", top="vright", right="vzeros", alpha=0.1, **LINE_ARGS)

#JS callbacks

callbackPlot = CustomJS(args=dict(srcData=srcData, srcHist=srcHist, p=p, pv=pv, ph=ph, pvx_range=pv.x_range, phy_range=ph.y_range, xaxis=p.xaxis[0], yaxis=p.yaxis[0]), code="""
    p.reset.emit();
    ph.reset.emit();
    pv.reset.emit();

    let result = createFancyHistData();

    let x_result = result[0][0];
    let y_result = result[0][1];

    let hhist_result = result[1][0];
    let hleft_result = result[1][1];
    let hright_result = result[1][2];

    let vhist_result = result[2][0];
    let vleft_result = result[2][1];
    let vright_result = result[2][2];

    let hzeros_result = new Array(hhist_result.length).fill(0);
    let vzeros_result = new Array(vhist_result.length).fill(0); 

    //console.log(x_result, y_result);
    //console.log(hhist_result, hleft_result, hright_result, hzeros_result);
    //console.log(vhist_result, vleft_result, vright_result, vzeros_result);

    let x = [];
    let y = []; 
    let hhist = []; 
    let hleft = []; 
    let hright = []; 
    let hzeros = []; 
    let vhist = [];
    let vleft = []; 
    let vright = []; 
    let vzeros = [];
    
    var dataData = srcData.data;

    dataData['x'] = [];
    dataData['y'] = [];

    var dataHist = srcHist.data;

    dataHist['hhist'] = [];
    dataHist['hleft'] = [];
    dataHist['hright'] = [];
    dataHist['hzeros'] = [];
    dataHist['vhist'] = [];
    dataHist['vleft'] = [];
    dataHist['vright'] = [];
    dataHist['vzeros'] = [];

    x = dataData['x'];
    y = dataData['y'];
    hhist = dataHist['hhist']; 
    hleft = dataHist['hleft'];
    hright = dataHist['hright'];
    hzeros = dataHist['hzeros'];
    vhist = dataHist['vhist']; 
    vleft = dataHist['vleft'];
    vright = dataHist['vright'];
    vzeros = dataHist['vzeros'];

    for (let i = 0; i < x_result.length; i++){
        x[i] = x_result[i];
        y[i] = y_result[i];
    }

    for (let i = 0; i < hhist_result.length; i++){
        hhist[i] = hhist_result[i];
        hleft[i] = hleft_result[i];
        hright[i] = hright_result[i];
        hzeros[i] = hzeros_result[i];

        vhist[i] = vhist_result[i];
        vleft[i] = vleft_result[i];
        vright[i] = vright_result[i];
        vzeros[i] = vzeros_result[i];
    }

    dataData['x'] = x;
    dataData['y'] = y;

    dataHist['hhist'] = hhist;
    dataHist['hleft'] = hleft;
    dataHist['hright'] = hright;
    dataHist['hzeros'] = hzeros;
    dataHist['vhist'] = vhist;
    dataHist['vleft'] = vleft;
    dataHist['vright'] = vright;
    dataHist['vzeros'] = vzeros;

    let hmax = Math.max(...hhist)*1.1;
    let vmax = Math.max(...vhist)*1.1;

    pvx_range.start = -vmax;
    pvx_range.end = vmax;
    phy_range.start = -hmax;
    phy_range.end = hmax;

    //console.log(x, y);
    //console.log(hhist, hleft, hright, hzeros);
    //console.log(vhist, vleft, vright, vzeros);

    xaxis.axis_label = fancyHistAxes[0];
    yaxis.axis_label = fancyHistAxes[1];

    srcData.change.emit();   
    srcHist.change.emit();  
    p.change.emit();
    ph.change.emit();
    pv.change.emit();
    

""")

callbackUpdateHAxis = CustomJS(code="""
    fancyHistAxes[0] = this.value;
""")

callbackUpdateVAxis = CustomJS(code="""
    fancyHistAxes[1] = this.value;
""")

callbackNormalization = CustomJS(code="""
    let active = this.active;

    fancyHistNormalization = [false, false];

    for (let i = 0; i < active.length; i++){
        fancyHistNormalization[active[i]] = true;
    }
""")

#widgets

#hmenu = [("Average KO Count per Game", "time_windows"), ("Half Yearly", "time_windows"), None, ("Yearly", "time_windows")]
#hdropdown = Dropdown(label="Time Period", button_type="success", menu=hmenu)
#hdropdown.on_change('value', function_to_call)

hOptions = ["Highest KO Count per Game", "Highest Damage Done per Game", "Average Damage Done per Game", "Player Count per Game"]
vOptions = ["Highest KO Count per Game", "Highest Damage Done per Game", "Average Damage Done per Game", "Player Count per Game"]

hSelect = Select(title =    "Horizontal Data", 
                 options =  hOptions,   #list of options
                 value =   "Highest KO Count per Game" #default value  
                 )

vSelect = Select(title =    "Vertical Data", 
                 options =  vOptions,   #list of options
                 value =   "Highest Damage Done per Game" #default value  
                 )

checkboxNormalization = CheckboxGroup(
        labels=["Normalize horizontal data", "Normalize vertical data"], active=[0,1])

#layout

grid = gridplot([[p, pv], [ph, None]], merge_tools=False)
widgets = row(hSelect, vSelect, checkboxNormalization)
layout = column(widgets, grid)

curdoc().add_root(layout)
curdoc().title = "Selection Histogram"

#interactivity

p.js_on_event(MouseEnter, callbackPlot) #plot whichever axes are currently selected
pv.js_on_event(MouseEnter, callbackPlot) 
ph.js_on_event(MouseEnter, callbackPlot) 

hSelect.js_on_change('value', callbackUpdateHAxis)
vSelect.js_on_change('value', callbackUpdateVAxis)

hSelect.js_on_change('value', callbackPlot)
vSelect.js_on_change('value', callbackPlot)

checkboxNormalization.js_on_change('active', callbackNormalization)
checkboxNormalization.js_on_change('active', callbackPlot)

#show(layout)
save(layout)