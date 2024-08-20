class Vehicle:
    def __init__(self, idx, lower_bound, upper_bound):
        self.idx = idx
        self.capacity = 0
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.assign = []

class Order:
    def __init__(self, idx, quantity, cost):
        self.idx = idx
        self.quantity = quantity
        self.cost = cost

def main():
    # Read input
    N, K = map(int, input().split())
    
    orders = []
    trucks = []

    for i in range(N):
        d, c = map(int, input().split())
        orders.append(Order(i + 1, d, c))  # Store orders with 1-based index

    for i in range(K):
        lb, ub = map(int, input().split())
        trucks.append(Vehicle(i + 1, lb, ub))  # Store trucks with 1-based index
    
    # Sort orders by cost descending, and by quantity ascending if costs are the same
    orders.sort(key=lambda x: (-x.cost, x.quantity))
    
    # Greedy assignment of orders to vehicles
    for order in orders:
        for truck in trucks:
            if truck.capacity + order.quantity <= truck.upper_bound:
                truck.capacity += order.quantity
                truck.assign.append(order.idx)
                break
    
    results = []
    for truck in trucks:
        if truck.capacity >= truck.lower_bound and truck.capacity <= truck.upper_bound:
            for ord_idx in truck.assign:
                results.append((ord_idx, truck.idx))
    
    results.sort()
    # Output number of assignments
    print(len(results))
    # Output each assignment
    for res in results:
        print(res[0], res[1])

if __name__ == "__main__":
    main()
