# -*- coding: utf-8 -*-
"""
@author Theresa Thomaier
"""

#overall imports
from app import app
#import localMain as app
#import main as app #enable this to run on server
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
#import json

#classes
import zctapolygons as zpoly

#helpers
import indexcolors as ic
import genoverviewdata as oData
import TypeHelper as th


#functions
def getHeatMapData(polyObjData, zctaOverviewData):
    return go.Data([
            go.Scattermapbox(
                    lat=zpoly.getLatsFromPolyData(polyObjData),
                    lon=zpoly.getLongsFromPolyData(polyObjData), 
                    mode='markers',
                    fillcolor='black',
                    text=zpoly.getZCTAsFromPolyData(polyObjData),
                    #customdata=zpoly.getZCTAsFromPolyData(polyObjData),
                    marker=dict(
                             color=[ic.getSpecificColor(oData.getOverviewForZCTA(p.ZCTATyped, zctaOverviewData).GenIndex) for p in polyObjData],#'navy',
                             #colorscale=ic.getColorScale(),
                             opacity=0.1,
#                             colorbar=dict(
#                                    title="Index",
#                                    x=0.935,
#                                    xpad=0,
#                                    #dtick=1,
#                                    #nticks=len(ic.getColorScale()),
#                                    tickfont=dict(
#                                        color='black'
#                                    ),
#                                    titlefont=dict(
#                                        color='black'
#                                    ),
#                                    titleside='left',
#                                    tickvals = [1, 50, 100],
#                                    ticktext = ['Low','Mid','High']
#                                )
                        )
                )
            ])
            
def getHeatMapLayout(mapboxtoken, polyObjData, centerPoint, zctaOverviewData):
    return go.Layout(
            height=800,
            autosize=True,
            showlegend=False,
            margin = dict(l = 0, r = 0, t = 0, b = 0),
            hovermode='closest',
            mapbox=dict(
                    layers=[
                            dict(
                                    sourcetype = 'geojson',
                                    source = zpoly.getSpecificPolyInfo(p.ObjectID),
                                    type = 'fill',
                                    color = ic.getSpecificColor(oData.getOverviewForZCTA(p.ZCTATyped, zctaOverviewData).GenIndex),
                                    opacity=0.8
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

#def getBlankCallbackElements():
#    return html.Div(id='zctaGenHeatMap'), html.Div(id='divOverviewData')

#genheatmapcallbacks
@app.callback(Output('divOverviewData', 'children'),
              [Input('zctaGenHeatMap', 'hoverData')])
def updateCurrentZCTA(hoverData):
    if not hoverData:
        return ""
    else:
        #return str(hoverData['points'][0]['text'])
        intZcta = th.cleanInts(hoverData['points'][0]['text'])
        if(intZcta == 0):
            return "Not Found" #hoverData['points']
            
    cZcta = oData.getOverviewForZCTA(intZcta, oData.GENOVERVIEWDATA) #change to call by zcta
        
    return [
            html.P(dcc.Markdown("**Zip Code Tabulation Area (ZCTA)**: " + str(cZcta.ZCTA)), id='zcta')
            ,html.P(dcc.Markdown("**Neighborhood(s)**: " + cZcta.Neighborhood), id="nbh")
            ,html.P(dcc.Markdown("**Borough**: " + cZcta.Boro), id='boroVal')
            ,html.P(dcc.Markdown("**Gentrification index**: " + str(cZcta.GenIndex)), id='genIndexVal')
            ,dcc.Link('Go To Dashboard >>', href="/details/" + str(cZcta.ZCTA), style={"color": "navy", "text-decoration": "underline", "cursor":"pointer"})
            #,html.P(hoverData)
            ]

@app.callback(Output('divtest', 'children'), [Input('test', 'hoverData')])
def test(hoverData):
    return "this is a test! " + str(hoverData)

#constants
mapboxtoken = 'pk.eyJ1IjoidHRob21haWVyIiwiYSI6ImNqZjduZzkzdjF6d2wyd2xubTI3djN4cGwifQ.3-bkCbF2NAzEyTsqK3okWg'
centerPoint = {"latitude": 40.702793, "longitude":-73.965584}
    
zctaGeojson = zpoly.getZCTAPolygons()
knownZips = [z.ZCTA for z in oData.GENOVERVIEWDATA]
polyOverviewData = zpoly.getZCTADataFromGeojson(knownZips, zctaGeojson)
    
#map setup
mapData = getHeatMapData(polyOverviewData, oData.GENOVERVIEWDATA)

mapLayout = getHeatMapLayout(mapboxtoken, polyOverviewData, centerPoint, oData.GENOVERVIEWDATA)
    
#actually runs the page
def runMapPage():
    #UI application
    #app.layout = html.Div(children=[
    return html.Div([
        #header
        html.Div(children=[
                html.H2(children='NYC Gentrification Trends', style={'text-align':'center'})
                ]
                , style={'height':'25px', 'background-color':'black', 'color':'white'}
                ),
        #body
        html.Div(children=[  
                html.P(id='test', children='testme!'),
                html.Div(id='divtest'),
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
                        ,html.Div(id="divOverviewData", style={})
                        ], style={'width':'28%', 'text-align':'left', 'float':'right'}),
            
                dcc.Graph(
                        id = 'zctaGenHeatMap',
                        style={'height':'90vh', 'width':'70%', 'float':'left'},
                        figure=dict(data=mapData, layout=mapLayout)
                        )
                ], style={'width':'100%'})
    ])
                

    #return pLayout

