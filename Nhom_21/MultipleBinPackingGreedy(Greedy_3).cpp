#include <bits/stdc++.h>
using namespace std;
struct Order{
	int id;
	int cost;
	int profit;
	bool isAssigned = false;
};
struct Vehicle{
	int id;
	int low;
	int up;
	int cur=0;
	vector<Order> orders;
};
struct Assignment{
	int orderID;
	int vehicleID=0;
};
//Danh sach thong tin don hang
vector<Order> orders;
//Danh sach cac phuong tien
vector<Vehicle> vehicles;
//2 danh sach cac phuong tien loai 1 va loai 2 de thuc hien Repair()
vector<Vehicle> upB;
vector<Vehicle> lowB;
//Danh sach cac Assignment
vector<Assignment> assignments;
void input(){
	int n,k;
	cin>>n>>k;
	for(int i=0;i<n;i++){
		Order o;
		o.id=i;
		cin>>o.cost>>o.profit;
		orders.push_back(o);
		Assignment a;
		a.orderID = i+1;
		assignments.push_back(a);
	}
	for(int i=0;i<k;i++){
		Vehicle v;
		v.id = i+1;
		cin>>v.low>>v.up;
		vehicles.push_back(v);
	}
}
//Giai doan tien xu ly, sap xep cac don hang va phuong tien theo thu tu uu tien
void preprocess(){
	sort(vehicles.begin(),vehicles.end(),[](Vehicle v1, Vehicle v2){
		if(v1.up-v1.low!=v2.up-v2.low) return (v1.up-v1.low<v2.up-v2.low);
		else return v1.low<v2.low;	
	});
	sort(orders.begin(),orders.end(),[](Order o1, Order o2){
		if(o1.profit>o2.profit){
			return true;
		}	
		if(o1.profit==o2.profit){
			return o1.cost<o2.cost;
		}
		return false;
	});
}
//Giai doan greedy insert(), tham lam nhet cac don hang vao cac phuong tien
//Neu 1 phuong tien khong chap nhan nua thi doi sang phuong tien ke tiep trong danh sach
void solve(){
	for(Vehicle &v: vehicles){
		for(Order &o: orders){
			if(!o.isAssigned){
				if(v.cur+o.cost<=v.up){
					v.cur+=o.cost;
					o.isAssigned = true;
					v.orders.push_back(o);
					assignments[o.id].vehicleID=v.id;
				}
			}
		}
	}
}
//Ham sua chua, bao gom ca doan code sap xep cac don hang loai 1 va loai 2
void repair(){
	sort(upB.begin(),upB.end(),[](Vehicle v1, Vehicle v2){
		if((v1.cur-v1.low)!=(v2.cur-v2.low)){
			return (v1.cur-v1.low)>(v2.cur-v2.low);
		}
		else return (v1.orders.size())>(v2.orders.size());
	});
	sort(lowB.begin(),lowB.end(),[](Vehicle v1, Vehicle v2){
		if((v1.up-v1.cur)!=(v2.up-v2.cur)){
			return (v1.up-v1.cur)>(v2.up-v2.cur);
		}
		else return (v1.low-v1.cur)>(v2.low-v1.cur);
	});
	for(Vehicle &v1: lowB){
		//Tinh phan con co the them vao cua phuong tien 2
		int tmp1 = v1.up-v1.cur;
		for(Vehicle &v2: upB){
			if(tmp1>0){
				//Tinh phan con co the bot di cua phuong tien loai 1
				int tmp2 = v2.cur-v2.low;
				if(tmp2>0){
					//Duyet toan bo danh sach don hang phuong tien loai 1 de them vao pt loai 2
 					for(int i=0;i<v2.orders.size();i++){
						int tmp = v2.orders[i].cost;
						if(tmp<=tmp2&&tmp<=tmp1){
							v2.cur-=tmp;
							v1.orders.push_back(v2.orders[i]);
							assignments[v2.orders[i].id].vehicleID = v1.id;
							v2.orders.erase(v2.orders.begin()+i);
							v1.cur+=tmp;
							tmp2-=tmp;
							tmp1-=tmp;
							i--;
						}
						//Neu nhu phuong tien loai 1 khong the them bot di
						//Hoac phuong tien loai 2 khong the them vao
						if(tmp2==0||tmp1==0){
							break;
						}
					}
				}
			}		
		}
	}
}
int main(){
	input();
	preprocess();
	solve();
	for(Vehicle v: vehicles){
		if(v.cur>=v.low){
			upB.push_back(v);
		}
		else lowB.push_back(v);
	}
	repair();
	//Phan in ra ket qua loi giai theo nhu format
	//Loi giai duoc luu trong assignments
	int assigned = 0;
	for(Assignment a: assignments){
		if(a.vehicleID!=0){
			assigned++;
		}
	}
	cout<<assigned<<endl;
	for(Assignment a: assignments){
		cout<<a.orderID<<" "<<a.vehicleID<<endl;
	}
}
