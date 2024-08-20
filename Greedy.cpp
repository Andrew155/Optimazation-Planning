#include <bits/stdc++.h>
using namespace std;

struct Vehicle {
    int idx; // index of vehicle
    int capacity;
    int lowerBound;
    int upperBound;
    vector<int> assign; // index of assigned orders
};

struct Order {
    int idx; // index of order
    int cost;
    int quantity;
};

int main() {
    int N, K;
    cin >> N >> K;
    
    vector<Order> orders(N);
    vector<Vehicle> trucks(K);
    
    for (int i = 0; i < N; ++i) {
        int d, c;
        cin >> d >> c;
        orders[i] = {i + 1, c, d}; // Store orders with 1-based index
    }
    
    for (int i = 0; i < K; ++i) {
        int lb, ub;
        cin >> lb >> ub;
        trucks[i] = {i + 1, 0, lb, ub, {}}; // Store trucks with 1-based index
    }
    
    // Sort orders by cost descending, and by quantity ascending if costs are the same
    sort(orders.begin(), orders.end(), [](Order a, Order b) {
        if (a.cost == b.cost) return a.quantity < b.quantity;
        return a.cost > b.cost;
    });
    
    // Greedy assignment of orders to vehicles
    for (const auto &odr : orders) {
        for (auto &trk : trucks) {
            if (trk.capacity + odr.quantity <= trk.upperBound) {
                trk.capacity += odr.quantity;
                trk.assign.push_back(odr.idx);
                break;
            }
        }
    }
    
    vector<pair<int, int>> results;
    for (const auto &trk : trucks) {
        if (trk.capacity >= trk.lowerBound && trk.capacity <= trk.upperBound) {
            for (int ordIdx : trk.assign) {
                results.push_back({ordIdx, trk.idx});
            }
        }
    }
    sort(results.begin(), results.end());
    // Output number of assignments
    cout << results.size() << endl;
    // Output each assignment
    for (const auto &p : results) {
        cout << p.first << " " << p.second << endl;
    }
    
    return 0;
}