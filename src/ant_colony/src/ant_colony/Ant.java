package ant_colony;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class Ant {
	
	private Map<String, Node> visitedNodes = new LinkedHashMap<>();
	
	private Map<String, Edge> visitedEdges = new LinkedHashMap<>();
	
	private Map<String, Integer> alreadyChecked = new LinkedHashMap<>();
	private Map<String, Node> newNodes = new LinkedHashMap<>();
	private Map<String, Edge> newEdges = new LinkedHashMap<>();
	private double newTour = -1;
	private Node newCurrent = null;
	
	private double tour_lenght;
	
	private double cost;
	
	private ArrayList<String> solutionPath = new ArrayList<>();
	
	private Node current_node;
	
	public Ant(Node source) {
		current_node = source;
		visitedNodes.put(source.getName(), source);
		tour_lenght = 0;
		
		cost = -1;
	}
	
	public void reset(Node source) {
		current_node = source;
		
		visitedNodes = new LinkedHashMap<>();
		visitedEdges = new LinkedHashMap<>();
		alreadyChecked = new LinkedHashMap<>();
		
		visitedNodes.put(source.getName(), source);
		
		tour_lenght = 0;
	}
	
	public boolean hasVisitedNode(Node node) {
		return visitedNodes.containsKey(node.getName());
	}
	
	public boolean hasVisitedEdge(Node n1, Node n2) {
		return visitedEdges.containsKey(n1 + "-" + n2);
	}
	
	public Map<String, Node> getVisitedNodes() {
		return visitedNodes;
	}

	public Map<String, Edge> getVisitedEdges() {
		return visitedEdges;
	}
	
	public Map<String, Integer> getAlreadyChecked() {
		return alreadyChecked;
	}
	
	public void addVisitedNode(Node n) {
		visitedNodes.put(n.getName(), n);
	}
	
	public void addVisitedEdge(Edge e) {
		visitedEdges.put(e.getName(), e);
	}

	public double getTourLenght() {
		return tour_lenght;
	}

	public void incTourLenght(double val) {
		this.tour_lenght += val;
	}
	
	public void seTourLenght(double val) {
		this.tour_lenght = val;
	}

	public void setVisitedNodes(Map<String, Node> visitedNodes) {
		this.visitedNodes = visitedNodes;
	}

	public void setVisitedEdges(Map<String, Edge> visitedEdges) {
		this.visitedEdges = visitedEdges;
	}

	public double getCost() {
		return cost;
	}

	public ArrayList<String> getSolutionPath() {
		return solutionPath;
	}

	public Node getCurrent_node() {
		return current_node;
	}

	public void setCurrentNode(Node current_node) {
		this.current_node = current_node;
	}

	public void newSolution() {
		if (cost < 0 || tour_lenght < cost) {
			solutionPath = new ArrayList<>(visitedNodes.keySet());
			cost = tour_lenght;
		}
	}
	
	public String toString() {
		return "Cost:" + cost + "\nCurrentNode: " + current_node;
	}
	
	public boolean hasLastBridge() {
		return newTour >= 0;
	}
	
	public void setLastBridge() {
		visitedEdges = new LinkedHashMap<>(newEdges);
		visitedNodes = new LinkedHashMap<>(newNodes);
		tour_lenght = newTour;
		current_node = newCurrent;
		
		newTour = -1;
	}
	
	public void buildLastBridge(List<Tuple<Double, Node>> probList) {
		if (newTour > 0)
			return;
		
		alreadyChecked.put(current_node.getName(), 0);
		
		newEdges = new LinkedHashMap<>(visitedEdges);
		newNodes = new LinkedHashMap<>(visitedNodes);
		newTour = tour_lenght;
		
		for (Tuple<Double, Node> tuple : probList) {
			
			if (!alreadyChecked.containsKey(tuple.getE2().getName())) {
				newCurrent = tuple.getE2();
				break;
			}
		}
	}

}
