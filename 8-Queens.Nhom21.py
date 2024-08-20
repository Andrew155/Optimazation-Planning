def is_safe(board, row, col):
    """
    Propagation Algorithm: Kiểm tra xem có thể đặt một quân hậu vào vị trí (row, col) trên bàn cờ hay không.
    Các tham số đầu vào:
        board (list): Bàn cờ hiện tại.
        row (int): Hàng cần kiểm tra.
        col (int): Cột cần kiểm tra.
    Hàm trả về: 
        bool: Trả về true nếu có thể đặt quân hậu vào vị trí này, false nếu không thể 
    """
    # Kiểm tra xem có quân hậu nào trên hàng này không
    for i in range(col):
        if board[row][i] == 1:
            return False

    # Kiểm tra đường chéo trên bên trái
    i, j = row, col
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    # Kiểm tra đường chéo dưới bên trái
    i, j = row, col
    while i < len(board) and j >= 0:
        if board[i][j] == 1:
            return False
        i += 1
        j -= 1

    

    return True

def solve_queen_util(board, col):
    """
    Branching Algorithm: Đệ quy quay lui
    Các tham số đầu vào:
        board (list): Bàn cờ hiện tại.
        col (int): Cột hiện tại cần đặt quân hậu.
    Hàm trả về: 
        bool: Trả về true nếu có giải pháp, false nếu không có giải pháp.
    """
    # Nếu tất cả quân hậu đã được đặt
    if col >= len(board):
        return True

    # Duyệt qua từng hàng trong cột col
    for i in range(len(board)):
        if is_safe(board, i, col):
            # Đánh dấu quân hậu được đặt
            board[i][col] = 1

            # Gọi đệ quy để thử tiếp cho các vị trí tiếp theo
            if solve_queen_util(board, col + 1):
                return True

            # Nếu không tìm được giải pháp, quay lui và thử lại
            board[i][col] = 0

    # Nếu không tìm được vị trí hợp lệ cho quân hậu trong cột này, trả về false
    return False

def solve_queen():
    """
    Exploration Algorithm: DFS duyệt tất cả các vị trí
        bool: Trả về True nếu có giải pháp, False nếu không có giải pháp.
    """
    # Khởi tạo bàn cờ 8x8
    board = [[0] * 8 for _ in range(8)]

    # Khởi tạo stack để lưu trữ trạng thái của bàn cờ
    stack = [(board, 0)]  

    # Duyệt qua các trạng thái trong stack
    while stack:
        current_board, col = stack.pop()  
        if col >= len(current_board):
            # Nếu đã đặt quân hậu ở cột cuối cùng, in ra lời giải và trả về True
            print("Giải pháp:")
            for row in current_board:
                print(" ".join(map(str, row)))
            return True
        else:
            # Thử từng vị trí hợp lệ để đặt quân hậu trong cột hiện tại
            for row in range(len(current_board)):
                if is_safe(current_board, row, col):  # Kiểm tra xem vị trí có hợp lệ không
                    # Tạo một bản sao của bàn cờ và đặt quân hậu ở vị trí hợp lệ
                    new_board = [row[:] for row in current_board]
                    new_board[row][col] = 1
                    # Thêm trạng thái mới vào stack để tiếp tục duyệt
                    stack.append((new_board, col + 1))

    # Nếu không tìm thấy giải pháp sau khi duyệt qua tất cả các trạng thái, trả về False
    print("Không có giải pháp")
    return False


solve_queen()
