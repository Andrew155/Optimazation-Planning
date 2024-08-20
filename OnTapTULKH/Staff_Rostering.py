from ortools.sat.python import cp_model

def staff_rostering_problem(N, D, A, B, days_off):
    model = cp_model.CpModel()

    # Biến số
    X = {}
    for i in range(N):
        for d in range(D):
            for s in range(5):  # 0=nghỉ, 1=sáng, 2=trưa, 3=chiều, 4=đêm
                X[i, d, s] = model.NewBoolVar(f'X_{i}_{d}_{s}')

    # Ràng buộc
    # 1. Mỗi nhân viên làm nhiều nhất một ca mỗi ngày
    for i in range(N):
        for d in range(D):
            model.Add(sum(X[i, d, s] for s in range(5)) <= 1)

    # 2. Nếu làm ca đêm, ngày hôm sau sẽ được nghỉ
    for i in range(N):
        for d in range(D-1):
            model.Add(X[i, d, 4] + sum(X[i, d+1, s] for s in range(1, 5)) <= 1)

    # 3. Mỗi ca cần ít nhất A và nhiều nhất B nhân viên
    for d in range(D):
        for s in range(1, 5):
            model.Add(sum(X[i, d, s] for i in range(N)) >= A)
            model.Add(sum(X[i, d, s] for i in range(N)) <= B)

    # 4. Tôn trọng các ngày nghỉ phép
    for i in range(N):
        for d in days_off[i]:
            model.Add(sum(X[i, d-1, s] for s in range(5)) == 1)
            model.Add(X[i, d-1, 0] == 1)

    # Hàm mục tiêu: Giảm thiểu số ca đêm tối đa của bất kỳ nhân viên nào
    max_night_shifts = model.NewIntVar(0, D, 'max_night_shifts')
    for i in range(N):
        night_shifts = sum(X[i, d, 4] for d in range(D))
        model.Add(night_shifts <= max_night_shifts)
    model.Minimize(max_night_shifts)

    # Giải bài toán
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300  # Giới hạn thời gian giải
    status = solver.Solve(model)

    # Xử lý kết quả
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        schedule = [[0] * D for _ in range(N)]
        for i in range(N):
            for d in range(D):
                for s in range(5):
                    if solver.BooleanValue(X[i, d, s]):
                        schedule[i][d] = s
        return schedule, solver.ObjectiveValue()
    else:
        return None, None

# Ví dụ sử dụng
N, D, A, B = 8, 6, 1, 3
days_off = [
    [1], [3], [4], [5], [2, 4], [], [], [3]
]
schedule, max_night_shifts = staff_rostering_problem(N, D, A, B, days_off)
if schedule:
    for row in schedule:
        print(' '.join(map(str, row)))
else:
    print("Không tìm thấy giải pháp")
