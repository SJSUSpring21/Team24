import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1,app2,app3,app4,app5,app6
app.title = 'WASH Analytics'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/wash-home':
        return app1.layout
    elif pathname == '/country-sanitation':
        return app2.layout
    elif pathname == '/mean-service':
        return app3.layout
    elif pathname == '/median-service':
        return app4.layout
    elif pathname == '/comparison':
        return app5.layout
    elif pathname == '/prediction':
        return app6.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)