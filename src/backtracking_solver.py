# Thuật toán Backtracking giải Sudoku

#================================
# Hàm tìm ô trống đầu tiên
#================================
class SolverStats:
    
    def __init__(self):
        self.steps = 0
        
        
def find_empty(board): 
    
    """Tìm ô trống đầu tiên trên bảng Sudoku"""
    
    for row in range(9): # Duyệt qua từng hàng
        
        for col in range(9): # Duyệt qua từng cột
             
            if board[row][col] == 0: # Nếu ô trống được tìm thấy
                return (row, col) # Dừng hàm và báo về 1 cặp tọa độ vd(0, 2)
            
    return None # Nếu không tìm thấy ô trống nào

#================================
# Kiểm tra hợp lệ
#================================

def is_valid_board(board, num, pos):
    
    row, col = pos # tách tọa độ pos thành 2 biến riêng lẻ là hàng row và cột col
    
    # Kiểm tra hàng
    for j in range(9):
        if board[row][j] == num and j != col: # Nếu số đã tồn tại trong hàng và không phải là vị trí hiện tại
            return False
        
    # Kiểm tra cột
    for i in range(9):
        if board[i][col] == num and i != row: # Nếu số đã tồn tại trong cột và không phải là vị trí hiện tại
            return False
        
    # Kiểm tra box 3x3
    
    # Lấy vị trí ô trống chia lấy nguyên cho 3 để xác định box 3x3 mà ô trống đang nằm trong đó
    box_x = col // 3 
    box_y = row // 3
    
    """ 
    Duyệt qua tất cả các ô trong box 3x3 bằng cách sử dụng 2 vòng lặp for lồng nhau.
    Vòng lặp bên ngoài duyệt qua các hàng của box 3x3,
    còn vòng lặp bên trong duyệt qua các cột của box 3x3.
    Cả hai vòng lặp đều bắt đầu từ vị trí của box 3x3 được xác định bởi box_x và box_y,
    và kết thúc sau 3 ô (vì box 3x3 có kích thước 3x3).
    """
    
    for i in range(box_y * 3, box_y * 3 + 3):
        
        for j in range(box_x * 3, box_x * 3 + 3):
            
            if board[i][j] == num and (i, j) != pos:
                return False # Nếu số đã tồn tại trong box 3x3 và không phải là vị trí hiện tại trả về False
    return True # đúng 3 điều kiện trên, cho phép đặt số

#===============================================
# Hàm giải Sudoku bằng thuật toán Backtracking
#===============================================
        
def solve_backtracking(board, stats): 
    
    empty = find_empty(board) 
    
    if not empty:
        return True # Sudoku đã được giải
    
    row, col = empty  # Xử lí tọa độ của ô trống tìm được 
    
    for num in range(1, 10):  # vòng lặp chạy từ 1 đến 9 để thử đặt từng số vào ô trống
        
        stats.steps += 1 # Tăng số bước mỗi khi thử đặt một số vào ô trống
        
        if is_valid_board(board, num, (row, col)): # Kiểm tra nếu số có thể được đặt tại vị trí hiện tại
            
            board[row][col] = num # Tạm thời đặt số vào ô trống
            
            if solve_backtracking(board, stats): # Đệ quy để giải tiếp nếu số được đặt tại vị trí hiện tại là hợp lệ
                return True
            
            board[row][col] = 0 # Nếu các bước sao bị kẹt, xóa số vừa đặt bằng cách gán về 0 và tiếp tục thử số tiếp theo
            
    return False # nếu thử từ 1-9 mà không có số nào hợp lệ, trả về False 

# =====================================
# Kiểm tra nghiệm Sudoku
# =====================================

def verify_solution(board):

    target = set(range(1, 10))
    # ==============================
    # Kiểm tra hàng
    # ==============================

    for row in range(9):

        if set(board[row]) != target:
            return False

    # ==============================
    # Kiểm tra cột
    # ==============================

    for col in range(9):

        col_values = [board[i][col] for i in range(9)]

        if set(col_values) != target:
            return False

    # ==============================
    # Kiểm tra box 3x3
    # ==============================

    for box_row in range(0, 9, 3):

        for box_col in range(0, 9, 3):

            box_values = []

            for i in range(box_row, box_row + 3):

                for j in range(box_col, box_col + 3):

                    box_values.append(board[i][j])

            if set(box_values) != target:
                return False

    return True