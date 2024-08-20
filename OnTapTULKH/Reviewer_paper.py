from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('SCIP')

def MIP(N, M, b, list_can_review):
    best_sol = []
    #Create variables
    X = {}
    for j in range(N):
        count_reviewers, reviewers_list = list_can_review[j]
        for i in reviewers_list:
            X[i, j] = solver.BoolVar(f'X_{i}_{j}')
    load = {}
    for i in range(1, M+1):
        load[i] = solver.IntVar(0, N, f'load[{i}]')
    
    #Adding constraint
    
    for j in range(N):
        count_reviewers, reviewers_list = list_can_review[j]
        solver.Add(sum(X[i, j] for i in reviewers_list) == b)
    max_load = solver.IntVar(0, N, 'max_load')
    for i in range(1, M+1):
        solver.Add(sum(X[i, j] for j in range(N) if (i, j) in X)  == load[i])
        solver.Add(load[i] <= max_load)
    #Objective Function:
    #minimum max_load
    objective = solver.Objective()
    objective.SetCoefficient(max_load, 1)
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        assignment =[]
        for j in range(N):
            reviewers_assigned = []
            for i in range(1, M+1):
                if (i,j) in X and X[i, j].solution_value() == 1:
                    reviewers_assigned.append(i)
            assignment.append(reviewers_assigned)
        print(N)
        for reviewers_assigned in assignment:
            print(b, ' '.join(map(str, reviewers_assigned)))
    else: 
        print("No solution found")



N, M, b = map(int, input().split())
list_can_review = []
for _ in range(N):
    line = input().strip()
    parts = line.split()
    count = int(parts[0])
    reviewers = list(map(int, parts[1:]))
    list_can_review.append((count, reviewers))

MIP(N, M, b, list_can_review)

