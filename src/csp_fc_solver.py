# Thuật toán CSP + MRV

class CSPStats:
    
    def __init__(self):
        
        self.steps = 0
        self.backtracks = 0
        
def initialize_domains(board):
    
    """Tính sẵn các số khả thi cho từng ô trống khi bắt đầu ván cờ"""    
    
    domains = {}
    
    for row in range(9):
        
        for col in range(9):
            
            if board[row][col] == 0:
                
                used = set()
                
                # Quét nhanh hàng và cột để gom các số đã dùng
                for i in range(9):
                    
                    if board[row][i] != 0: used.add(board[row][i])
                    
                    if board[i][col] != 0: used.add(board[i][col])  
                
                # Quét nhanh khối 3x3
                
                box_row, box_col = (row//3) * 3, (col//3)* 3
                for i in range(box_row, box_row + 3):
                    
                    for j in range(box_col, box_col + 3):
                        
                        if board[i][j] != 0: used.add(board[i][j])
                        
                # Miền giá trị còn lại = {1..9} trừ đi các số đã dùng
                domains[(row, col)] = [num for num in range(1, 10) if num not in used]
    return domains
# =======================================================
# Hàm giải Sudoku bằng CSP + MRV + Active Forward Checking
# =======================================================   
     
def solve_csp(board, stats):
    # Khởi tạo bảng danh sách miền giá trị ban đầu
    domains = initialize_domains(board)
    
    def backtrack(current_domains):
        # Nếu không còn ô trống nào trong danh sách -> Đã giải xong hoàn toàn!
        if not current_domains:
            return True
            
        # 1. HEURISTIC MRV: Chọn ô trống có ít lựa chọn nhất (Độ phức tạp siêu rẻ O(K))
        min_cell = min(current_domains, key=lambda k: len(current_domains[k]))
        row, col = min_cell
        domain = current_domains[row, col]
        
        # 2. Thử từng số trong miền giá trị của ô tối ưu vừa chọn
        for num in domain:
            stats.steps += 1
            board[row][col] = num  # Đặt thử số vào bàn cờ
            
            # --- BƯỚC LAN TRUYỀN FORWARD CHECKING CHỦ ĐỘNG ---
            # Tạo bản sao mới cho các ô trống còn lại (loại bỏ ô vừa điền)
            next_domains = {k: list(v) for k, v in current_domains.items() if k != min_cell}
            fc_failed = False
            
            # Xác định phạm vi ảnh hưởng (Hàng xóm cùng hàng, cùng cột, cùng khối 3x3)
            box_r, box_c = (row // 3) * 3, (col // 3) * 3
            
            for neighbor in list(next_domains.keys()):
                nr, nc = neighbor
                if nr == row or nc == col or (box_r <= nr < box_r + 3 and box_c <= nc < box_c + 3):
                    # Nếu số vừa điền có tồn tại trong miền giá trị của hàng xóm -> Cắt tỉa nó đi
                    if num in next_domains[neighbor]:
                        next_domains[neighbor].remove(num)
                        
                        # MẮT THẦN FC: Nếu hàng xóm bị rỗng sạch domain -> Phát hiện ngõ cụt lập tức!
                        if len(next_domains[neighbor]) == 0:
                            fc_failed = True
                            break
            
            # Nếu kiểm tra nhìn trước (Forward Checking) an toàn -> Đệ quy tiến lên
            if not fc_failed:
                if backtrack(next_domains):
                    return True
                    
            # THU HỒI TRẠNG THÁI (Backtrack) nếu nhánh phía trước bị kẹt
            board[row][col] = 0
            
        return False

    return backtrack(domains)

# =======================================================
# Hàm xác minh nghiệm (Giữ nguyên cấu trúc của bồ)
# =======================================================
def verify_solution(board):
    target = set(range(1, 10))
    
    for row in range(9):
        if set(board[row]) != target: return False
        
    for col in range(9):
        col_values = [board[i][col] for i in range(9)]
        if set(col_values) != target: return False
        
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            values = []
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    values.append(board[i][j])
            if set(values) != target: return False
            
    return True

# =======================================================
# Khối chạy thử nghiệm nghiệm thu thuật toán
# =======================================================
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
    
    print("Bàn cờ mẫu ban đầu:")
    for row in board:
        print(row)
    
    # Kích hoạt bộ giải siêu tốc
    solved = solve_csp(board, stats)
    
    print("\nResult")
    print("="*60)
    print("Solved:", solved)
    print("Steps:", stats.steps)
    
    print("\nBoard sau khi giải:\n")
    for row in board:
        print(row)
   
    print("\nKiểm tra tính chính xác của nghiệm:")
    print("Correct:", verify_solution(board))