package ant_colony;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;

public class Graph {
	
	public Map<String, Node> nodes = new HashMap<>();
	
	public Map<String, Edge> edges = new HashMap<>();
	
	private Util util;
	
	public double initialPheromone;
	
	public Graph(double initialPheromone) throws IOException {
		
		util = new Util(); 
		
		this.initialPheromone = initialPheromone;
		
		String path = "../data/graph_test.txt";
		
		FileReader fr = new FileReader(path);
		
		BufferedReader br = new BufferedReader(fr);
		
		br.readLine();	
		
		String line = "";
		String[] args;
		
		Node s, t = null;
		
		while (!(line = br.readLine()).contains("EDGE")) {
			
			args = line.split("\\|");
			
			nodes.put(args[0], new Node(args[0], Double.parseDouble(args[1]), Double.parseDouble(args[2])));
		}
		
		while((line = br.readLine()) != null) {
			
			args = line.split("\\|");
			
			s = nodes.get(args[0]);
			
			t = nodes.get(args[1]);
			
			edges.put(args[0] + "-" + args[1], new Edge(s, t, Double.parseDouble(args[2]), Double.parseDouble(args[3]), initialPheromone));
						
			s.addEdge(args[1], edges.get(args[0] + "-" + args[1]));
		}
		
		br.close();
		fr.close();
	}
	
	public Edge findEdge(Node n1, Node n2) {
		return edges.get(n1.getName() + "-" + n2.getName());
	}
	
	public boolean hasPath(Node source, Node target) {
		NodeComparator comparator = new NodeComparator();
		PriorityQueue<Tuple<Double, Node>> pQueue = new PriorityQueue<Tuple<Double,Node>>(comparator);
		HashMap<String, Node> visited = new HashMap<>();
		
		Node current = source;
		double heuristic = 0;
		
		while(true) {
			visited.put(current.getName(), current);
			
			if (current.equals(target))
				return true;
			
			for (Edge neighbour: current.getEdges().values()) {
				if (visited.containsKey(neighbour.getDestiny().getName()))
					continue;
				
				Node n = neighbour.getDestiny();
				heuristic = util.haversine(n.getLatitude(), n.getLongitude(), target.getLatitude(), target.getLongitude());
				pQueue.add(new Tuple<Double, Node>(heuristic, n));
			}
			
			if (pQueue.size() == 0)
				return false;
			
			current = pQueue.remove().getE2();
		}
				
	}
	
	public class NodeComparator implements Comparator<Tuple<Double,Node>> {

		@Override
		public int compare(Tuple<Double, Node> o1, Tuple<Double, Node> o2) {
			// TODO Auto-generated method stub
			if (o1.getE1() < o2.getE1())
				return -1;
			if (o1.getE1() > o2.getE1())
				return 1;
			return 0;
		}

	}
	
    public boolean checkValidPair(Node source, Node target, ArrayList<Tuple<Integer, Integer>> dists_nodes) {
		
		if (!hasPath(source,  target))
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
