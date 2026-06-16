# Đo thời gian và số bước
import time
from backtracking_solver import verify_solution
from backtracking_solver import (solve_backtracking, SolverStats)

#================================================
# Hàm theo dõi thời gian và số bước giải Sudoku
#================================================

def benchmark_backtracking(board):
    
    stats = SolverStats() # Tạo đối tượng để lưu trữ số bước
    
    start_time = time.perf_counter() # Bắt đầu đo hiệu suất
    
    solved = solve_backtracking(board, stats) # Giải Sudoku và truyền đối tượng stats để theo dõi số bước
    
    end_time = time.perf_counter() # Kết thúc đo hiệu suất
    
    is_correct = verify_solution(board) # Sau khi kết thúc đo hiệu xuất, thực hiện kiểm tra đồ án
    
    # Tính thời gian thực thi
    execution_time = (
        
        end_time - start_time 
        
    ) * 1000 # Chuyển đổi thời gian sang milliseconds

    return {
        "solved": solved,
        "correct": is_correct,
        "time_ms": execution_time,
        "steps": stats.steps
    }
    