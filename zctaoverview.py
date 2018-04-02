# -*- coding: utf-8 -*-
"""

"""

import TypeHelper as th

class ZCTAOverview:
    Boro = ''
    ZCTA = 0
    Neighborhood = ''
    GenIndex = 0.0
    
    def __init__(self, boro, zcta, nbh, genIndex):
        self.Boro = boro
        self.ZCTA = th.cleanInts(zcta)
        self.Neighborhood = nbh
        self.GenIndex = th.cleanFloats(genIndex)
    
    def CombinedLabel(self):
        return str(self.ZCTA) + " - " + self.Neighborhood