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
    
    # Tính thời gian thực thi
    execution_time = round(
        
        (end_time - start_time ) * 1000, 
        3
    ) # Chuyển đổi thời gian sang milliseconds

    is_correct = verify_solution(board) if solved else False
    
    return {
        "solved": solved,
        "correct": is_correct,
        "time_ms": execution_time,
        "steps": stats.steps,
        "backtracks": stats.backtracks
    }
    
# ================================================
# Kiểm thử độc lập
# ================================================

if __name__ == "__main__":
    
    import pandas as pd
    
    from data_loader import string_to_board
    
    df = pd.read_csv(
        "data/processed_sudoku.csv",
        dtype={
            "quizzes": str,
            "solutions": str
        }
    )
    
    puzzle = df.iloc[0]["quizzes"]
    
    board = string_to_board(puzzle)

    result = benchmark_csp(board)
    
    print("\nCSP TEST")
    print("=" * 50)
    
    print(f"Solved     : {result['solved']}")
    print(f"Correct    : {result['correct']}")
    print(f"Time (ms)  : {result['time_ms']}")
    print(f"Steps      : {result['steps']}")
    print(f"Backtracks : {result['backtracks']}")
    
    
   
    
  