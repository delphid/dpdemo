import json

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(
    children=[
        dbc.Button(id={'type': 'fire_show', 'index': 1}, children='show'),
        html.Div(id={'type': 'content', 'index': 1}, children=[]),
        dbc.Modal(
            id={'type': 'confirm', 'index': 1},
            children=[
                dbc.ModalBody('go ahead and choose'),
                dbc.ModalFooter(
                    children=[
                        dbc.Button(
                            id={'type': 'confirm_show', 'index': 1},
                            children='do it',
                            n_clicks=0,
                        ),
                        dbc.Button(
                            id={'type': 'cancel_show', 'index': 1},
                            children='no I regret',
                            n_clicks=0,
                        )
                    ]
                )
            ],
            autoFocus=False
        )
    ]
)


@app.callback(
    Output({'type': 'content', 'index': MATCH}, 'children'),
    Output({'type': 'confirm', 'index': MATCH}, 'is_open'),
    Input({'type': 'fire_show', 'index': MATCH}, 'n_clicks'),
    Input({'type': 'confirm_show', 'index': MATCH}, 'n_clicks'),
    Input({'type': 'cancel_show', 'index': MATCH}, 'n_clicks')
)
def show(fire_clicks, confirm_clicks, cancel_clicks):
    ctx = dash.callback_context
    if not any([fire_clicks, confirm_clicks, cancel_clicks]):
        raise PreventUpdate
    else:
        id_string = ctx.triggered[0]['prop_id'].split('.')[0]
        id_dic = json.loads(id_string)
        trigger = id_dic['type']
        print(trigger)
        if trigger == 'fire_show':
            return dash.no_update, True
        elif trigger == 'confirm_show':
            return f'you confirmed for {confirm_clicks} times', False
        elif trigger == 'cancel_show':
            return dash.no_update, False


if __name__ == "__main__":
    app.run_server(debug=True)
