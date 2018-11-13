from .server import app, ar
from dash.dependencies import Input, Output, Event
import dash_html_components as html
import dash_core_components as dcc
import time
import pandas as pd

import random
from collections import deque
import plotly
import json
import plotly.graph_objs as go

# show the temperatuur
@app.callback(
    Output('temperatuur_home', 'children'),
    [Input('hidden_temp', 'children')]
)
def show_temp(n):
    return n

# show the light intensity
@app.callback(
    Output('lichtintensiteit_home', 'children'),
    [Input('hidden_light', 'children')]
)
def show_temp(n):
    return n

# show the time
@app.callback(
    Output('tijd_home', 'children'),
    [Input('hidden_time', 'children')]
)
def show_time(n):
    return n

# show the date
@app.callback(
    Output('datum_home', 'children'),
    [Input('hidden_date', 'children')]
)
def show_date(n):
    return n

# temperature graph
#ser = serial.Serial('/dev/tty.usbmodem1411', 19200)

def conv_temp(reading):
    voltage = reading * 5.0
    voltage /= 1024.0
    temperatureC = (voltage - 0.5) * 100
    return temperatureC

def update_values(times, temperature):
    times.append(time.time())
    temp = ar.get_temperature()
    temp = conv_temp(temp)
    temperature.append(temp)
    return times, temperature

max_length = 12
times = deque(maxlen=max_length)
temperature = deque(maxlen=max_length)

data_dict = {"Temperature":temperature}

time.sleep(2)
times, temperature = update_values(times, temperature)

@app.callback(
    Output('temperatuur_grafiek_home', 'children'),
    events=[Event('temperatuur_grafiek_home_interval', 'interval')]
)
def update_graph():
    graphs = []
    update_values(times, temperature)
    if len(temperature)>2:
        class_choice = 'col s12 m6 l4'
    elif len(temperature) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'

    data = go.Scatter(
        x=list(times),
        y=list(data_dict['Temperature']),
        name='Scatter'
        )

    graphs.append(html.Div(dcc.Graph(
        id='temperature',
        animate=True,
        figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                                    yaxis=dict(range=[min(data_dict['Temperature']),max(data_dict['Temperature'])]),
                                                    margin={'l':50,'r':1,'t':45,'b':1},
                                                    title='{}'.format('Temperature'))}
        ), className=class_choice))

    return graphs
