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
import pandas as pd

#classes
import zctaoverview as zo

def runMapPage(app):
    #constants
    mapboxtoken = 'pk.eyJ1IjoidHRob21haWVyIiwiYSI6ImNqZjduZzkzdjF6d2wyd2xubTI3djN4cGwifQ.3-bkCbF2NAzEyTsqK3okWg'
    zctaPolygonFile = os.getcwd() + "/mysite/Datafiles/Map/nyczipcodetabulationareas.geojson"
    zctaRentIndexFile = os.getcwd() + "/mysite/Datafiles/withZCTA_MockRentIndex.csv"
    
    zctaGeojson = getZCTAPolygons(zctaPolygonFile)
    zctaZips, zctaLats, zctaLongs = getZCTADataFromGeojson(zctaGeojson)
    
    centerPoint = {"latitude": 40.702793, "longitude":-73.965584}

    #dynamic constants
    CURRENT_ZCTA = zo.ZCTAOverview('', 0, '', 0)
    
    #data
    genOverviewData = pd.read_csv(zctaRentIndexFile)
    
    #map setup
    mapData = getHeatMapData(zctaZips, zctaLats, zctaLongs)

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
#                dcc.RangeSlider(
#                        marks={i: i['year'] for i in genData},
#                        min=min(genData['year']),
#                        max=max(genData['year']),
#                        value=[min(genData), max(genData)]
#                        )
#                
                html.Div(children=[
                        html.H4(children='Overview')
                        ,html.P(id='divOverviewTitle'
                                , children='Hover over an area to view'
                                , style={'font-style':'italic'})
                        ,html.Div(id="divOverviewData"
                                  , children=[
                                          html.P(CURRENT_ZCTA.CombinedLabel(), id='zctaNbh')
                                          ,html.P("Borough: " + CURRENT_ZCTA.Boro, id='boroVal')
                                          ,html.P("Change in rental price: " + str(CURRENT_ZCTA.GenIndex), id='genIndexVal')
                                          ]
                                  , style={})
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

def getZCTADataFromGeojson(zctaGeojson):
    zctaZips = []
    zctaLats=[]
    zctaLongs=[]
    for item in zctaGeojson['features']:
        pItem = item['properties']
        zctaZips.append(pItem['postalCode'])
        zctaLats.append(pItem['latitude'])
        zctaLongs.append(pItem['longitude'])
    
    return zctaZips, zctaLats, zctaLongs

def getHeatMapData(texts, lats, longs):
    return go.Data([
            go.Scattermapbox(
                    lat=lats,
                    lon=longs, #this is for markers right now, figure out how to do hover
                    mode='markers',
                    text=texts
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
                    
