# -*- coding: utf-8 -*-
"""

@author: TT
"""

import os

import FileHelper as fh
import datadisplaycleaner as dc

#functions
def getSubwayEntrywayData():
    fileName = os.getcwd() + "/mysite/Datafiles/SUBWAY_STATION_LOCATIONS.csv"
    #added the label, latitude, and longitude columns in excel manually instead...
    return fh.readInCSVPandas(fileName, 0)

#save data
subwayEntryways = getSubwayEntrywayData()
ZCTAColName = 'zcta'
BoroColName = 'boroLabel'
