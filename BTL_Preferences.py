import numpy as np
from functools import reduce
import random
import copy
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

### Backtracking ###
def Solve_Backtracking(N, K, items, cars):
    W = np.transpose(np.array([[i[0] for i in items]]))
    P = np.transpose(np.array([[i[1] for i in items]]))

    #x[i,j] = 1 if item i is placed on car j
    x = np.array([[0 for k in range(K)] for n in range(N)])
    x_best = np.array([[0 for k in range(K)] for n in range(N)])

    def g(i, x): #weight of car i
        return np.matmul(np.transpose(x)[i], W)[0]

    def f(x):
        return np.sum(np.matmul(np.transpose(x), P))

    #check for upper bounds
    def check_1(x):
        return reduce(lambda x, y: x and y, [g(k, x) <= cars[k][1] for k in range(K)]) 

    #check for lower bounds
    def check_2(x):
        return reduce(lambda x, y: x and y, [g(k, x) >= cars[k][0] for k in range(K)])
    
    def solution():
        nonlocal f_best
        if f(x) > f_best and check_1(x) and check_2(x):
            f_best = f(x)
            x_best[:] = x

    def Try(n):
        for k in range(K+1):
            if check_1(x):
                if k != 0:
                    x[n-1][k-1] = 1
                if n == N-1:
                    solution()
                else:
                    Try(n+1)
            if k != 0:
                x[n-1][k-1] = 0
    
    f_best = 0         
    Try(0)
    
    #Utilities function to transform the solution from array form to list form
    def convert_array_to_list(array):
        N, K = array.shape
        result = [0] * N
        for i in range(N):
            for j in range(K):
                if array[i, j] == 1:
                    result[i] = j + 1
                    break
        return result
    return f_best, convert_array_to_list(x_best)
        
### Local search and Iterated local search ###
def is_valid_state(N, K, state, items, cars):
    weight = [0]*len(cars)
    for i in range(len(items)):
        if state[i] != 0:
            weight[state[i]-1] += items[i][0]
    for j in range(len(cars)):
        if weight[j] < cars[j][0] or weight[j] > cars[j][1]:
            return False
    return True

def get_value(state, items):
    value = 0
    for i in range(len(items)):
        if state[i] != 0:
            value += items[i][1]
    return value

def generate_random_state(N, K):
    return [random.choice(range(K+1)) for j in range(N)]

def Solve_Local_Search(N, K, items, cars):
    current_state = generate_random_state(N, K)
    best_value = 0    
    best_state = [0] * N
    if is_valid_state(N, K, current_state, items, cars):
        best_value = get_value(current_state, items)
    while True:
        best_neighbor_value = 0
        best_neighbor_state = copy.deepcopy(current_state)
        for i in range(N): 
            neighbor_state = copy.deepcopy(current_state)        
            if neighbor_state[i] != K:
                neighbor_state[i] += 1
            else:
                neighbor_state[i] = 0
            if is_valid_state(N, K, neighbor_state, items, cars):
                if get_value(neighbor_state, items) > best_neighbor_value:
                    best_neighbor_value = get_value(neighbor_state, items)
                    best_neighbor_state = copy.deepcopy(neighbor_state)
        if best_neighbor_value > best_value:
            best_value = best_neighbor_value
            current_state = copy.deepcopy(best_neighbor_state)
            best_state = copy.deepcopy(best_neighbor_state)
        else:
          break
    return best_value, best_state

def Solve_Iterated_Local_Search(N, K, items, cars, iterations = 1000):
    current_state = generate_random_state(N, K)
    best_value = 0  
    best_state = [0] * N
    max_value = sum([i[1] for i in items])
    if is_valid_state(N, K, current_state, items, cars):
        best_value = get_value(current_state, items)
    for iteration in range(iterations):
        while True:
            best_neighbor_value = 0
            best_neighbor_state = copy.deepcopy(current_state)
            for i in range(N):        
                neighbor_state = copy.deepcopy(current_state)        
                if neighbor_state[i] != K:
                    neighbor_state[i] += 1
                else:
                    neighbor_state[i] = 0
                if is_valid_state(N, K, neighbor_state, items, cars):
                    if get_value(neighbor_state, items) > best_neighbor_value:
                        best_neighbor_value = get_value(neighbor_state, items)
                        best_neighbor_state = copy.deepcopy(neighbor_state)
            if best_neighbor_value > best_value:
                best_value = best_neighbor_value
                current_state = copy.deepcopy(best_neighbor_state)
                best_state = copy.deepcopy(best_neighbor_state)
            else:
                break
        if best_value == max_value:
            break
        current_state = generate_random_state(N, K)        
    return best_value, best_state

### Ortools ###
def Solve_MIP(N, K, items, cars, time_limit = 300):
    best_sol = [0] * N
    # Create the MIP solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')      
    
    if solver is None:
        print('SCIP solver unavailable.')
        return
    
    # Variables.
    ## x[i, b] = 1 if item i is packed in car b.
    x = {}
    for i in range(N):
        for b in range(K):
            x[i, b] = solver.BoolVar(f'x_{i}_{b}')
            
    # Constraints.
    ## Each item is assigned to at most one car.
    for i in range(N):
        solver.Add(sum(x[i, b] for b in range(K)) <= 1)    
    
    ## The amount packed in each car must be in range of lower and upper capacity.
    for b in range(K):
        solver.Add(sum(x[i, b] * items[i][0] for i in range(N)) >= cars[b][0])
        solver.Add(sum(x[i, b] * items[i][0] for i in range(N)) <= cars[b][1])
    
    #Objective.
    ## Maximize total value of packed items.
    objective = solver.Objective()
    for i in range(N):
        for b in range(K):
            objective.SetCoefficient(x[i, b], items[i][1])
    objective.SetMaximization()
    
    #Time limit
    solver.set_time_limit(time_limit * 1000)
    
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        for b in range(K):
            for i in range(N):
                if x[i, b].solution_value() > 0:
                    best_sol[i] = b + 1
        return int(objective.Value()), best_sol
    else:
        return 0, best_sol


def Solve_CP(N, K, items, cars, time_limit = 300):
    best_sol = [0] * N
    model = cp_model.CpModel()
    
    # Variables.
    ## x[i, b] = 1 if item i is packed in car b.
    x = {}
    for i in range(N):
        for b in range(K):
            x[i, b] = model.NewBoolVar(f'x_{i}_{b}')
        
    # Constraints.
    ## Each item is assigned to at most one car.
    for i in range(N):
        model.AddAtMostOne(x[i, b] for b in range(K))
    ## The amount packed in each car cannot exceed its capacity.
    for b in range(K):
        model.Add(sum(x[i, b] * items[i][0] for i in range(N)) >= cars[b][0])
        model.Add(sum(x[i, b] * items[i][0] for i in range(N)) <= cars[b][1])
    
    # Objective.
    ## Maximize total value of packed items.
    objective = []
    for i in range(N):
        for b in range(K):
            objective.append(cp_model.LinearExpr.Term(x[i, b], items[i][1]))
    model.Maximize(cp_model.LinearExpr.Sum(objective))       
    
    solver = cp_model.CpSolver()
    # Time limit
    solver.parameters.max_time_in_seconds = time_limit
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        for b in range(K):
            for i in range(N):
                if solver.Value(x[i, b]) > 0:
                    best_sol[i] = b + 1
        return int(solver.ObjectiveValue()), best_sol
    else:
        return 0, best_sol     

### Utilities function to print the results ###
def Print_Result(best_value, solution, N, K):
    if best_value == 0:
        print("An optimal solution for the problem is not found.")
    else:
        print("Total packed value is:", best_value)
        for k in range(K):
            print(f"Car {k+1}:")
            for n in range(N):
                if solution[n] == k + 1:
                    print(f"Item {n+1}")
                    
### Utilities function to read the datasets ###
def read_dataset(file_num):
    file_path = "..\\dataset\\" + "{:03d}.txt".format(file_num)
    with open(file_path, 'r') as f:
        data = f.readlines()
        N, K = [int(x) for x in data[0].split()]
        items = []
        for i in range(1, N + 1):
            w, v = [int(x) for x in data[i].split()]
            items.append([w, v])
        cars = []
        for i in range(N + 1, N + K + 1):
            l, u = [int(x) for x in data[i].split()]
            cars.append([l, u])
    return N, K, items, cars
        
        


    
        
    
            