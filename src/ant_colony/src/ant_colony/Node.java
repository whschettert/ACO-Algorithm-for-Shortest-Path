package ant_colony;

import java.util.LinkedHashMap;
import java.util.Map;

public class Node {
	
	private String name;
	
	private double latitude;
	
	private double longitude;
	
	private Boolean visited;
	
	private Map<String, Edge> edges = new LinkedHashMap<>();
	
	public Node(String name, double latitude, double longitude) {
		this.name = name;
		this.latitude = latitude;
		this.longitude = longitude;
	}
	
	public void addEdge(String destiny, Edge edge) {
		edges.put(destiny, edge);
	}

	public Map<String, Edge> getEdges() {
		return edges;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public double getLatitude() {
		return latitude;
	}

	public void setLatitude(double latitude) {
		this.latitude = latitude;
	}

	public double getLongitude() {
		return longitude;
	}

	public void setLongitude(double longitude) {
		this.longitude = longitude;
	}

	public Boolean getVisited() {
		return visited;
	}

	public void setVisited(Boolean visited) {
		this.visited = visited;
	}
	
	public Edge getEdgeByDestiny(Node destiny) {
		return edges.get(destiny.getName());
	}
	
	@Override
	public String toString() {
		return name;
	}

	@Override
	public boolean equals(Object o) {
		if (o == null)
			return false;
		
		if (!Node.class.isAssignableFrom(o.getClass()))
			return false;
		
		final Node node = (Node) o;
		
		return this.name.equals(node.getName());
	}
	
}
