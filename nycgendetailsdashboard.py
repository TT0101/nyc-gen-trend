# -*- coding: utf-8 -*-
"""

"""
#overall imports
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly import tools
import pandas as pd

#import localMain as app
#import main as app #enable this to run on server
from app import app

import zctapolygons as zpoly
import indexcolors as ic
import genoverviewdata as oData
import subwaydatarepository as sdres
import schooldatarepository as scres
import foodrepository as fres
import housingpricerepository as hpres
import counttimerepository as ctres

import TypeHelper as th
import maphelpers as mh
import config

mapboxtoken = config.mapboxtoken
zctaOverview = None 
zctaPoly = None
pointsDic = None
mapCountDic = None
chartDic = None
genIndexColor = None
mapOptions = {}
graphOptions = {}

#options for multiselects
#map
mapOptionsStore = [  
                {'label': 'Schools', 'value':'SC'}
                ,{'label': 'Subway Stations', 'value': 'SE'}
                ,{'label': 'Food Stores', 'value': 'FS'}
                
             ]

#graph
graphOptionsStore = [
                    {'label': 'Housing Prices (per Sq Ft)', 'value': 'HP', 'ytitle': 'Dollars per Sq. Ft.'},
                    {'label': 'Rental Prices (per Sq Ft)', 'value': 'RP', 'ytitle': 'Dollars per Sq. Ft.'},
                    {'label': 'DOB Permits Issued', 'value':'DP', 'ytitle': 'Number Issued'},
                    {'label': 'Food Permits', 'value': 'FP', 'ytitle': 'Number Issued'},
                    {'label': 'Sidewalk Cafe Licenses', 'value': 'SCL', 'ytitle': 'Number Issued'}
                ]
    
def runDetailsDash(zcta):
    #define in globals so callbacks can use it, but we must assign here due to zcta value being needed
    global zctaOverview
    global zctaPoly
    global pointsDic
    global mapCountDic
    global chartDic
    global genIndexColor
    global mapOptions
    global graphOptions
    
    if zcta == None:
        return html.P(children='Invalid call: ' + str(zcta))
    else:
        zctaOverview = oData.getOverviewForZCTA(th.cleanInts(zcta), oData.GENOVERVIEWDATA)
        
    #data load
    zctaPoly = zpoly.getAllPolygonsForZCTA(zctaOverview.ZCTA)
    genIndexColor = ic.getSpecificColor(zctaOverview.GenIndex)

    #data dictionaries
    pointsDic = getDataWithLocationDictionary(zctaOverview)
    mapCountDic = getDataWithLocationCounts(zctaOverview)
    chartDic = getDataForChartsDictionary(zctaOverview)
    
    #remove options not avaliable
    foundPointData = [key for key in pointsDic if len(pointsDic[key]) > 0]
    foundChartData = [key for key in chartDic if len(chartDic[key]) > 0]
    mapOptions = [item for item in mapOptionsStore if item['value'] in foundPointData]
    graphOptions = [item for item in graphOptionsStore if item['value'] in foundChartData]
    
    #get default option
    if(len(foundPointData) > 0):
        mapDefault = "SE" if "SE" in foundPointData else foundPointData[0]
    else:
        mapDefault = ""
        
    if(len(foundChartData) > 0):
        chartDefault = "HP" if "HP" in foundChartData else foundChartData[0]
    else:
        chartDefault = ""
        
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
                            value=[mapDefault]
                        ),
                        dcc.Graph(
                        id = 'zctaRegionMap',
                        style={'height':'100%', 'width':'100%'} #figure comes from callback
                        ),
                        ], style={'width':'35%', 'height':'75vh', 'float':'right'}),
                #graphs and charts
                html.Div(children=[
                #select time trends
                dcc.Dropdown(
                    id='chartDataSelect',
                    options=graphOptions,
                    multi=True,
                    value=[chartDefault]
                ),
                dcc.Graph(id='detailsGraph')
                ], style={'width': '64%', 'float':'left', 'height':'75vh'})
            ])
            
    ], style={'width':'100%', 'height':'100%', 'padding':'0px'})
    
    


#functions                
#set up all the data for the zcta chosen
def getDataWithLocationDictionary(zctaOverview):
    return {
             'SE': sdres.getSubwaysInBoros(zctaOverview.Boro)
            ,'SC': scres.getSchoolsInZcta(zctaOverview.ZCTA)
            , 'FS': fres.getStoresInZcta(zctaOverview.ZCTA)
            }

def getDataWithLocationCounts(zctaOverview):
    return {
                'SE': sdres.getNumberOfSubwaysInZcta(zctaOverview.ZCTA),
                'SC': scres.getNumberOfSchoolsInZcta(zctaOverview.ZCTA),
                'FS': fres.getNumberOfFoodStormesInZcta(zctaOverview.ZCTA)
            }

def getDataForChartsDictionary(zctaOverview):
    return {
                'HP': hpres.getMedianSellZcta(zctaOverview.ZCTA)
                ,'RP': hpres.getMedianRentalZcta(zctaOverview.ZCTA)
                ,'DP': ctres.getDOBPermitZcta(zctaOverview.ZCTA)
                ,'FP':ctres.getFoodPermitZcta(zctaOverview.ZCTA)
                ,'SCL':ctres.getSidewalkPermitZcta(zctaOverview.ZCTA)
            }

#helpers
#used to get labels and titles for the key
def getLabelForMultiKey(key, options):
    matching = list(filter(lambda option: option['value'] == key, options))
    if(len(matching)>0):
        return matching[0]
    
    return [{'label': '', 'ytitle': ''}]

#gets the keys and values from the dictionaries based on the items chosen
def getDataFromChosen(valuesChosen, data):
    return [[key, data[key]] for key in valuesChosen]

#all the map stuff below
def getBlankMap():
    return go.Data([
            go.Scattermapbox(
                    mode='markers'
                    )
            ])

#gets the legend with the number of items in the zcta for the map
def getPointCategoryForLayer(key):
    return getLabelForMultiKey(key, mapOptions)['label'] + " (" + str(mapCountDic[key]) + ")"


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

#build charts based on chosen values
def getLinePlot(values, dataDic):
    #lineOptions = ['HP', 'RP', 'DP', 'FP','SCL']
    valuesChosen = values#[val for val in values if val in lineOptions]
    lineSets = getDataFromChosen(valuesChosen, dataDic)
    if(len(lineSets) == 0):
        return getBlankChart()
    
    return [[go.Scatter(
                    x=item[1].index
                    ,y=item[1]['y']
                    ,connectgaps=True
                    ,mode='lines'
                    ,line=dict(shape='spline')
                    ,name=getLabelForMultiKey(item[0], graphOptions)['label']
            ),
            getLabelForMultiKey(item[0], graphOptions)['ytitle']
            ]
            for item in lineSets if len(item[1]) > 0] 

def getBlankChart():
    return ''

def getLineChartData(values, dataDic):
    lineChart = getLinePlot(values, dataDic)
    lineChartLength = len(lineChart)
    
    if lineChartLength == 0:
        return getBlankChart()
    else:
        #make subplots out of it (should work with one as well)
        fig = tools.make_subplots(rows=lineChartLength, cols=1, shared_xaxes=True, vertical_spacing=0.1)
        c = 1
        for t in lineChart:
            fig.append_trace(t[0], c, 1)
            fig['layout']['yaxis' + str(c)].update(title=t[1])
            c += 1
            
        return fig
    
    
#callbacks
@app.callback(Output('detailsGraph', 'figure'),
              [Input('chartDataSelect', 'value')])
def onChartDataSelected(values):
    if values == None or len(values) == 0:
        chartData = getBlankChart()
    else:
        chartData = getLineChartData(values, chartDic)
        
    return dict(data=chartData)

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

##
@app.callback(Output('mapScript', 'children'),
              [Input('chartDataSelect', 'value')])
def loadZoomOnMapLoad(value):

    return ''#str([[key, len(chartDic[key])] for key in chartDic])