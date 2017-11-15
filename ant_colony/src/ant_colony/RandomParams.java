package ant_colony;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.Random;

public class RandomParams {
	
	private Util util;
	
	private Graph g;
	
	ArrayList<Tuple<Node, Node>> arr_nodes = new ArrayList<>();
	
	ArrayList<Tuple<Integer, Integer>> dists_nodes = new ArrayList<Tuple<Integer,Integer>>();
	
	public RandomParams() {
		util = new Util();
		
		dists_nodes.addAll(Arrays.asList(
				new Tuple<Integer,Integer>(10,14),
				new Tuple<Integer,Integer>(20,24),
				new Tuple<Integer,Integer>(30,34),
				new Tuple<Integer,Integer>(40,44),
				new Tuple<Integer,Integer>(50,54),
				new Tuple<Integer,Integer>(60,64),
				new Tuple<Integer,Integer>(70,74),
				new Tuple<Integer,Integer>(80,84),
				new Tuple<Integer,Integer>(90,94),
				new Tuple<Integer,Integer>(100,104)));
	}
	
	
	
	public void run() throws IOException, InterruptedException {
		g = new Graph("graph.txt", 0.0001);
		
		String source, target = null;
		
		ArrayList<String> nodes = new ArrayList<>(g.nodes.keySet());
		
		Random rn = new Random();
		
		Date d = new Date();
		
		SimpleDateFormat dt = new SimpleDateFormat("dd-MM-yyyy '-' HH.mm.ss");
		
		PrintWriter f = new PrintWriter("../out/" + dt.format(d) +".txt", "UTF-8");
		
		int numAnts = 0;
		double init_pheromone = 0;
		double alpha = 0;
		double beta = 0;
		double evaporation = 0;
		
		double bestResult = 0;
		double avgResult = 0;
		double stdResult = 0;
		ArrayList<Tuple<Double, ArrayList<String>>> acoResultClean;
		ArrayList<Tuple<Double, ArrayList<String>>> acoResults;
		
		double parametersRunTime = 0;
		double timeAllTests = System.currentTimeMillis();
		
		while(arr_nodes.size() < 10) {
			source = nodes.get(rn.nextInt(nodes.size()));
			target = nodes.get(rn.nextInt(nodes.size()));
			
			if (checkValidPair(g.nodes.get(source), g.nodes.get(target)))
				arr_nodes.add(new Tuple<Node, Node>(g.nodes.get(source), g.nodes.get(target)));
		}
		
		for (Tuple<Node,Node> nodePair : arr_nodes) {
			
			f.println("Source, Target " + nodePair + " -: " + 
			util.haversine(nodePair.getE1().getLatitude(), nodePair.getE1().getLongitude(), nodePair.getE2().getLatitude(), nodePair.getE2().getLongitude()));
			
			parametersRunTime = System.currentTimeMillis();
			for (int i = 0; i < 20; i++) {
				System.out.println("Amostra " + i);
				
				numAnts = util.randRange(10000, 20000, 1000);
				init_pheromone = util.randRange(0.0001, 0.01);
				alpha = util.randRange(0.0, 5);
				beta = util.randRange(0.0, 5);
				evaporation = util.randRange(0.3, 0.95);
				
				f.println("AMOSTRAGEM " + i);
				f.println("Ants:" + numAnts + " - Pheromone:" + init_pheromone + " - Alpha:" + alpha + " - Beta:" + beta + " - Evaporation:" + evaporation);
				
				acoResults = new ArrayList<>();
				
				for (int j=0 ; j<10; j++) {
					double t1, t2;
					
					t1 = System.currentTimeMillis();
					AntColonyOptimization aco = new AntColonyOptimization(new Graph("graph.txt", init_pheromone), numAnts, 500, alpha, beta, evaporation, "weight", nodePair.getE1().getName());
					Tuple<Double, ArrayList<String>> result = aco.run(nodePair.getE2().getName());
					t2 = System.currentTimeMillis();
					if (result.getE2().size() > 0)
						f.printf("Cost: %2f - Path: %s", result.getE1(), result.getE2().toString());
					else
						f.printf("Sem solucao");
						f.printf("Run time: %2f \n", (t2-t1)/1000);
						
					acoResults.add(result);
				}
				
				acoResultClean = new ArrayList<>();
				for (Tuple<Double, ArrayList<String>> tuple : acoResults) {
					if (tuple.getE2().size() == 0)
						continue;
					acoResultClean.add(tuple);
				}
				
				if (acoResultClean.size() > 0) {
					bestResult = util.min(acoResultClean);
					avgResult = util.sum(acoResultClean)/acoResultClean.size();
					stdResult = util.getStdDev(acoResultClean);
				}
				
				f.printf("Best result: %2f - Average Result: %2f - Standard Deviation: %2f - Run time: %2f\n", bestResult, avgResult, stdResult, (System.currentTimeMillis()-parametersRunTime)/1000);
				f.flush();
			}
			
			f.printf("TOTAL RUNNING TIME: %2f\n", (System.currentTimeMillis() - timeAllTests)/1000);
		}
		
		f.close();
	}
	
	public boolean checkValidPair(Node source, Node target) {
		
		if (!g.hasPath(source,  target))
			return false;
		
		double haversine = util.haversine(source.getLatitude(), source.getLongitude(), target.getLatitude(), target.getLongitude());
		
		int index = -1;
		
		for (int i=0; i<dists_nodes.size();i++) {
			if (dists_nodes.get(i).getE1() <= haversine && haversine <= dists_nodes.get(i).getE2()) {
				index = i;
				break;
			}
		}
		
		if (index >= 0) {
			dists_nodes.remove(index);
			return true;
		}
		
		return false;
	}
	
	

}
