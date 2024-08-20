#include <bits/stdc++.h>
using namespace std;
int result=0;
int obj=0;
int n,k;
int quantity[1001];
int cost[1001];
int low_cap[101];
int up_cap[101];
int res[1001];
int cur_quantity[101];
int cur_solution[1001];
int best_quantity=0;
int best_cost=0;
double best_ratio=0;
void try_(int x){
	if(x==n+1){
		bool acp = true;
		for(int j=1;j<=k;j++){
		if(cur_quantity[j]<low_cap[j]){
			acp = false;
			break;
			}
		}
		if(acp == true){
			if(result<obj){
				result=obj;
				for(int j=1;j<=n;j++){
				res[j]=cur_solution[j];
				}
			}
		}
	}
	else{
		int bound=0;
		for(int i=1;i<=k;i++){
			bound += (up_cap[i]-cur_quantity[i])/best_quantity;
		}
		bound *= best_cost;
		if(obj+bound<result){
			return;
		}
		for(int i=k;i>=1;i--){
			if(cur_quantity[i]+quantity[x]<=up_cap[i]){
				cur_solution[x]=i;
				cur_quantity[i]+=quantity[x];
				obj+=cost[x];
				try_(x+1);
				cur_quantity[i]-=quantity[x];
				obj-=cost[x];
			}
		}
		cur_solution[x]=0;
		try_(x+1);
	}
}
int main(){
cin>>n>>k;
for(int i=1;i<=n;i++){
	cin>>quantity[i]>>cost[i];
	if(best_ratio<(double)cost[i]/quantity[i]){
		best_ratio = (double) cost[i]/quantity[i];
		best_cost = cost[i];
		best_quantity = quantity[i];
	}
}
for(int i=1;i<=k;i++){
	cin>>low_cap[i]>>up_cap[i];
}
try_(1);
int m=0;
for(int i=1;i<=n;i++){
	if(res[i]!=0) m++;
}
cout<<m<<endl;
for(int i=1;i<=n;i++){
	cout<<i<<" "<<res[i]<<endl;
}
}
