import graph as graph
import time
import pickle
from ant_colony import *
from aco import *

class Main:

    def __init__(self):
        gp = graph.Graph()

        start_time = time.time()
    
        gp.build_graph_stop_points(1)

        print gp.get_pos()

        # gp.save()

        # aco = AntColonyOptimization(5, 1, 5, 0.5)

        # aco = Aco(gp.graph, 0.1, 1, 5, 0.5)

        # aco.run(10, 10, '1S0', '1S2')

        # aco.run(gp, '1S0', '1S4')

        elapsed_time = time.time() - start_time

        print("Time build graph %.2f seconds.", elapsed_time)

        # gp.draw_graph()

        # while True:
            # input = raw_input('Nodos(origem,destino) >>')
            # args = input.split(',')
        args = ['1S0','1S9']
        print 'Menor caminho DISTANCIA(path, custo):', gp.astar(args[0], args[1], 'weight')
        print 'Menor caminho TEMPO(path, custo):', gp.astar(args[0], args[1], 'travelTime')
        
if __name__ == "__main__":
    
    try:
        main = Main()    
    except KeyboardInterrupt as k:
        pass
    except Exception as e:
        raise e
    finally:
        print '\nexiting'
