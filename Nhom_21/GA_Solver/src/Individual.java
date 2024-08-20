//Lop Individual luu giu 1 loi giai, tuan theo mo hinh assignments va thao tac tren loi giai do
//Voi su ho tro cua lop VehicleManager
import Model.Assignment;
import Model.Order;
import Model.Vehicle;

import java.util.*;

public class Individual {
    int fitness;
    ArrayList<Assignment> assignments;
    //Khoi tao loi giai ngau nhien
    Individual(){
        //a = new ArrayList<>();
        assignments = new ArrayList<>();
        Random random = new Random();
        for(int i=0;i<GA.orderNumber;i++) {
            int tmp = random.nextInt(GA.vehicleNumber+1);
            //a.add(random.nextInt(GA.vehicleNumber + 1));
            assignments.add(new Assignment(i,tmp));
            //assignments.add(new Assignment(GA.orderManager.orders.get(i),GA.vehicleManager.vehicles.get(random.nextInt(GA.vehicleNumber + 1))));
        }
        computeFitness(false);
        computeFitness(false);
    }
    //Sinh ra mot loi giai moi bang cach lai tao 2 loi giai cu
    Individual(Individual i1, Individual i2){
        //a = new ArrayList<>();
        assignments = new ArrayList<>();
        Random random = new Random(10);
        for(int i=0;i<GA.orderNumber;i++){
            if(random.nextInt()>4){
                //a.add(i1.a.get(i));
                assignments.add(i1.assignments.get(i));
            }
            else {
                //a.add(i2.a.get(i));
                assignments.add(i2.assignments.get(i));
            }
        }
        //Mot loi giai moi duoc sinh ra se duoc gay dot bien nhe
        mutate();
        computeFitness(false);
        computeFitness(false);
    }
    Individual(String s){
        assignments = new ArrayList<>();
        fitness = Integer.MIN_VALUE;
    }
    //Ham gay dot bien se la hoan doi gia tri vehicleID cua 2 assignment bat ky
    void mutate(){
        Random rand = new Random();
        int tmp1 = rand.nextInt(GA.orderNumber);
        int tmp2 = rand.nextInt(GA.orderNumber);
        int tmp = assignments.get(tmp1).vehicleIndex;
        assignments.get(tmp1).vehicleIndex = assignments.get(tmp2).vehicleIndex;
        assignments.get(tmp2).vehicleIndex = tmp;
    }
    //Phuong thuc nay yeu cau lop VehicleManager tinh toan gia tri fitness
    //Bang cach doc danh sach assignments va thuc hien local search
    //Truyen vao 1 flag true/false de VehicleManager khong reset ket qua neu day la lan tinh toan cuoi cung de in ra loi giai
    void computeFitness(boolean isLast){
        GA.vehicleManager.assign(this);
        GA.vehicleManager.reAssign(this);
        assignments.sort(new Comparator<Assignment>() {
            @Override
            public int compare(Assignment o1, Assignment o2) {
                return Integer.compare(o1.orderIndex,o2.orderIndex);
            }
        });
        //Cap nhat tinh dung dan cua loi giai bang cach kiem tra rang buoc tai trong
        isCorrect = GA.vehicleManager.capacityCheck();
        fitness = GA.vehicleManager.computeFitness();
        if(!isLast){
            GA.vehicleManager.reset();
        }
    }
    public boolean isLast = false;
    public boolean isCorrect = false;
    //In ra loi giai
    void printSol(){
        isLast = true;
        computeFitness(true);
        System.out.println("Highest profit found is "+fitness);
        int tmp = 0;
        for(Assignment a: assignments){
            if(a.vehicleIndex!=0){
                tmp+=1;
            }
            else{
                System.out.println("Unserved: "+GA.orderManager.orders.get(a.orderIndex).cost);
            }
        }
        System.out.println("Number of orders served is "+tmp);
        isCorrect = GA.vehicleManager.capacityCheck();
        if(isCorrect){
            System.out.println("Satisfied all capacity check");
        }
        for(Assignment a: assignments){
            if(a.vehicleIndex!=0){
                System.out.println((a.orderIndex+1)+" "+a.vehicleIndex);
            }
        }
    }
    //Ham change() thay doi don hang tu phuong tien nay sang phuong tien khac
    //Do cau truc cua assignment ma chi can 1 tham so phuong tien khac
    //Tuy nhien neu muon an toan co the them dieu kien kiem tra phuong tien goc
    public void change(Order o,Vehicle v1, Vehicle v2) {
        int orderIndex=-1;
        for(int i=0;i<GA.orderNumber;i++){
            if(GA.orderManager.orders.get(i)==o){
                orderIndex = i;
                break;
            }
        }
        for(int i=0;i<GA.orderNumber;i++){
            if(assignments.get(i).orderIndex==orderIndex){
                assignments.get(i).vehicleIndex=v1.id;
            }
        }
    }
}
