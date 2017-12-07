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
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(10,14), new Params(13000, 500, 0.00323785881583585, 4.47695064596545, 0.2752473157234814, 0.742637634868853, "", "")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(20,24), new Params(13000, 500, 0.000277201357131145, 4.02905805897487, 1.012739801074115, 0.312711485473852, "", "")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(30,34), new Params(12000, 500, 0.00861821851041004, 3.88921715624105, 2.5138228981984807, 0.872182700296826, "", "")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(40,44), new Params(12000, 500, 0.000738522854477927, 4.72743338580322, 0.194600080393372, 0.47351094376164, "", "")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(50,54), new Params(14000, 500, 0.005737784583950242, 2.343907654893633, 0.35194514072547534, 0.3876243988010378, "", "")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(60,64), new Params(14000, 500, 0.005575580484252124, 4.354077057457647, 1.803416085553875, 0.3111352160998969, "", "")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(70,74), new Params(20000, 500, 0.004836146482033643, 2.0040331845764, 0.15212628094981417, 0.34588802143414393, "", "")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(80,84), new Params(10000, 500, 0.005806632585866077, 3.7008223439976367, 0.0823497287227872, 0.9335343053405849, "", "")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(90,94), new Params(10000, 500, 0.005783940300653847, 0.8062283688184391, 0.0014237056513854984, 0.5909983989504586, "", "")),
				new Tuple<Tuple<Integer, Integer>, Params>(new Tuple<Integer, Integer>(100,104), new Params(17000, 500, 0.007451, 2.1757, 0.39347, 0.43626, "", ""))
				
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
			//  arr_nodes.add(dists_nodes.remove(0).getE2());
			
			// pares gerados aleatoriamente
			Tuple<Tuple<Integer, Integer>, Params> dist = dists_nodes.get(0);
			source = nodes.get(rn.nextInt(nodes.size()));
			target = nodes.get(rn.nextInt(nodes.size()));
			if (validatePair(g.nodes.get(source), g.nodes.get(target), dist)) {
				dist.getE2().source = source;
				dist.getE2().target = target;
				arr_nodes.add(dist.getE2());
				System.out.println(dist.getE2().source + "-" + dist.getE2().target);
				dists_nodes.remove(0);
			}
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
						param.numAnts, 500, param.alpha, param.beta, param.evaporation, "timeTravel", param.source);
				
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


