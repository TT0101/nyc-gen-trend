# -*- coding: utf-8 -*-
"""
@author Theresa Thomaier
"""

#overall imports
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import json
import os

def runMapPage(app):
    #constants
    mapboxtoken = 'pk.eyJ1IjoidHRob21haWVyIiwiYSI6ImNqZjduZzkzdjF6d2wyd2xubTI3djN4cGwifQ.3-bkCbF2NAzEyTsqK3okWg'
    zctaPolygonFile = os.getcwd() + "/mysite/Datafiles/Map/nyczipcodetabulationareas.geojson"
     
    zctaGeojson = getZCTAPolygons(zctaPolygonFile)
    centerPoint = {"latitude": 40.702793, "longitude":-73.965584}

    #map setup
    mapData = getHeatMapData()

    mapLayout = getHeatMapLayout(mapboxtoken, zctaGeojson, centerPoint)

    #UI application
    app.layout = html.Div(children=[
        #header
        html.Div(children =[
                html.H2(children='NYC Gentrification Trends', style={'text-align':'center'})
                ]
                , style={'height':'25px', 'background-color':'black', 'color':'white'}
                ),
        #body
        html.Div(children=[         
                html.Div(children=[
                        html.H4(children='Overview')
                        ,html.Div(id='divOverviewNone'
                                , children='Hover over an area to see the overview'
                                , style={'font-style':'italic'})
                        ], style={'width':'28%', 'text-align':'left', 'float':'right'}),
            
                dcc.Graph(
                        id = 'zctaheatmap',
                        style={'height':'90vh', 'width':'70%', 'float':'left'},
                        figure=dict(data=mapData, layout=mapLayout)
                        )
                ], style={'width':'100%'})
    ], style={'width':'100%', 'height':'100%', 'padding':'0px'})

    return app


def getZCTAPolygons(fileLocation):
    #get geojson for zcta areas
    geofile = open(fileLocation)
    geojsonlayer = json.load(geofile)
    geofile.close()
    
    return geojsonlayer

def getHeatMapData():
    return go.Data([
            go.Scattermapbox(
                    lat=[],
                    lon=[], #this is for markers right now, figure out how to do hover
                    mode='markers'
                    )
            ])
            
def getHeatMapLayout(mapboxtoken, polygons, centerPoint):
    return go.Layout(
            height=800,
            autosize=True,
            margin = dict(l = 0, r = 0, t = 0, b = 0),
            hovermode='closest',
            mapbox=dict(
                    layers=[
                            dict(
                                    sourcetype = 'geojson',
                                    source = polygons,
                                    type = 'fill',
                                    color = 'rgba(200,22,10,0.8)'
                                    )
                            ],
                    accesstoken=(mapboxtoken),
                    bearing=0,
                    center=dict(
                                lat=centerPoint["latitude"],
                                lon=centerPoint["longitude"]
                                ),
                    pitch=0,
                    zoom=9.95,
                    style='light'
                    )
                )
                    
