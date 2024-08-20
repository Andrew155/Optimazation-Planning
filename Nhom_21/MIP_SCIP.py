from ortools.linear_solver import pywraplp
import time

def MIP_Solver(N, K, orders, vehicles):
    best_sol = [0] * N #store the best solution
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return
    
    #Create variables (binary) from modeling: X[i,j] = 1 if vehicle i contains order j
    #otherwise, X[i,j] = 0
    X = {}
    for i in range(K):
        for j in range(N):
            X[i, j] = solver.BoolVar(f'X_{i}_{j}')
    #Adding constrains
    #Each order is served by at most one vehicle
    for j in range(N):
        solver.Add(sum(X[i,j] for i in range(K)) <=1)
    #Sum of quantity of orders loaded (served) in a vehicle must be between the low-capacity and up-capacity of that vehicle
    for i in range(K):
        
        solver.Add(sum(X[i,j] * orders[j][0] for j in range(N)) >= vehicles[i][0])
        solver.Add(sum(X[i,j] * orders[j][0] for j in range(N)) <= vehicles[i][1])
    

    #Objective Function: Max the total cost of served orders
    objective = solver.Objective()
    for i in range(K):
        for j in range(N):
            objective.SetCoefficient(X[i,j], orders[j][1])
    objective.SetMaximization()

    #Setup TimeLimit

    #solver.set_time_limit(time_limit * 1000)
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        for i in range(K):
            for j in range(N):
                if X[i,j].solution_value() > 0:
                    best_sol[j] = i+1
        return int(objective.Value()), best_sol
    else:
        return 0, best_sol


N, K = map(int, input().split())

orders = []
vehicles = []

for i in range(N):
    quantity, cost = map(int, input().split())
    orders.append([quantity, cost])
for i in range (K):
    lower_bound, upper_bound = map(int, input().split())
    vehicles.append([lower_bound, upper_bound])
# Start timer
start_time = time.time()
# N = 5
# K = 2
# orders = [[5, 9], [7, 2], [12, 6], [12, 4], [7, 6]]
# vehicles = [[12, 14], [27, 31]]

total_cost, best_solution = MIP_Solver(N, K, orders, vehicles)

# End timer
end_time = time.time()
execution_time = end_time - start_time
# In kết quả
print("Total cost of served orders:", total_cost)
print("Best solution (vehicle assigned to each order):", best_solution)

print(f"Execution time: {execution_time:.6f} seconds")
