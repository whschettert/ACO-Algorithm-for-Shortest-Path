import math
import random as rand

class tabu:
    def euc_2d(c1, c2):
        return math.sqrt((c1[0] - c2[0])**2.0 + (c1[1] - c2[1])**2.0).round


    def cost(perm, cities):
        distance = 0
        for c1 in perm: #.each_with_index do |c1, i| /// para cada index c1 (chave), i (valor)
            c2 = (c1 == len(perm-1) ? perm[0] : perm[c1+1]
            #troquei os 'i's por c1 na linha de cima
            distance += self.euc_2d(cities[c1], cities[c2])
        
        return distance


    def random_permutation(cities):
        perm = None
        for n in cities:
            i = 0
            perm.append(i)
            i++
        
        #isso em baixo virou aquilo em cima
        #perm = array(self.cities.length){|i| i}

        #perm.each_index do |i|
        for i in range(0,len(perm)):
            #r = rand(perm.size-i) + i
            r = rand.randint(0,len(perm-i)) + i
            auxList[r] = perm[r]
            perm[r] = perm[i]
            perm[i] = auxList[r]
            #perm[r], perm[i] = perm[i], perm[r] essa associação paralela virou aquilo
        
        return perm


    def stochastic_two_opt(parent):
        perm = parent  #Array.new(parent)
        #c1, c2 = rand.randrange(perm.size), rand.randrange(perm.size)
        c1 = rand.randrange(len(perm))
        c2 = rand.randrange(len(perm))
        exclude = [c1]
        exclude << ((c1==0) ? perm.size-1 : c1-1)
        exclude << ((c1==perm.size-1) ? 0 : c1+1)

        #como fazer as linhas de cima?

        #c2 = rand(perm.size) while exclude.include?(c2) -> parecido com contains
        #linha decima significa Executa Codigo WHILE condição
        c2 = rand.randrange(len(perm))
        while exclude.__contains__(c2):
            c2 = rand.randrange(len(perm))

        if c2 < c1:
            auxInt = c2
            c2 = c1
            c1 = auxInt

        #c1, c2 = c2, c1 if c2 < c1
        
        perm[c1...c2] = perm[c1...c2].reverse
        return perm, [[parent[c1-1], parent[c1]], [parent[c2-1], parent[c2]]]


    def is_tabu(permutation, tabu_list):
        #permutation.each_with_index do |c1, i|
        for c1 in permutation:
            
            c2 = (c1==len(permutation)-1) ? permutation[0] : permutation[c1+1]
            tabu_list.each do |forbidden_edge|
            return true if forbidden_edge == [c1, c2]
            
        
        return false


    def generate_candidate(best, tabu_list, cities):
        perm, edges = None
        begin
            perm, edges = stochastic_two_opt(best[:vector])
        end while is_tabu?(perm, tabu_list)
        candidate = {:vector=>perm}
        candidate[:cost] = cost(candidate[:vector], cities)
        return candidate, edges


    def search(cities, tabu_list_size, candidate_list_size, max_iter)
        current = {:vector=>random_permutation(cities)}
        current[:cost] = cost(current[:vector], cities)
        best = current
        tabu_list = Array.new(tabu_list_size)
        max_iter.times do |iter|
            candidates = Array.new(candidate_list_size) do |i|
            generate_candidate(current, tabu_list, cities)
            
            candidates.sort! {|x,y| x.first[:cost] <=> y.first[:cost]}
            best_candidate = candidates.first[0]
            best_candidate_edges = candidates.first[1]
            if best_candidate[:cost] < current[:cost]
            current = best_candidate
            best = best_candidate if best_candidate[:cost] < best[:cost]
            best_candidate_edges.each {|edge| tabu_list.push(edge)}
            tabu_list.pop while tabu_list.size > tabu_list_size
            
            print() #puts " > iteration #{(iter+1)}, best=#{best[:cost]}"
        
        return best
        

    
    #problem configuration
    berlin52 = [[565,575],[25,185],[345,750],[945,685],[845,655],
    [880,660],[25,230],[525,1000],[580,1175],[650,1130],[1605,620],
    [1220,580],[1465,200],[1530,5],[845,680],[725,370],[145,665],
    [415,635],[510,875],[560,365],[300,465],[520,585],[480,415],
    [835,625],[975,580],[1215,245],[1320,315],[1250,400],[660,180],
    [410,250],[420,555],[575,665],[1150,1160],[700,580],[685,595],
    [685,610],[770,610],[795,645],[720,635],[760,650],[475,960],
    [95,260],[875,920],[700,500],[555,815],[830,485],[1170,65],
    [830,610],[605,625],[595,360],[1340,725],[1740,245]]

    # algorithm configuration
    max_iter = 100
    tabu_list_size = 15
    max_candidates = 50

    # execute the algorithm
    best = search(berlin52, tabu_list_size, max_candidates, max_iter)
    print("Done. Best Solution: c=#{best[:cost]}, v=#{best[:vector].inspect}")
    