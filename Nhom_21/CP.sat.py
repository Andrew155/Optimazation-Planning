import time
from ortools.sat.python import cp_model

def CP_Solver(N, K, orders, vehicles):
    model = cp_model.CpModel()

    # Variables
    x = {}
    for i in range(N):
        for k in range(K):
            x[i, k] = model.NewBoolVar(f'x[{i},{k}]')

    # Constraints
    #Sum of quantity of orders loaded (served) in a vehicle must be between
    # the low-capacity and up-capacity of that vehicle
    for k in range(K):
        load = sum(x[i, k] * orders[i][0] for i in range(N))
        model.Add(load >= vehicles[k][0])
        model.Add(load <= vehicles[k][1])
    #Each order is served by at most one vehicle
    for i in range(N):
        model.Add(sum(x[i, k] for k in range(K)) <= 1)

    # Objective: Maximize the total value of the items assigned
    total_value = sum(x[i, k] * orders[i][1] for i in range(N) for k in range(K))
    model.Maximize(total_value)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        assignment = []
        for i in range(N):
            for k in range(K):
                if solver.BooleanValue(x[i, k]):
                    assignment.append((i + 1, k + 1))
        return solver.ObjectiveValue(), assignment
    else:
        return None, None

# Read input
N, K = map(int, input().split())

orders = []
vehicles = []

for i in range(N):
    quantity, cost = map(int, input().split())
    orders.append([quantity, cost])

for i in range(K):
    lower_bound, upper_bound = map(int, input().split())
    vehicles.append([lower_bound, upper_bound])

# Start timer
start_time = time.time()

# Solve the problem
total_value, best_solution = CP_Solver(N, K, orders, vehicles)

# End timer
end_time = time.time()
execution_time = end_time - start_time

# Output result
if best_solution:
    print("Total value:", total_value)
    print(len(best_solution))
    for i, b in best_solution:
        print(i, b)
else:
    print('No solution found')

print(f"Execution time: {execution_time:.6f} seconds")
