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
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(10,14), new Params(11000, 500, 0.00454086890194393, 4.22485815330664, 0.098463467848146, 0.738033854470105, "398S5", "423S4")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(20,24), new Params(11000, 500, 0.00057428336323527, 1.40113839186818, 0.671867740355784,	0.932520435189094, "439S1", "525S9")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(30,34), new Params(16000, 500, 0.00938973013753504, 4.89074108324041, 0.236287969061914, 0.70157055583896, "591S48", "416S27")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(40,44), new Params(17000, 500, 0.00357954034147196, 4.75812603323567, 2.50055407112918, 0.764991688847031, "311S13", "363S19")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(50,54), new Params(17000, 500, 0.00601493670647097, 0.42515935150438, 0.0248860232737169, 0.904061270232578, "98S8", "591S63")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(60,64), new Params(14000, 500, 0.00379520320924374, 1.81887566191999, 0.0252688911255433, 0.644589642143173, "564S2", "637S19")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(70,74), new Params(11000, 500, 0.00173846712644101, 4.66500425419624, 0.204994981834971, 0.893953894928224, "527S8", "591S86")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(80,84), new Params(13000, 500, 0.000426261492134647, 4.08933257373996, 0.0964400208487564, 0.688435080629192, "490S8", "637S26")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(90,94), new Params(11000, 500, 0.00266975604879154, 1.02266783665256, 0.0417999511611427, 0.358615034407506, "464S17", "637S26")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(100,104), new Params(11000, 500, 0.00492663697122965, 2.13472992853583, 0.666989318093701, 0.329770983735447, "604S1", "637S31"))
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


