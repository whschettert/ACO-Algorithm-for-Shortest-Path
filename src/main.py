import graph as graph
import time

class Main:

    def __init__(self):
        gp = graph.Graph()

        start_time = time.time()
    
        gp.build_graph_stop_points(15)

        elapsed_time = time.time() - start_time

        print("Time build graph %.2f seconds.", elapsed_time)

        gp.draw_graph()

if __name__ == "__main__":
    main = Main()
