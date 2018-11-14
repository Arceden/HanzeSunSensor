from .server import app, ar
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import time

# button
@app.callback(
    Output('bediening_knop_1', 'children'),
    [Input('bediening_knop_1', 'n_clicks')]
)
def update(n_clicks):
    if ar.get_state() is False:
        ar.set_state(True)
        return "Aan"
    if ar.get_state() is True:
        ar.set_state(False)
        return "Uit"

# show the temperatuur
@app.callback(
    Output('temperatuur_bediening', 'children'),
    [Input('hidden_temp', 'children')]
)
def show_temp(n):
    return n

# show the light intensity
@app.callback(
    Output('lichtintensiteit_bediening', 'children'),
    [Input('hidden_light', 'children')]
)
def show_temp(n):
    return n

# show the time
@app.callback(
    Output('tijd_bediening', 'children'),
    [Input('hidden_time', 'children')]
)
def show_time(n):
    return n

# show the date
@app.callback(
    Output('datum_bediening', 'children'),
    [Input('hidden_date', 'children')]
)
def show_date(n):
    return n

# return output range slider
#if ar.get_state() == True:
@app.callback(
    Output('output-range-slider', 'children'),
    [Input('uitrol_bereik_handmatig', 'value')]
)
def get_output(value):
    value_min = value[0]
    value_max = value[1]
    ar.write('tmpl {}'.format(value_min))
    ar.readline()
    ar.write('tmph {}'.format(value_max))
    return "Min: {}, Max: {}".format(value_min, value_max)
    #returns a list
