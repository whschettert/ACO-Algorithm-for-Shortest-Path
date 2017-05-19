import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import data_import as data
import util as util
import maps as mp

class Graph:

    def __init__(self):
        self.graph = nx.Graph()

    def build_graph_stop_points(self, max_routes):
        lastNode = None

        if (max_routes > 0):
            routes = data.ROUTES.head(max_routes)
        else:
            routes = data.ROUTES

        for rt in routes.values:
            
            trip = data.TRIPS[data.TRIPS['route_id'] == rt[0]].head(1).values

            stops = pd.merge(data.STOPS, data.STOP_TIMES[data.STOP_TIMES['trip_id'] == trip[0][2]], on='stop_id').sort_values('stop_sequence').values

            for st in stops:
                self.graph.add_node(str(rt[0]) + '-' + str(st[8]), pos=(st[3],st[4]))

                if (lastNode is not None):
                    wgt = util.haversine(lastNode[4], lastNode[3], st[4], st[3])
                    self.graph.add_edge(str(rt[0]) + '-' + str(lastNode[8]), str(rt[0]) + '-' + str(st[8]), weight=wgt)

                lastNode = st

            lastNode = None
        
    def build_graph_shape_points(self, max_routes):
        lastNode = None
        routes = None

        if (max_routes > 0):
            routes = data.ROUTES.head(max_routes)
        else:
            routes = data.ROUTES

        for rt in routes.values:
            trip = data.TRIPS[data.TRIPS['route_id'] == rt[0]].head(1).values

            shapes = data.SHAPES[data.SHAPES['shape_id'] == trip[0][5]].sort_values(['shape_pt_sequence']).values

            for sh in shapes:
                self.graph.add_node(str(rt[0]) + '-' + str(sh[3]))

                if (lastNode is not None):
                    wgt = util.haversine(lastNode[2], lastNode[1], sh[2], sh[1])
                    self.graph.add_edge(str(rt[0]) + '-' + str(lastNode[3]), str(rt[0]) + '-' + str(sh[3]), weight=wgt)

                lastNode = sh

            lastNode = None

    def draw_map(self):
        points = []

        maps = mp.Maps()

        for rt in data.ROUTES[data.ROUTES['route_id'] == 2].head(1).values:
            
            trip = data.TRIPS[data.TRIPS['route_id'] == rt[0]].head(1).values

            stops = pd.merge(data.STOPS, data.STOP_TIMES[data.STOP_TIMES['trip_id'] == trip[0][2]], on='stop_id').sort_values('stop_sequence').values

            for st in stops:
                points.append(st)
            
            maps.draw_route(points)
            

    def draw_graph(self):
        if (len(self.graph) < 2000):
            pos = nx.get_node_attributes(self.graph,'pos')
            nx.draw_networkx(self.graph, pos)
            plt.show()
        else:
            print('Nodes :', len(self.graph))