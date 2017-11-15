package ant_colony;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

public class ClassicAco implements Runnable {
	
	private static final double RANDOM_COEFFICIENT = 0.15;
	
	private Graph graph;
	private Node target;
	private int ant_thread_index;
	private int ants_by_thread;
	private Ant[] ants;
	private Node source;
	private String weight;
	private Ant bestAnt;
	private double alpha;
	private double beta;
	public HashMap<String, Integer> badpath;
	private Util util;
	
	public ClassicAco(Graph graph, Node source, Node target, int ant_thread_index, int ants_by_thread, Ant[] ants, String weight, double alpha, double beta) {
		this.graph = graph;
		this.source = source;
		this.target = target;
		this.ant_thread_index = ant_thread_index;
		this.ants_by_thread = ants_by_thread;
		this.ants = ants;
		this.weight = weight;
		this.alpha = alpha;
		this.beta = beta;
		this.util = new Util();
		this.badpath = new HashMap<>();
	}

	@Override
	public void run() {
		
		bestAnt = null;
		
		for (int k = ant_thread_index; k < (ant_thread_index + ants_by_thread); k++) {
			
			Ant ant = ants[k];
			
			while (!target.equals(ant.getCurrent_node())) {
				
				Node next = getNextNode(ant);
				
				if (next == null) {
					if (ant.getVisitedEdges().size() > 0) {
						ArrayList<String> aux = new ArrayList<>(ant.getVisitedEdges().keySet());
						badpath.put(aux.get(aux.size()-1), k);
					}

					ant.reset(source);
					break;
				}
				
				Edge edge = graph.findEdge(ant.getCurrent_node(), next);
				
				ant.incTourLenght(edge.getWeight(weight));
				
				ant.addVisitedNode(next);
				
				ant.addVisitedEdge(edge);
				
				ant.setCurrentNode(next);
				
				if (target.equals(ant.getCurrent_node())) {
					
					ant.newSolution();
					
					for (Edge e : graph.edges.values()) {
						
						double delta = 0;
						
						double pheromone = e.getPheromone();
						
						
						if (ant.hasVisitedEdge(e.getOrigin(), e.getDestiny()))
							delta = 1.0 / ant.getTourLenght();
							
						pheromone = (1.0 - 0.5) * pheromone + delta;
						
						// TODO
						if (pheromone < 0.0000000000000000001)
							pheromone = 0.00000001;
						
						e.setPheromone(pheromone);
					}
					
					if (bestAnt == null)
						bestAnt = ant;
					else if (ant.getTourLenght() < bestAnt.getTourLenght())
						bestAnt = ant;
				}
			}
			
		}
	}

	private Node getNextNode(Ant ant) {
		
		double prob = 0;
		
		if (ant.getCurrent_node().getEdges().size() == 0)
			return null;
		
		List<Tuple<Double, Node>> probList = new ArrayList<Tuple<Double, Node>>();
		
		for (Edge neighbor : ant.getCurrent_node().getEdges().values()) {
			
			if (ant.hasVisitedNode(neighbor.getDestiny()) || badpath.containsKey(neighbor.getName()))
				continue;
			
			prob = compute_probabilitie(ant.getCurrent_node(), neighbor.getDestiny(), ant);
			
			probList.add(new Tuple<Double, Node>(prob, neighbor.getDestiny()));
		}
		
		return choice(probList);
	}
	
	private double compute_probabilitie(Node current, Node next, Ant k) {
		
		if (k.getVisitedNodes().containsKey(next.getName()))
			return 0;
		
		Edge edge = current.getEdgeByDestiny(next);
		
		double pheromone = 0;
		double heuristic = 0;
		double sum = 0;
		
		for (Edge succ : current.getEdges().values()) {
			if (k.hasVisitedNode(succ.getDestiny()) || badpath.containsKey(succ.getDestiny().getName()))
				continue;
			sum += Math.pow(succ.getPheromone(), alpha) * Math.pow(1.0/succ.getWeight(weight), beta);
		}
		
		if (sum == 0)
			sum = 1;
		
		pheromone = Math.pow(edge.getPheromone(), alpha);
		heuristic = Math.pow(1.0/edge.getWeight(weight), beta);
		
		double prob = (pheromone * heuristic) / sum;
		
		return prob;
	}
	
	private Node choice(List<Tuple<Double, Node>> probList) {
		Random rnd = new Random();
		
		double st = rnd.nextDouble();
		double r = rnd.nextDouble();
		
		if (probList.size() == 1)
			return probList.get(0).getE2();
		
		if (st < RANDOM_COEFFICIENT && probList.size() > 0) {
			Collections.shuffle(probList);			
			return probList.get(0).getE2();
		}
				
		for (Tuple<Double, Node> tuple : probList) {
			if (r <= tuple.getE1())				
				return tuple.getE2();
			
			r -= tuple.getE1();
		}
		
		return null;
	}
	
	public Ant getBestAnt() {
		return bestAnt;
	}

}
