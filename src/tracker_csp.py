# Đo thời gian và số bước
import time
from csp_solver import verify_solution
from csp_solver import (solve_csp, CSPStats)

#================================================
# Hàm theo dõi thời gian và số bước giải Sudoku
#================================================

def benchmark_csp(board):
    
    stats = CSPStats() # Tạo đối tượng để lưu trữ số bước
    
    start_time = time.perf_counter() # Bắt đầu đo hiệu suất
    
    solved = solve_csp(board, stats) # Giải Sudoku và truyền đối tượng stats để theo dõi số bước
    
    
    end_time = time.perf_counter() # Kết thúc đo hiệu suất
    
    is_correct = verify_solution(board)
    
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
    

if __name__ == "__main__":
    
    from data_loader import string_to_board
    import pandas as pd
    
    df = pd.read_csv("data/processed_sudoku.csv")
    
    puzzle = df.iloc[0]["quizzes"]
    
    board = string_to_board(puzzle)
    
    print(board)
    result = benchmark_csp(board)
    
    print("\nCSP TEST")
    print("=" * 50)
    
    print(result)
    
    
   
    
  