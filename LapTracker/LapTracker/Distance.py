from __future__ import division
from math import radians, cos, sin, asin, sqrt

"""
Higher precision, slower, requires testing if the hardware can use it fast enough
"""
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km/1000

"""
Less precision, much faster, requires testing if it's enough
"""
def equirectangular_dist_approx(lon1, lat1, lon2, lat2):
	R = 6371 
	x = (lon2 - lon1) * cos( 0.5*(lat2+lat1) )
	y = lat2 - lat1
	d = R * sqrt( x*x + y*y )
	return d/1000
