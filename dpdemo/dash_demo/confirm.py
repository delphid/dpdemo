import dash
from dash.dependencies import Input, Output, State, MATCH
import dash_html_components as html
import dash_core_components as dcc
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Button(
        id='show',
        children='show'
    ),
    html.Div(
        id='content',
        children=[]
    )
])


def get_div(no):
    result_div = html.Div([
        html.Div(html.Button('just a button')),
        dcc.ConfirmDialogProvider(
            children=html.Button(
                'Click Me',
            ),
            id={'type': 'danger-danger-provider', 'index': no},
            message='Danger danger! Are you sure you want to continue?'
        ),
        html.Div(id={'type': 'output-provider', 'index': no})
    ],
    style={
        'display': 'flex'
    }
)
    return result_div

@app.callback(
    Output('content', 'children'),
    Input('show', 'n_clicks')
)
def show(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    else:
        result = [get_div(i) for i in range(3)]
        return result


@app.callback(
    Output({'type': 'output-provider', 'index': MATCH}, 'children'),
    Input({'type': 'danger-danger-provider', 'index': MATCH}, 'submit_n_clicks')
)
def update_output(submit_n_clicks):
    if not submit_n_clicks:
        return ''
    if submit_n_clicks:
        return """
            It was dangerous but we did it!
            Submitted {} times
        """.format(submit_n_clicks)


if __name__ == '__main__':
    app.run_server(debug=True)
