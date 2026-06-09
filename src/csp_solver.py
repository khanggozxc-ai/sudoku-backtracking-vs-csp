# Thuật toán CSP + MRV

class CSPStats:
    
    def __init__(self):
        self.steps = 0
        
def is_valid_board(board, num, pos, stats=None):
    
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


def get_domain(board, row, col):
    
    domain = []
    
    for num in range(1, 10):
        
        if is_valid_board(board, num, (row, col)):
            domain.append(num)
            
    return domain

def find_mrv_cell(board):
    
    best_cell = None
    best_domain = []
    best_domain_size = 10
    
    for row in range(9):
        
        for col in range(9):
            
            if board[row][col] == 0:
                
                domain = get_domain(board, row, col)
                
                if len(domain) == 0:
                    
                    return (row, col), domain
                
                if len(domain) < best_domain_size:
                    
                    best_domain_size = len(domain)
                    best_cell = (row, col)
                    best_domain = domain
                    
    return best_cell, best_domain


def solve_csp(board, stats):
    # Chọn ô theo MRV
    
    empty, domain =find_mrv_cell(board)
    
    # Không còn ô trống
    
    if not empty:
        return True
    
    row, col = empty
    
    # Thử từng giá trị trong domain
    
    for num in domain:
        
        stats.steps += 1 
        
        board[row][col] = num
                    
        if solve_csp(board, stats):
            
            return True
            
        board[row][col] = 0
            
    return False

def verify_solution(board):
    
    target = set(range(1,10))
    
    # Kiểm tra hàng
    
    for row in range(9):

        if set(board[row]) != target:
            
            return False
        
    # Kiểm tra cột
    
    for col in range(9):

        col_values = [board[i][col] for i in range(9)]

        if set(col_values) != target:
            
            return False
        
    # Kiểm tra box 3x3
    
    for box_row in range(0, 9, 3):
        
        for box_col in range(0, 9, 3):
            
            values = []
            
            for i in range(box_row, box_row + 3):
                
                for j in range(box_col, box_col + 3):
                    
                    values.append(board[i][j])
                    
            if set(values) != target:
                return False
            
    return True

if __name__ == "__main__":
    
    board = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ]
    
    stats = CSPStats()
    
    print("Bàn cờ mẫu:")
    
    for row in board:
        print(row)
    
    solved = solve_csp(board, stats)
    
    print("\nResult")
    print("="*60)
    
    print("Solved:", solved)
    print("Steps:", stats.steps)
    
    print("\nBoard sau khi giải:\n")
    for row in board:
        print(row)
   
    print("Kiểm tra chính xác:")
    print("Correct:", verify_solution(board))
    
    

    