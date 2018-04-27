# -*- coding: utf-8 -*-
"""
@author TT
"""

import os

import FileHelper as fh
import analysishelpers as ah

import pandas as pd

#median housing sales
def getMedianSellSqFtData():
    fileName = os.getcwd() + "/mysite/Datafiles/housingMedianSqFt.csv"
    return fh.readInCSVPandasProcessing(fileName, -1, processMedianHousingData)

    
def getMedianSellZcta(zcta):
    data = medianSellSqFoot
    return ah.filterByZcta(data, zcta, medianZCTA)


#median rental prices
def getMedianRentalSqFtData():
    fileName = os.getcwd() + "/mysite/Datafiles/housingMedianRentalSqFt.csv"
    return fh.readInCSVPandasProcessing(fileName, -1, processMedianHousingData)

    
def getMedianRentalZcta(zcta):
    data = medianRentalSqFoot
    return ah.filterByZcta(data, zcta, medianZCTA)

#processing
def processMedianHousingData(df):
    df['date'] = pd.to_datetime(df.year*10000+df.month*100+1,format='%Y%m%d')
    df = df.set_index(['date'])
    
    dfclean = df.rename(index=str, columns={'medianPrice':'y'})
    dfclean = dfclean.loc[:, ['zcta', 'y']]
    
    return dfclean.sort_index()

medianSellSqFoot = getMedianSellSqFtData()
medianRentalSqFoot = getMedianRentalSqFtData()
medianZCTA = 'zcta'
