package ant_colony;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.Random;

public class TestParams {
	
	private Util util;
	Graph g;

	public TestParams() throws IOException {
		this.util = new Util();
		this.g = new Graph(0);
	}
	
	public void run() throws IOException, InterruptedException {
		
		ArrayList<Tuple<Tuple<Integer, Integer>, Params>> dists_nodes = new ArrayList<>();
		
		dists_nodes.addAll(Arrays.asList(
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(20,24), new Params(10000, 500, 0.001300568018154422, 3.5453538979317614, 0.33500983208537893, 0.37870467710191685, "39S1", "61S0")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(10,14), new Params(16000, 500, 0.0063353088584364, 1.3962429970803614, 0.3068086831856759, 0.3099138008830667, "241S1", "160S11")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(30,34), new Params(13000, 500, 0.0023336142115786846, 0.522514651109075, 0.0765991524247367, 0.5811955425428774, "458S2", "57S5")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(40,44), new Params(14000, 500, 0.0010440373512414299, 1.7263098448602787, 0.06647868855316985, 0.8880839857525336, "174S5", "232S43")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(50,54), new Params(17000, 500, 0.006334488679871194, 0.11505926807957145, 0.00744865219720503, 0.42248344822971867, "641S3", "174S10")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(60,64), new Params(13000, 500, 0.008191928718105097, 1.767255738432569, 1.8682476134382369, 0.34204419349976317, "42S0", "37S23")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(70,74), new Params(14000, 500, 0.00536819648506351, 1.7453084763243891, 0.4125457268129333, 0.37586866066323293, "41S26", "130S15")),				
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(80,84), new Params(17000, 500, 3.097382799551567E-4, 0.6479181999934513, 0.20324537450723934, 0.5238581133892463, "625S9", "130S17")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(90,94), new Params(18000, 500, 3.4569712402988365E-4, 2.2792071390392543, 0.7486322909156092, 0.7472330760872458, "253S2", "130S22")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(100,104), new Params(13000, 500, 0.002979989166906917, 4.342049917001485, 0.11152733342115806, 0.7565399197229654, "162S8", "130S27"))
				
				));
		
		String source, target = null;
		
		ArrayList<String> nodes = new ArrayList<>(g.nodes.keySet());
		
		ArrayList<Params> arr_nodes = new ArrayList<>();
		
		Random rn = new Random();
		
		Date d = new Date();
		
		SimpleDateFormat dt = new SimpleDateFormat("dd-MM-yyyy '-' HH.mm.ss");
		
		PrintWriter f = new PrintWriter("../out/result/" + dt.format(d) +".txt", "UTF-8");
		
		double bestResult = 0;
		double avgResult = 0;
		double stdResult = 0;
		ArrayList<Tuple<Double, ArrayList<String>>> acoResultClean;
		ArrayList<Tuple<Double, ArrayList<String>>> acoResults;
		
		double parametersRunTime = 0;
		double timeAllTests = System.currentTimeMillis();
		
		while(dists_nodes.size() > 0) {
			// para quando ja possui os pares
			arr_nodes.add(dists_nodes.remove(0).getE2());
			
			// pares gerados aleatoriamente
//			Tuple<Tuple<Integer, Integer>, Params> dist = dists_nodes.get(0);
//			source = nodes.get(rn.nextInt(nodes.size()));
//			target = nodes.get(rn.nextInt(nodes.size()));
//			if (validatePair(g.nodes.get(source), g.nodes.get(target), dist)) {
//				dist.getE2().source = source;
//				dist.getE2().target = target;
//				arr_nodes.add(dist.getE2());
//				dists_nodes.remove(0);
//			}
		}
		
		for (Params param : arr_nodes) {
			
			f.println("Source, Target " + param.source + ", " + param.target + " : " + util.haversine(g.nodes.get(param.source).getLatitude(), 
					g.nodes.get(param.source).getLongitude(), g.nodes.get(param.target).getLatitude(), g.nodes.get(param.target).getLongitude()));
			
			f.println("Ants:" + param.numAnts + " - Pheromone:" + param.initialPheromone + " - Alpha:" + param.alpha + " - Beta:" + param.beta + " - Evaporation:" + param.evaporation);
			
			parametersRunTime = System.currentTimeMillis();
			
			acoResults = new ArrayList<>();
			
			for (int i = 0; i < 10; i++) {
				System.out.println("Amostra " + i);
				
				f.println("AMOSTRAGEM " + i);
				
				double t1, t2;
				
				t1 = System.currentTimeMillis();
				
				AntColonyOptimization aco = new AntColonyOptimization(new Graph(param.initialPheromone), 
						param.numAnts, 500, param.alpha, param.beta, param.evaporation, "travelTime", param.source);
				
				Tuple<Double, ArrayList<String>> result = aco.run(param.target);
				
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
			
			f.printf("Best result: %2f - Average Result: %2f - Standard Deviation: %2f - Run time: %2f\n\n", bestResult, avgResult, stdResult, (System.currentTimeMillis()-parametersRunTime)/1000);
			f.flush();
		}
		
		f.printf("TOTAL RUNNING TIME: %2f\n", (System.currentTimeMillis() - timeAllTests)/1000);
		
		f.close();
	}
	

	
	private boolean validatePair(Node source, Node target, Tuple<Tuple<Integer, Integer>, Params> dist) {
		if (!g.hasPath(source, target))
			return false;
		
		double haversine = util.haversine(source.getLatitude(), source.getLongitude(), target.getLatitude(), target.getLongitude());
		
		if (dist.getE1().getE1() <= haversine && haversine <= dist.getE1().getE2())
			return true;
		
		return false;
	}



	class Params {
		public int numAnts;
		public int numIterations;
		public double alpha;
		public double beta;
		public double evaporation;
		public double initialPheromone;
		public String source;
		public String target;
		
		public Params(int numAnts, int numIterations, double initialPheromone, double alpha, double beta, double evaporation, String source, String target) {
			this.numAnts = numAnts;
			this.numIterations = numIterations;
			this.alpha = alpha;
			this.beta = beta;
			this.evaporation = evaporation;
			this.initialPheromone = initialPheromone;
			this.source = source;
			this.target = target;
		}
		
	}
	
}


