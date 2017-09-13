import graph as graph
import time
import pickle

class Main:

    def __init__(self):
        gp = graph.Graph()

        start_time = time.time()
    
        gp.build_graph_stop_points(15)

        elapsed_time = time.time() - start_time

        print("Time build graph %.2f seconds.", elapsed_time)

       # gp.draw_graph()

        while True:
            #input = raw_input('Nodos(origem,destino) >>')
            #args = input.split(',')
            args = ['1S9','8S13']
            print 'Menor caminho(path, custo, custoKm):', gp.astar(args[0], args[1])
        
if __name__ == "__main__":
    
    try:
        main = Main()    
    except KeyboardInterrupt as k:
        pass
    except Exception as e:
        raise e
    finally:
        print '\nexiting'
