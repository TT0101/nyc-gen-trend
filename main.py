import dash
import dash_core_components as dcc
from dash.dependencies import Output, Input
import dash_html_components as html


import nycgenheatmap as home
import nycgendetailsdashboard as detail
import genoverviewdata as oData

import TypeHelper as th

from flask import Flask

from app import app

#move this to app when on server
#fServer = Flask(__name__)
#app = dash.Dash(__name__, server=fServer, static_folder='static', url_base_pathname='/')
#
#app.config['suppress_callback_exceptions']=True

#main setup
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='pageContent')#, children=home.runMapPage())
            ])


#link callback
@app.callback(Output('pageContent', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
         return home.runMapPage()
    elif '/details/' in pathname:
            zcta = re.search(r'\d{5}$', pathname)
            return detail.runDetailsDash(zcta.group(0).strip())
    else:
        return '404'

