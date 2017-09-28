from aco import *
import random
import graph as graph

class RandParam:

    def __init__(self):

        self.gp = graph.Graph()

        self.gp.build_graph_stop_points(-1)

    def run(self):

        f = open('./out/rand_param.txt', 'w')

        for r in range(0, 10):

            num_ants = random.randint(10, 20)

            init_pheromone = random.uniform(0.0001, 0.001)

            alpha = random.uniform(0.1, 1)

            beta = random.randint(4, 6)

            evaporation = random.uniform(0.2, 0.5)

            f.write('AMOSTRAGEM ' + str(r) + '\n')
            for i in range(0, 10):

                aco = Aco(self.gp.graph, init_pheromone, alpha, beta, evaporation)
                # TODO: escolher origem e destino aleatorio?
                result = aco.run(10, num_ants, '1S0', '1S9', 'weight')

                f.write('Ants:' + str(num_ants) + ' - Init pheromone:' + str(init_pheromone) + 
                    ' - Alpha:' + str(alpha) + ' - Beta:' + str(beta) + ' - Evaporation:' + str(evaporation) +
                    ' - Result:' + str(result))

                f.write('\n')

        f.close()

if __name__ == "__main__":
    test = RandParam()

    test.run()