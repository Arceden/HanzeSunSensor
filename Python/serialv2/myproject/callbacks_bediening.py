from .server import app
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import time

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
@app.callback(
    Output('output-range-slider', 'children'),
    [Input('uitrol_bereik_handmatig', 'value')]
)
def update_output(value):
    return "You have selected {}".format(value)
    #returns a list
