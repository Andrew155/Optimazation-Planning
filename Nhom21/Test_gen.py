import random

def write_test_case_to_file(file_num, N, K, orders, vehicles):
    filename = "{:03d}.txt".format(file_num)
    with open(filename, "w") as f:
        f.write("{} {}\n".format(N, K))
        for order in orders:
            f.write("{} {}\n".format(order[0], order[1]))
        for vehicle in vehicles:
            f.write("{} {}\n".format(vehicle[0], vehicle[1]))

def is_valid_test_case(orders, vehicles):
    total_weight = sum(order[0] for order in orders)
    for vehicle in vehicles:
        if total_weight < vehicle[0] or total_weight > vehicle[1]:
            return False
    return True


def generate_N(K):
    if K == 2:
        N = random.randint(4, 6)
    else:
        N = random.randint(K ** 2 - K, K ** 2 + K)
    return N
        
def generate_test_case(N, K):    
    orders = []
    for i in range(N):
        weight = random.randint(1, 10)
        value = random.randint(1, 10)
        orders.append((weight, value))
    vehicles = []
    for i in range(K):
        lower = random.randint(3 * K, 5 * K)
        upper = random.randint(lower + 3, 7 * K)
        vehicles.append((lower, upper))
    return orders, vehicles

if __name__ == "__main__":
    #Easy cases
    for i in range(20):
        K = i // 5 + 2
        N = generate_N(K)
        orders, vehicles = generate_test_case(N, K)
        while not is_valid_test_case(orders, vehicles):
            items, cars = generate_test_case(N, K)
        write_test_case_to_file(i + 1, N, K, orders, vehicles)
    
    #Medium cases
    for i in range(6, 16):
        K = i
        N = generate_N(K)
        orders, vehicles = generate_test_case(N, K)
        while not is_valid_test_case(orders, vehicles):
            orders, vehicles = generate_test_case(N, K)
        write_test_case_to_file(15 + i, N, K, orders, vehicles)
    
    #Hard cases
    for i in range (4, 9):
        K = 5 * i
        N = generate_N(K)
        orders, vehicles = generate_test_case(N, K)
        while not is_valid_test_case(orders, vehicles):
            orders, vehicles = generate_test_case(N, K)
        write_test_case_to_file(27+ i, N, K, orders, vehicles)
    
    #Limit_testing
    K = 50
    N = generate_N(K)
    orders, vehicles = generate_test_case(N, K)
    while not is_valid_test_case(orders, vehicles):
        orders, vehicles = generate_test_case(N, K)
    write_test_case_to_file(36, N, K, orders, vehicles)
        
