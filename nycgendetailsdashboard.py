# -*- coding: utf-8 -*-
"""

"""
#overall imports
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

#import localMain as app
#import main as app #enable this to run on server
from app import app

import zctapolygons as zpoly
import indexcolors as ic
import genoverviewdata as oData
import subwaydatarepository as sdres
import schooldatarepository as scres

import TypeHelper as th
import maphelpers as mh
import config

mapboxtoken = config.mapboxtoken
zctaOverview = None 
zctaPoly = None
pointsDic = None
mapCountDic = None
genIndexColor = None

#map
mapOptions = [  
                {'label': 'Schools', 'value':'SC'}
                ,{'label': 'Subway Stations', 'value': 'SE'}
                
             ]

#graph
graphOptions = [
                        {'label': 'Rental Prices', 'value': 'RP'},
                        {'label': 'New Construction', 'value': 'NC'},
                        {'label': 'Food Permits', 'value': 'FP'},
                        {'label': 'Sidewalk Cafe Licences', 'value': 'SCL'},
                        {'label': 'School Class Sizes', 'value': 'SCS'}
                ]
    
def runDetailsDash(zcta):
    #define in globals so callbacks can use it, but we must assign here due to zcta value being needed
    global zctaOverview
    global zctaPoly
    global pointsDic
    global mapCountDic
    global genIndexColor
    
    if zcta == None:
        return html.P(children='Invalid call: ' + str(zcta))
    else:
        zctaOverview = oData.getOverviewForZCTA(th.cleanInts(zcta), oData.GENOVERVIEWDATA)
        
    #data load
    zctaPoly = zpoly.getAllPolygonsForZCTA(zctaOverview.ZCTA)
    genIndexColor = ic.getSpecificColor(zctaOverview.GenIndex)

    pointsDic = getDataWithLocationDictionary(zctaOverview)
    mapCountDic = getDataWithLocationCounts(zctaOverview)
    
    #this is mock data for now, would get from whatever is chosen in multiselect 
    x = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    y = [2,4,6,8,1,3,5,7,9]
    chartData = pd.DataFrame({'x': x, 'y': y})
    chartData.head()
    
    
    #chart
    currentChartData = getChartData(chartData)
    
    #ui
    return html.Div(children=[
        #header
        html.Div(children =[
                html.H2(children='NYC Gentrification Dashboard: ' + str(zctaOverview.ZCTA), style={'text-align':'center'})
                ]
                , style={'height':'25px', 'background-color':'black', 'color':'white'}
                ),
        #html.Br(),
        #scripts
        html.Div(id="mapScript"),
        #body
        html.Div(children=[
                #overview
                html.Div(children=[
                        dcc.Markdown('**ZCTA**: ' + str(zctaOverview.ZCTA) + '&nbsp;&nbsp;&nbsp;&nbsp;**Neighborhood(s)**: ' + zctaOverview.Neighborhood + '&nbsp;&nbsp;&nbsp;&nbsp;**Borough**: ' + zctaOverview.Boro + '&nbsp;&nbsp;&nbsp;&nbsp;**Gentrification Index**: ' + str(zctaOverview.GenIndex))       
                ], style={'width':'75%', 'float':'left', 'text-align':'left'})
                ,html.Div(children=[
                        dcc.Link('<< Go Back to Overview', href="/", style={"color": "navy", "text-decoration": "underline", "cursor":"pointer"})
                        ], style={'width':'15%', 'float':'right', 'text-align':'right'})
                #map
                ,html.Div(children=[
                         dcc.Dropdown(id='mapDataSelect',
                            options= mapOptions,
                            multi=True,
                            value=["SE"]
                        ),
                        dcc.Graph(
                        id = 'zctaRegionMap',
                        style={'height':'100%', 'width':'100%'} #figure comes from callback
                        ),
                        #html.Div(id="mapCountStats")
                        ], style={'width':'35%', 'height':'65%', 'float':'right'}),
                #graphs and charts
                html.Div(children=[
                #select time trends
                dcc.Dropdown(
                    options=graphOptions,
                    multi=True,
                    value=["RP"]
                ),
                dcc.Graph(
                            id='detailsGraph',
                            figure=dict(data=currentChartData)
                        )
                ], style={'width': '64%', 'float':'left'})
            ])
            
    ], style={'width':'100%', 'height':'100%', 'padding':'0px'})
    
    


#functions
def getDataWithLocationDictionary(zctaOverview):
    return {
             'SE': sdres.getSubwaysInBoros(zctaOverview.Boro)
            ,'SC': scres.getSchoolsInZcta(zctaOverview.ZCTA)
            }

def getDataWithLocationCounts(zctaOverview):
    return {
                'SE': sdres.getNumberOfSubwaysInZcta(zctaOverview.ZCTA),
                'SC': scres.getNumberOfSchoolsInZcta(zctaOverview.ZCTA)
            }

def getDataFromChosen(valuesChosen, data):
    return [[key, data[key]] for key in valuesChosen]
    

def getListOfCountsFormatted(dataDict):
    return ["Number of " + getPointCategoryForLayer(key) + ": " + str(dataDict[key]) for key in dataDict]
        

def getBlankMap():
    
    return go.Data([
            go.Scattermapbox(
                    mode='markers'
                    )
            ])

def repeatItemForNumberOfLats(items, dataSets):
    setCount = 0
    repeatArray = []
    for s in dataSets:
        repeatArray += [items[setCount] for item in s['lat']]
        setCount += 1

    return repeatArray


def getPointCategoryForLayer(key):
    return list(filter(lambda option: option['value'] == key, mapOptions))[0]['label'] + " (" + str(mapCountDic[key]) + ")"


#build a scattermapbox for each dataset, so this results in one loop
def getMarkerDataForLayers(data):
    return [go.Scattermapbox({
                         'lat': item[1]['latitude'].values
                         , 'lon': item[1]['longitude'].values
                         , 'text': item[1]['label'].values
                         , 'mode':'marker'
                         , 'name': getPointCategoryForLayer(item[0])
                         , 'marker': dict(color=ic.getDetailSpecificColor(item[0]),
                                          opacity=1.0,
                                          size=10)
                         })
            for item in data]

#get the map data when there's data to display
def getMapWithPoints(valuesChosen, data):
    layers = getDataFromChosen(valuesChosen, data)
    
    if len(layers) <= 0:
        return getBlankMap()
    
    return getMarkerDataForLayers(layers)

#get map layout with polygon of zcta
def getMapLayout(mapboxtoken, polygons, genColor):
    return go.Layout(
            #height=800,
            autosize=True,
            showlegend=True,
            legend=dict(orientation='h'),
            margin = dict(l = 0, r = 0, t = 0, b = 0),
            hovermode='closest',
            mapbox=dict(
                    layers=[
                            dict(
                                    sourcetype = 'geojson',
                                    source = polygons,
                                    type = 'fill',
                                    color = genColor,
                                    opacity = 0.2
                                    )
                            ],
                    accesstoken=(mapboxtoken),
                    bearing=0,
                    center=dict(
                                lat=zpoly.getCenterLatFromMultPolys(polygons),
                                lon=zpoly.getCenterLongFromMultPolys(polygons)
                                ),
                    pitch=0,
                    zoom=mh.getBoundsZoomLevel(zpoly.getMinMaxLatLongForPolygons(polygons), {'height':400, 'width':450}), #rewrite to do it my way....
                    style='light'
                    )
                )

def getChartData(data):
    return go.Data([
                go.Scatter(
                    x=data['x'],
                    y=data['y'],
                    name = 'example',
                    connectgaps=True
                )
            ])


    
#callbacks
#you HAVE to use 0.20.1 or lower version of core-components of dash for this to work. 0.21.1 introduced a bug where a re-load of the markers doesn't fully render on the map; upgrading doesn't fix this yet
@app.callback(Output('zctaRegionMap', 'figure'),
              [Input('mapDataSelect', 'value')])
def onMapDataSelected(value):
    #map
    mapLayout = getMapLayout(mapboxtoken, zctaPoly, genIndexColor)
    
    if value == None or len(value) == 0:
        mapData = getBlankMap()
    else:
        mapData = getMapWithPoints(value, pointsDic)
       
    return dict(data=mapData, layout=mapLayout)   

#
#@app.callback(Output('mapScript', 'children'),
#              [Input('mapDataSelect', 'value')])
#def loadZoomOnMapLoad(value):
#    #latLongCorners = zpoly.getMinMaxLatLongForPolygons(zctaPoly)
#    #app.scripts.append_script('document.getElementById("zctaRegionMap").fitBounds([[' + str(latLongCorners[0][0]) + ',' + str(latLongCorners[0][1]) + '],['+ str(latLongCorners[1][0]) + ',' + str(latLongCorners[1][1]) + ']]);')
#    #return html.Div(str(latLongCorners))
#    #layers = getPointsToPlot(value, pointsDic)
#    return str(ic.getSpecificColor(zctaOverview.GenIndex))