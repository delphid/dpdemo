import json

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


def popover_div(n):
    result_div = html.Div(
        [
            html.Div(
                dbc.Button(
                    children="show",
                    id=f'button_to_pop{n}'
                )
            ),
            html.Div(
                id={'type': 'content', 'index': n},
                children=[]
            ),
            dbc.Popover(
                [
                    dbc.PopoverHeader(f"a popover from button {n}"),
                    dbc.PopoverBody(
                        children=[
                            dbc.Button(
                                id={'type': 'confirm_show', 'index': n},
                                children='do it',
                                n_clicks=0,
                                color='danger'
                            ),
                            dbc.Button(
                                id={'type': 'cancel_show', 'index': n},
                                children='no I regret',
                                n_clicks=0,
                            )
                        ],
                        style={
                            'display': 'flex',
                            'justify-content': 'space-around'
                        }
                    ),
                ],
                id={
                    'type': 'popover',
                    'index': n
                },
                is_open=False,
                target=f"button_to_pop{n}",
                trigger='legacy'
            ),
        ]
    )
    return result_div


app.layout = html.Div(
    [
        popover_div(0),
        popover_div(1)
    ]
)


@app.callback(
    Output({'type': 'content', 'index': MATCH}, 'children'),
    Output({'type': 'popover', 'index': MATCH}, "is_open"),
    Input({'type': 'confirm_show', 'index': MATCH}, 'n_clicks'),
    Input({'type': 'cancel_show', 'index': MATCH}, 'n_clicks')
)
def show(confirm_clicks, cancel_clicks):
    ctx = dash.callback_context
    if not any([confirm_clicks, cancel_clicks]):
        raise PreventUpdate
    else:
        id_string = ctx.triggered[0]['prop_id'].split('.')[0]
        id_dic = json.loads(id_string)
        trigger = id_dic['type']
        print(trigger)
        if trigger == 'confirm_show':
            return f'you confirmed for {confirm_clicks} times', False
        elif trigger == 'cancel_show':
            return dash.no_update, False


if __name__ == "__main__":
    app.run_server(debug=True)
