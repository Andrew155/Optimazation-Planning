def add_goods(num_orders, num_vehicles, quantities, values, lower_bounds, upper_bounds, prioritize_ord="quantity", prioritize_veh="lower"):
    if prioritize_ord == "quantity":
        order_rate = [(i, quantities[i]) for i in range(num_orders)]
    elif prioritize_ord == "value":
        order_rate = [(i, values[i]) for i in range(num_orders)]
    elif prioritize_ord == "efficiency":
        order_rate = [(i, values[i] / quantities[i]) for i in range(num_orders)]
    order_rate.sort(key=lambda x: -x[1])  #sort descending by features above

    if prioritize_veh == "lower":
        vehicle_rate = [(i, lower_bounds[i]) for i in range(num_vehicles)]
    elif prioritize_veh == "upper":
        vehicle_rate = [(i, upper_bounds[i]) for i in range(num_vehicles)]
    elif prioritize_veh == "difference":
        vehicle_rate = [(i, upper_bounds[i] - lower_bounds[i]) for i in range(num_vehicles)]
    vehicle_rate.sort(key=lambda x: x[1])  #sort vehilce ascending by features above
    #Create a matrix to follow the orders status (binary matrix)
    order_status = [[0] * num_vehicles for _ in range(num_orders)]
    real_load = [0] * num_vehicles
    # Greedy
    # Assign to ensure the lower constraint
    for ord_idx, _ in order_rate:
        quantity_ord = quantities[ord_idx]
        for veh_idx, _ in vehicle_rate:
            lower = lower_bounds[veh_idx]
            upper = upper_bounds[veh_idx]

            if real_load[veh_idx] < lower and real_load[veh_idx] + quantity_ord <= upper:
                real_load[veh_idx] += quantity_ord
                order_status[ord_idx][veh_idx] = 1
                break
    # Check again to ensure lower constraint
    for veh_idx, _ in vehicle_rate:
        if real_load[veh_idx] < lower_bounds[veh_idx]:
            raise ValueError(f"Vehicle {veh_idx} with lower bound {lower_bounds[veh_idx]} only contains {real_load[veh_idx]} quantity")
    #Already ensure the lower constraint, need to check the orders is assign with vehicle? 
    # If not assign we will assign them, and assign until upper bound
    for ord_idx, _ in order_rate:
        if sum(order_status[ord_idx]) > 0: #check to see the order is served by vehicle yet?
            continue
        quantity_ord = quantities[ord_idx]
        for veh_idx, _ in vehicle_rate:
            lower = lower_bounds[veh_idx]
            upper = upper_bounds[veh_idx]
            # Adding till upper bounds touch
            if real_load[veh_idx] + quantity_ord <= upper:
                real_load[veh_idx] += quantity_ord
                order_status[ord_idx][veh_idx] = 1
                break

    return order_status

def solve(num_orders, num_vehicles, quantities, values, lower_bounds, upper_bounds, prioritize_ord=None, prioritize_veh=None):
    if prioritize_ord is None:
        prioritize_ord = ["efficiency", "value", "quantity"]
    else:
        prioritize_ord = [prioritize_ord]
    if prioritize_veh is None:
        prioritize_veh = ["lower", "upper", "difference"]
    else:
        prioritize_veh = [prioritize_veh]
    #try add goods with prioritize_ord and prioritize_veh
    order_status = None
    try:
        for a in prioritize_ord:
            for b in prioritize_veh:
                try:
                    order_status = add_goods(num_orders, num_vehicles, quantities, values, lower_bounds, upper_bounds, prioritize_ord=a, prioritize_veh=b)
                    raise ArithmeticError("Done")   # Used to break the nested for loops
                except ValueError:
                    pass
    except ArithmeticError:
        pass

    if order_status is None:
        return None
    vehicle_values = [sum(order_status[j][i] * values[j] for j in range(num_orders)) for i in range(num_vehicles)]
    real_load = [sum(order_status[j][i] * quantities[j] for j in range(num_orders)) for i in range(num_vehicles)]
    objective_value = sum(vehicle_values)
    num_deliver_orders = sum(sum(row) for row in order_status)

    return list(zip(*order_status)), vehicle_values, real_load, objective_value, num_deliver_orders

def plan(order_status):
    plan_list = []
    for vehicle_idx, orders in enumerate(order_status):
        for order_idx, served in enumerate(orders):
            if served == 1:
                plan_list.append((order_idx + 1, vehicle_idx + 1))

    result_lines = [f"{order} {vehicle}" for order, vehicle in plan_list]
    result = f"{len(plan_list)}\n" + "\n".join(result_lines)
    return result

def main():
    num_orders, num_vehicles = map(int, input().split())  # Number orders, number vehicles

    quantities = []
    values = []
    for _ in range(num_orders):
        q, v = map(int, input().split())
        quantities.append(q)
        values.append(v)

    lower_bounds = []
    upper_bounds = []
    for _ in range(num_vehicles):
        l, u = map(int, input().split())
        lower_bounds.append(l)
        upper_bounds.append(u)

    order_status, vehicle_values, real_load, objective_value, num_deliver_orders = solve(num_orders, num_vehicles, quantities, values, lower_bounds, upper_bounds)
    
    if order_status is not None:
        plan_result = plan(order_status)
        print(plan_result)
    else:
        print("No solution found")

if __name__ == "__main__":
    main()
