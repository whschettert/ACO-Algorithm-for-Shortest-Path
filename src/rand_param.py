from aco import *
import parallel_aco as p_aco
import random
import graph as graph
import time
import os
import shortest_aco as short_aco

dir = os.path.dirname(__file__)

class RandParam:

    def __init__(self):

        self.gp = graph.Graph()

        self.gp.build_graph_stop_points(250)

    def run(self):

        file_name = time.strftime('../out/%d-%m-%Y - %H.%M.%S.txt')

        f = open(os.path.join(dir, file_name), 'w')

        start_run_time = time.time()

        arr_nodes = []

        num_nodes = len(self.gp.graph)

        # rotas
        while len(arr_nodes) < 10:

            source_node = self.gp.graph.nodes()[random.randint(0, num_nodes-1)]

            target_node = self.gp.graph.nodes()[random.randint(0, num_nodes-1)]

            if self.check_valid_pair(source_node, target_node):
                arr_nodes.append([source_node, target_node])

        # amostras
        for r in range(0, 10):

            print 'Amostra %d' % r

            num_ants = random.randrange(2500, 4000, 200)

            init_pheromone = 0#random.uniform(0.0001, 0.0002)

            alpha = random.uniform(0.5, 2)

            beta = 0 #random.randint(1, 5)

            evaporation = random.uniform(0.2, 0.8)

            f.write('AMOSTRAGEM ' + str(r) + '\n')

            f.write('Num Ants:' + str(num_ants) + ' - Init pheromone:' + str(init_pheromone) +  ' - Alpha:' + str(alpha) + ' - Beta:' + str(beta) + ' - Evaporation:' + str(evaporation) + '\n')

            for nodes in arr_nodes:

                f.write('Source, Target ' + str(nodes) + '\n')
                
                f.write('A*: ' + str(self.gp.astar(nodes[0], nodes[1], 'weight')) + '\n')

                # cada caminho roda 10 vezes
                for i in range(0, 10):

                    start_time = time.time()
                    
                    aco = short_aco.Aco(self.gp.graph, num_ants, 200, init_pheromone, alpha, beta, evaporation, 'weight', nodes[0])
                    result = aco.run(nodes[1])

                    # aco = Aco(self.gp.graph, init_pheromone, alpha, beta, evaporation)
                    # result = aco.run(num_ants, nodes[0], nodes[1], 'weight')

                    elapsed_time = time.time() - start_time

                    f.write('ACO: ' + str(result) + ' - Run Time: ' + str(elapsed_time))

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