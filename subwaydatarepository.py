# -*- coding: utf-8 -*-
"""

@author: TT
"""

import os

import FileHelper as fh
import analysishelpers as ah

import numpy as np
import pandas as pd

#functions
def getSubwayStationData():
    fileName = os.getcwd() + "/mysite/Datafiles/SUBWAY_STATION_LOCATIONS2.csv"
    #added the label, latitude, and longitude columns in excel manually instead...
    return fh.readInCSVPandas(fileName, 0)

def getNumberOfSubwaysInZcta(zcta):
    return ah.getCountByZcta(zcta, subwayLocations, ZCTAColName, 'label')

def getSubwaysInBoros(boro):
    return ah.filterByNearbyBoro(subwayLocations, boro, BoroColName)

#save data
subwayLocations = getSubwayStationData()
ZCTAColName = 'zcta'
BoroColName = 'boroLabel'
