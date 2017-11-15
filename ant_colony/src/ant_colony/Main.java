package ant_colony;

import java.io.IOException;
import java.util.ArrayList;

public class Main {

	public static void main(String[] args) throws IOException, InterruptedException {
		
		Graph gp = new Graph(0);
		
//		new RandomParams().run();
		
		new TestParams().run();

//		System.out.printf("Nodes: %d Edges: %d\n", gp.nodes.size(), gp.edges.size());		
//		
//		double best = Double.MAX_VALUE;
//		
//		String ar[] = {"425S7", "310S12"};
//		
//		System.out.println("Source, Target: " + ar[0] + ", " + ar[1]);
//		
//		for  (int i=0; i<10;i++) {
//			System.out.println("Amostra " + i);
//			
//			double t1, t2;
//			
//			t1 = System.currentTimeMillis();
//			AntColonyOptimization aco = new AntColonyOptimization(new Graph(0.0049266369712296565 ), 11000, 500, 2.1347299285358345, 0.6669893180937014, 0.3297709837354471, "weight", ar[0]);
//			Tuple<Double, ArrayList<String>> result = aco.run(ar[1]);
//			t2 = System.currentTimeMillis();
//			if (result.getE2().size() > 0) {
//				if (result.getE1() < best)
//					best = result.getE1();
//				System.out.printf("Cost: %2f - Path: %s\n", result.getE1(), result.getE2().toString());
//			}
//			else
//				System.out.println("Sem solucao");
//			System.out.printf("Run time: %2f \n\n", (t2-t1)/1000);
//		}
//		
//		System.out.println("Best: " + best);
	}
}