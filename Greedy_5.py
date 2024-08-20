import logging
import numpy as np
class GreedySolver:
    def __init__(self, num_orders, num_vehicles, quantities, values, lower_bounds, upper_bounds, logger = None, **kwargs):
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
            self.__prioritize_ord = kwargs["prioritize_ord"] #value
        except KeyError:
            self.__prioritize_ord = None
        try: 
            self.__prioritize_veh = kwargs["prioritize_veh"] #vehilce
        except KeyError:
            self.__prioritize_veh = None
        if logger is None:
            logger = logging.getLogger("GreedySolver")
        self.__logger = logger

    def __add_goods__(self, prioritize_ord: str = "quantity", prioritize_veh: str = "lower"):
        if prioritize_ord == "quantity":
            order_rate = [(i, self.__quantity[i]) for i in range(self.__num_orders)]
        if prioritize_ord == "value":
            order_rate = [(i, self.__value[i]) for i in range(self.__num_orders)]
        if prioritize_ord == "efficiency":
            order_rate = [(i, self.__value[i] / self.__quantity[i]) for i in range(self.__num_orders)]
        order_rate.sort(key = lambda x: -x[1]) #sort descending by features above

        if prioritize_veh == "lower":
            vehicle_rate =[(i, self.__lower_bound[i]) for i in range(self.__num_vehicles)]
        if prioritize_veh == "upper": 
            vehicle_rate = [(i, self.__upper_bound[i]) for i in range(self.__num_vehicles)]
        if prioritize_veh == "difference":
            vehicle_rate = [(i, self.__upper_bound[i] - self.__lower_bound[i]) for i in range (self.__num_vehicles)]
        
        vehicle_rate.sort(key = lambda x: x[1]) #sort vehilce ascending by features above

        #Create a matrix to follow the orders status (binary matrix)
        order_status = np.zeros(shape = (self.__num_orders, self.__num_vehicles))

        real_load = [0 for vehilce in range (self.__num_vehicles)]   

        #Greedy
        # Assign to ensure the lower constraint
        for ord_idx, rate in order_rate:
            quantity_ord = self.__quantity[ord_idx] #store the quantity of order
            for veh_idx, rate in vehicle_rate:
                lower = self.__lower_bound[veh_idx]
                upper = self.__upper_bound[veh_idx]

                if real_load[veh_idx] < lower and real_load[veh_idx] + quantity_ord <= upper:
                    real_load[veh_idx] += quantity_ord
                    order_status[ord_idx][veh_idx] = 1
                    break
        # Check again to ensure lower constraint
        for veh_idx, rate in vehicle_rate:
            if real_load[veh_idx] < self.__lower_bound[veh_idx]:
                error_message = f"Vehilce {veh_idx} with lower bound {self.__lower_bound[veh_idx]} only contains {real_load[veh_idx]} quantity  "
                self.__logger.error(error_message)
                raise ValueError(error_message)
        self.__logger.info(f"Condition satisfied")
        
        #Already ensure the lower constraint, need to check the orders is assign with vehicle? 
        # If not assign we will assign them, and assign until upper bound
        for ord_idx, rate in order_rate:
            if order_status[ord_idx].sum() > 0: #check to see the order is served by vehicle yet?
                continue
            quantity_ord = self.__quantity[ord_idx]
            for veh_idx, rate in vehicle_rate:
                lower = self.__lower_bound[veh_idx]
                upper = self.__upper_bound[veh_idx]

                if real_load[veh_idx] + quantity_ord < upper:
                    real_load[veh_idx] += quantity_ord
                    order_status[ord_idx][veh_idx] = 1
                    break

        self.__logger.info(f"Done")
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
                        self.__logger.info(f"Try to use greedy algorithm with order sorted by {a} and vehicle sorted by {b} bound")
                        order_status = self.__add_goods__(prioritize_ord= a, prioritize_veh=b)
                        raise ArithmeticError("Done")  # Used to break nested for loops
                    except ValueError:
                         self.__logger.error(f"Fail when using greedy algorithm with order sorted by {a} and vehicle sorted by {b} bound")
        except ArithmeticError:
            pass
        if order_status is None:
            self.__logger.info(f"No solution found")
            return None
        self.__logger.info(f"Solution found")
        self.__solution = order_status
        self.__vehicle_values = (order_status.T @ np.array(self.__value)).astype(int)
        self.__real_load = (order_status.T @ np.array(self.__quantity)).astype(int)
        self.__objective_value = self.__vehicle_values.sum()
        self.__num_deliver_orders = int(order_status.sum())
        for veh_idx in range(self.__num_vehicles):
            self.__logger.debug(f"Vehicle {veh_idx+1}: Bounds: [{self.__lower_bound[veh_idx]}, {self.__upper_bound[veh_idx]}], Load: {self.__real_load[veh_idx]}, Goods values: {self.__vehicle_values[veh_idx]}")

        self.__logger.info(f"Number of orders delivered: {self.__num_deliver_orders}/{self.__num_orders}")
        self.__logger.info(f"Total orders' values: {self.__objective_value}")

        return order_status.T
        
    def plan(self):
        self.__solution = self.solve()
        if self.__solution is None:
            return "No solution found"
        plan = []
        for weight in self.__solution:
            on_this_vehicle = []
            for index, elem in enumerate(weight):
                if elem == 1:
                    on_this_vehicle.append(index + 1)
            plan.append(on_this_vehicle)

        string_plan = "\n\n".join([f"- Vehicle {idx+1} contains goods of {len(plan[idx])} orders: {', '.join([str(val) for val in on_this_vehicle])}" for idx, on_this_vehicle in enumerate(plan)])
        res = f"With the maximum total values of {int(self.__objective_value)}/{self.__total_value}, we deliver {self.__num_deliver_orders}/{self.__num_orders} orders with the plan below: \n{string_plan}"
        return res
        
def main():
    logging.basicConfig(level=logging.INFO)
    
    
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
