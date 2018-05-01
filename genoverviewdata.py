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
    

def getOverviewForZCTA(zcta, overviewData):
    matching = [z for z in overviewData if z.ZCTA == zcta]
    
    if len(matching) > 0:
        return matching[0]
    
    return zo.ZCTAOverview('', zcta, '', 0.0)

#processing
def processOverviewData(fileList):
    data = []
    #rowCount = 0
    for line in fileList:
        #if rowCount > 0:
            
        lineZCTA = th.cleanInts(line['ZCTA'])
        staticData = list(filter(lambda s: s.ZCTA == lineZCTA, allZCTAWithNBH))
        if(len(staticData) > 0):
            sLine = staticData[0]
            #ov = zo.ZCTAOverview(line['boroLabel'], line['zcta'], line['nbhLabel'], line['PctChange'])
            ov = zo.ZCTAOverview(sLine.Boro, line['ZCTA'], sLine.Neighborhood, line['G.Index'])
            data.append(ov)
        #rowCount += 1
    
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
#get the main zcta file first, this isn't going to change
zctaStaticFile = os.getcwd() + "/mysite/Datafiles/zip_to_zcta10_nyc_with_NBH.csv"
allZCTAWithNBH = fh.readInCSVDicData(zctaStaticFile, processStaticFileData)

#then the index file, which needs the all zcta file to get the nbh and other data
zctaIndexFile = os.getcwd() + "/mysite/Datafiles/GIndexByZCTA.csv"
#data
genOverviewData = fh.readInCSVDicData(zctaIndexFile, processOverviewData)

GENOVERVIEWDATA = mergeForMissingZCTA(genOverviewData, allZCTAWithNBH) #load the data first so we have it
