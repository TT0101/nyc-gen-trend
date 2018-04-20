# -*- coding: utf-8 -*-
"""

@author: TT
"""

import os

import FileHelper as fh

#functions
def getSchoolLocationData():
    fileName = os.getcwd() + "/mysite/Datafiles/School_Locations.csv"
    #added the label, latitude, and longitude columns in excel manually instead...
    return fh.readInCSVPandas(fileName, 0)

#save data
schoolLocations = getSchoolLocationData()
ZCTAColName = 'zcta'
BoroColName = 'boroLabel'
