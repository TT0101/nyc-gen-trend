# -*- coding: utf-8 -*-
"""
@author: TT
"""

def addStandardColsToData(data, latColName, longColName, labelName):
     data['latitude'] = data[latColName].apply(lambda x: x)
     data['longitude'] = data[longColName].apply(lambda x: x)
     data['label'] = data[labelName].apply(lambda x: x)
     
     return data
