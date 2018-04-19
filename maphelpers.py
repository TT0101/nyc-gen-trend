# -*- coding: utf-8 -*-
"""

@author: TT
"""
import numpy as np

"""
    adapted from the solution found at: https://community.plot.ly/t/scattermapbox-setting-visible-range/6140/3
    source: https://stackoverflow.com/questions/6048975/google-maps-v3-how-to-calculate-the-zoom-level-for-a-given-bounds
    :param bounds: list of ne and sw lat/lon
    :param mapDim: dictionary with image size in pixels
    :return: zoom level to fit bounds in the visible area
"""

def latRad(lat):
    sin = np.sin(lat * np.pi / 180)
    radX2 = np.log((1 + sin) / (1 - sin)) / 2
    return max(min(radX2, np.pi), -np.pi) / 2

def zoom(mapPx, worldPx, fraction):
    return round(np.log(mapPx / worldPx / fraction) / np.log(2), 2) - 0.15
    #changed floor to round because zoom can handle partial zoom amounts and that will hopefully get it closer to fitting
    # - amount is to get a small buffer without resorting to making 16.7 16 for example
    
def getBoundsZoomLevel(bounds, mapDim):
   
    ne_lat = bounds[1][0] #different input format
    ne_long = bounds[1][1]
    sw_lat = bounds[0][0]
    sw_long = bounds[0][1]

    scale = 2 # adjustment to reflect MapBox base tiles are 512x512 vs. Google's 256x256
    WORLD_DIM = {'height': 256 * scale, 'width': 256 * scale}
    ZOOM_MAX = 18

    latFraction = (latRad(ne_lat) - latRad(sw_lat)) / np.pi

    lngDiff = ne_long - sw_long
    lngFraction = ((lngDiff + 360) if lngDiff < 0 else lngDiff) / 360

    latZoom = zoom(mapDim['height'], WORLD_DIM['height'], latFraction)
    lngZoom = zoom(mapDim['width'], WORLD_DIM['width'], lngFraction)

    return min(latZoom, lngZoom, ZOOM_MAX)
