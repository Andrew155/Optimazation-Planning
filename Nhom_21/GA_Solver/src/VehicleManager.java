//Lop VehicleManager co tac dung doc mot loi giai cua mot Individual
//Sau do "giai ma" va cai thien loi giai nay de sinh ra mot loi giai tot hon va tinh gia tri ham muc tieu cua loi giai do
//No hoat dong dua tren danh sach phuong tien
import Model.Assignment;
import Model.Order;
import Model.Vehicle;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Scanner;

public class VehicleManager {
    //Danh sach phuong tien
    ArrayList<Vehicle> vehicles;
    //2 danh sach phuong tien loai 1 va loai 2
    ArrayList<Vehicle> low;
    ArrayList<Vehicle> up;
    public VehicleManager(int k){
        vehicles = new ArrayList<>(k);
        low = new ArrayList<>();
        up = new ArrayList<>();
    }
    public void add(Vehicle v){
        //vehicles.add(v);
        low.add(v);
    }
    //Giai doan 1 cua thuat toan Local Search, gan cac don hang co the duoc gan vao phuong tien hien tai
    public void assign(Individual individual){
        Collections.shuffle(individual.assignments);
        for(Assignment a: individual.assignments){
            if(a.vehicleIndex!=0){
                if(!low.get(a.vehicleIndex-1).assign(GA.orderManager.orders.get(a.orderIndex))){
                    a.vehicleIndex = 0;
                }
            }
        }
        updateLowUp();
    }
    //Giai doan 2 cua thuat toan Local Search, gan cac don hang chua duoc gan vao phuong tien hop le
    public void reAssign(Individual individual){
        Collections.shuffle(individual.assignments);
        Collections.shuffle(low);
        Collections.shuffle(up);
        for(Assignment a: individual.assignments){
            if(a.vehicleIndex==0){
                for(Vehicle v: low){
                    if(v.assign(GA.orderManager.orders.get(a.orderIndex))){
                        a.vehicleIndex = v.id;
                        break;
                    }
                }
                for(Vehicle v: up){
                    if(v.assign(GA.orderManager.orders.get(a.orderIndex))){
                        a.vehicleIndex = v.id;
                        break;
                    }
                }
            }
        }
        updateLowUp();
        repair(individual);
        vehicles.addAll(low);
        vehicles.addAll(up);
        vehicles.sort(new Comparator<Vehicle>() {
            @Override
            public int compare(Vehicle o1, Vehicle o2) {
                return Integer.compare(o1.id,o2.id);
            }
        });
    }
    //Thuc hien phan chia 2 loai phuong tien de kich hoat ham Repair()
    private void updateLowUp(){
        for(Vehicle v: low){
            if(v.curWeight>=v.low_cap){
                up.add(v);
            }
        }
        low.removeAll(up);
    }
    //Giai doan 3 cua thuat toan chinh la ham Repair()
    private void repair(Individual individual){
        Collections.shuffle(low);
        Collections.shuffle(up);
        for(Vehicle v1: low){
            int upReq = v1.up_cap - v1.curWeight;
            for(Vehicle v2: up){
                int overLow = v2.curWeight - v2.low_cap;
                ArrayList<Order> acc = new ArrayList<>();
                for(Order o: v2.orders){
                    if(o.cost<=overLow){
                        acc.add(o);
                    }
                }
                for(Order o: acc){
                    if(o.cost<=overLow){
                        if(o.cost<=upReq){
                            v1.assign(o);
                            v2.remove(o);
                            individual.change(o,v1,v2);
                            overLow-=o.cost;
                            upReq-=o.cost;
                        }
                    }
                    if(overLow==0||upReq==0){
                        break;
                    }
                }
            }
        }
    }
    //Tinh gia tri fitness cua individual hien tai sau khi thuc hien localSearch
    public int computeFitness(){
        int tmp=0;
        //int violated = 0;
        for(Vehicle v: vehicles){
            tmp += v.computeFitness();
        }
        return tmp;
    }
    //Reset lai cac thong so cua cac phuong tien de thuc hien tinh toan individual tiep theo
    //Chinh la "bo het" cac don hang ra khoi xe de "xep lai" cac don hang khac vao xe
    void reset(){
        low.clear();
        up.clear();
        for(Vehicle v: vehicles){
            v.reset();
            low.add(v);
        }
        vehicles.clear();
    }
    //Kiem tra tinh dung dan cua loi giai hien tai thong qua cac rang buoc ve tai trong
    public boolean capacityCheck() {
        for(Vehicle v: vehicles){
            if(v.isViolated()){
                return false;
            }
        }
        return true;
    }
}
