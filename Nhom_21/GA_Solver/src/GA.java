//Day la lop chinh cua giai thuat di truyen
//No dieu khien lop con cua giai thuat, cu the la lop Population luu tru cac loi giai
import Model.Assignment;
import Model.Order;
import Model.Vehicle;

import java.util.Scanner;

public class GA {
    static int geNumber;
    static int orderNumber;
    static int vehicleNumber;
    static VehicleManager vehicleManager;
    static OrderManager orderManager;
    public GA(){
        Scanner scanner = new Scanner(System.in);
        orderNumber = scanner.nextInt();
        vehicleNumber = scanner.nextInt();
        orderManager = new OrderManager(orderNumber);
        vehicleManager = new VehicleManager(vehicleNumber);
        int tmp1, tmp2;
        for(int i=0;i<orderNumber;i++){
            tmp1 = scanner.nextInt();
            tmp2 = scanner.nextInt();
            Order o = new Order(tmp1,tmp2);
            orderManager.add(o);;
        }
        for(int i=0;i<vehicleNumber;i++){
            tmp1 = scanner.nextInt();
            tmp2 = scanner.nextInt();
            Vehicle v = new Vehicle(i+1,tmp1,tmp2);
            vehicleManager.add(v);;
        }
        geNumber = Settings.iterationNumber;
    }
    Population population;
    //Phuong thuc co ban cua lop GA la thuc hien khoi tao quan the moi va goi cac phuong thuc lai ghep cua Population
    //Hoac thuc hien Repeated Local Search bang cach khoi tao quan the loi giai lien tuc
    void run(){
        population = new Population();
        int iteration = 0;
        if(!Settings.repeatedLocalSearchOnly) {
            //Phai lap lai den khi tim duoc mot loi giai dung
            while (!population.best.isCorrect || iteration < geNumber) {
                iteration++;
                System.out.println(population.best.fitness);
                population.generateNextGeneration();
                //Neu so luong the he khong co su cai thien cao thi khoi tao mot quan the moi va lai tao tu dau
                if (population.wOImprovement == population.maxWO) {
                    population.wOImprovement = 0;
                    population.generateInitialIndividuals();
                }
            }
        }
        else{
            //Repeated Local Search bang cach khoi tao quan the loi giai lien tuc
            while(!population.best.isCorrect || iteration < geNumber){
                iteration++;
                population.generateInitialIndividuals();
            }
        }
        population.best.printSol();
    }
}
