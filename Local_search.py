import random

def compute_cost(assignment, orders, vehicles):
    vehicle_costs = [0] * len(vehicles)
    for order, vehicle in enumerate(assignment):
        vehicle_costs[vehicle - 1] += orders[order][1]
    return sum(vehicle_costs)


def local_search(N, K, orders, vehicles, max_iterations):
    # Random initialization
    assignment = [random.randint(1, K) for _ in range(N)]
    current_cost = compute_cost(assignment, orders, vehicles)

    for _ in range(max_iterations):
        # Randomly select an order and vehicle
        order_index = random.randint(0, N - 1)
        vehicle_index = random.randint(0, K - 1)
        current_vehicle = assignment[order_index]

        # If moving the order to a new vehicle doesn't violate capacity constraints
        if vehicles[vehicle_index][0] <= sum(orders[i][0] for i, v in enumerate(assignment) if v == vehicle_index + 1) + orders[order_index][0] <= vehicles[vehicle_index][1]:
            assignment[order_index] = vehicle_index + 1
            new_cost = compute_cost(assignment, orders, vehicles)
            # Accept the move if it reduces the cost
            if new_cost > current_cost:
                current_cost = new_cost
            # Otherwise revert the assignment
            else:
                assignment[order_index] = current_vehicle

    return assignment, current_cost

# Input
N, K = map(int, input().split())  # Number of orders, Number of vehicles
orders = [list(map(int, input().split())) for _ in range(N)]  # Orders (quantity, cost)
vehicles = [list(map(int, input().split())) for _ in range(K)]  # Vehicles (low-capacity, up-capacity)
max_iterations = 1000  # Maximum number of iterations

# Compute solution using local search
assignment, total_cost = local_search(N, K, orders, vehicles, max_iterations)

# Output
print(len(assignment))
for i, b in enumerate(assignment):
    print(i + 1, b)
