package ant_colony;

import java.io.IOException;
import java.util.ArrayList;

public class Main {

	public static void main(String[] args) throws IOException, InterruptedException {
		
		Graph gp = new Graph(0);
	
		System.out.printf("Nodes: %d Edges: %d\n", gp.nodes.size(), gp.edges.size());		

		// new RandomParams().run();
		
		// new TestParams().run();		
		
		String ar[] = {"240S7", "244S25"};
		
		System.out.println("Source, Target: " + ar[0] + ", " + ar[1]);

		double best = Double.MAX_VALUE;

		for  (int i=0; i<10;i++) {
			System.out.println("Amostra " + i);
			
			double t1, t2;
			
			t1 = System.currentTimeMillis();
			AntColonyOptimization aco = new AntColonyOptimization(new Graph(5.742833632352706E-4), 11000, 500, 1.4011383918681863, 0.06718677403557849, 0.9325204351890948, "weight", ar[0]);
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
