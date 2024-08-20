//Lop Vehicle thao tac 1 phuong tien
package Model;

import java.util.ArrayList;

import static java.lang.Math.min;

public class Vehicle {
    public int id;
    public int low_cap;
    public int up_cap;
    public int curWeight;
    public int curProfit;
    private int penalty = 100;
    public ArrayList<Order> orders;
    public Vehicle(int id, int low, int up){
        this.id = id;
        low_cap = low;
        up_cap = up;
        orders = new ArrayList<>();
        reset();
    }
    //Reset lai cac chi so de tinh toan loi giai ke tiep
    public void reset(){
        curProfit = 0;
        curWeight = 0;
        orders.clear();
    }
    //Gan 1 don hang vao 1 phuong tien
    public boolean assign(Order o){
        if(curWeight+o.cost<=up_cap) {
            curWeight += o.cost;
            curProfit += o.profit;
            orders.add(o);
            return true;
        }
        else return false;
    }
    //Bo mot don hang khoi 1 phuong tien
    public void remove(Order o){
            orders.remove(o);
            curWeight-=o.cost;
            curProfit-=o.profit;
    }
    //Tra ve tong gia tri don hang tru di mot ham penalty, tuc la hinh phat
    //Penalty, theo nhu quan sat thuc nghiem, chi co tac dung trong thuat toan GA
    public int computeFitness(){
        int tmp = curProfit;
        tmp+= min(curWeight-low_cap,0)*penalty;
        return tmp;
    }
    //Kiem tra rang buoc ve tai trong
    public boolean isViolated() {
        return (curWeight-low_cap<0)||(curWeight-up_cap>0);
    }
}
