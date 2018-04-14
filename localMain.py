# -*- coding: utf-8 -*-
"""

@author: TT
"""
#import dash
import dash_core_components as dcc
from dash.dependencies import Output, Input
import dash_html_components as html

import re

from app import app

import nycgenheatmap as home
import nycgendetailsdashboard as detail
import app1 #testing....

#main layout
#overview = home.runMapPage()
app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='pageContent') #why do the callbacks for genmap only work when this is the one loaded with the layout????
            ])


#paging callbacks
@app.callback(Output('pageContent', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    try:
        if pathname == '/':
             return home.runMapPage()
        elif '/details/' in pathname:
            zcta = re.search(r'\d{5}$', pathname)
            return detail.runDetailsDash(zcta.group(0).strip())
        elif pathname == '/app1':
            return app1.getLayout()
        else:
            return 'Error 404: Page Not Found'
    except Exception as e:
        return 'Error 500: ' + str(e)



#run (for local only...if you want to see the app run on your machine, use this not main.py (that's for pythonanywhere to work))
if __name__ == '__main__':
    app.run_server(debug=True)



