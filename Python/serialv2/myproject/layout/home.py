import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event
import plotly.graph_objs as go

import time
from collections import deque



# LAYOUT
layout = html.Div([

    # row 1
    html.Div([
        html.Div([

            html.H1('Welkom, dit is uw Dashboard')

        ],
        style={'background-color':'#FFFFFF', 'height':'100px', 'width':'99.3%', 'border':'0.1vw solid #C8D4E3', 'margin':'0.25%', 'text-align':'center'}
        )
    ]),
    #row2
    html.Div([
        html.Div([

            html.P('Uitleg'),

            html.Span('Dit dashboard geeft u een overzicht van de data die binnenkomt via het apparaat. Daarnaast is het ook mogelijk om uw apparaat in te stellen. Kijk gerust op de verschillende tabs.')

        ],
        style={'background-color':'#FFFFFF', 'height':'600px', 'width':'49.3%', 'float':'left', 'border':'0.1vw solid #C8D4E3', 'margin':'0.25%', 'text-align':'center'}
        ),

        html.Div([

            html.P('Temperatuur'),

            html.Div(children=html.Div(id='temperatuur_grafiek_home')),
            dcc.Interval(
                id='temperatuur_grafiek_home_interval',
                interval=1*5000
            )

        ],
        style={'background-color':'#FFFFFF', 'height':'600px', 'width':'49.3%', 'float':'left', 'border':'0.1vw solid #C8D4E3', 'margin':'0.25%', 'text-align':'center'}
        )

    ]),
    #row3
    html.Div([

        html.Div([

            html.P('Huidige temperatuur'),

            html.Span(id='temperatuur_home', style={'font-size': '24px', 'position':'relative', 'top':'25%'})

        ],
        style={'float':'left', 'width':'24.33%', 'box-sizing':'border-box','height':'250px', 'margin':'0.25%', 'background-color':'#FFFFFF', 'border':'0.1vw solid #C8D4E3', 'text-align':'center'}
        ),

        html.Div([

            html.P('Huidige lichtintensiteit'),

            html.Span(id='lichtintensiteit_home', style={'font-size': '24px', 'position':'relative', 'top':'25%'})

        ],
        style={'float':'left', 'width':'24.3%', 'height':'250px', 'margin':'0.25%', 'background-color':'#FFFFFF','border':'0.1vw solid #C8D4E3', 'text-align':'center'}
        ),

        html.Div([

            html.P('Huidige tijd'),

            html.Span(id='tijd_home', style={'font-size': '24px', 'position':'relative', 'top':'25%'})

        ],
        style={'float':'left', 'width':'24.3%', 'height':'250px', 'margin':'0.25%', 'background-color':'#FFFFFF','border':'0.1vw solid #C8D4E3', 'text-align':'center'}
        ),

        html.Div([

            html.P('Huidige datum'),

            html.Span(id='datum_home', style={'font-size': '24px', 'position':'relative', 'top':'25%'})

        ],
        style={'float':'left', 'width':'24.3%', 'height':'250px', 'margin':'0.25%', 'background-color':'#FFFFFF','border':'0.1vw solid #C8D4E3', 'text-align':'center'}
        )

    ],
    style={'display': 'table', 'width':'100%'}
    )

])
