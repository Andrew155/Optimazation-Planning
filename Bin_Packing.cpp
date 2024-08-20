#include <iostream>
#include <vector>
using namespace std;

int result = 0;
int obj = 0;
int n, k;
int quantity[1001];
int cost[1001];
int low_cap[101];
int up_cap[101];
int res[1001];
int cur_quantity[101];
int cur_solution[1001];

void try_(int x) {
    for (int i = 1; i <= k; i++) { // Chạy từ 1 đến k thay vì từ 0 đến k
        if (cur_quantity[i] + quantity[x] <= up_cap[i]) {
            cur_solution[x] = i;
            cur_quantity[i] += quantity[x];
            obj += cost[x];
            if (x == n) {
                bool acp = true;
                for (int j = 1; j <= k; j++) { // Chạy từ 1 đến k thay vì từ 0 đến k
                    if (cur_quantity[j] < low_cap[j]) {
                        acp = false;
                        break;
                    }
                }
                if (acp == true) {
                    if (result < obj) {
                        result = obj;
                        for (int j = 1; j <= n; j++) {
                            res[j] = cur_solution[j];
                        }
                    }
                }
            } else
                try_(x + 1);
            cur_quantity[i] -= quantity[x];
            obj -= cost[x];
        }
    }
}

int main() {
    cin >> n >> k;
    for (int i = 1; i <= n; i++) {
        cin >> quantity[i] >> cost[i];
    }
    for (int i = 1; i <= k; i++) {
        cin >> low_cap[i] >> up_cap[i];
    }
    try_(1);
    for (int i = 1; i <= n; i++) {
        cout << i << " " << res[i] << "\n";
    }
    return 0;
}
