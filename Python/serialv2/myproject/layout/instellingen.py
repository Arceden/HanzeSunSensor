import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

layout = html.Div([
    html.Span('TESTER', id='tester'),
    dcc.Interval(id='tester_interval', interval=9000, n_intervals=0)
])
