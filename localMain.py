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

import TypeHelper as th

#ug, it only doesn't work locally! going to have to hack for now, works as intended on main.py

#main layout
app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            #...and the downgrade must have downgraded or upgraded something else, because now those callbacks are working locally without the hack...
            html.Div(id='pageContent')#, children=home.runMapPage()) #why do the callbacks for genmap only work when this is the one loaded with the layout????
            ])


#Link callbacks for pages
@app.callback(Output('pageContent', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    try:
        if pathname == '/' or pathname == '':
             return home.runMapPage()
        elif '/details/' in pathname:
            zcta = re.search(r'\d{5}$', pathname)
            return detail.runDetailsDash(zcta.group(0).strip())
        else:
            return 'Error 404: You are very lost. '
    except Exception as e:
        return 'Error 500: ' + str(e)

#reroutes based on events
@app.callback(Output('url', 'pathname'),
              [Input('zctaGenHeatMap', 'clickData')])
def onClickForReroute(clickData):
    if 'points' in clickData:
        intZcta = th.cleanInts(clickData['points'][0]['text'])
        if(intZcta == 0):
            return "/"

        return "/details/" + str(intZcta)
    else:
        return "/"

#run (for local only...if you want to see the app run on your machine, use this not main.py (that's for pythonanywhere to work))
if __name__ == '__main__':
    app.run_server(debug=True)



