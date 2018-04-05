# -*- coding: utf-8 -*-
"""

@author: theresa
"""

def getColorScale():
    return [[-1, 'rgb(0,0,10)'],[0, 'rgb(153,204,255)'],[5, 'rgb(139,185,241)'],[10,'rgb(125,167,227)'],[15,'rgb(111,148,213)'],[20,'rgb(97,130,199)'],[25,'rgb(83,111,185)'],[30,'rgb(70,93,172)'],[35,'rgb(56,74,158)'],[40,'rgb(42,56,144)'],[45,'rgb(28,37,130)'],[50,'rgb(14,19,116)'], [10000000,'rgb(0,0,102)']]


def getSpecificColor(index):
    colorsAbove = [item[1] for item in getColorScale() if item[0] >= index]
    if len(colorsAbove) > 0:
        return colorsAbove[0]
    
    return getColorScale()[-1]
    
    