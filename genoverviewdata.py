# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 20:01:09 2018

@author: TNT
"""
import os

#classes
import zctaoverview as zo

import FileHelper as fh
import TypeHelper as th


#get data seperately so that we can get this first, before everything else runs
def getOverviewData():
    zctaRentIndexFile = os.getcwd() + "/mysite/Datafiles/withZCTA_MockRentIndex.csv"
    zctaStaticFile = os.getcwd() + "/mysite/Datafiles/zip_to_zcta10_nyc_with_NBH.csv"

    #data
    genOverviewData = fh.readInCSVDicData(zctaRentIndexFile, processOverviewData)
    allZCTAWithNBH = fh.readInCSVDicData(zctaStaticFile, processStaticFileData)

    return mergeForMissingZCTA(genOverviewData, allZCTAWithNBH)


def getOverviewForZCTA(zcta, overviewData):
    matching = [z for z in overviewData if z.ZCTA == zcta]
    
    if len(matching) > 0:
        return matching[0]
    
    return zo.ZCTAOverview('', zcta, '', 0.0)

#processing
def processOverviewData(fileList):
    data = []
    rowCount = 0
    for line in fileList:
        if rowCount > 0:
            ov = zo.ZCTAOverview(line['boroLabel'], line['zcta'], line['nbhLabel'], line['PctChange'])
            data.append(ov)
        rowCount += 1
    
    return data

def processStaticFileData(fileList):
    data = []
    rowCount = 0
    for line in fileList:
        if rowCount > 0:
            cleanZip = th.cleanInts(line['zcta5'])
            if len(line['zcta5']) == 5 and cleanZip != 0 and cleanZip not in [z.ZCTA for z in data]:
                ov = zo.ZCTAOverview(line['boro'], line['zcta5'], line['neighborhoodlabel'], 0.0)
                data.append(ov)
        rowCount += 1
    
    return data

def mergeForMissingZCTA(indexData, zctaData):
    zctasWIndex = [i.ZCTA for i in indexData]
    missing = [z for z in zctaData if z.ZCTA not in zctasWIndex]
    return indexData + missing

#max and min
def GetMinGenIndex():
    minObj = min(GENOVERVIEWDATA, key=lambda z: z.GenIndex)
    if minObj is not None:
        return minObj.GenIndex
    
    return 0

def GetMaxGenIndex():
    maxObj = max(GENOVERVIEWDATA, key=lambda z: z.GenIndex)
    if maxObj is not None:
        return maxObj.GenIndex
    
    return 100

#run first
GENOVERVIEWDATA = getOverviewData() #load the data first so we have it