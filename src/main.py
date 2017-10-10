import graph as graph
import time
import pickle
from aco import *
import parallel_aco as paco

class Main:

    def __init__(self):
        gp = graph.Graph()

        start_time = time.time()
    
        gp.build_graph_stop_points(-1)

        elapsed_time = time.time() - start_time

        print "Time build graph %.2f seconds." % elapsed_time

        print "Nodes: %.1f Edges: %.1f" % (gp.graph.number_of_nodes(), gp.graph.number_of_edges())

        # while True:
            # input = raw_input('Nodos(origem,destino) >>')
            # args = input.split(',')
        args = ['1S0','8S37']
        # args = ['1S0','1S9']
        # args = ['260S4', '374S0']

        start_time = time.time()
        print 'A* Menor caminho DISTANCIA(path, custo):', gp.astar(args[0], args[1], 'weight'), 'Run Time: ' + str(time.time()-start_time)
        # print 'A* Menor caminho TEMPO(path, custo):', gp.astar(args[0], args[1], 'travelTime')

        start_time = time.time()
        aco = Aco(gp.graph, 0.0003123, 0.1, 1, 0.5)
        print 'ACO Menor caminho DISTANCIA(path, custo):', aco.run(10, args[0], args[1], 'weight'), 'Run Time: ' + str(time.time()-start_time)

        start_time = time.time()
        aco = paco.Aco(gp.graph, 0.0003123, 0.5, 1.2, 0.4)
        print 'P_ACO Menor caminho DISTANCIA(path, custo) ,', aco.run(1000, args[0], args[1], 'weight'), 'Run Time: ' + str(time.time()-start_time)

        # start_time = time.time()
        # aco = paco.Aco(gp.graph, 0.0003123, 0.5, 1.2, 0.4)
        # print 'ACO Menor caminho TEMPO(path, custo) ,', aco.run(100, args[0], args[1], 'travelTime'), 'Run Time: ' + str(time.time()-start_time)

        gp.draw_graph()
        
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
