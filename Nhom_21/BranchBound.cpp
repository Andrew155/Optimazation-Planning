#include <iostream>
#include<algorithm>
#include<vector>
#include <random>       // std::default_random_engine
#include <chrono>  

using namespace std;
int result = 0;
int currentResult = 0;
int n, k;
int quantity[1001];
int cost[1001];
int low_cap[101];
int up_cap[101];
int res[1001];
int cur_quantity[101];
int cur_solution[1001];
int current_lost = 0;

int time_cut = 0;
int total_call = 0;
float min_cut = 0;

bool can_cut_here(int x) {
	int cost_max_remain = 0;
	int cost_remain = 0;
	int quantity_min = INT32_MAX;
	for (int i = x; i < n + 1; i++)
	{
		cost_remain += cost[i];
		if (cost_max_remain < cost[i]) cost_max_remain = cost[i];
		if (quantity_min > quantity[i]) quantity_min = quantity[i];
	}

	int availabel_cost = 0;
	for (int i = 1; i <= k; i++)
	{
		if ((up_cap[i] - cur_quantity[i]) > quantity_min) availabel_cost += cost_max_remain;
	}

	availabel_cost = availabel_cost > cost_remain ? cost_remain : availabel_cost;

	if (currentResult + availabel_cost < result) {
		return true;
	}

	return false;
}

bool can_cut_new(int x) {
	return false;
}

void try_(int x) {
	total_call++;
	if (x == n + 1) {
		bool acp = true;
		for (int j = 1; j <= k; j++) {
			if (cur_quantity[j] < low_cap[j]) {
				acp = false;
				break;
			}
		}
		if (acp == true) {
			if (result < currentResult) {
				result = currentResult;
				for (int j = 1; j <= n; j++) {
					res[j] = cur_solution[j];
				}
			}
		}
	}
	else {
		if (can_cut_here(x)) {
			time_cut++;
			return;
		}

		for (int i = 0; i < k; i++) {
			if (cur_quantity[i + 1] + quantity[x] <= up_cap[i + 1]) {
				cur_solution[x] = i + 1;
				cur_quantity[i + 1] += quantity[x];
				currentResult += cost[x];
				try_(x + 1);
				cur_quantity[i + 1] -= quantity[x];
				currentResult -= cost[x];
			}
		}
		cur_solution[x] = 0;
		try_(x + 1);
	}
}

void GetInput() {
	cin >> n >> k;
	for (int i = 1; i <= n; i++) {
		cin >> quantity[i] >> cost[i];
	}
	for (int i = 1; i <= k; i++) {
		cin >> low_cap[i] >> up_cap[i];
		current_lost -= low_cap[i];
	}

}

int main() {
	GetInput();
	try_(1);
	int m = 0;
	for (int i = 1; i <= n; i++) {
		if (res[i] != 0) m++;
	}
	cout << m << endl;
	for (int i = 1; i <= n; i++) {
		cout << i << " " << res[i] << endl;
	}
}
