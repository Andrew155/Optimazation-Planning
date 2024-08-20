from ortools.linear_solver import pywraplp

def maximize_profit(n, areas, rice_revenue, potato_revenue, cassava_revenue, costs, limits):
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None

    # Variables
    x = {}
    for i in range(n):
        for j in range(3):
            x[i, j] = solver.IntVar(0, 1, f'x[{i},{j}]')

    # Constraints
    # Each field can only be planted with one type of crop
    for i in range(n):
        solver.Add(sum(x[i, j] for j in range(3)) == 1)

    # Area limits for each crop
    solver.Add(sum(x[i, 0] * areas[i] for i in range(n)) <= limits[0])  # Rice
    solver.Add(sum(x[i, 1] * areas[i] for i in range(n)) <= limits[1])  # Potato
    solver.Add(sum(x[i, 2] * areas[i] for i in range(n)) <= limits[2])  # Cassava

    # Objective: Maximize profit
    profit = solver.Sum(x[i, 0] * (rice_revenue[i] - costs[0]) * areas[i] +
                        x[i, 1] * (potato_revenue[i] - costs[1]) * areas[i] +
                        x[i, 2] * (cassava_revenue[i] - costs[2]) * areas[i]
                        for i in range(n))
    solver.Maximize(profit)

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        return solver.Objective().Value()
    else:
        return None

if __name__ == "__main__":
    # Đọc dữ liệu đầu vào
    n = int(input())
    areas = list(map(int, input().split()))
    rice_revenue = list(map(int, input().split()))
    potato_revenue = list(map(int, input().split()))
    cassava_revenue = list(map(int, input().split()))
    costs = list(map(int, input().split()))
    limits = list(map(int, input().split()))

    # Tính lợi nhuận tối đa
    max_profit = maximize_profit(n, areas, rice_revenue, potato_revenue, cassava_revenue, costs, limits)
    print(int(max_profit) if max_profit is not None else "No solution found")
