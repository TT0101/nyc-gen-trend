# -*- coding: utf-8 -*-
"""

@author: theresa
"""
import json
import os

import TypeHelper as th

class ZCTAPolyOverview:
    ObjectID = ''
    ZCTA = ''
    ZCTATyped = 0
    Latitude = ''
    Longitude = ''
    
    def __init__(self, objectID, zcta, lat, long):
        self.ObjectID = objectID
        self.ZCTA = zcta
        self.ZCTATyped = th.cleanInts(zcta)
        self.Latitude = lat
        self.Longitude = long
    

def getZCTAPolygons():
    fileLocation = os.getcwd() + "/mysite/Datafiles/Map/nyczipcodetabulationareas.geojson"
    #get geojson for zcta areas
    geofile = open(fileLocation)
    geojsonlayer = json.load(geofile)
    geofile.close()
    
    return geojsonlayer

def getZCTADataFromGeojson(knownData, zctaGeojson):
    
    zctaPolyData = []
    for item in zctaGeojson['features']:
        pItem = item['properties']
        if th.cleanInts(pItem['postalCode']) in knownData:
            zctaPolyData.append(ZCTAPolyOverview(pItem['OBJECTID'], pItem['postalCode'], pItem['latitude'],pItem['longitude']))
    
    return zctaPolyData

def getZCTAsFromPolyData(data):
    return [p.ZCTA for p in data]

def getLatsFromPolyData(data):
    return [p.Latitude for p in data]

def getLongsFromPolyData(data):
    return [p.Longitude for p in data]

def getCenterLatFromMultPolys(polys):
    lats = []
    for p in polys['features']:
        lats.append(p['properties']['latitude'])
    
    if len(lats) == 0:
        return 0
    
    return lats[0] #fix this to calcualte the middle if more than one later

def getCenterLongFromMultPolys(polys):
    longs = []
    for p in polys['features']:
        longs.append(p['properties']['longitude'])
    if len(longs) == 0:
        return 0
    
    return longs[0]

def getSpecificPolyInfo(objID):
    zctaGeojson = getZCTAPolygons()
    
    for item in zctaGeojson['features']:
        pItem = item['properties']
        if(str(pItem['OBJECTID']) == str(objID)): 
            return item
    
    return {'properties':{'latitude':0.0, 'longitude':0.0}}

def getAllPolygonsForZCTA(zctaVal):
    zctaGeojson = getZCTAPolygons()
    
    matching = []
    for item in zctaGeojson['features']:
        pItem = item['properties']
        if(str(pItem['postalCode']) == str(zctaVal)): 
            matching.append(item)
    
    return {"type": "FeatureCollection", "features": matching } 