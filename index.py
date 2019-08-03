import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
import layouts
import callbacks

server=app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/cycling_overview':
         return layouts.cycling_overview_layout
    else:
        return layouts.home_layout

if __name__ == '__main__':
    
    app.run_server(debug=True)