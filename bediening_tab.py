import dash
import dash_core_components as dcc
import dash_html_components as html

import visuals

layout = html.Div([

    html.Div([
        html.Div([

            html.P('Handmatig', style={'font-size':'24px'}),

            html.Div([
                # when button is pressed children changes to 'UIT', also need counter variable
                html.Button(
                    children='AAN',
                    id='bediening_knop_1'
                )

            ]),

            html.Div([

                html.P(children='Geef het gewenste uitrol bereik aan:'),

                dcc.RangeSlider(

                    id='uitrol_bereik_handmatig',
                    min=0,
                    max=160,
                    value=[10, 160],
                    marks={
                        0: {'label': '0cm'},
                        20: {'label': '20cm'},
                        40: {'label': '40cm'},
                        60: {'label': '60cm'},
                        80: {'label': '80cm'},
                        100: {'label': '100cm'},
                        120: {'label': '120cm'},
                        140: {'label': '140cm'},
                        160: {'label': '160cm'}
                    },
                    allowCross=False,
                )
            ],
            style={'width':'50%', 'margin':'0 auto', 'padding-top':'50px'}
            )

        ],
        style={'background-color': '#FFFFFF',
            'border':'0.1vw solid #C8D4E3','height': '500px','width':'49.3%',
            'margin':'0.25%','text-align':'center', 'float':'left', 'padding-top':'10px'}
        ),

        html.Div([

            html.P('Autonoom', style={'font-size':'24px'}),

            html.Div([
                # when button is pressed change 'UIT' to 'AAN' and vice versa. Need counter variable
                html.Button(
                    children='UIT',
                    id='bediening_knop_2'
                )

            ]),

            html.Div([

                html.P(children='Geef het gewenste temperatuur bereik aan:'),

                dcc.RangeSlider(

                    id='temperatuur_bereik_autonoom',
                    min=-30,
                    max=40,
                    value=[10, 35],
                    marks={
                        -30: {'label': '-30°C', 'style': {'color': '#9EE4D9'}},
                        -20: {'label': '-20°C'},
                        -10: {'label': '-10°C'},
                        0: {'label': '0°C', 'style': {'color':'#A5F2F3'}},
                        10: {'label': '10°C'},
                        20: {'label': '20°C'},
                        30: {'label': '30°C'},
                        40: {'label': '40°C', 'style': {'color':'#FF0000'}}
                    },
                    allowCross=False,
                )
            ],
            style={'width':'50%', 'margin':'0 auto', 'padding-top':'50px'}
            ),

            html.Div([

                html.P(children='Geef het gewenste uitrol bereik aan:'),

                dcc.RangeSlider(

                    id='uitrol_bereik_autonoom',
                    min=0,
                    max=160,
                    value=[10, 160],
                    marks={
                        0: {'label': '0cm'},
                        20: {'label': '20cm'},
                        40: {'label': '40cm'},
                        60: {'label': '60cm'},
                        80: {'label': '80cm'},
                        100: {'label': '100cm'},
                        120: {'label': '120cm'},
                        140: {'label': '140cm'},
                        160: {'label': '160cm'}
                    },
                    allowCross=False,
                )
            ],
            style={'width':'50%', 'margin':'0 auto', 'padding-top':'50px'}
            )
        ],
        style={'background-color': '#FFFFFF',
            'border':'0.1vw solid #C8D4E3', 'height': '500px','width':'49.3%',
            'margin': '0.25%', 'text-align':'center', 'float':'left', 'padding-top':'10px'}
        )
    ],
    style={'display': 'table', 'margin-top': '10px',  'width':'100%'}
    ),
    # row 2
    html.Div([

        html.Div([

            html.P('Huidige temperatuur'),

            html.Span('16°C.', id='temperatuur_bediening', style={'font-size': '24px', 'position':'relative', 'top':'25%'})

        ],
        style={'float':'left', 'width':'24.33%','height':'250px', 'margin':'0.25%', 'background-color':'#FFFFFF', 'border':'0.1vw solid #C8D4E3', 'text-align':'center'}
        ),

        html.Div([

            html.P('Huidige lichtintensiteit'),

            html.Span('135cd', id='lichtintensiteit_bediening', style={'font-size': '24px', 'position':'relative', 'top':'25%'})

        ],
        style={'float':'left', 'width':'24.3%', 'height':'250px', 'margin':'0.25%', 'background-color':'#FFFFFF','border':'0.1vw solid #C8D4E3', 'text-align':'center'}
        ),

        html.Div([

            html.P('Huidige tijd'),

            html.Span('17:30', id='tijd_bediening', style={'font-size': '24px', 'position':'relative', 'top':'25%'})

        ],
        style={'float':'left', 'width':'24.3%', 'height':'250px', 'margin':'0.25%', 'background-color':'#FFFFFF','border':'0.1vw solid #C8D4E3', 'text-align':'center'}
        ),

        html.Div([

            html.P('Huidige datum'),

            html.Span('31 Oktober', id='datum_bediening', style={'font-size': '24px', 'position':'relative', 'top':'25%'})

        ],
        style={'float':'left', 'width':'24.3%', 'height':'250px', 'margin':'0.25%', 'background-color':'#FFFFFF','border':'0.1vw solid #C8D4E3', 'text-align':'center'}
        )

    ],
    style={'display': 'table', 'width':'100%'}
    )


])
