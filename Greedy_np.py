import numpy as np

class GreedySolver:
    def __init__(self, num_orders, num_vehicles, quantities, values, lower_bounds, upper_bounds, **kwargs):
        self.__num_orders = num_orders
        self.__num_vehicles = num_vehicles
        self.__quantity = quantities
        self.__value = values
        self.__total_value = sum(values)
        self.__lower_bound = lower_bounds
        self.__upper_bound = upper_bounds
        self.__objective_value = 0
        self.__num_deliver_orders = 0
        try:
            self.__prioritize_ord = kwargs["prioritize_ord"]
        except KeyError:
            self.__prioritize_ord = None
        try:
            self.__prioritize_veh = kwargs["prioritize_veh"]
        except KeyError:
            self.__prioritize_veh = None

    def __add_goods__(self, prioritize_ord: str = "quantity", prioritize_veh: str = "lower"):
        if prioritize_ord == "quantity":
            order_rate = [(i, self.__quantity[i]) for i in range(self.__num_orders)]
        if prioritize_ord == "value":
            order_rate = [(i, self.__value[i]) for i in range(self.__num_orders)]
        if prioritize_ord == "efficiency":
            order_rate = [(i, self.__value[i] / self.__quantity[i]) for i in range(self.__num_orders)]
        order_rate.sort(key=lambda x: -x[1])

        if prioritize_veh == "lower":
            vehicle_rate = [(i, self.__lower_bound[i]) for i in range(self.__num_vehicles)]
        if prioritize_veh == "upper":
            vehicle_rate = [(i, self.__upper_bound[i]) for i in range(self.__num_vehicles)]
        if prioritize_veh == "difference":
            vehicle_rate = [(i, self.__upper_bound[i] - self.__lower_bound[i]) for i in range(self.__num_vehicles)]

        vehicle_rate.sort(key=lambda x: x[1])

        order_status = np.zeros(shape=(self.__num_orders, self.__num_vehicles))
        real_load = [0 for vehicle in range(self.__num_vehicles)]

        for ord_idx, rate in order_rate:
            quantity_ord = self.__quantity[ord_idx]
            for veh_idx, rate in vehicle_rate:
                lower = self.__lower_bound[veh_idx]
                upper = self.__upper_bound[veh_idx]

                if real_load[veh_idx] < lower and real_load[veh_idx] + quantity_ord <= upper:
                    real_load[veh_idx] += quantity_ord
                    order_status[ord_idx][veh_idx] = 1
                    break

        for veh_idx, rate in vehicle_rate:
            if real_load[veh_idx] < self.__lower_bound[veh_idx]:
                raise ValueError(f"Vehicle {veh_idx} with lower bound {self.__lower_bound[veh_idx]} only contains {real_load[veh_idx]} quantity")

        for ord_idx, rate in order_rate:
            if order_status[ord_idx].sum() > 0:
                continue
            quantity_ord = self.__quantity[ord_idx]
            for veh_idx, rate in vehicle_rate:
                lower = self.__lower_bound[veh_idx]
                upper = self.__upper_bound[veh_idx]

                if real_load[veh_idx] + quantity_ord <= upper:
                    real_load[veh_idx] += quantity_ord
                    order_status[ord_idx][veh_idx] = 1
                    break

        return order_status

    def solve(self):
        if self.__prioritize_ord is None:
            prioritize_ord = ["efficiency", "value", "quantity"]
        else:
            prioritize_ord = [self.__prioritize_ord]
        if self.__prioritize_veh is None:
            prioritize_veh = ["lower", "upper", "difference"]
        else:
            prioritize_veh = [self.__prioritize_veh]

        order_status = None
        try:
            for a in prioritize_ord:
                for b in prioritize_veh:
                    try:
                        order_status = self.__add_goods__(prioritize_ord=a, prioritize_veh=b)
                        raise ArithmeticError("Done")
                    except ValueError:
                        pass
        except ArithmeticError:
            pass
        if order_status is None:
            return None
        self.__solution = order_status
        self.__vehicle_values = (order_status.T @ np.array(self.__value)).astype(int)
        self.__real_load = (order_status.T @ np.array(self.__quantity)).astype(int)
        self.__objective_value = self.__vehicle_values.sum()
        self.__num_deliver_orders = int(order_status.sum())
        return order_status.T

    def plan(self):
        self.__solution = self.solve()
        if self.__solution is None:
            return "No solution found"
        plan = []
        for vehicle_idx, orders in enumerate(self.__solution):
            for order_idx, served in enumerate(orders):
                if served == 1:
                    plan.append((order_idx + 1, vehicle_idx + 1))

        result_lines = [f"{order} {vehicle}" for order, vehicle in plan]
        result = f"{len(plan)}\n" + "\n".join(result_lines)
        return result

def main():
    num_orders, num_vehicles = map(int, input().split())  # Number of orders, Number of vehicles

    quantities = []
    values = []
    for i in range(num_orders):
        q, v = map(int, input().split())
        quantities.append(q)
        values.append(v)

    lower_bounds = []
    upper_bounds = []
    for i in range(num_vehicles):
        l, u = map(int, input().split())
        lower_bounds.append(l)
        upper_bounds.append(u)

    solver = GreedySolver(num_orders, num_vehicles, quantities, values, lower_bounds, upper_bounds)
    
    solution = solver.solve()
    if solution is not None:
        plan = solver.plan()
        print(plan)
    else:
        print("No solution found")

if __name__ == "__main__":
    main()
