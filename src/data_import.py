import pandas as pd
import numpy as numpy
import os

dir = os.path.dirname(__file__)

FARE_ATTRIBUTES = pd.read_csv(os.path.join(dir,'../data/fare_attributes.txt'),
    dtype = {
        'fare_id' : numpy.str,
        'price' : numpy.float,
        'currency_type' : numpy.str,
        'payment_method' : numpy.int32,
        'transfers' : numpy.int32 })

FARE_RULES = pd.read_csv(os.path.join(dir,'../data/fare_rules.txt'),
    dtype = {
        'fare_id' : numpy.str,
        'route_id' : numpy.int32 })

ROUTES = pd.read_csv(os.path.join(dir,'../data/routes.txt'),
    dtype = {
        'route_id' : numpy.int32,
        'route_short_name' : numpy.str,
        'route_long_name' : numpy.str,
        'route_desc' : numpy.str,
        'route_type' : numpy.int32 }).sort_values('route_id')

SHAPES = pd.read_csv(os.path.join(dir,'../data/shapes.txt'),
    dtype = {
        'shape_id' : numpy.str,
        'shape_pt_lat' : numpy.float,
        'shape_pt_lon' : numpy.float,
        'shape_pt_sequence' : numpy.int32 })

STOP_TIMES = pd.read_csv(os.path.join(dir,'../data/stop_times.txt'),
    dtype = {
       'trip_id' : numpy.str,
       'arrival_time' : numpy.str,
       'departure_time' : numpy.str,
       'stop_id' : numpy.str,
       'stop_sequence' : numpy.int32,
       'pickup_type' : numpy.int32,
       'drop_off_type' : numpy.int32,
       'timepoint' : numpy.int32 })

STOPS = pd.read_csv(os.path.join(dir,'../data/stops.txt'),
    dtype = {
        'stop_id' : numpy.str,
        'stop_name' : numpy.str,
        'stop_desc' : numpy.str,
        'stop_lat' : numpy.float,
        'stop_lon' : numpy.float })

TRIPS = pd.read_csv(os.path.join(dir,'../data/trips.txt'),
    dtype = {
        'route_id' : numpy.int32,
        'service_id' : numpy.str,
        'trip_id' : numpy.str,
        'trip_headsign' : numpy.str,
        'direction_id' : numpy.int32,
        'shape_id' : numpy.str })

# print(ROUTES[ROUTES['route_id'] == 3])

# print(pd.merge(STOPS[['stop_lat' , 'stop_lon', 'stop_id']], STOP_TIMES[['trip_id', 'stop_id']][STOP_TIMES['trip_id'] == '1T0'], on='stop_id'))