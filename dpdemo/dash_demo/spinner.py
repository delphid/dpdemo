import json
import time

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(
    children=[
        dbc.Button(
            id='button',
            children=[dbc.Spinner(size='sm'), 'aaa'],
        ),
        html.Div(
            id='content',
            children=[]
        )
    ]
)


@app.callback(
    Output('content', 'children'),
    Input('button', 'n_clicks'),
)
def do(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    else:
        time.sleep(0.5)
    return str(time.time())



if __name__ == "__main__":
    app.run_server(debug=True)
