import dash
import dash_core_components as dcc
from dash.dependencies import Output, Input
import dash_html_components as html


import nycgenheatmap as home
import nycgendetailsdashboard as detail

from flask import Flask


CURRENT_ZCTA = None #global to allow grab of data across pages

fServer = Flask(__name__)
#initLayout = html.Div(id='page-content', children="init")
app = dash.Dash(__name__, server=fServer, static_folder='static', url_base_pathname='/')
#app.layout = initLayout

app.config['suppress_callback_exceptions']=True

#link callback
@app.callback(Output('pageContent', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
         return home.runMapPage()
    elif pathname == '/details':
         return detail.runDetailsDash()
    else:
        return '404'


app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='pageContent', children=home.runMapPage())
            ])

#app = test.run(app)