# -*- coding: utf-8 -*-
"""

@author: TT
"""

import genoverviewdata as oData

#gen index
def getColorScale():
    return [[0.0, '#f7fbff'],[0.1, '#deebf7'],[0.2,'#c6dbef'],[0.3,'#9ecae1'],[0.4,'#6baed6'],[0.5,'#4292c6'],[0.6,'#2171b5'],[0.7,'#08519c'],[0.8,'#08306b'],[0.9,'#052047'],[1.0,'#020b18']]
 
def normedGenColorScale():
    maxGenIndex = oData.GetMaxGenIndex()
    minGenIndex = oData.GetMinGenIndex()
    
    seg = (maxGenIndex - minGenIndex)/10
    genColorScale = getColorScale()
    
    
    newIndex = [genColorScale[0]]
    runningIndex = minGenIndex
    for i in range(1, len(genColorScale)):
        genItem = genColorScale[i]
        runningIndex = runningIndex + seg
        newIndex.append([round(runningIndex, 4), genItem[1]])
    
    return newIndex

def getSpecificColor(index):
    normedScale = normedGenColorScale()
    colorsAbove = [item[1] for item in normedScale if item[0] >= index]
    if len(colorsAbove) > 0:
        return colorsAbove[0]
    
    return '#f7fbff'

#map points for details
def getDetailColorScale():
    return [['SE', '#00d129'], ['SC', '#f9c60c'], ['FS', '#d104cd']]

def getDetailSpecificColor(index):
    return [item[1] for item in getDetailColorScale() if item[0] == index][0]
