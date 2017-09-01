# encoding:utf-8

import math
import copy

class Ant:

    def __init__(self, source):

        self.currentNode = source
        self.solution = []
        self.cost = None
        self.visited_nodes = [source]

class AntColonyOptimization:

    def __init__(self, num_ants, alfa, beta, evaporation):
        self.graph = None
        self.ants = None

        self.num_ants = num_ants
        self.alfa = alfa
        self.beta = beta
        self.evaporation = evaporation

    def get_pheromone(self, source, target):
        edge = self.graph.edge[source][target]
        if edge and 'pheromone' in edge:
            return edge['pheromone']
        else:
            return 0

    def get_distance(self, source, target):
        d = self.graph.edge[source][target]
        return d['weight']

    def converged(self, target):
        for ant in self.ants:
            if len(ant.solution) > 0 and ant.solution[-1] == target:
                return True
        
        return False

    def get_solution(self, target):
        for ant in self.ants:
            if len(ant.solution) > 0 and ant.solution[-1] == target:
                return ant.solution, ant.cost
        
        return [], None

    def run(self, graph, sourceNode, targetNode):

        # TODO: evitar copia
        self.graph = copy.copy(graph.graph)

        if sourceNode in graph.nodes_dict:
            sourceNode = graph.nodes_dict[sourceNode]
        if targetNode in graph.nodes_dict:
            targetNode = graph.nodes_dict[targetNode]

        # TODO: adicionar formiga a cada iteracao
        self.ants = []
        self.ants.append(Ant(sourceNode))
        self.ants.append(Ant(sourceNode))

        while True:

            if self.converged(targetNode):
                break

            for ant in self.ants:
                unvisited_nodes = list( set(self.graph.succ[ant.currentNode]) - set(ant.visited_nodes))

                pheromone = 0
                distance = 0

                sum = 0.0
                for node in unvisited_nodes:

                    pheromone = self.get_pheromone(ant.currentNode, node)
                    distance = self.get_distance(ant.currentNode, node)
                    sum += (math.pow(pheromone, self.alfa) * math.pow(1.0 / distance, self.beta))
        
                # probabilidades dos caminhoas
                prob = {}

                for node in unvisited_nodes:

                    # calcula probabilidade
                    p = (math.pow(pheromone, self.alfa) * math.pow(1.0 / distance, self.beta)) / (sum if sum > 0 else 1)

                    prob[node] = p

                # pega nodo maior probabilidade
                target = max(prob, key=prob.get)

                # aresta para nodo
                edge = self.graph.edge[ant.currentNode][target]

                if not 'pheromone' in edge:
                    edge['pheromone'] = 0

                edge['pheromone'] += 1

                # adiciona a nodo a lista de visitados pela formiga
                ant.visited_nodes.append(target)
                ant.currentNode = target
                ant.solution.append(target)

                if ant.cost is None:
                    ant.cost = 0

                ant.cost += edge['weight']

            # atualiza quantidade de feromonio
            for source in self.graph.edge:
                for dest in self.graph.edge[source]:
                    edge = self.graph.edge[source][dest]

                    # calcula o novo feromonio
                    if 'pheromone' in edge:
                        edge['pheromone'] = (1.0 - self.evaporation) * edge['pheromone']
        
        # construir solucao
        return self.get_solution(target)