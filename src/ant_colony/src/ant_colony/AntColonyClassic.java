package ant_colony;

import java.util.ArrayList;
import java.util.HashMap;

public class AntColonyClassic {
	
	private static final int NUM_THREAD = Runtime.getRuntime().availableProcessors();
	
	private int numAnts;
	
	private int numIterations;
	
	private double alpha;
	
	private double beta;
	
	private double evaporation;
	
	private String weight;
	
	private Node source;
	
	private Graph graph;
	
	private Ant[] ants;
	
	public AntColonyClassic(Graph graph, int numAnts, int numIterations,
			double alpha, double beta, double evaporation, String weight, String source) {
	
		this.graph = graph;
		this.numAnts = numAnts;
		this.numIterations = numIterations;
		this.alpha = alpha;
		this.beta = beta;
		this.evaporation = evaporation;
		this.weight = weight;
		this.source = graph.nodes.get(source);
		ants = new Ant[numAnts];
		
		for (int i=0; i<numAnts;i++) {
			ants[i] = new Ant(graph.nodes.get(source));
		}
		
	}
	
	public void run(String t) throws InterruptedException {
	
		Node target = graph.nodes.get(t);
		
		Ant bestAnt = null;
		
		int ants_by_thread = numAnts / NUM_THREAD;
		
		int ant_thread_index = 0;
		
		ArrayList<Thread> threads = new ArrayList<>(); 
		ArrayList<ClassicAco> progs = new ArrayList<>();
		
		double cost = 0;
		boolean newC = false;
		
		for (int i = 0; i < numIterations; i++) {
			
//			bestAnt = null;
			
			ant_thread_index = 0;
			threads = new ArrayList<Thread>(); 
			progs = new ArrayList<ClassicAco>();
			
			for (int j = 0; j < NUM_THREAD; j++) {
				progs.add(new ClassicAco(graph, source, target, ant_thread_index, ants_by_thread, ants, weight, alpha, beta));
				threads.add(new Thread(progs.get(j)));
				ant_thread_index += ants_by_thread;
				threads.get(j).start();
			}
			
			for (Thread th : threads) {
				th.join();
			}
			
			for (ClassicAco acoThread : progs) {
				if (acoThread.getBestAnt() != null) {
					if (bestAnt == null)
						bestAnt = acoThread.getBestAnt();
					else if (acoThread.getBestAnt().getTourLenght() < bestAnt.getTourLenght())
						bestAnt = acoThread.getBestAnt();
				}
			}
			
			updatePheromone(bestAnt);
			
			if (bestAnt != null) {
				if (cost == 0) {
					cost = bestAnt.getCost();
					newC = true;
				}
				else if (bestAnt.getCost() < cost) {
					cost = bestAnt.getCost();
					newC = true;
				}
			}
			
			if (newC) {
				newC = false;
				System.out.printf("IT: %d Bad: %d Cost: %f \n", i, progs.get(0).badpath.size(), cost);
			}
		}
		
		getSolution();
	}
	
	public void updatePheromone(Ant bestAnt) {
		for (Edge edge : graph.edges.values()) {
			
			double delta = 0;
			
			double pheromone = edge.getPheromone();
			
			if (bestAnt != null)
				if (bestAnt.hasVisitedEdge(edge.getOrigin(), edge.getDestiny()))
					delta = 1.0 / bestAnt.getTourLenght();
				
			pheromone = (1.0 - evaporation) * pheromone + delta;
			
			// TODO
			if (pheromone < 0.0000000000000000001)
				pheromone = 0.00000001;
			
			edge.setPheromone(pheromone);
		}
	}
	
	private void getSolution() {
		
		Ant best = null;
		
		for (Ant ant : ants) {
			
			if (ant.getSolutionPath().size() == 0)
				continue;
			
			if (best == null)
				best = ant;
			else if (ant.getCost() < best.getCost())
				best = ant;
		}
		
		if (best != null)
			System.out.println("Custo: " + best.getCost() +" - Caminho: "+ best.getSolutionPath().toString());
		else
			System.out.println("Sem solucao");
	}

}
