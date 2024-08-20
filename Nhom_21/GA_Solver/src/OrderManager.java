import Model.Order;

import java.util.ArrayList;

public class OrderManager {
    public ArrayList<Order> orders;
    public OrderManager(int k){
        orders = new ArrayList<>(k);
    }
    public void add(Order o){
        orders.add(o);
    }
}
