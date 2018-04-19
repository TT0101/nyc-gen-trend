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

import TypeHelper as th
import maphelpers as mh
import config

mapboxtoken = config.mapboxtoken
zctaOverview = None 
zctaPoly = None
pointsDic = None
genIndexColor = None
    
def runDetailsDash(zcta):
    #define in globals so callbacks can use it, but we must assign here due to zcta value being needed
    global zctaOverview
    global zctaPoly
    global pointsDic
    global genIndexColor
    
    if zcta == None:
        return html.P(children='Invalid call: ' + str(zcta))
    else:
        zctaOverview = oData.getOverviewForZCTA(th.cleanInts(zcta), oData.GENOVERVIEWDATA)
        
    #data load
    zctaPoly = zpoly.getAllPolygonsForZCTA(zctaOverview.ZCTA)
    genIndexColor = ic.getSpecificColor(zctaOverview.GenIndex)

    pointsDic = getDataWithLocationDictionary(zctaOverview)
    
    
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
                            options=[
                                #{'label': 'Schools', 'value': 'S'},
                                {'label': 'Subway Stations', 'value': 'SE'},
                                #{'label': 'CitiBike Stands', 'value': 'CS'}
                            ],
                            multi=True,
                            value=["SE"]
                        ),
                        dcc.Graph(
                        id = 'zctaRegionMap',
                        style={'height':'100%', 'width':'100%'} #figure comes from callback
                        )
                        ], style={'width':'35%', 'height':'65%', 'float':'right'}),
                #graphs and charts
                html.Div(children=[
                #select time trends
                dcc.Dropdown(
                    options=[
                        {'label': 'Rental Prices', 'value': 'RP'},
                        {'label': 'New Construction', 'value': 'NC'},
                        {'label': 'Food Permits', 'value': 'FP'},
                        {'label': 'Sidewalk Cafe Licences', 'value': 'SCL'},
                        {'label': 'School Class Sizes', 'value': 'SCS'}
                    ],
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
    return {'SE': filterByNearbyBoro(sdres.subwayEntryways, zctaOverview.Boro, sdres.BoroColName)}

def getPointsToPlot(valuesChosen, data):
    layers = []
    for key in data:
        if key in valuesChosen:
            layers.append([key, data[key]])
    
    return layers

def getBlankMap():
    
    return go.Data([
            go.Scattermapbox(
                    mode='markers'
                    )
            ])


#need this to mark each set of points with a color so we can color different datasets different colors
def getColorsForLayers(data, dataSets): #pass in datasets so we don't calculate again
    #dataSets = [list(item[1]['latitude'].values.T.flatten()) for item in data] # use lat just as an index of count
    colors = [ic.getDetailSpecificColor(item[0]) for item in data]
    colorPointArray = []
    setCount = 0
    for s in dataSets:
        colorPointArray += [colors[setCount] for item in s['lat']]
        setCount += 1
    
    return colorPointArray

#build the whole marker dictionary since we can go through the array twice instead of 6 times then....
def getMarkerDataForLayers(data):
    dataSets = [{'lat':list(item[1]['latitude'].values.T.flatten()),'lon':list(item[1]['longitude'].values.T.flatten()), 'text': list(item[1]['label'].values.T.flatten())} for item in data]
    mergedData = {'lat': [], 'lon': [], 'text': []
                 , 'mode':'marker'
                 , 'marker': dict(color=getColorsForLayers(data, dataSets),
                             opacity=1.0,
                             size=10)
                 }
    
    #get rid of the sub arrays and make it one array for each
    for s in dataSets:
        for k in s:
            mergedData[k] += s[k]
    
    return mergedData

#get the map data when there's data to display
def getMapWithPoints(valuesChosen, data):
    layers = getPointsToPlot(valuesChosen, data)
    
    if len(layers) <= 0:
        return getBlankMap()
    
    return go.Data([go.Scattermapbox(getMarkerDataForLayers(layers))])

#get map layout with polygon of zcta
def getMapLayout(mapboxtoken, polygons, genColor):
    return go.Layout(
            #height=800,
            autosize=True,
            margin = dict(l = 0, r = 0, t = 0, b = 0),
            hovermode='closest',
            mapbox=dict(
                    layers=[
                            dict(
                                    sourcetype = 'geojson',
                                    source = polygons,
                                    type = 'fill',
                                    color = genColor,
                                    opacity = 0.4
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

#helpers
def filterByZcta(df, zcta, zctaColName):
    return df[df[zctaColName] == zcta]

def filterByNearbyBoro(df, boro, boroColName):
    boroList = [boro]
    if(boro == "Brooklyn"):
        boroList.append("Queens")
    elif(boro == "Queens"):
        boroList.append("Brooklyn")
    return df[df[boroColName].isin(boroList)]
    
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

#@app.callback(Output('mapScript', 'children'),
#              [Input('mapDataSelect', 'value')])
#def loadZoomOnMapLoad(value):
#    latLongCorners = zpoly.getMinMaxLatLongForPolygons(zctaPoly)
#    app.scripts.append_script('document.getElementById("zctaRegionMap").fitBounds([[' + str(latLongCorners[0][0]) + ',' + str(latLongCorners[0][1]) + '],['+ str(latLongCorners[1][0]) + ',' + str(latLongCorners[1][1]) + ']]);')
#    #return html.Div(str(latLongCorners))
#    #layers = getPointsToPlot(value, pointsDic)
#    return str(getMapWithPoints(value, pointsDic))