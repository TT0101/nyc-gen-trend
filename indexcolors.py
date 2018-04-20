# -*- coding: utf-8 -*-
"""

@author: theresa
"""

def getColorScale():
    #return [[0, 'rgb(153,204,255)'],[5, 'rgb(139,185,241)'],[10,'rgb(125,167,227)'],[15,'rgb(111,148,213)'],[20,'rgb(97,130,199)'],[25,'rgb(83,111,185)'],[30,'rgb(70,93,172)'],[35,'rgb(56,74,158)'],[40,'rgb(42,56,144)'],[45,'rgb(28,37,130)'],[50,'rgb(14,19,116)'], [100,'rgb(0,0,102)']]
    #return [[0.0, 'rgb(153,204,255)'],[0.1, 'rgb(139,185,241)'],[0.2,'rgb(125,167,227)'],[0.3,'rgb(111,148,213)'],[0.4,'rgb(97,130,199)'],[0.5,'rgb(83,111,185)'],[0.6,'rgb(70,93,172)'],[0.7,'rgb(56,74,158)'],[0.8,'rgb(42,56,144)'],[0.9,'rgb(28,37,130)'],[1.0,'rgb(14,19,116)']]
    return [[0.0, '#f7fbff'],[0.1, '#deebf7'],[0.2,'#c6dbef'],[0.3,'#9ecae1'],[0.4,'#6baed6'],[0.5,'#4292c6'],[0.6,'#2171b5'],[0.7,'#08519c'],[0.8,'#08306b'],[0.9,'#052047'],[1.0,'#020b18']]
    

def getSpecificColor(index):
    decIndex = index/100
    colorsAbove = [item[1] for item in getColorScale() if item[0] >= decIndex]
    if len(colorsAbove) > 0:
        return colorsAbove[0]
    
    return 'rgb(0,0,10)'
    
def getDetailColorScale():
    return [['SE', '#015409'], ['SC', '#bc8700']]

def getDetailSpecificColor(index):
    return [item[1] for item in getDetailColorScale() if item[0] == index][0]