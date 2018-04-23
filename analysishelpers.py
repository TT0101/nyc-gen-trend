# -*- coding: utf-8 -*-
"""
@author TT
"""
import numpy as np

def getCountByZcta(zcta, df, zctaColName, countColName):
    groupedData = df.groupby(zctaColName)[countColName].agg(np.count_nonzero)
    zctaData = groupedData[groupedData.index == zcta].values
    if len(zctaData) <= 0:
        return []
    
    return zctaData[0]

#filters
def filterByZcta(df, zcta, zctaColName):
    return df[df[zctaColName] == zcta]

def filterByNearbyBoro(df, boro, boroColName):
    boroList = [boro]
    if(boro == "Brooklyn"):
        boroList.append("Queens")
    elif(boro == "Queens"):
        boroList.append("Brooklyn")
    return df[df[boroColName].isin(boroList)]