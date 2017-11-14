package ant_colony;

import java.io.IOException;
import java.util.ArrayList;

public class Main {

	public static void main(String[] args) throws IOException, InterruptedException {
		
		Graph gp = new Graph("graph.txt", 0);
		
		Util util = new Util();
		
		new RandomParams().run();
		
//		for (int i=0;i<20;i++) {
//			System.out.println(util.randRange(0.2, 0.95));
//		}
		
//		if (true)
//			return;

		System.out.printf("Nodes: %d Edges: %d\n", gp.nodes.size(), gp.edges.size());
		
//		
		
//		String ar[] = {"10S10", "130S21"};
//		String ar[] = {"90S0", "219S7"};
//		String ar[] = {"1S0", "8S37"};
		String ar[] = {"7S3", "104S9"};
		
		double best = Double.MAX_VALUE;
		
		for  (int i=0; i<10;i++) {
			System.out.println("Amostra " + i);
			
			double t1, t2;
			
			t1 = System.currentTimeMillis();
			AntColonyOptimization aco = new AntColonyOptimization(new Graph("graph.txt", 0.0001), 10000, 500, 1, 0.5, 0.5, "weight", ar[0]);
			Tuple<Double, ArrayList<String>> result = aco.run(ar[1]);
			t2 = System.currentTimeMillis();
			if (result.getE2().size() > 0) {
				if (result.getE1() < best)
					best = result.getE1();
				System.out.printf("Cost: %2f - Path: %s\n", result.getE1(), result.getE2().toString());
			}
			else
				System.out.println("Sem solucao");
			System.out.printf("Run time: %2f \n\n", (t2-t1)/1000);
		}
		
		System.out.println("Best: " + best);
	}
}
