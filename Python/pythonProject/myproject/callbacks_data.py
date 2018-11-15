from .server import app
from dash.dependencies import Input, Output, Event
import dash_html_components as html
import dash_core_components as dcc
import time
import pandas as pd

import random
from collections import deque
import plotly
import json
import serial
import plotly.graph_objs as go

ser = serial.Serial('/dev/tty.usbmodem1411', 19200)

def wait_for_buffer():
    for i in range(0,20):
        time.sleep(.1)
        if ser.in_waiting>0:
            return True
    return False
# checks if a port is usable (function needs improvement, is also not used)
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

# temperature graph

print('1')
def get_temperature_arduino(port):
    if wait_for_buffer() is True:
        port.write(b'd$')
        data = str(port.readline())
        d = data[2:-5]
        json_acceptable_string = d.replace("'", "\"")
        temp = json.loads(json_acceptable_string)
        temp = temp['temperature']
        return temp

    else:
        return 1
print('2')
def conv_temp(reading):
    voltage = reading * 5.0
    voltage /= 1024.0
    temperatureC = (voltage - 0.5) * 100
    return temperatureC

print('3')
def update_values(times, temperature):
    times.append(time.time())
    temp = get_temperature_arduino(ser)
    temp = conv_temp(temp)
    temperature.append(temp)
    return times, temperature


print('4')
max_length = 10
times = deque(maxlen=max_length)
temperature = deque(maxlen=max_length)
print('5')
data_dict = {"Temperature":temperature}
print('6')
time.sleep(3)
print('7')
times, temperature = update_values(times, temperature) #bug
print('8')

@app.callback(
    Output('temperatuur_grafiek_data', 'children'),
    events=[Event('temperatuur_grafiek_data_interval', 'interval')]
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

# light intensity graphs


light_max_length = 10
times_l = deque(maxlen=light_max_length)
light_intensity = deque(maxlen=light_max_length)
print('9')
def get_lightintensity_arduino(port):
    if wait_for_buffer() == True:
        port.write(b'd$')
        data = str(ser.readline())
        d = data[2:-5]
        json_acceptable_string = d.replace("'", "\"")
        temp = json.loads(json_acceptable_string)
        temp = temp['light_intensity']
        return temp
    else:
        return 1
print('10')
def update_values_l(times_l, light_intensity):
    times_l.append(time.time())
    temp = get_lightintensity_arduino(ser)
    light_intensity.append(temp)
    return times_l, light_intensity
print('11')
data_dict_l = {"Light":light_intensity}
print('12')
time.sleep(2)
print('13')
times_l, light_intensity = update_values_l(times_l, light_intensity)
print('14')
@app.callback(
    Output('lichtintensiteit_grafiek_data', 'children'),
    events=[Event('lichtintensiteit_grafiek_data_interval', 'interval')]
)
def update_graph_l():
    graphs_l = []
    update_values_l(times_l, light_intensity)
    if len(light_intensity)>2:
        class_choice = 'col s12 m6 l4'
    elif len(light_intensity) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'

    data = go.Scatter(
        x=list(times_l),
        y=list(data_dict_l['Light']),
        name='Scatter'
        )

    graphs_l.append(html.Div(dcc.Graph(
        id='light',
        animate=True,
        figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times_l),max(times_l)]),
                                                    yaxis=dict(range=[min(data_dict_l['Light']),max(data_dict_l['Light'])]),
                                                    margin={'l':50,'r':1,'t':45,'b':1},
                                                    title='{}'.format('Light'))}
        ), className=class_choice))

    return graphs_l
