from aco import *
import random
import graph as graph
import time
import os

dir = os.path.dirname(__file__)

class RandParam:

    def __init__(self):

        self.gp = graph.Graph()

        self.gp.build_graph_stop_points(250)

    def run(self):

        f = open(os.path.join(dir, '../out/rand_param.txt'), 'w')

        for r in range(0, 10):

            num_ants = random.randint(10, 50)

            init_pheromone = random.uniform(0.0001, 0.001)

            alpha = random.uniform(0.1, 1)

            beta = random.randint(4, 6)

            evaporation = random.uniform(0.2, 0.5)

            num_nodes = len(self.gp.graph)

            arr_nodes = []

            while len(arr_nodes) < 10:

                source_node = self.gp.graph.nodes()[random.randint(0, num_nodes-1)]

                target_node = self.gp.graph.nodes()[random.randint(0, num_nodes-1)]

                if self.check_valid_pair(source_node, target_node):
                    arr_nodes.append([source_node, target_node])

            f.write('AMOSTRAGEM ' + str(r) + '\n')

            for nodes in arr_nodes:

                f.write('Origem - Destino ' + str(nodes) + '\n')

                for i in range(0, 10):

                    aco = Aco(self.gp.graph, init_pheromone, alpha, beta, evaporation)
                    
                    start_time = time.time()

                    result = aco.run(num_ants, nodes[0], nodes[1], 'weight')

                    elapsed_time = time.time() - start_time

                    f.write('Otimizacao Distancia - Ants:' + str(num_ants) + ' - Init pheromone:' + str(init_pheromone) + 
                        ' - Alpha:' + str(alpha) + ' - Beta:' + str(beta) + ' - Evaporation:' + str(evaporation) +
                        ' - Result:' + str(result) + ' - Time:' + str(elapsed_time))

                    f.write('\n')

        f.close()

    def check_valid_pair(self, source, target):

        has_path = self.gp.has_path(source, target)

        haversine = self.gp.h_dist(source, target)

        return has_path and haversine > 20

if __name__ == "__main__":
    test = RandParam()

    test.run()