import math
import random
import copy

import os
import time

dir = os.path.dirname(__file__)

class Ant:

    def __init__(self, current_node):
        self.current_node = current_node
        self.visited_nodes = []
        self.edges = []
        self.tour_length = 0
        self.valid = False

        self.solution_path = []
        self.cost = None

    def reset(self, current_node):
        self.current_node = current_node
        self.visited_nodes = []
        self.edges = []
        self.tour_length = 0
        self.valid = False

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

        self.edges_to_update = []

        self.irregular_nodes = []

    def run(self, num_ants, source, target, weight):

        # melhor formiga da iteracao atual
        best_ant = None

        self.graph = copy.copy(self.c_graph)

        # inicializa ferominios
        for i in self.graph.succ:
            for j in self.graph.succ[i]:
                self.graph.succ[i][j]['pheromone'] = self.initial_pheromone

        self.weight = weight

        for i in range(10):

            # for ant in self.ants:
            #     ant.reset(source)
            
            best_ant = None

            # cada formiga constroi solucao
            for a in range(num_ants):

                if not len(self.ants) == num_ants:
                    self.ants.append(Ant(source))

                ant = self.ants[a]

                ant.reset(source)
                
                s_time = time.time()

                for e in range(self.graph.number_of_edges()):

                    ant.visited_nodes.append(ant.current_node)

                    next = self.select_next_node(ant.current_node, ant)

                    # Grafo irregular, caminho sem saida
                    if not next or next in self.irregular_nodes:
                        self.irregular_nodes.append(ant.current_node)
                        break

                    edge = self.graph.succ[ant.current_node][next]

                    ant.edges.append(ant.current_node + next)

                    if not (ant.current_node + '-' + next) in self.edges_to_update:
                        self.edges_to_update.append(ant.current_node + '-' + next)

                    ant.tour_length += edge[self.weight]

                    ant.current_node = next

                    if ant.current_node == target:
                        ant.visited_nodes.append(ant.current_node)
                        ant.new_solution(ant.visited_nodes, ant.tour_length)

                        if not best_ant:
                            best_ant = ant
                        elif ant.tour_length < best_ant.cost:
                            best_ant = ant

                        break
                
                # print 'Seq time: ' + str(time.time()-s_time)

            # atualiza feromonios
            self.update_pheromone(best_ant)

        return self.get_solution()

    def select_next_node(self, current_node, ant):

        if len(self.graph.succ[current_node]) == 0:
            return None
        else:
            best = -1
            result = None

            for neighbor in self.graph.succ[current_node]:
                 if not neighbor in ant.visited_nodes and not neighbor in self.irregular_nodes:

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
    def update_pheromone(self, best_ant):

        for e in self.edges_to_update:
            i, j = e.split('-')
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