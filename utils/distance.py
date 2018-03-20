#! /usr/bin/env python3
import math


def get_distance(lat1, lat2, lon1, lon2) -> float:
    ''' derive the spherical distance between two points '''
    RADIUS = 6731
    print('{0}, {1}, {2}, {3}'.format(lat1, lat2, lon1, lon2))

    def haversine(x):
        return pow(math.sin(x/2), 2)

    def radians(d):
        return d * (math.pi/180)

    lat_deg = haversine(radians(lat2 - lat1))
    lon_deg = haversine(radians(lon2 - lon1))

    v = math.cos(radians(lat1)) * math.cos(radians(lat2))
    h = lat_deg + (v * lon_deg)
    c = math.atan2(math.sqrt(h), math.sqrt(1 - h)) * 2
    return c * RADIUS
