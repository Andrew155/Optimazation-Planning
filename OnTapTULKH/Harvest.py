from ortools.linear_solver import pywraplp

def harvest_planning(N, fields, M, m):
    d = [field[0] for field in fields]
    s = [field[1] for field in fields]
    e = [field[2] for field in fields]

    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    X = {}
    for i in range(N):
        for t in range(s[i], e[i] + 1):
            X[i, t] = solver.IntVar(0, 1, 'x[%i,%i]' % (i, t))

    Y = {}
    for t in range(max(e) + 1):
        Y[t] = solver.BoolVar('y[%i]' % t)

    # Constraints
    # Constraint 1: Total harvest <= M if machine is running
    for t in range(max(e) + 1):
        if t in Y:
            solver.Add(sum(X[i, t] * d[i] for i in range(N) if (i, t) in X) <= M * Y[t])

    # Constraint 2: Machine runs if total harvest >= m
    for t in range(max(e) + 1):
        if t in Y:
            solver.Add(sum(X[i, t] * d[i] for i in range(N) if (i, t) in X) >= m * Y[t])

    # Constraint 3: Each field is harvested once
    for i in range(N):
        solver.Add(sum(X[i, t] for t in range(s[i], e[i] + 1) if (i, t) in X) == 1)

    # Objective: Minimize the difference in harvest between days
    objective = solver.Objective()
    for t in range(max(e) + 1):
        if t in Y:
            objective.SetCoefficient(Y[t], 1)

    objective.SetMinimization()

    # Solve the problem
    status = solver.Solve()

    # Output the solution
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Objective value =', solver.Objective().Value())
        for i in range(N):
            for t in range(s[i], e[i] + 1):
                if (i, t) in X and X[i, t].solution_value() > 0:
                    print('Field', i+1, 'harvested on day', t)
    else:
        print('The problem does not have an optimal solution.')

# Example usage
def main():
    N, m, M = map(int, input().split())
    fields = []

    for _ in range(N):
        di, si, ei = map(int, input().split())
        fields.append([di, si, ei])

    harvest_planning(N, fields, M, m)

if __name__ == "__main__":
    main()
