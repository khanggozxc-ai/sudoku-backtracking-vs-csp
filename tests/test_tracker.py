import pandas as pd

from data_loader import string_to_board

from tracker import benchmark_backtracking  

df = pd.read_csv(
    "data/processed_sudoku.csv"
)

puzzle = df.iloc[0]["quizzes"]

board = string_to_board(puzzle)

result = benchmark_backtracking(board)

print("\nRESULT")
print("="*30)

print(
    f"Time: {result['time_ms']:.3f} ms"
)

print(
    f"Steps: {result['steps']}"
)