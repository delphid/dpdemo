import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State, MATCH
from dash.exceptions import PreventUpdate
import dash_html_components as html
import dash_core_components as dcc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=False
)

URL = ''


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(dcc.Input(id='input-on-submit', type='text')),
                html.Div(html.Button('Submit', id='submit-val', n_clicks=0)),
            ],
            style={
                'display': 'flex',
                #'flex-direction': 'row',
                'border-bottom': 'thin lightgrey solid'
            }
        ),
        html.Div(
            id='container-button-basic',
            children='Enter a value and press submit')
    ],
    #style={'width': '96%', 'padding-left': '3%', 'padding-right': '1%'}
    style={
        #'background': 'PowderBlue',
        'paddingTop': '50px',
        'width': '60%',
        'marginLeft': '20%',
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'baseline',
        'justifyContent': 'flex-start',
        #'text-align': 'center',
        #'border-bottom': 'thin lightgrey solid'
    }
)


def line(row_no):
    result_div = html.Div(
        children=[
            html.Div(
                children=str(row_no)
            ),
            html.Div(
                id={
                    'type': 'dynamic-show1',
                    'index': f'{row_no}'
                },
                children='la lala lalala',
                style={'width': '70px'}
            ),
            html.Div(
                children=[
                    dcc.Link(
                        html.Button('aleilei'),
                        href=URL,
                        target='_blank'
                    )
                ]
            ),
            html.Div(
                id={
                    'type': 'button-container',
                    'index': f'{row_no}'
                },
                children=[
                    html.Button(
                        id={
                            'type': 'dynamic-button',
                            'index': f'{row_no}'
                        },
                        children='Submit',
                        n_clicks=0
                    )
                ]
            )
        ],
        className='emphasize',
        style={
            'display': 'flex'
        }
    )
    return result_div


@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def generate_lines(n_clicks, value):
    result = 'not clicked yet'
    if n_clicks:
        result = [line(i) for i in range(int(value))]
    return result


@app.callback(
    Output({'type': 'dynamic-show1', 'index': MATCH}, 'children'),
    Output({'type': 'button-container', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'dynamic-show1', 'index': MATCH}, 'children')
)
def renew_line(n_clicks, text):
    print('clicked')
    if not n_clicks:
        raise PreventUpdate
    else:
        result = f'{text} x {text}'
    return result, ['already wasted your click']


if __name__ == '__main__':
    app.run_server(debug=True)
