import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv('myproject/gem_temp.csv', delimiter=';')

def generate_table(dataframe, max_rows=5):
    return html.Table(
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    , style={'text-align':'center'})

layout = html.Div([
    # row 1
    html.Div([
        html.Div([

            html.P('Huidige temperatuur'),

            html.Span(id='temperatuur_data', style={'font-size': '24px', 'position':'relative', 'top':'25%'})

        ],
        style={'background-color':'#FFFFFF', 'height':'200px', 'width':'32.65%', 'float':'left', 'border':'0.1vw solid #C8D4E3', 'margin':'0.25%', 'text-align':'center'}
        ),

        html.Div([

            html.P('Huidige lichtintensiteit'),

            html.Span(id='lichtintensiteit_data', style={'font-size': '24px', 'position':'relative', 'top':'25%'})

        ],
        style={'background-color':'#FFFFFF', 'height':'200px', 'width':'32.65%', 'float':'left','border':'0.1vw solid #C8D4E3', 'margin':'0.25%', 'text-align':'center'}
        ),

        html.Div([

            html.P('Huidige status'),

            html.Span(id='status_data', style={'font-size': '24px', 'position':'relative', 'top':'25%'})


        ],
        style={'background-color':'#FFFFFF', 'height':'200px', 'width':'32.65%', 'float':'left','border':'0.1vw solid #C8D4E3', 'margin':'0.25%', 'text-align':'center'}
        )

    ],
    style={'display': 'table', 'width':'100%', 'margin-top':'10px'}
    ),
    # row 2
    html.Div([
        html.Div([

            html.P('Temperatuur', style={'font-size':'24px'}),

            html.Div(children=html.Div(id='temperatuur_grafiek_data')),
            dcc.Interval(
                id='temperatuur_grafiek_data_interval',
                interval=1*5000
            )

        ],
        style={'background-color':'#FFFFFF', 'height':'600px', 'width':'49.3%', 'float':'left', 'border':'0.1vw solid #C8D4E3', 'margin':'0.25%', 'text-align':'center'}
        ),

        html.Div([

            html.P('Lichtintensiteit', style={'font-size':'24px'}),

            html.Div(children=html.Div(id='lichtintensiteit_grafiek_data')),
            dcc.Interval(
                id='lichtintensiteit_grafiek_data_interval',
                interval=1*5000
            )

        ],
        style={'background-color':'#FFFFFF', 'height':'600px', 'width':'49.3%', 'float':'left', 'border':'0.1vw solid #C8D4E3', 'margin':'0.25%', 'text-align':'center'}
        )
    ]
    ),
    # row 3
    #html.Div([
    #    html.Div([
    #
    #        html.P('Gemiddelde temperatuur'),
    #
    #        generate_table(df)

    #    ],
    #    style={'background-color':'#FFFFFF', 'height':'400px', 'width':'49.3%', 'float':'left', 'border':'0.1vw solid #C8D4E3', 'margin':'0.25%', 'text-align':'center'}
    #    ),

    #    html.Div([

    #        html.P('Gemiddelde lichtintensiteit'),

    #        generate_table(df)

    #    ],
    #    style={'background-color':'#FFFFFF', 'height':'400px', 'width':'49.3%', 'float':'left', 'border':'0.1vw solid #C8D4E3', 'margin':'0.25%',  'text-align':'center'}
    #    )
    #]
    #)


])
