import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.exceptions import PreventUpdate

from one import run


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(dcc.Input(id='text-input1', type='text', placeholder='put task_queue here')),
    html.Div(dcc.Input(id='text-input2', type='text', placeholder='put name here')),
    html.Button('call', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='enter value and call')
])


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('text-input1', 'value')],
    [dash.dependencies.State('text-input2', 'value')])
def udpate_some_message(n_clicks, task_queue, name):
    if not n_clicks:
        raise PreventUpdate
    else:
        result = run(task_queue, name)
    return result


if __name__ == '__main__':
    app.run_server(debug=True)
