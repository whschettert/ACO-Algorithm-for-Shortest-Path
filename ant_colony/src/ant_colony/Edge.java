package ant_colony;

public class Edge {
	
	private double weight;
	
	private double travelTime;
	
	private double pheromone;
	
	private Node origin;
	
	private Node destiny;
	
	public Edge(Node origin, Node destiny, double weight, double traveltime, double pheromone) {
		this.weight = weight;
		this.travelTime = traveltime;
		this.pheromone = pheromone;
		this.origin = origin;
		this.destiny = destiny;
	}

	public Node getOrigin() {
		return origin;
	}

	public void setOrigin(Node origin) {
		this.origin = origin;
	}

	public Node getDestiny() {
		return destiny;
	}
	
	public String getName() {
		return origin.getName() +  "-" + destiny.getName();
	}

	public void setDestiny(Node destiny) {
		this.destiny = destiny;
	}

	public double getWeight(String s) {
		if (s == "weight")
			return weight;
		return travelTime;
	}

	public double getPheromone() {
		return pheromone;
	}

	public void setPheromone(double pheromone) {
		this.pheromone = pheromone;
	}
	
	public String toString() {
		return origin.getName() + "-" + destiny.getName();
	}
}
