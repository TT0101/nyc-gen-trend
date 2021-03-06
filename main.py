#import dash
import dash_core_components as dcc
from dash.dependencies import Output, Input
import dash_html_components as html
import re

import nycgenheatmap as home
import nycgendetailsdashboard as detail

import TypeHelper as th

from app import app

#main setup
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='pageContent')
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