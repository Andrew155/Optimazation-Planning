#include<bits/stdc++.h>
using namespace std;
int n,k;
int sum_profit = 0;
int min_cost = 100000;
struct Order{
	int id;
	int cost;
	int profit;
	bool isAssigned = false;
	int assign = 0;
};
struct Vehicle{
	int id;
	int low;
	int up;
	int cur=0;
	vector<Order> orders;
};
//Danh sach don hang va phuong tien
vector<Order> orders;
vector<Vehicle> vehicles;
//Nhap input
void input(){
	cin>>n>>k;
	for(int i=0;i<n;i++){
		Order o;
		o.id=i;
		cin>>o.cost>>o.profit;
		orders.push_back(o);
		sum_profit+=o.profit;
		if(o.cost<min_cost){
			min_cost = o.cost;
		}
	}
	for(int i=0;i<k;i++){
		Vehicle v;
		v.id = i+1;
		cin>>v.low>>v.up;
		vehicles.push_back(v);
	}
}
//Sap xep cac don hang va phuong tien theo thu tu uu tien de cat them nhieu nhanh
void preprocess(){
	sort(vehicles.begin(),vehicles.end(),[](Vehicle v1, Vehicle v2){
		if(v1.up-v1.low!=v2.up-v2.low) return (v1.up-v1.low<v2.up-v2.low);
		else return v1.low>v2.low;	
	});
	sort(orders.begin(),orders.end(),[](Order o1, Order o2){
		return o1.cost<o2.cost;
	});
}
int res[1001];
int bsf = 0;
vector<int> rv_cap;
//Ta biet truoc thu tu sap xep cac phuong tien
//Do do ta hoan toan tinh duoc tong can duoi tai trong cua cac phuong tien con lai sau khi da xep xong 1 phuong tien nao do
//rv_cap[i] nghia la tong tai trong con lai sau khi sap xep phuong tien i+1
void total_cap(){
	int tmp = 0;
	rv_cap.push_back(tmp);
	for(int i=k-1;i>0;i--){
		tmp+=vehicles[i].low;
		rv_cap.push_back(tmp);
	}
	reverse(rv_cap.begin(),rv_cap.end());
}
//Ham tinh tong trong luong cac don hang con lai
int remain(){
	int tmp = 0;
	for(Order o: orders){
		if(o.assign==0){
			tmp+= o.cost;
		}
	}
	return tmp;
}
//Ham quay lui
void backtrack(int order_number, int vehicle_number,int accum,int profit){
	//Dieu kien can thu nhat: da sap xep duoc tat ca cac don hang
	if(bsf==sum_profit){
		return;
	}
	if(vehicle_number==k){
		//Da hoan thanh sap xep cho k xe, ghi nhan loi giai
		if(profit>bsf){
			bsf = profit;
			for(Order o: orders){
				res[o.id+1] = o.assign;
			}
		}
		return;
	}
	//Da duyet het danh sach don hang hien tai, chuyen sang sap xep cho xe ke tiep
	if(order_number==n){
		if(accum>=vehicles[vehicle_number].low){
			//Dieu kien can thu hai: tong trong luong cac don con lai nho hon tong can duoi tai trong cac phuong tien con lai
			if(remain()<rv_cap[vehicle_number]){
				return;
			}
			backtrack(0,vehicle_number+1,0,profit);
		}
		else return;
	}
	else{
		//Neu chua gan vao xe nao thi thu gan va thu 0 gan
		if(orders[order_number].assign==0){
			if((accum+orders[order_number].cost)<=vehicles[vehicle_number].up){
				orders[order_number].assign = vehicles[vehicle_number].id;
				accum+=orders[order_number].cost;
				profit+=orders[order_number].profit;
				backtrack(order_number+1,vehicle_number,accum,profit);
				accum-=orders[order_number].cost;
				profit-=orders[order_number].profit;
				orders[order_number].assign = 0;
			}
			else{
				//Dieu kien can thu 3: xet den mot don hang khong co kha nang xep vao nua do vi pham rang buoc tai trong
				//Thuc hien duoc bang cach xet cac don hang theo thu tu trong luong tang dan
				if(accum>=vehicles[vehicle_number].low){
					backtrack(0,vehicle_number+1,0,profit);
				}
			}
		}
		backtrack(order_number+1,vehicle_number,accum,profit);
	}
}
int vehicle_capacity[100];
int main(){
	input();
	preprocess();
	total_cap();
	backtrack(0,0,0,0);
	int total = 0;
	for(int i=1;i<=n;i++){
		if(res[i]!=0){
			total++;
		}
	}
	cout<<total<<endl;
	sort(orders.begin(),orders.end(),[](Order o1, Order o2){
		return o1.id<o2.id;
	});
	for(int i=1;i<=n;i++){
		if(res[i]!=0){
			vehicle_capacity[res[i]]+=orders[i-1].cost;
			cout<<i<<" "<<res[i]<<endl;
		}
	}
}
