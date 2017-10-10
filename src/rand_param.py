from aco import *
import parallel_aco as p_aco
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

        file_name = time.strftime('../out/%d-%m-%Y - %H.%M.%S.txt')

        f = open(os.path.join(dir, file_name), 'w')

        start_run_time = time.time()

        # amostras
        for r in range(0, 10):

            print 'Amostra %d' % r

            num_ants = random.randrange(1000, 1200, 10)

            init_pheromone = random.uniform(0.0001, 0.0002)

            alpha = random.uniform(0.1, 1)

            beta = random.randint(1, 5)

            evaporation = random.uniform(0.4, 0.8)

            num_nodes = len(self.gp.graph)

            arr_nodes = []

            # rotas para cada amostra
            while len(arr_nodes) < 10:

                source_node = self.gp.graph.nodes()[random.randint(0, num_nodes-1)]

                target_node = self.gp.graph.nodes()[random.randint(0, num_nodes-1)]

                if self.check_valid_pair(source_node, target_node):
                    arr_nodes.append([source_node, target_node])

            f.write('AMOSTRAGEM ' + str(r) + '\n')

            for nodes in arr_nodes:

                f.write('Origem - Destino ' + str(nodes) + '- Ants:' + str(num_ants) + ' - Init pheromone:' + str(init_pheromone) + 
                        ' - Alpha:' + str(alpha) + ' - Beta:' + str(beta) + ' - Evaporation:' + str(evaporation) + '\n')

                # cada caminho roda 10 vezes
                for i in range(0, 10):

                    aco = p_aco.Aco(self.gp.graph, init_pheromone, alpha, beta, evaporation)
                    
                    start_time = time.time()

                    result = aco.run(num_ants, nodes[0], nodes[1], 'weight')

                    elapsed_time = time.time() - start_time

                    f.write('Otimizacao Distancia - Result: ' + str(result) + ' - Run Time: ' + str(elapsed_time))

                    f.write('\n')

        f.write('TOTAL RUNNING TIME: ' + str(time.time() - start_run_time))

        f.close()

    def check_valid_pair(self, source, target):

        has_path = self.gp.has_path(source, target)

        haversine = self.gp.h_dist(source, target)

        return has_path and haversine > 20

if __name__ == "__main__":
    test = RandParam()

    test.run()