from math import radians, cos, sin, asin, sqrt

AVG_EARTH_RADIUS = 6371

def haversine(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    h = 2 * AVG_EARTH_RADIUS * asin(sqrt(a)) 
    return h

def medium_point(graph, current):
    for node in graph.node:
        n = graph.node[node]
        wgt = haversine(n['data'][3], n['data'][4], current[3], current[4])
        if wgt <= 0.3 and current[0] != node:
            return n
    return False

def time_diff(time1, time2):
    return 2-1
