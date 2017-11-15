package ant_colony;

import java.io.IOException;
import java.util.ArrayList;

public class Main {

	public static void main(String[] args) throws IOException, InterruptedException {
		
		Graph gp = new Graph("graph_params.txt", 0);
		
		Util util = new Util();
		
//		new RandomParams().run();

		System.out.printf("Nodes: %d Edges: %d\n", gp.nodes.size(), gp.edges.size());		

		String ar[] = {"53S4", "246S3"};
		
		double best = Double.MAX_VALUE;
		
		for  (int i=0; i<10;i++) {
			System.out.println("Amostra " + i);
			
			double t1, t2;
			
			t1 = System.currentTimeMillis();
			AntColonyOptimization aco = new AntColonyOptimization(new Graph("graph_test.txt", 0.004540868901943936), 20000, 500, 2.3, 0, 0.7380338544701056, "weight", ar[0]);
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
