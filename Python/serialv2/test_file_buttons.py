import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

app = dash.Dash()

manual = True
#True, 1 , False, 0


app.layout = html.Div([

    html.Span('status', id='status'),

    html.Button(
        children='aan',
        id='button1',
        n_clicks=0
    ),
    html.Button(
        children='uit',
        id='button2',
        n_clicks=0
    )
])

@app.callback(
    Output('button1', 'children'),
    [Input('button1', 'n_clicks')]
)
def update(n_clicks):
    global manual
    if manual is False:
        manual = True
        return "Aan"
    if manual is True:
        manual = False
        return "Uit"




if __name__ == '__main__':
    app.run_server(debug=True)
