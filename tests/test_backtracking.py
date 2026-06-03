import pandas as pd
from data_loader import string_to_board
from backtracking_solver import solve_backtracking

df = pd.read_csv("data/processed_sudoku.csv")

puzzle = df.iloc[0]["quizzes"]

board = string_to_board(puzzle)

print("Before:\n")

for row in board:
    print(row)
    
solve_backtracking(board)

print("\nAfter:\n")

for row in board:
    print(row)