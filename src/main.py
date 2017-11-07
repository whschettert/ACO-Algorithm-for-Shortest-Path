import graph as graph
import time
import pickle
from aco import *
import parallel_aco as paco
import shortest_aco as short_aco

class Main:

    def __init__(self):
        gp = graph.Graph()

        start_time = time.time()

        gp.build_graph_stop_points(250)

        elapsed_time = time.time() - start_time

        print "Time build graph %.2f seconds." % elapsed_time

        print "Nodes: %d Edges: %d" % (gp.graph.number_of_nodes(), gp.graph.number_of_edges())

        # ALFA se 0 somente heuristica importa
        # BETA se 0 somente info feromonio importa

        # while True:
            # input = raw_input('Nodos(origem,destino) >>')
            # args = input.split(',')
        args = ['1S0','8S37']
        # args = ['221S6', '157S13']
        # args = ['260S4', '374S0']
        # args = ['42S5', '458S17']

        # print gp.compute_path(['1S0', '1S1', '1S2', '415S10', '415S11', '1S3', '1S4', '1S5', '1S6', '1S7', '1S8', '1S9', '288S12', '8S15', '8S16', '8S18', '8S19', '8S20', '8S21', '8S22', '8S23', '8S24', '8S25', '8S26', '8S27', '8S28', '8S29', '8S30', '8S31', '8S32', '418S2', '8S33', '8S34', '8S35', '8S36', '8S37'],'weight')

        start_time = time.time()
        star_path, cost = gp.astar(args[0], args[1], 'weight')
        print 'A*: (custo, path):', cost, star_path, 'Run Time: ' + str(time.time()-start_time)

        for i in range(10):
            print 'Amostra %1d' % i
        #     start_time = time.time()
        #     aco = Aco(gp.graph, 0.0001, 1.2, 0, 0.5)
        #     aco_path, cost = aco.run(1000, args[0], args[1], 'weight')
        #     print 'ACO: (custo, path):', aco_path, cost, 'Run Time: ' + str(time.time()-start_time)
    

        # start_time = time.time()
        # p_aco = paco.Aco(gp.graph, 0.0001, 1.2, 0, 0.5)
        # aco_path, cost = p_aco.run(1000, args[0], args[1], 'weight')
        # print 'P_ACO: (custo, path):', aco_path, cost, 'Run Time: ' + str(time.time()-start_time)

        # Num Ants:1900 - Init pheromone:0.000161031217354 - Alpha:0.239075890865 - Beta:0 - Evaporation:0.647256741985

            start_time = time.time()
            s_aco = short_aco.Aco(gp.graph, 3000, 100, 0, 1.2, 0, 0.5, 'weight', args[0])
            aco_path, cost = s_aco.run(args[1])
            print 'SHORT_ACO: (custo, path):', cost, aco_path, 'Run Time: ' + str(time.time()-start_time)

        # gp.draw_graph(aco_path)

if __name__ == "__main__":
    Main()
    # try:
    #     main = Main()
    # except KeyboardInterrupt as k:
    #     pass
    # except Exception as e:
    #     raise e
    # finally:
    #     print '\nexiting'
