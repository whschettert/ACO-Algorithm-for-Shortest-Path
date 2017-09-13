import graph as graph
import time
import pickle
from ant_colony import *

class Main:

    def __init__(self):
        gp = graph.Graph()

        start_time = time.time()
    
        gp.build_graph_stop_points(2)

        # gp.save()

        aco = AntColonyOptimization(5, 1, 5, 0.5)

        # aco.run(gp, '1S0', '1S4')

        elapsed_time = time.time() - start_time

        print("Time build graph %.2f seconds.", elapsed_time)

       # gp.draw_graph()

        while True:
<<<<<<< HEAD
            #input = raw_input('Nodos(origem,destino) >>')
            #args = input.split(',')
            args = ['1S9','8S13']
            print 'Menor caminho(path, custo, custoKm):', gp.astar(args[0], args[1])
=======
            input = raw_input('Nodos(origem,destino) >>')

            if input == 'exit':
                break

            args = input.split(',')

            print 'A* (path, custo):', gp.astar(args[0], args[1])
            print 'ACO (path, custo):', aco.run(gp, args[0], args[1])
>>>>>>> 97fec692ce7de81d05208d0bcdc7528511c2daf3
        
if __name__ == "__main__":
    
    try:
        main = Main()    
    except KeyboardInterrupt as k:
        pass
    except Exception as e:
        raise e
    finally:
        print '\nexiting'
