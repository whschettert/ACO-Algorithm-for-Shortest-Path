import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import data_import as data
import util as util
import maps as mpx
import Queue
import astar as ast

class Graph:

    def __init__(self):
        self.graph = nx.DiGraph()
        # self.nodes_dict = dict()
        # self.nodes_dict_rev = dict()

    def build_graph_stop_points(self, max_routes):
        lastNode = None

        if (max_routes > 0):
            routes = data.ROUTES.head(max_routes)
        else:
            routes = data.ROUTES

        for rt in routes.values:
            
            # duas viagens para cada rota, uma de ida e outra de volta(algumas rotas nao possuem volta)
            trip0 = data.TRIPS[(data.TRIPS['route_id'] == rt[0]) & (data.TRIPS['direction_id'] == 0)].head(1)
            trip1 = data.TRIPS[(data.TRIPS['route_id'] == rt[0]) & (data.TRIPS['direction_id'] == 1)].head(1)

            trips = pd.concat([trip0, trip1]).values

            for tr in trips:
                
                # join entre registro da tabela de paradas(infos geograficas) e tempo de paradas(timestamp)
                stops = pd.merge(data.STOPS, data.STOP_TIMES[data.STOP_TIMES['trip_id'] == tr[2]], on='stop_id').sort_values('stop_sequence').values

                for st in stops:

                    self.graph.add_node(st[0], pos=(st[3], st[4]), data=st)

                    if lastNode is not None:
                        wgt = util.haversine(lastNode[4], lastNode[3], st[4], st[3])
                        time = util.time_diff(lastNode[7], st[7])
                        if lastNode[0] != st[0]:
                            self.graph.add_edge(lastNode[0], st[0], weight=wgt, travelTime=time)

                    lastNode = st

            lastNode = None
        
        # verifica se ha paradas proximas(<=300)
        for node in self.graph.node:

            node_data = self.graph.node[node]['data']
            
            n, dist = util.medium_point(self.graph, node_data)

            if n and not self.nodes_connected(node, n['data'][0]) and not self.nodes_connected(n['data'][0], node):
                time = dist / 0.00166667
                # duas arestas direcionais
                self.graph.add_edge(node_data[0], n['data'][0], weight=dist, travelTime=time)
                self.graph.add_edge(n['data'][0], node_data[0], weight=dist, travelTime=time)

    def nodes_connected(self, n1, n2):
        return n1 in self.graph.neighbors(n2)

    def astar(self, n1, n2, weight='weight'):
        resp = None
        length = None

        try:

            if weight == 'weight':
                resp = nx.astar_path(self.graph, n1, n2, self.h_dist, weight)
                length = nx.astar_path_length(self.graph, n1, n2, self.h_dist, weight)
            else:
                resp = nx.astar_path(self.graph, n1, n2, self.h_time, weight)
                length = nx.astar_path_length(self.graph, n1, n2,  self.h_time, weight)

        except nx.NetworkXNoPath:
             print 'Nao ha caminho entre os nodos'
             resp = []
        finally:
            return resp, length

    def get_graph(self):
        return self.graph

    def save(self):
        f = open('graph.txt', 'w') 

        # nodes = json.dumps(self.graph)

        # edges = self.graph.edges()
        
        # for n in self.graph.node:
        #     node = self.graph.node[n]    

    # def read(self):
    #     dg = pickle.load(open('/tmp/graph.txt'))
    #     print dg.edges()

    def get_pos(self):
        arr = []
        for n in self.graph.node:
            node = self.graph.node[n]
            arr.append([ node['pos'][0], node['pos'][1] ])
        
        return arr

    def h_dist(self, a, b):
        n1 = self.graph.node[a]['data']
        n2 = self.graph.node[b]['data']
        return util.haversine(n1[3], n1[4], n2[3], n2[4])

    def h_time(self, a, b):
        # distancia em km
        dist = self.h_dist(a, b)

        # velocidade media em km/h
        med_speed = 24

        # tempo de viagem em segundos
        return (dist / med_speed) * 3600

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