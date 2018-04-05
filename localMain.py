# -*- coding: utf-8 -*-
"""

@author: TT
"""
import dash
import dash_core_components as dcc
from dash.dependencies import Output, Input
import nycgenheatmap as home
import dash_html_components as html
import nycgendetailsdashboard as detail

app = dash.Dash()
app.config['suppress_callback_exceptions']=True

CURRENT_ZCTA = None

@app.callback(Output('pageContent', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
         return home.runMapPage()
    elif pathname == '/details':
         return detail.runDetailsDash()
    else:
        return '404'

#run (for local only...if you want to see the app run on your machine, use this not main.py (that's for pythonanywhere to work))
if __name__ == '__main__':
    app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='pageContent', children=home.runMapPage())
            ])
    app.run_server(debug=True)
    