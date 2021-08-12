import dash
import dash_html_components as html
import dash_core_components as dcc


values = []

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children='d1 aaa',
                    className='emphasize',
                    style={'width': '20%'}
                ),
                html.Div(
                    children='d1 bbb',
                    className='emphasize',
                    style={'width': '20%'}
                ),
                html.Div(
                    children='d1 ccc',
                    className='emphasize',
                    style={'width': '20%'}
                )
            ],
            style={
                'width': '60%',
                'display': 'flex',
                'flex-direction': 'row'
            },
            className='show'
        ),
        html.Div(
            children=[
                html.Div(children='d2 aaa'),
                html.Div(children='d2 bbb')
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row'
            },
            className='show'
        )
    ],
    # https://flexbox.help/
    style={
        'width': '60%',
        'marginLeft': '20%',
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'baseline',
        'justify-content': 'flex-start',
        #'text-align': 'center',
    },
    className='emphasize'
)


if __name__ == '__main__':
    app.run_server(debug=True)
