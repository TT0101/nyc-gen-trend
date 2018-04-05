# -*- coding: utf-8 -*-
"""

"""
#overall imports
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

import localMain as app
#from main import app

import zctapolygons as zpoly
import indexcolors as ic


def runDetailsDash():
    if app.CURRENT_ZCTA == None:
        return html.P(children='Invalid call')
    else:
        zctaOverview = app.CURRENT_ZCTA
        
    #data
    mapboxtoken = 'pk.eyJ1IjoidHRob21haWVyIiwiYSI6ImNqZjduZzkzdjF6d2wyd2xubTI3djN4cGwifQ.3-bkCbF2NAzEyTsqK3okWg'
   
    zctaPoly = zpoly.getAllPolygonsForZCTA(zctaOverview.ZCTA)
    genIndexColor = ic.getSpecificColor(zctaOverview.GenIndex)

    pointsDic = getDataWithLocationDictionary(zctaOverview.ZCTA)
    
    #this is mock data for now, would get from whatever is chosen in multiselect 
    x = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    y = [2,4,6,8,1,3,5,7,9]
    chartData = pd.DataFrame({'x': x, 'y': y})
    chartData.head()
    
    #map
    mapData = getMapData(pointsDic)
    mapLayout = getMapLayout(mapboxtoken, zctaPoly, genIndexColor)
    
    #chart
    currentChartData = getChartData(chartData)
    
    #ui
    #app.layout = html.Div(children=[
    pLayout = html.Div(children=[
        #header
        html.Div(children =[
                html.H2(children='NYC Gentrification Dashboard: ' + str(zctaOverview.ZCTA), style={'text-align':'center'})
                ]
                , style={'height':'25px', 'background-color':'black', 'color':'white'}
                ),
        #html.Br(),
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
                         dcc.Dropdown(
                            options=[
                                {'label': 'Schools', 'value': 'S'},
                                {'label': 'Subway Entry', 'value': 'SE'},
                                {'label': 'CitiBike Stands', 'value': 'CS'}
                            ],
                            multi=True,
                            value="SE"
                        ),
                        dcc.Graph(
                        id = 'zctaRegionMap',
                        style={'height':'100%', 'width':'100%'},
                        figure=dict(data=mapData, layout=mapLayout)
                        )
                        ], style={'width':'35%', 'height':'50vh', 'float':'right'}),
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
                    value="RP"
                ),
                dcc.Graph(
                            id='detailsGraph',
                            figure=dict(data=currentChartData)
                        )
                ], style={'width': '64%', 'float':'left'})
            ])
    ], style={'width':'100%', 'height':'100%', 'padding':'0px'})
    
    return pLayout


#functions
def getDataWithLocationDictionary(zctaVal):
    return {}

def getMapData(pointsDic):
    
    return go.Data([
            go.Scattermapbox(
                    #lat=lats,
                    #lon=longs, 
                    mode='markers',
                    #text=texts
                    )
            ])
            
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
                                    opacity = 0.6
                                    )
                            ],
                    accesstoken=(mapboxtoken),
                    bearing=0,
                    center=dict(
                                lat=zpoly.getCenterLatFromMultPolys(polygons),
                                lon=zpoly.getCenterLongFromMultPolys(polygons)
                                ),
                    pitch=0,
                    zoom=13,
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

