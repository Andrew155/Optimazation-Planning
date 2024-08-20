//Day la lop Population, no co tac dung thao tac cac thanh vien trong quan the, tuc la cac loi giai
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Random;

public class Population {
    //Loi giai tot nhat tim duoc trong tat ca the he lai ghep
    Individual best = new Individual("");
    ArrayList<Individual> individuals;
    //So luong loi giai trong quan the
    int size;
    //So luong ca the duoc chon ra de lai tao the he ke tiep
    int candidateNumber;
    public int wOImprovement = 0;
    //So luong the he toi da khong co su cai thien duoc cho phep
    public int maxWO = 10;
    //Khoi tao quan the
    public Population(){
        individuals = new ArrayList<>();
        size = Settings.populationSize;
        candidateNumber = Settings.candidateNumber;
        generateInitialIndividuals();
    }
    //Khoi tao ngau nhien cac loi giai trong quan the
    void generateInitialIndividuals() {
        individuals.clear();
        for(int i=0;i<size;i++){
            //Phuong thuc khoi tao mac dinh cua Individual la ngau nhien
            Individual individual = new Individual();
            individuals.add(individual);
        }
        sortAcFitness();
    }
    void generateNextGeneration(){
        //Sinh ra quan the cua the he ke tiep
        ArrayList<Individual> selected = binaryTournamentSelection();
        ArrayList<Individual> next = new ArrayList<>();
        Random rand = new Random();
        for(int i=0;i<size;i++){
            int tmp1 = rand.nextInt(candidateNumber);
            int tmp2 = rand.nextInt(candidateNumber);
            next.add(new Individual(selected.get(tmp1),selected.get(tmp2)));
        }
        individuals.clear();
        individuals.addAll(next);
        sortAcFitness();
    }
    private ArrayList<Individual> selectCandidates(){
        ArrayList<Individual> tmp = new ArrayList<>();
        for(int i=0;i<candidateNumber;i++){
            tmp.add(individuals.get(i));
        }
        return tmp;
    }
    //Su dung Binary Tournament va chon ra cac loi giai de lai tao quan the ke tiep
    private ArrayList<Individual> binaryTournamentSelection(){
        ArrayList<Individual> tmp = new ArrayList<>();
        int i = 0;
        Random random = new Random();
        while(i<candidateNumber){
            int tmp1 = random.nextInt(size);
            int tmp2 = random.nextInt(size);
            if(tmp1!=tmp2){
                if(individuals.get(tmp1).fitness<individuals.get(tmp2).fitness){
                    tmp.add(individuals.get(tmp1));
                }
                else tmp.add(individuals.get(tmp2));
                i++;
            }
        }
        return tmp;
    }
    //Phuong thuc nay dung de tinh gia tri fitness, tuc gia tri ham muc tieu cua moi loi giai
    //Va cung de cap nhat loi giai tot nhat sau tung the he
    private void sortAcFitness(){
        individuals.sort(new Comparator<Individual>() {
            @Override
            public int compare(Individual o1, Individual o2) {
                return Integer.compare(o2.fitness,o1.fitness);
            }
        });
        //Sap xep loi giai theo gia tri fitness de loi giai co fitness tot nhat luon o dau tien
        if(best.fitness<individuals.get(0).fitness){
            wOImprovement = 0;
            best = individuals.get(0);
        }
        else{
            wOImprovement++;
        }
    }
}
