from .server import app
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import time
import pandas as pd

import random
from collections import deque

import serial

def portIsUsable(portName):
    try:
       ser = serial.Serial(port=portName)
       return True
    except:
       return False

# show the temperatuur
@app.callback(
    Output('temperatuur_data', 'children'),
    [Input('hidden_temp', 'children')]
)
def show_temp(n):
    return n

# show the light intensity
@app.callback(
    Output('lichtintensiteit_data', 'children'),
    [Input('hidden_light', 'children')]
)
def show_temp(n):
    return n

# change status
@app.callback(
    Output('status_data', 'children'),
    [Input('hidden_status', 'children')]
)
def connection_check(n):
    return n
