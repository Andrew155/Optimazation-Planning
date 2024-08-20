from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    x1 = solver.NumVar(0, 14, 'x1')
    x2 = solver.IntVar(0, 20, 'x2')

    solver.Add(x1 - 10*x2 <=7)
    solver.Add(2*x1 + 3*x2 <=20)

    solver.Maximize(x1 + x2)

    # Solve the system.
    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print(f"Objective value = {solver.Objective().Value():0.1f}")
        print(f"x1 = {x1.solution_value():0.1f}")
        print(f"x2 = {x2.solution_value():0.1f}")
    else:
        print("The problem does not have an optimal solution.")


    # c1 = solver.Constraint(-solver.infinity(), 0)
    # c1.SetCoefficient(x1, 1)
    # c1.SetCoefficient(x2, -10)

    # c2 = solver.Constraint(0, 20)
    # c2.SetCoefficient(x1, 2)
    # c2.SetCoefficient(x2, 3)

    # obj = solver.Objective()
    # obj.SetCoefficient(x1, 1)
    # obj.SetCoefficient(x2, 1)
    # obj.SetMaximization()

    # result_status = solver.Solve()

    # if result_status != pywraplp.Solver.OPTIMAL:
    #     print('Cannot find optimal solution')
    # else:
    #     print('Objective value =', obj.Value())
    #     print('x1 =', x1.SolutionValue())
    #     print('x2 =', x2.SolutionValue())

main()
