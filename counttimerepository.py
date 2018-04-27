# -*- coding: utf-8 -*-
"""
@author TT
"""

import os

import FileHelper as fh
import analysishelpers as ah

import pandas as pd

#DOB permits
def getDOBPermitData():
    fileName = os.getcwd() + "/mysite/Datafiles/DOBPermitIssuance.csv"
    return fh.readInCSVPandasProcessing(fileName, -1, processYearMonthCountData)

    
def getDOBPermitZcta(zcta):
    data = dobPermitCounts
    return ah.filterByZcta(data, zcta, 'ZCTA')

#food permits
def getFoodPermitData():
    fileName = os.getcwd() + "/mysite/Datafiles/foodPermits.csv"
    return fh.readInCSVPandasProcessing(fileName, -1, processYearMonthCountData)

    
def getFoodPermitZcta(zcta):
    data = foodPermitCounts
    return ah.filterByZcta(data, zcta, 'ZCTA')

#sidewalk permits
def getSidewalkPermitData():
    fileName = os.getcwd() + "/mysite/Datafiles/sidewalkCoffeeshop.csv"
    return fh.readInCSVPandasProcessing(fileName, -1, processYearMonthCountData)

    
def getSidewalkPermitZcta(zcta):
    data = sidewalkPermitCounts
    return ah.filterByZcta(data, zcta, 'ZCTA')

#processing
def processYearMonthCountData(df):
    df['date'] = pd.to_datetime(df["Year-Month"],format='%Y-%m')
    df = df.set_index(['date'])
    
    dfclean = df.rename(index=str, columns={'ZCTAcount':'y'})
    dfclean = dfclean.loc[:, ['ZCTA', 'y']]
    
    return dfclean.sort_index()

dobPermitCounts = getDOBPermitData()
foodPermitCounts= getFoodPermitData()
sidewalkPermitCounts= getSidewalkPermitData()