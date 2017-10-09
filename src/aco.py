import math
import random
import copy

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

    def run(self, num_ants, source, target, weight):

        # melhor formiga da iteracao atual
        best_ant = None

        self.irregular_nodes = []

        self.graph = copy.copy(self.c_graph)

        # inicializa ferominios
        for i in self.graph.edge:
            for j in self.graph.edge[i]:
                self.graph.edge[i][j]['pheromone'] = self.initial_pheromone

        self.weight = weight

        for i in range(num_ants):
            self.ants.append(Ant(source))

        for i in range(10):

            for ant in self.ants:
                ant.reset(source)
            
            best_ant = None

            # cada formiga constroi solucao
            for ant in self.ants:
                 
                for e in range(len(self.graph.edges())):

                    ant.visited_nodes.append(ant.current_node)

                    next = self.select_next_node(ant.current_node, ant)

                    # Caminho sem saida, o que fazer?
                    # Resetar formiga? Recolocar no inicio? Marcar caminho como invalido???
                    if not next:
                        # marcar nodos sem saida como irregulares, melhor solucao?
                        self.irregular_nodes.append(ant.current_node)
                        break

                    edge = self.graph.edge[ant.current_node][next]

                    ant.edges.append(ant.current_node + next)

                    ant.tour_length += edge[self.weight]

                    ant.current_node = next

                    if ant.current_node == target:
                        ant.visited_nodes.append(ant.current_node)
                        # cada formiga constroi sua solucao
                        ant.new_solution(ant.visited_nodes, ant.tour_length)

                        if not best_ant:
                            best_ant = ant
                        elif ant.tour_length < best_ant.tour_length:
                            best_ant = ant

                        break

            # atualiza feromonios
            self.update_pheromone(best_ant)

        return self.get_solution()

    def select_next_node(self, current_node, ant):

        if len(self.graph.edge[current_node]) == 0:
            return None
        else:
            best = -1
            result = None

            for neighbor in self.graph.edge[current_node]:
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
            pheromone = self.graph.edge[current_node][node]['pheromone']
            distance = self.get_distance(current_node, node)
            sum += (math.pow(pheromone, self.alpha) * math.pow(1.0 / distance, self.beta))

        if sum == 0:
            sum = 1

        pheromone = self.graph.edge[current_node][target_node]['pheromone']

        prob = (math.pow(pheromone, self.alpha) * math.pow(1.0 / distance, self.beta)) / sum

        return prob

    # atualizacao de feromonio por max-min(MMAS)
    def update_pheromone(self, best_ant):
        for i in self.graph.edge:
            for j in self.graph.edge[i]:

                edge = self.graph.edge[i][j]

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
        edge = self.graph.edge[source][target]

        return edge[self.weight]

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