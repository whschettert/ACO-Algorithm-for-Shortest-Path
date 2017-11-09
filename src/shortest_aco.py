import copy
import math
import os
import random
import time
import util as util
import numpy

dir = os.path.dirname(__file__)

class Ant:

    def __init__(self, current_node):
        self.current_node = current_node
        self.visited_nodes = [current_node]
        self.visited_edges = []
        self.tour_length = 0
        self.route_count = 0

        self.solution_path = []
        self.cost = None

    def reset(self, current_node):
        self.current_node = current_node
        self.visited_nodes = [current_node]
        self.visited_edges = []
        self.tour_length = 0

    def new_solution(self, path, cost):
        if not self.cost or cost < self.cost:
            self.solution_path = path[:]
            self.cost = cost

class Aco:

    def __init__(self, graph, num_ants, num_iterations, initial_pheromone, alpha, beta, evaporation, weight, source):
        
        self.weight = weight

        self.evaporation = evaporation

        self.alpha = alpha
        
        self.beta = beta

        self.ants = []

        self.graph = copy.copy(graph)

        self.min_pheromone = 1.0e-20

        self.num_iterations = num_iterations

        self.source = source

        C = 0

        for i in self.graph.succ:
            for j in self.graph.succ[i]:
                self.graph.succ[i][j]['pheromone'] = initial_pheromone
                self.graph.succ[i][j]['visited'] = False

                if self.graph.succ[i][j][weight] > C:
                    C = self.graph.succ[i][j][weight]

            self.graph.node[i]['visited'] = False
        
        #TODO
        length = C - 1

        time = 0

        listTime = dict()

        for k in range(num_ants):
            
            self.ants.append(Ant(source))
            #setRun = ant routers count to 0
            #setNode = ant to source node
            #setVisited = source visited by ant k
            if not time in listTime:
                listTime[time] = [k]
            else:
                listTime[time].append(k)

        convergence = 0
        last_length = float("inf")

    def run(self, target):
        
        best_ant = None

        for i in range(self.num_iterations):

            best_ant = None

            for ant in self.ants:
                
                while ant.current_node != target:
                    
                    next = self.select_next_edge(ant.current_node, ant)

                    if not next:
                        ant.reset(self.source)
                        break

                    self.graph.succ[ant.current_node][next]['visited'] = True
                    self.graph.node[ant.current_node]['visited'] = True
                    self.graph.node[next]['visited'] = True

                    ant.tour_length += self.graph.succ[ant.current_node][next][self.weight]

                    ant.visited_nodes.append(next)

                    ant.visited_edges.append(ant.current_node+next)

                    ant.current_node = next

                    if ant.current_node == target:
                        
                        ant.new_solution(ant.visited_nodes, ant.tour_length)

                        ant.route_count += 1

                        if not best_ant:
                            best_ant = ant
                        elif ant.cost < best_ant.cost:
                            best_ant = ant

            self.evaporate(best_ant)

        return self.get_solution()

    def select_next_edge(self, source, ant):

        if len(self.graph.succ[source]) == 0:
            return None

        nodes = []
        probs = []
 
        for neighbor in self.graph.succ[source]:
            
            if neighbor in ant.visited_nodes:
                continue
                
            nodes.append(neighbor)
            probs.append(self.compute_coefficient(source, neighbor, ant))
        
        if not nodes:
            return None

        resp = numpy.random.choice(nodes, p=probs)

        return str(resp)

    def compute_coefficient(self, current, next, ant):
        
        if next in ant.visited_nodes:
            return 0

        edge = self.graph.succ[current][next]

        unvisited_nodes = list(set(self.graph.succ[current]) - set(ant.visited_nodes))

        pheromone = 0
        distance = 0
        sum = 0.0

        for node in unvisited_nodes:
            pheromone = self.graph.succ[current][node]['pheromone']
            sum += math.pow(pheromone, self.alpha)

        if sum == 0:
            sum = 1

        pheromone = self.graph.succ[current][next]['pheromone']

        prob = math.pow(pheromone, self.alpha) / sum

        return prob

        # if edge['pheromone'] == 0:
            
        #     if not self.graph.node[next]['visited'] and not edge['visited']:
                
        #         # for node in unvisited_nodes:
        #         #     distance = self.graph.succ[current][node][self.weight]
        #         #     sum += math.pow(1.0 / distance, self.alpha) * math.pow((1 + self.beta), 2)

        #         # if sum == 0:
        #         #     sum = 1

        #         distance = self.graph.succ[current][next][self.weight]

        #         return (math.pow(1.0 / distance, self.alpha) * math.pow((1 + self.beta), 2))
        #     else:
                
        #         # for node in unvisited_nodes:
        #         #     distance = self.graph.succ[current][node][self.weight]
        #         #     sum += math.pow(1.0 / distance, self.alpha)

        #         # if sum == 0:
        #         #     sum = 1

        #         distance = self.graph.succ[current][next][self.weight]

        #         return math.pow(1.0 / distance, self.alpha)
        
        # if ant.route_count < 3:
        #     return 0 # 1.0 / len(unvisited_nodes)
        # else:
            
        #     # for node in unvisited_nodes:
        #     #     pheromone = self.graph.succ[current][node]['pheromone']
        #     #     distance = self.graph.succ[current][node][self.weight]
        #     #     sum += (math.pow(pheromone, self.alpha) * math.pow(1.0 / distance, self.beta))

        #     # if sum == 0:
        #     #     sum = 1

        #     pheromone = self.graph.succ[current][next]['pheromone']
        #     # distance = self.graph.succ[current][next][self.weight]

        #     return (math.pow(pheromone, self.alpha) * math.pow((1.0 + self.beta),2))
    
    def evaporate(self, best_ant):

        for i in self.graph.succ:
            for j in self.graph.succ[i]:

                pheromone = self.graph.succ[i][j]['pheromone']

                delta = 0

                if best_ant:
                    if i+j in best_ant.visited_edges:
                        delta = 1.0 / best_ant.tour_length

                pheromone = (1.0 - self.evaporation) * pheromone + delta

                if pheromone < self.min_pheromone:
                    pheromone = self.min_pheromone
                
                self.graph.succ[i][j]['pheromone'] = pheromone
                
    def get_solution(self):
        solution, cost = None, None

        for ant in self.ants:
            if len(ant.solution_path) == 0:
                continue

            if not solution:
                solution = ant.solution_path
                cost = ant.cost
                continue
            
            if ant.cost < cost:
                solution = ant.solution_path
                cost = ant.cost

        return solution, cost
