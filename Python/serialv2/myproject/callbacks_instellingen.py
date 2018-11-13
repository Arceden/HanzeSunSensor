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

@app.callback(
    Output('tester', 'children'),
    [Input('tester_interval', 'n_intervals')]
)
def update(n):
    x = ar.get_settings()
    y = ar.get_state()
    return 'FUCKER {} {} {}'.format(random.randint(1, 20), x, y)
