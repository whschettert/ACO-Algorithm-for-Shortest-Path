def haversine_distance(geo_a, geo_b, miles=false)
  # Get latitude and longitude
  lat1, lon1 = geo_a
  lat2, lon2 = geo_b

  # Calculate radial arcs for latitude and longitude
  dLat = (lat2 - lat1) * Math::PI / 180
  dLon = (lon2 - lon1) * Math::PI / 180


  a = Math.sin(dLat / 2) * 
      Math.sin(dLat / 2) +
      Math.cos(lat1 * Math::PI / 180) * 
      Math.cos(lat2 * Math::PI / 180) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2)

  c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))

  d = 6371 * c * (miles ? 1 / 1.6 : 1)
end

def cost(perm, cities)
  distance = 0
  perm.each_with_index do |c1, i|
    c2 = (i==perm.size-1) ? perm[0] : perm[i+1]
    distance += haversine_distance(cities[c1], cities[c2])
  end
  return distance
end

def random_permutation(cities)
  perm = Array.new(cities.size){|i| i}
  perm.each_index do |i|
    r = rand(perm.size-i) + i
    perm[r], perm[i] = perm[i], perm[r]
  end
  return perm
end

def stochastic_two_opt(parent)
  perm = Array.new(parent)
  c1, c2 = rand(perm.size), rand(perm.size)
  exclude = [c1]
  exclude << ((c1==0) ? perm.size-1 : c1-1)
  exclude << ((c1==perm.size-1) ? 0 : c1+1)
  c2 = rand(perm.size) while exclude.include?(c2)
  c1, c2 = c2, c1 if c2 < c1
  perm[c1...c2] = perm[c1...c2].reverse
  return perm, [[parent[c1-1], parent[c1]], [parent[c2-1], parent[c2]]]
end

def is_tabu?(permutation, tabu_list)
  permutation.each_with_index do |c1, i|
    c2 = (i==permutation.size-1) ? permutation[0] : permutation[i+1]
    tabu_list.each do |forbidden_edge|
      return true if forbidden_edge == [c1, c2]
    end
  end
  return false
end

def generate_candidate(best, tabu_list, cities)
  perm, edges = nil, nil
  begin
    perm, edges = stochastic_two_opt(best[:vector])
  end while is_tabu?(perm, tabu_list)
  candidate = {:vector=>perm}
  candidate[:cost] = cost(candidate[:vector], cities)
  return candidate, edges
end

def search(cities, tabu_list_size, candidate_list_size, max_iter)
  current = {:vector=>random_permutation(cities)}
  current[:cost] = cost(current[:vector], cities)
  best = current
  tabu_list = Array.new(tabu_list_size)
  max_iter.times do |iter|
    candidates = Array.new(candidate_list_size) do |i|
      generate_candidate(current, tabu_list, cities)
    end
    candidates.sort! {|x,y| x.first[:cost] <=> y.first[:cost]}
    best_candidate = candidates.first[0]
    best_candidate_edges = candidates.first[1]
    if best_candidate[:cost] < current[:cost]
      current = best_candidate
      best = best_candidate if best_candidate[:cost] < best[:cost]
      best_candidate_edges.each {|edge| tabu_list.push(edge)}
      tabu_list.pop while tabu_list.size > tabu_list_size
    end
    puts " > iteration #{(iter+1)}, best=#{best[:cost]}"
  end
  return best
end

if __FILE__ == $0
  # problem configuration
  berlin52 = [[19.390556724515623, -99.19930327578787], [19.3910323, -99.1917229], [19.392800571631128, -99.17712137799887], [19.364161576256127, -99.27095647194113], [19.362189162215948, -99.27613731818288],
  [19.374597263863443, -99.25739098109841], [19.392812276731, -99.17324158446604], [19.379132082949067, -99.24666879807842], [19.38743724622681, -99.22208797929363],
  [19.381147615654395, -99.2412095530641], [19.380181988421946, -99.24365227874814], [19.386789934097862, -99.22275445718807], [19.38325474806389, -99.23517000315945], [19.36177285612866, -99.27800796029956],
  [19.377693079527685, -99.25153663726631], [19.377893111329385, -99.25053455885435], [19.390072583816906, -99.20960386346293], [19.39065618060116, -99.20199660786051],
  [19.368685977979787, -99.26253126844549], [19.387674685142656, -99.21533899434459], [19.386701409576077, -99.21820549283044], [19.389890295990256, -99.20504863157188], [19.390607286230992, -99.20746140048423],
  [19.388746902613804, -99.18276074798037], [19.38955358141359, -99.19058201307665], [19.391394829755686, -99.17724627927949], [19.379252264690194, -99.24640018210012]]
  # algorithm configuration
  max_iter = 100
  tabu_list_size = 15
  max_candidates = 50
  # execute the algorithm
  best = search(berlin52, tabu_list_size, max_candidates, max_iter)
  puts "Done. Best Solution: c=#{best[:cost]}, v=#{best[:vector].inspect}"
end