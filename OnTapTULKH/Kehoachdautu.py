from ortools.linear_solver import pywraplp

def MIP_Invest(n, areas, gao_revenue, khoai_revenue, san_revenue, costs, limits):
   
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None

    # Variables
    x = {}
    for i in range(n):
        for j in range(3):
            x[i, j] = solver.BoolVar(f'x[{i},{j}]')

    # Constraints
    # Mỗi cánh đồng chỉ trồng 1 loại
    for i in range(n):
        solver.Add(sum(x[i, j] for j in range(3)) == 1)

    # Giới hạn 
    solver.Add(sum(x[i, 0] * areas[i] for i in range(n)) <= limits[0])  # Gạo
    solver.Add(sum(x[i, 1] * areas[i] for i in range(n)) <= limits[1])  # Khoai
    solver.Add(sum(x[i, 2] * areas[i] for i in range(n)) <= limits[2])  # Sắn

    # Objective: Maximize profit
    profit = solver.Sum(x[i, 0] * (gao_revenue[i] - costs[0] * areas[i]) +
                        x[i, 1] * (khoai_revenue[i] - costs[1] * areas[i]) +
                        x[i, 2] * (san_revenue[i] - costs[2] * areas[i])
                        for i in range(n))
    solver.Maximize(profit)

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        return solver.Objective().Value()
    else:
        return None

if __name__ == "__main__":

    n = int(input())
    areas = list(map(int, input().split()))
    gao_revenue = list(map(int, input().split()))
    khoai_revenue = list(map(int, input().split()))
    san_revenue = list(map(int, input().split()))
    costs = list(map(int, input().split()))
    limits = list(map(int, input().split()))

    max_profit = MIP_Invest(n, areas, gao_revenue, khoai_revenue, san_revenue, costs, limits)
    print(int(max_profit) if max_profit is not None else "No solution found")
