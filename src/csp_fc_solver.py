import numpy as np

class CSPStats:
    def __init__(self):
        self.steps = 0
        self.backtracks = 0

def initialize_domains(board):
    """Tính sẵn các số khả thi cho từng ô trống khi bắt đầu ván cờ (TỐI ƯU HÓA)"""    
    domains = {}
    
    # 1. Gom trước dữ liệu hàng, cột, block để quét siêu nhanh
    rows_used = [set() for _ in range(9)]
    cols_used = [set() for _ in range(9)]
    boxes_used = [set() for _ in range(9)]
    
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val != 0:
                rows_used[r].add(val)
                cols_used[c].add(val)
                box_idx = (r // 3) * 3 + (c // 3)
                boxes_used[box_idx].add(val)
                
    # 2. Xây dựng domain cho các ô trống dựa trên dữ liệu đã gom
    all_nums = set(range(1, 10))
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                box_idx = (r // 3) * 3 + (c // 3)
                # Dùng phép toán tập hợp (Set operations) của Python: Trừ đi các số đã dùng
                used = rows_used[r] | cols_used[c] | boxes_used[box_idx]
                domains[(r, c)] = all_nums - used
                
    return domains

# =======================================================
# Hàm giải Sudoku bằng CSP + MRV + Active Forward Checking
# =======================================================     
def solve_csp(board, stats):
    domains = initialize_domains(board)
    
    def backtrack(current_domains):
        if not current_domains:
            return True
            
        # 1. HEURISTIC MRV: Chọn ô trống có ít lựa chọn nhất 
        min_cell = min(current_domains, key=lambda k: len(current_domains[k]))
        row, col = min_cell
        domain = current_domains[min_cell]
        
        # 2. Thử từng số trong miền giá trị
        for num in domain:
            stats.steps += 1
            board[row][col] = num
            
            # --- BƯỚC LAN TRUYỀN FORWARD CHECKING CHỦ ĐỘNG (TỐI ƯU HÓA COPY) ---
            # Chỉ copy những domain bị ảnh hưởng thay vì copy TOÀN BỘ current_domains
            next_domains = {}
            fc_failed = False
            
            box_r, box_c = (row // 3) * 3, (col // 3) * 3
            
            for neighbor, n_domain in current_domains.items():
                if neighbor == min_cell:
                    continue
                    
                nr, nc = neighbor
                
                # Nếu hàng xóm nằm trong vùng ảnh hưởng và 'num' có trong domain của nó
                if (nr == row or nc == col or (box_r <= nr < box_r + 3 and box_c <= nc < box_c + 3)):
                    if num in n_domain:
                        # Copy và remove số 'num' (Phép toán set - tạo set mới cực nhanh)
                        new_domain = n_domain.copy()
                        new_domain.remove(num)
                        
                        # MẮT THẦN FC: Nếu rỗng -> Phát hiện ngõ cụt
                        if len(new_domain) == 0:
                            fc_failed = True
                            break 
                        next_domains[neighbor] = new_domain
                    else:
                         next_domains[neighbor] = n_domain
                else:
                    # Không bị ảnh hưởng thì giữ nguyên tham chiếu để tiết kiệm RAM
                    next_domains[neighbor] = n_domain
            
            if not fc_failed:
                if backtrack(next_domains):
                    return True
                    
            board[row][col] = 0
            # Ghi nhận số lần Backtrack để vẽ biểu đồ
            stats.backtracks += 1
            
        return False

    return backtrack(domains)

# =======================================================
# Hàm xác minh nghiệm 
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
# Khối chạy thử nghiệm 
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
    
    solved = solve_csp(board, stats)
    
    print("\nResult")
    print("="*60)
    print("Solved:", solved)
    print("Steps:", stats.steps)
    print("Backtracks:", stats.backtracks)
    
    print("\nBoard sau khi giải:\n")
    for row in board:
        print(row)
   
    print("\nKiểm tra tính chính xác của nghiệm:")
    print("Correct:", verify_solution(board))
