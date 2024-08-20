package Model;

public class Assignment {
    public int orderIndex;
    public int vehicleIndex;
    public Order o;
    public Vehicle v;
    public Assignment(Order o, Vehicle v){
        this.o = o;
        this.v = v;
    }
    public Assignment(int orderIndex,int vehicleIndex){
        this.orderIndex = orderIndex;
        this.vehicleIndex = vehicleIndex;
    }
}
