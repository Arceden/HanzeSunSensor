from .server import app, server
from . import callbacks_home
from . import callbacks_data
from . import callbacks_bediening
from .layout import home
from .layout import bediening
from .layout import data

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import random
import time
import datetime
import serial
import json
import sys

com = '/dev/tty.usbmodem1411'
try:
    ser = serial.Serial(com, 19200)
except serial.serialutil.SerialException:
    com = input("Enter com port: ")
    ser = serial.Serial(com, 19200)

'''def port_is_usable():
    try:
        global ser
        if not ser:
            ser = serial.Serial('/dev/tty.usbmodem1411', 19200)
            return True
    except Exception:
        return False

port_is_usable()'''



def get_temperature_arduino(port):
    port.write(b'd')
    data = str(ser.readline())
    d = data[2:-5]
    json_acceptable_string = d.replace("'", "\"")
    temp = json.loads(json_acceptable_string)
    temp = temp['temperature']
    return temp

def conv_temp(reading):
    voltage = reading * 5.0
    voltage /= 1024.0
    temperatureC = (voltage - 0.5) * 100
    return temperatureC

def conv_temp_arduino(temperatureC):
    voltage += 0.5
    voltage = temperatureC / 100
    voltage *= 1024.0
    reading = voltage /5.0
    return reading


def get_lightintensity_arduino(port):
    port.write(b'd')
    data = str(ser.readline())
    d = data[2:-5]
    json_acceptable_string = d.replace("'", "\"")
    temp = json.loads(json_acceptable_string)
    temp = temp['light_intensity']
    return temp

def conv_light(reading):
    light = reading * 4.98
    light /= 1023
    return light

def con_light_arduino(light):
    light *= 1024
    reading = light / 4.98
    return reading
    



app.layout = html.Div([


    html.Div([

        html.Link(href="https://fonts.googleapis.com/css?family=Roboto", rel='stylesheet'),

        html.H1('DSIO Dashboard', style={'color':'#FFFFFF', 'margin-left':'10px'})

    ], style={'background-color': '#1f618d ', 'overflow':'hidden'}),

    html.Div([

        dcc.Tabs(
            id='tabs',
            children=[

                dcc.Tab(
                    label='Home',
                    value='home_tab'
                    ),

                dcc.Tab(
                    label='Data',
                    value='data_tab',
                ),

                dcc.Tab(
                    label='Bediening',
                    value='bediening_tab',
                ),

                dcc.Tab(
                    label='Instellingen',
                    value='instellingen_tab',
                )

            ]
            , value='home_tab'
        )

    ]),

    html.Div(id='tab_content'),

    html.Div(id='hidden_temp', style={'display':'none'}),
    dcc.Interval(id='hidden_temp_interval', interval=1*5000, n_intervals=0),

    html.Div(id='hidden_light', style={'display':'none'}),
    dcc.Interval(id='hidden_light_interval', interval=1*5000, n_intervals=0),

    html.Div(id='hidden_time', style={'display':'none'}),
    dcc.Interval(id='hidden_time_interval', interval=1*1000, n_intervals=0),

    html.Div(id='hidden_date', style={'display':'none'}),
    dcc.Interval(id='hidden_date_interval', interval=1*5000, n_intervals=0),

    html.Div(id='hidden_status', style={'display':'none'}),
    dcc.Interval(id='hidden_status_interval', interval=1*5000, n_intervals=0)


], style={'width':'100%','background-color':'#e5e8e6','height':'100%','min-height':'1024px'})

@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "home_tab":
        return home.layout
    elif tab == "data_tab":
        return data.layout
    elif tab == "bediening_tab":
        return bediening.layout
    else:
        return 'must still be done :D'

# update temperature
@app.callback(
    Output('hidden_temp', 'children'),
    [Input('hidden_temp_interval', 'n_intervals')]
)
def update_temp(n):
    temp = get_temperature_arduino(ser)
    temp = round(conv_temp(temp), 2)
    return '{}°C.'.format(temp)



# update light
@app.callback(
    Output('hidden_light', 'children'),
    [Input('hidden_light_interval', 'n_intervals')]
)
def update_light(n):
    light = get_lightintensity_arduino(ser)
    light = conv_light(light)
    return light


# update time
@app.callback(
    Output('hidden_time', 'children'),
    [Input('hidden_time_interval', 'n_intervals')]
)
def update_time(n):
    current = time.strftime('%H:%M:%S')
    return current

# update date
@app.callback(
    Output('hidden_date', 'children'),
    [Input('hidden_date_interval', 'n_intervals')]
)
def update_date(n):
    current_date = datetime.datetime.now().strftime('%d/%m/%y')
    return current_date

# update status
@app.callback(
    Output('hidden_status', 'children'),
    [Input('hidden_status_interval', 'n_intervals')]
)
def update_status(n):
    return html.Span(children="aangesloten", style={"color":"green"})
