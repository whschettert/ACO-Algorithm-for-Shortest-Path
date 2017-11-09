from aco import *
import parallel_aco as p_aco
import random
import graph as graph
import time
import os
import shortest_aco as short_aco
import numpy as np

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

        self.dists_nodes = [(10,14),(18,24),(28,34),(38,44),(48,54),(58,64),(68,74),(78,84),(88,94),(96,100)]

        # rotas
        while len(arr_nodes) < 10:

            source_node = self.gp.graph.nodes()[random.randint(0, num_nodes-1)]

            target_node = self.gp.graph.nodes()[random.randint(0, num_nodes-1)]

            if self.check_valid_pair(source_node, target_node):
                
                arr_nodes.append([source_node, target_node])

        # amostras
        for nodes in arr_nodes:

            f.write('Source, Target ' + str(nodes) + ' - Dist: ' + str(self.gp.h_dist(nodes[0],nodes[1])) +'\n')
  
            for r in range(0, 20):

                print 'Amostra %d' % r

                num_ants = random.randrange(500, 1000, 100)

                init_pheromone = random.uniform(0.00001, 0.001)

                alpha = random.uniform(1, 3)

                beta = 0 #random.randint(1, 5)

                evaporation = random.uniform(0.4, 0.8)

                f.write('AMOSTRAGEM ' + str(r) + '\n')

                f.write('Num Ants:' + str(num_ants) + ' - Init pheromone:' + str(init_pheromone) +  ' - Alpha:' + str(alpha) + ' - Beta:' + str(beta) + ' - Evaporation:' + str(evaporation) + '\n')
                
                # f.write('A*: ' + str(self.gp.astar(nodes[0], nodes[1], 'weight')) + '\n')

                self.aco_result = []

                time_for_route = time.time()

                # cada caminho roda 5 vezes
                for i in range(0, 5):

                    start_time = time.time()
                    
                    aco = short_aco.Aco(self.gp.graph, num_ants, 100, init_pheromone, alpha, beta, evaporation, 'weight', nodes[0])
                    result = aco.run(nodes[1])
                    self.aco_result.append(result[1])

                    # aco = Aco(self.gp.graph, init_pheromone, alpha, beta, evaporation)
                    # result = aco.run(num_ants, nodes[0], nodes[1], 'weight')

                    elapsed_time = time.time() - start_time

                    f.write('ACO: ' + str(result) + ' - Run Time: ' + str(elapsed_time))

                    f.write('\n')

                best_result = 0
                avg_result = 0
                std_dev = 0

                self.aco_result = filter(lambda x: x != None, self.aco_result)
                if len(self.aco_result) > 0:
                    best_result = min(self.aco_result)
                    avg_result = sum(self.aco_result)/len(self.aco_result) 
                    std_dev = np.std(self.aco_result)
                
                f.write('Best result: ' + str(best_result) + ' - Average Result: ' + str(avg_result) + ' - Standard Deviation: ' + str(std_dev) + ' - time to run all tests: ' + str(time.time() - start_run_time) )

        f.write('TOTAL RUNNING TIME: ' + str(time.time() - start_run_time))

        f.close()

    def check_valid_pair(self, source, target):

        has_path = self.gp.has_path(source, target)

        haversine = self.gp.h_dist(source, target)
        
        if has_path and len(filter(lambda s: s[0] <= haversine <= s[1], self.dists_nodes)) > 0:
            self.dists_nodes = set(self.dists_nodes) - set (filter(lambda s: s[0] <= haversine <= s[1], self.dists_nodes))
            return True

        return False

if __name__ == "__main__":
    test = RandParam()

    test.run()
