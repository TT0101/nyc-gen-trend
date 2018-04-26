# -*- coding: utf-8 -*-
"""

@author: TT
"""

import FileHelper as fh
import analysishelpers as ah

import numpy as np
import pandas as pd

#functions
def getData(filename, processingFunction):
   
    return #fh.readInCSVPandas(fileName, 0)

def getInZcta(zcta):
    return ah.filterByZcta(data, zcta, ZCTAColName)

def getInBoros(boro):
    return ah.filterByNearbyBoro(data, boro, BoroColName)

#save data
data = getData()
ZCTAColName = 'zcta'
BoroColName = 'boroLabel'
