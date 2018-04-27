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
def getFoodStoreData():
    fileName = os.getcwd() + "/mysite/Datafiles/RetailFoodStoreLocation.csv"
    #added the label, latitude, and longitude columns in excel manually instead...
    return fh.readInCSVPandas(fileName, 0)

def getNumberOfFoodStormesInZcta(zcta):
    return ah.getCountByZcta(zcta, foodStores, ZCTAColName, 'label')

def getStoresInZcta(zcta):
    return ah.filterByZcta(foodStores, zcta, ZCTAColName)



#save data
foodStores = getFoodStoreData()
ZCTAColName = 'zcta'
BoroColName = 'boroLabel'
