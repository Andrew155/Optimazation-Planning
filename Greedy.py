import logging
import numpy as np

class GreedySolver:
    def __init__(self, num_customers, num_trucks, quantities, values, lower_bounds, upper_bounds, prioritize="efficiency", order="lower"):
        self.num_customers = num_customers
        self.num_trucks = num_trucks
        self.quantities = quantities
        self.values = values
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds
        self.prioritize = prioritize
        self.order = order
        self.total_value = sum(values)
        self.objective_value = 0
        self.num_deliver_packages = 0
        self.logger = logging.getLogger("GreedySolver")

    def __prioritize_customers(self):
        if self.prioritize == "quantity":
            return sorted(range(self.num_customers), key=lambda x: -self.quantities[x])
        elif self.prioritize == "value":
            return sorted(range(self.num_customers), key=lambda x: -self.values[x])
        elif self.prioritize == "efficiency":
            return sorted(range(self.num_customers), key=lambda x: -self.values[x] / self.quantities[x])
        else:
            return sorted(range(self.num_customers), key=lambda x: -self.values[x] * self.quantities[x])

    def __order_trucks(self):
        if self.order == "lower":
            return sorted(range(self.num_trucks), key=lambda x: -self.lower_bounds[x])
        elif self.order == "upper":
            return sorted(range(self.num_trucks), key=lambda x: -self.upper_bounds[x])
        else:
            return sorted(range(self.num_trucks), key=lambda x: self.upper_bounds[x] - self.lower_bounds[x])

    def solve(self):
        customer_order = self.__prioritize_customers()
        truck_order = self.__order_trucks()

        loads = [0] * self.num_trucks
        goods_pos = np.zeros((self.num_customers, self.num_trucks), dtype=int)

        for customer in customer_order:
            for truck in truck_order:
                if loads[truck] < self.lower_bounds[truck] and loads[truck] + self.quantities[customer] <= self.upper_bounds[truck]:
                    loads[truck] += self.quantities[customer]
                    goods_pos[customer][truck] = 1
                    break

        for truck in truck_order:
            if loads[truck] < self.lower_bounds[truck]:
                raise ValueError(f"Truck {truck} does not meet the lower bound requirement.")

        for customer in customer_order:
            if not goods_pos[customer].any():
                for truck in truck_order:
                    if loads[truck] + self.quantities[customer] <= self.upper_bounds[truck]:
                        loads[truck] += self.quantities[customer]
                        goods_pos[customer][truck] = 1
                        break

        self.objective_value = sum(self.values[i] for i in range(self.num_customers) if goods_pos[i].any())
        self.num_deliver_packages = sum(goods_pos.sum(axis=1) > 0)
        return goods_pos.T

    def plan(self):
        solution = self.solve()
        plan = []
        for i in range(self.num_trucks):
            on_this_truck = [j + 1 for j in range(self.num_customers) if solution[i][j] == 1]
            plan.append(on_this_truck)

        string_plan = "\n\n".join([f"- Truck {idx+1} contains goods of {len(on_this_truck)} customers: {', '.join(map(str, on_this_truck))}" for idx, on_this_truck in enumerate(plan)])
        res = f"With the maximum total values of {self.objective_value}/{self.total_value}, we deliver {self.num_deliver_packages}/{self.num_customers} packages with the plan below: \n{string_plan}"
        return res

def main():
    # logging.basicConfig(level=logging.INFO)

    # num_customers = int(input("Enter the number of customers: "))
    # num_trucks = int(input("Enter the number of trucks: "))

    # quantities = []
    # values = []
    # for i in range(num_customers):
    #     q, v = map(int, input(f"Enter quantity and value for customer {i+1}: ").split())
    #     quantities.append(q)
    #     values.append(v)

    # lower_bounds = []
    # upper_bounds = []
    # for i in range(num_trucks):
    #     l, u = map(int, input(f"Enter lower and upper bounds for truck {i+1}: ").split())
    #     lower_bounds.append(l)
    #     upper_bounds.append(u)
    num_customers, num_trucks = map(int, input().split())  # Number of orders, Number of vehicles

    quantities = []
    values = []
    for i in range(num_customers):
        q, v = map(int, input().split())
        quantities.append(q)
        values.append(v)

    lower_bounds = []
    upper_bounds = []
    for i in range(num_trucks):
        l, u = map(int, input().split())
        lower_bounds.append(l)
        upper_bounds.append(u)

    solver = GreedySolver(num_customers, num_trucks, quantities, values, lower_bounds, upper_bounds)
    print(solver.plan())

if __name__ == "__main__":
    main()
