# -*- coding: utf-8 -*-
"""

@author: TT
"""

import os

import FileHelper as fh
import analysishelpers as ah

#functions
def getSchoolLocationData():
    fileName = os.getcwd() + "/mysite/Datafiles/School_Locations.csv"
    #added the label, latitude, and longitude columns in excel manually instead...
    return fh.readInCSVPandas(fileName, 0)

def getNumberOfSchoolsInZcta(zcta):
    return ah.getCountByZcta(zcta, schoolLocations, ZCTAColName, 'label')

def getSchoolsInZcta(zcta):
    return ah.filterByZcta(schoolLocations, zcta, ZCTAColName)

#save data
schoolLocations = getSchoolLocationData()
ZCTAColName = 'zcta'
BoroColName = 'boroLabel'
