import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import data_import as data
import util as util
import maps as mp

class Graph:

    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes_dict = dict()

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
                
                stops = pd.merge(data.STOPS, data.STOP_TIMES[data.STOP_TIMES['trip_id'] == tr[2]], on='stop_id').sort_values('stop_sequence').values

                for st in stops:

                    # procura parada proxima a atual
                    n = util.medium_point(self.graph, st)

                    if n == False:
                        n = st
                        self.graph.add_node(n[0], pos=(n[3], n[4]), data=n, nodes=[])
                    else:
                        n = n['data']
                        self.graph.node[n[0]]['nodes'].append(st)
                        self.nodes_dict[st[0]] = n[0]

                    if lastNode is not None:
                        wgt = util.haversine(lastNode[4], lastNode[3], n[4], n[3])
                        time = util.time_diff(lastNode[7], n[7])
                        if lastNode[0] != n[0]:
                            self.graph.add_edge(lastNode[0], n[0], weight=wgt, travelTime=time)

                    lastNode = n

            lastNode = None

    def astar(self, n1, n2):
        resp = None
        length = None

        # verifica se nodos foram clusterizados(menos de 300metros)
        if n1 in self.nodes_dict:
            n1 = self.nodes_dict[n1]
        if n2 in self.nodes_dict:
            n2 = self.nodes_dict[n2]

        try:
            resp = nx.astar_path(self.graph, n1, n2, self.h, weight='travelTime') #weight='travelTime'
            length = nx.astar_path_length(self.graph, n1, n2, self.h, weight='travelTime') #weight='travelTime'

        except nx.NetworkXNoPath:
            print 'Nao ha caminho entre os nodos'
            resp = []
        finally:
            return resp, length

    def get_graph(self):
        return self.graph

    # def save(self):
    #     pickle.dump(self.graph, open('/tmp/graph.txt', 'w'))

    # def read(self):
    #     dg = pickle.load(open('/tmp/graph.txt'))
    #     print dg.edges()

    def h(self, a, b):
        n1 = self.graph.node[a]['data']
        n2 = self.graph.node[b]['data']
        return util.haversine(n1[3], n1[4], n2[3], n2[4])

    def draw_graph(self):
        if (len(self.graph) < 2000):
            pos = nx.get_node_attributes(self.graph,'pos')
            nx.draw_networkx(self.graph, pos)
            labels = nx.get_edge_attributes(self.graph,'travelTime')
            nx.draw_networkx_edge_labels(self.graph, pos,edge_labels=labels)

            plt.xlabel('Latitude', fontsize=23)
            plt.ylabel('Longitude', fontsize=23)

            plt.show()
        else:
            print('Nodes :', len(self.graph))