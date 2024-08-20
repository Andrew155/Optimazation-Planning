def greedy(n, weights, values, max_weight):
    # Chọn tiêu chí tham lam
    items = []
    for i in range(n):
        items.append((values[i] / weights[i], weights[i], values[i], i))
    
    #Tham lam lấy đồ dựa trên giá trị / trọng lượng
    items.sort(reverse=True, key=lambda x: x[0])

    
 
    selected = [0] * n
    total_weight = 0
    total_value = 0
    
    # Hàm tính discount
    def calculate_discounted_value(count, value):
        if count == 1:
            return value
        elif count == 2:
            return value + value * 0.9
        elif count == 3:
            return value + value * 0.9 + value * 0.7
        return 0
    
    # tham lam lấy đồ tới khi đầy max weight
    for value_per_weight, weight, value, index in items:
        for count in range(1, 4):
            if total_weight + count * weight <= max_weight:
                discounted_value = calculate_discounted_value(count, value)
                selected[index] = count
                total_weight += count * weight
                total_value += discounted_value
                break
            

    return n, selected

#input
n = int(input())
weights = list(map(int, input().split()))
values = list(map(int, input().split()))
max_weight = int(input())


n, selected = greedy(n, weights, values, max_weight)


print(n)
print(' '.join(map(str, selected)))
