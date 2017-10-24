import math
import random
import copy
from multiprocessing import Process

import os
import time

dir = os.path.dirname(__file__)

MAX_PROCS = 4

class Ant:

    def __init__(self, current_node):
        self.current_node = current_node
        self.visited_nodes = []
        self.edges = []
        self.tour_length = 0

        self.solution_path = []
        self.cost = None

    def reset(self, current_node):
        self.current_node = current_node
        self.visited_nodes = []
        self.edges = []
        self.tour_length = 0

    def new_solution(self, path, cost):
        if not self.cost or cost < self.cost:
            self.solution_path = path[:]
            self.cost = cost

class Aco:

    def __init__(self, graph, initial_pheromone, alpha, beta, evaporation):

        self.initial_pheromone = initial_pheromone

        self.min_pheromone = 0.1

        self.max_pheromone = 10

        self.evaporation = evaporation

        self.alpha = alpha

        self.beta = beta

        self.c_graph = graph

        self.ants = []

        self.irregular_nodes = []

    def run(self, num_ants, source, target, weight):

        procs = []

        self.best_ant = None

        self.graph = copy.copy(self.c_graph)

        # inicializa feromonios
        for i in self.graph.succ:
            for j in self.graph.succ[i]:
                self.graph.succ[i][j]['pheromone'] = self.initial_pheromone

        self.weight = weight

        for i in range(num_ants):
            self.ants.append(Ant(source))

        for i in range(10):
            procs = []

            ants_per_proc = num_ants / MAX_PROCS
            ant_index = 0

            for p in range(MAX_PROCS):
                procs.append(Process(target=self.construct_solution, args=(ant_index, ants_per_proc, source, target, weight,)))
                ant_index += ants_per_proc

            for t in procs:
                t.start()

            for t in procs:
                t.join()

            # atualiza feromonios
            self.update_pheromone()

        return self.get_solution()

    def construct_solution(self, ant_index, num_ants, source, target, weight):

        s_time = time.time()

        for a in range(ant_index, ant_index + num_ants):
            
            ant = self.ants[a]

            ant.reset(source)
                    
            for e in range(self.graph.number_of_edges()):

                ant.visited_nodes.append(ant.current_node)

                next = self.select_next_node(ant.current_node, ant)

                # Grafo irregular, caminho sem saida
                if not next:
                #     self.irregular_nodes.append(ant.current_node)
                    break

                edge = self.graph.succ[ant.current_node][next]

                ant.edges.append(ant.current_node + next)

                ant.tour_length += edge[self.weight]

                ant.current_node = next

                if ant.current_node == target:
                    ant.visited_nodes.append(ant.current_node)
                    ant.new_solution(ant.visited_nodes, ant.tour_length)
                    break
        # print 'IT %d ant %d Time: %.2f ' % (it, ant_index, time.time() - s_time)

    def select_next_node(self, current_node, ant):

        if len(self.graph.succ[current_node]) == 0:
            return None
        else:
            best = -1
            result = None

            for neighbor in self.graph.succ[current_node]:
                 if not neighbor in ant.visited_nodes:

                    prob = self.node_probability(current_node, neighbor, ant)

                    if prob > best:
                        best = prob
                        result = neighbor
                    elif prob == best and random.randint(0, 10) > 5:
                        result = neighbor

        return result

    def node_probability(self, current_node, target_node, ant):

        if target_node in ant.visited_nodes:
            return 0

        unvisited_nodes = list( set(self.graph.succ[current_node]) - set(ant.visited_nodes) )

        pheromone = 0
        distance = 0
        sum = 0.0

        for node in unvisited_nodes:
            pheromone = self.graph.succ[current_node][node]['pheromone']
            distance = self.get_distance(current_node, node)
            sum += (math.pow(pheromone, self.alpha) * math.pow(1.0 / distance, self.beta))

        if sum == 0:
            sum = 1

        pheromone = self.graph.succ[current_node][target_node]['pheromone']

        prob = (math.pow(pheromone, self.alpha) * math.pow(1.0 / distance, self.beta)) / sum

        return prob

    # atualizacao de feromonio por max-min(MMAS)
    def update_pheromone(self):

        best_ant = None

        for ant in self.ants:
            if not len(ant.solution_path) > 0:
                continue

            if not best_ant:
                best_ant = ant
            elif ant.cost < best_ant.cost:
                best_ant = ant

        for i in self.graph.succ:
            for j in self.graph.succ[i]:

                edge = self.graph.succ[i][j]

                pheromone = edge['pheromone']
                sum = 0
                delta  = 0

                if best_ant:
                    if i+j in best_ant.edges:
                        delta = 1.0 / best_ant.cost

                edge['pheromone'] = (1.0 - self.evaporation) * pheromone + delta

                if edge['pheromone'] < self.min_pheromone:
                    edge['pheromone'] = self.min_pheromone

                if edge['pheromone'] > self.max_pheromone:
                    edge['pheromone'] = self.max_pheromone

    def get_distance(self, source, target):
        edge = self.graph.succ[source][target]

        return edge[self.weight]

    def get_solution(self):

        #  f = open(os.path.join(dir, '../out/test.txt'), 'w')

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