# Đo thời gian và số bước
import time
from csp_fc_solver import (solve_csp_fc, CSPFCStats, verify_solution)

#================================================
# Hàm theo dõi thời gian và số bước giải Sudoku
#================================================

def benchmark_csp_fc(board):
    
    stats = CSPFCStats() # Tạo đối tượng để lưu trữ số bước
    
    start_time = time.perf_counter() # Bắt đầu đo hiệu suất
    solved = solve_csp_fc(board, stats) # Giải Sudoku và truyền đối tượng stats để theo dõi số bước
    end_time = time.perf_counter() # Kết thúc đo hiệu suất
    
    execution_time = round(
        (end_time - start_time) * 1000,
        3
    )
    
    is_correct = verify_solution(board) if solved else False
    

    return {
        "solved": solved,
        "correct": is_correct,
        "time_ms": execution_time,
        "steps": stats.steps,
        "backtracks": stats.backtracks
    }
    

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
    
    result = benchmark_csp_fc(board)
    
    print("\n" + "=" * 50)
    print("\nCSP + FORWARD CHECKING TEST")
    print("=" * 50)

    print(f"Solved     : {result['solved']}")
    print(f"Correct    : {result['correct']}")
    print(f"Time (ms)  : {result['time_ms']}")
    print(f"Steps      : {result['steps']}")
    print(f"Backtracks : {result['backtracks']}")
    
   
    
  