def bin_packing_with_constraints(N, K, quantities, values, lower_bounds, upper_bounds):
    # Kết hợp số lượng và chi phí thành danh sách các đơn hàng
    orders = list(zip(quantities, values, range(1, N+1)))  # Thêm index của đơn hàng để truy vết
    
    # Kết hợp dung lượng tối thiểu và tối đa thành danh sách các xe
    vehicles = list(zip(lower_bounds, upper_bounds, range(1, K+1)))  # Thêm index của xe để truy vết
    
    # Sắp xếp các đơn hàng theo tiêu chí tham lam kết hợp
    orders = sorted(orders, key=lambda x: (x[1]/x[0]) * x[0], reverse=True)
    
    # Lưu trữ kết quả
    assignment = []
    m = 0  # số lượng đơn hàng đã được phân
    
    # Theo dõi dung lượng hiện tại của từng xe
    load = [0] * K
    load_orders = [[] for _ in range(K)]
    
    # Bước 1: Phân bổ các đơn hàng vào các xe
    for quantity, cost, order_id in orders:
        best_fit_vehicle = None
        min_extra_capacity = float('inf')
        
        # Tìm xe phù hợp nhất cho đơn hàng hiện tại
        for k in range(K):
            if load[k] + quantity <= vehicles[k][1]:  # Kiểm tra dung lượng tối đa
                extra_capacity = vehicles[k][1] - (load[k] + quantity)
                if extra_capacity < min_extra_capacity:
                    min_extra_capacity = extra_capacity
                    best_fit_vehicle = k
        
        if best_fit_vehicle is not None:
            load[best_fit_vehicle] += quantity
            load_orders[best_fit_vehicle].append(order_id)
            assignment.append((order_id, vehicles[best_fit_vehicle][2]))  # Lưu index của đơn hàng và xe
            m += 1
    
    # Bước 2: Đảm bảo các xe đáp ứng dung lượng tối thiểu và tối đa
    for k in range(K):
        if not (vehicles[k][0] <= load[k] <= vehicles[k][1]):
            # Nếu xe không đáp ứng được ràng buộc, thử tái phân bổ các đơn hàng đã được phân
            for order_id, assigned_vehicle in assignment:
                if assigned_vehicle == vehicles[k][2]:  # Xe cần kiểm tra lại
                    # Thử phân bổ lại đơn hàng này vào xe khác
                    for alt_vehicle in range(K):
                        if alt_vehicle != k and load[alt_vehicle] + quantities[order_id - 1] <= vehicles[alt_vehicle][1]:
                            # Hủy phân bổ cũ
                            load[k] -= quantities[order_id - 1]
                            load_orders[k].remove(order_id)
                            # Thử phân bổ mới
                            load[alt_vehicle] += quantities[order_id - 1]
                            load_orders[alt_vehicle].append(order_id)
                            assignment.append((order_id, vehicles[alt_vehicle][2]))  # Lưu index của đơn hàng và xe mới
                            m += 1
                            break
                    else:
                        print(f"Order {order_id} with quantity {quantities[order_id-1]} and cost {values[order_id-1]} could not be reassigned to any vehicle.")
    
    # Kiểm tra xem tất cả các đơn hàng đã được phân chưa
    assigned_orders = set([order for order, _ in assignment])
    if len(assigned_orders) != N:
        for order_id in range(1, N + 1):
            if order_id not in assigned_orders:
                print(f"Order {order_id} with quantity {quantities[order_id-1]} and cost {values[order_id-1]} could not be assigned to any vehicle.")
    
    # Kiểm tra xem tất cả các xe có đáp ứng dung lượng tối thiểu và tối đa không
    for k in range(K):
        if not (vehicles[k][0] <= load[k] <= vehicles[k][1]):
            print(f"Vehicle {vehicles[k][2]} does not meet the capacity constraints.")
    
    return m, assignment

# Đọc dữ liệu đầu vào
N, K = map(int, input().split())  # Số lượng đơn hàng và số lượng xe

quantities = []
values = []
for _ in range(N):
    q, v = map(int, input().split())
    quantities.append(q)
    values.append(v)

lower_bounds = []
upper_bounds = []
for _ in range(K):
    l, u = map(int, input().split())
    lower_bounds.append(l)
    upper_bounds.append(u)

# Gọi hàm giải quyết bài toán
m, assignment = bin_packing_with_constraints(N, K, quantities, values, lower_bounds, upper_bounds)

# In kết quả
print(m)
for order, vehicle in assignment:
    print(order, vehicle)
