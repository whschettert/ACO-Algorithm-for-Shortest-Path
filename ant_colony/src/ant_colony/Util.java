package ant_colony;

import java.util.ArrayList;
import java.util.Date;
import java.text.ParseException;
import java.text.SimpleDateFormat;

public class Util {
    
	private static final int EARTH_RADIUS = 6371; // Approx Earth radius in KM
	
	
	public Util() {

	}

    public double haversine(double startLat, double startLong, double endLat, double endLong) {

        double dLat  = Math.toRadians((endLat - startLat));
        double dLong = Math.toRadians((endLong - startLong));

        startLat = Math.toRadians(startLat);
        endLat   = Math.toRadians(endLat);

        double a = haversin(dLat) + Math.cos(startLat) * Math.cos(endLat) * haversin(dLong);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

        return EARTH_RADIUS * c; // <-- d
    }

    private double haversin(double val) {
        return Math.pow(Math.sin(val / 2), 2);
    }
    
    public Tuple<Node,Double> mediumPoint(Graph graph, Node current) {
    	
    	double dist = 0;
    	
    	for (Node node : graph.nodes.values()) {
			
    		dist = haversine(current.getLatitude(), current.getLongitude(), node.getLatitude(), node.getLongitude());
    		
    		if (dist <= 0.3)
    			return new Tuple<Node, Double>(node, dist);
		}
    	
    	return null;
    }
    
    public double timeDiff(String time1, String time2) {
    	SimpleDateFormat format = new SimpleDateFormat("HH:mm:ss");
    	try {
	    	Date date1 = format.parse(time1);
	    	Date date2 = format.parse(time2);
	    	
	    	double milliseconds = date2.getTime() - date1.getTime();
			return milliseconds / 1000.0;
    	}
    	catch (ParseException e) {
    		return 0;
		}
    }
    
    public double min (ArrayList<Tuple<Double, ArrayList<String>>> values) {
		double min = Double.MAX_VALUE;
		for (Tuple<Double, ArrayList<String>> tuple : values)			
			if (tuple.getE1() < min)
				min = tuple.getE1();
		
		if (min == Double.MAX_VALUE)
			return 0;
		
		return min;
	}
	
	public double sum (ArrayList<Tuple<Double, ArrayList<String>>> values) {
		double sum = 0;
		for (Tuple<Double, ArrayList<String>> tuple : values)
			sum += tuple.getE1();
		
		return sum;
	}
	
	public int randRange(int min, int max, int step) {
		int rand = (int)(Math.random() * (max-min+1));
		int result = rand - rand%step + min;
		
		return result;
	}
	
	public double randRange(double min, double max) {
		double result = min + (max - min) * Math.random();
		
		return result;
	}
	

    private double getMean(ArrayList<Tuple<Double, ArrayList<String>>> data, int size)
    {
        double sum = 0.0;
        for(Tuple<Double, ArrayList<String>> a : data)
            sum += a.getE1();
        return sum/size;
    }

    private double getVariance(ArrayList<Tuple<Double, ArrayList<String>>> data, int size)
    {
        double mean = getMean(data, size);
        double temp = 0;
        for(Tuple<Double, ArrayList<String>> a : data)
            temp += (a.getE1()-mean)*(a.getE1()-mean);
        return temp/(size-1);
    }

    public double getStdDev(ArrayList<Tuple<Double, ArrayList<String>>> data)
    {
	    int size = data.size();
	    
        return Math.sqrt(getVariance(data, size));
    }

}
