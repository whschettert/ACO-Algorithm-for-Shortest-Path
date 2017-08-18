import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import data_import as data
import util as util
import maps as mp

class Graph:

    def __init__(self):
        self.graph = nx.Graph()

    def build_generic(self, max_routes):
        #TODO: considerar duas trips(direction=0 & direction=1)

        lastNode = None

        if (max_routes > 0):
            routes = data.ROUTES.head(max_routes)
        else:
            routes = data.ROUTES

        for rt in routes.values:
            
            trip = data.TRIPS[data.TRIPS['route_id'] == rt[0]].head(1).values

            stops = pd.merge(data.STOPS, data.STOP_TIMES[data.STOP_TIMES['trip_id'] == trip[0][2]], on='stop_id').sort_values('stop_sequence').values

            for st in stops:

                node = util.mediumPoint(self.graph, st[3], st[4])

                if node is None:
                    self.graph.add_node(st[0], pos=(st[3],st[4]))
                    node = st[0]

                if (lastNode is not None):
                    wgt = util.haversine(lastNode[3], lastNode[4], st[3], st[4])
                    self.graph.add_edge(lastNode[0], st[0], weight=wgt)


            lastNode = None

    def build_graph_stop_points(self, max_routes):
        lastNode = None

        if (max_routes > 0):
            routes = data.ROUTES.head(max_routes)
        else:
            routes = data.ROUTES

        for rt in routes.values:
            
            trip = data.TRIPS[(data.TRIPS['route_id'] == rt[0]) & (data.TRIPS['direction_id'] == 0)].head(1).values

            #trip2 = data.TRIPS[(data.TRIPS['route_id'] == rt[0]) & (data.TRIPS['direction_id'] == 1)].head(1).values

            stops = pd.merge(data.STOPS, data.STOP_TIMES[data.STOP_TIMES['trip_id'] == trip[0][2]], on='stop_id').sort_values('stop_sequence').values

            #stops2 = pd.merge(data.STOPS, data.STOP_TIMES[data.STOP_TIMES['trip_id'] == trip2[0][2]], on='stop_id').sort_values('stop_sequence').values

            for st in stops:

                # procura parada proxima a atual
                n = util.medium_point(self.graph, st)

                if n == False:
                    n = st
                    self.graph.add_node(n[0], pos=(n[3], n[4]), data=n, nodes=[])
                else:
                    n = n['data']
                    self.graph.node[n[0]]['nodes'].append(st)

                if lastNode is not None:
                    wgt = util.haversine(lastNode[4], lastNode[3], n[4], n[3])
                    if lastNode[0] != n[0]:
                        self.graph.add_edge(lastNode[0], n[0], weight=wgt)

                lastNode = n

            lastNode = None

    def astar(self):
        resp = nx.astar_path(self.graph, '1S0', '3S2', self.h)
        print resp

    def h(self, a, b):
        n1 = self.graph.node[a]['data']
        n2 = self.graph.node[b]['data']
        return util.haversine(n1[3], n1[4], n2[3], n2[4])

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
            labels = nx.get_edge_attributes(self.graph,'weight')
            nx.draw_networkx_edge_labels(self.graph, pos,edge_labels=labels)

            plt.xlabel('Latitude', fontsize=23)
            plt.ylabel('Longitude', fontsize=23)

            plt.show()
        else:
            print('Nodes :', len(self.graph))