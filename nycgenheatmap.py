# -*- coding: utf-8 -*-
"""
@author Theresa Thomaier
"""

#overall imports
import localMain as app
#import main as app #enable this to run on server
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
#import json
import os
import pandas as pd

#classes
import zctaoverview as zo
import zctapolygons as zpoly

import indexcolors as ic
import FileHelper as fh
import TypeHelper as th

def runMapPage():
    #constants
    mapboxtoken = 'pk.eyJ1IjoidHRob21haWVyIiwiYSI6ImNqZjduZzkzdjF6d2wyd2xubTI3djN4cGwifQ.3-bkCbF2NAzEyTsqK3okWg'
    zctaRentIndexFile = os.getcwd() + "/mysite/Datafiles/withZCTA_MockRentIndex.csv"
    zctaStaticFile = os.getcwd() + "/mysite/Datafiles/zip_to_zcta10_nyc_with_NBH.csv"
    
    centerPoint = {"latitude": 40.702793, "longitude":-73.965584}

    #data
    genOverviewData = fh.readInCSVDicData(zctaRentIndexFile, processOverviewData)
    allZCTAWithNBH = fh.readInCSVDicData(zctaStaticFile, processStaticFileData)

    combinedOverviewData = mergeForMissingZCTA(genOverviewData, allZCTAWithNBH)
    
    zctaGeojson = zpoly.getZCTAPolygons()
    knownZips = [z.ZCTA for z in combinedOverviewData]
    polyOverviewData = zpoly.getZCTADataFromGeojson(knownZips, zctaGeojson)
    
    
    #mock for now, will deal with on hover later
    app.CURRENT_ZCTA = combinedOverviewData[0]
    
    #map setup
    mapData = getHeatMapData(polyOverviewData)

    mapLayout = getHeatMapLayout(mapboxtoken, polyOverviewData, centerPoint, combinedOverviewData)

    #UI application
    #app.layout = html.Div(children=[
    pLayout = html.Div(children=[
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
                                          html.P(dcc.Markdown("**Zip Code Tabulation Area (ZCTA)**: " + str(app.CURRENT_ZCTA.ZCTA)), id='zcta')
                                          ,html.P(dcc.Markdown("**Neighborhood(s)**: " + app.CURRENT_ZCTA.Neighborhood), id="nbh")
                                          ,html.P(dcc.Markdown("**Borough**: " + app.CURRENT_ZCTA.Boro), id='boroVal')
                                          ,html.P(dcc.Markdown("**Gentrification index**: " + str(app.CURRENT_ZCTA.GenIndex)), id='genIndexVal')
                                          ,dcc.Link('Go To Dashboard >>', href="/details", style={"color": "navy", "text-decoration": "underline", "cursor":"pointer"})
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
                

    return pLayout
    #return app

#processing
def processOverviewData(fileList):
    data = []
    rowCount = 0
    for line in fileList:
        if rowCount > 0:
            ov = zo.ZCTAOverview(line['boroLabel'], line['zcta'], line['nbhLabel'], line['PctChange'])
            data.append(ov)
        rowCount += 1
    
    return data

def processStaticFileData(fileList):
    data = []
    rowCount = 0
    for line in fileList:
        if rowCount > 0:
            cleanZip = th.cleanInts(line['zcta5'])
            if len(line['zcta5']) == 5 and cleanZip != 0 and cleanZip not in [z.ZCTA for z in data]:
                ov = zo.ZCTAOverview(line['boro'], line['zcta5'], line['neighborhoodlabel'], 0.0)
                data.append(ov)
        rowCount += 1
    
    return data

def mergeForMissingZCTA(indexData, zctaData):
    zctasWIndex = [i.ZCTA for i in indexData]
    missing = [z for z in zctaData if z.ZCTA not in zctasWIndex]
    return indexData + missing
    
#functions
def getOverviewForZCTA(zcta, overviewData):
    matching = [z for z in overviewData if z.ZCTA == zcta]
    
    if len(matching) > 0:
        return matching[0]
    
    return zo.ZCTAOverview('', zcta, '', 0.0)
    
def getHeatMapData(polyObjData):
    return go.Data([
            go.Scattermapbox(
                    lat=zpoly.getLatsFromPolyData(polyObjData),
                    lon=zpoly.getLongsFromPolyData(polyObjData), 
                    mode='markers',
                    fillcolor='black',
                    text=zpoly.getZCTAsFromPolyData(polyObjData),
                    marker=dict(
                             colorscale=[item[0] for item in ic.getColorScale()],
                             color=[item[1] for item in ic.getColorScale()],
                             opacity=0.8,
                             colorbar=dict(
                                     title="Index"
                             )
                    )
                )
            ])
            
def getHeatMapLayout(mapboxtoken, polyObjData, centerPoint, zctaOverviewData):
    return go.Layout(
            height=800,
            autosize=True,
            margin = dict(l = 0, r = 0, t = 0, b = 0),
            hovermode='closest',
            mapbox=dict(
                    layers=[
                            dict(
                                    sourcetype = 'geojson',
                                    source = zpoly.getSpecificPolyInfo(p.ObjectID),
                                    type = 'fill',
                                    color = ic.getSpecificColor(getOverviewForZCTA(p.ZCTATyped, zctaOverviewData).GenIndex),
                                    opacity=0.6
                                    ) for p in polyObjData #g in zctaOverviewData
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

