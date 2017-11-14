package ant_colony;

public class Tuple<L,R> {

	private final L e1;
	private final R e2;

	public Tuple(L e1, R e2) {
		this.e1 = e1;
		this.e2 = e2;
	}

	public L getE1() { return e1; }
	public R getE2() { return e2; }
	
    @Override
    public int hashCode() { return e1.hashCode() ^ e2.hashCode(); }
    
    @Override
    public String toString() {
    	return e1.toString() + ", " + e2.toString();
    }
}
