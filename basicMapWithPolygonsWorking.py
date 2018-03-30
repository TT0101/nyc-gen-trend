# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 20:02:21 2018

@author: theresa
"""
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import json
import os

def run(app):
    mapboxtoken = 'pk.eyJ1IjoidHRob21haWVyIiwiYSI6ImNqZjduZzkzdjF6d2wyd2xubTI3djN4cGwifQ.3-bkCbF2NAzEyTsqK3okWg'
    zctaPolygonFile = os.getcwd() + "/mysite/Datafiles/Map/nyczipcodetabulationareas.geojson"

    #get geojson for zcta areas
    geofile = open(zctaPolygonFile)
    geojsonlayer = json.load(geofile)
    geofile.close()

    centerLat = 40.702793
    centerLong =-73.965584

    #map
    mapData = go.Data([
            go.Scattermapbox(
                    lat=[centerLat],
                    lon=[centerLong],
                    mode='markers'
                    )
            ])

    mapLayout = go.Layout(
            height=800,
            autosize=True,
            margin = dict(l = 0, r = 0, t = 0, b = 0),
            hovermode='closest',
            mapbox=dict(
                    layers=[
                            dict(
                                    sourcetype = 'geojson',
                                    source = geojsonlayer,
                                    type = 'fill',
                                    color = 'rgba(163,22,19,0.8)'
                                    )
                            ],
                    accesstoken=(mapboxtoken),
                    bearing=0,
                    center=dict(
                                lat=centerLat,
                                lon=centerLong
                                ),
                    pitch=0,
                    zoom=9.95,
                    style='light'
                    )
                )


    #UI application
    #app = dash.Dash()

    app.layout = html.Div(children=[
        html.H1(children='Test App'),

        html.Div(children='''
            Hover to see values, click to see area dashboard:
        '''),
        dcc.Graph(
                id = 'zcta-example',
                style={'height':'90vh'},
                figure=dict(data=mapData, layout=mapLayout)
                )
    ])

    return app
#run
#if __name__ == '__main__':
#    app.run_server(debug=True)