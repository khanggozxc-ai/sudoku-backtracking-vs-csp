# Đọc CSV → chuyển thành ma trận NumPy 9x9
import numpy as np
import pandas as pd

#===============================
# LOAD DATASET
#===============================

# đọc file CSV chứa dữ liệu sudoku
df = pd.read_csv("data/sudoku.csv")

print("="*50)
print('DATASET INFORMATION')
print("="*50)

print(f"Columns: {list(df.columns)}")
print(f"Rows: {df.shape[0]}")
print(f"Columns Count: {df.shape[1]}")

print("=" * 50)

#===============================
# String -> Numpy 9x9
#===============================

def string_to_board(puzzle):
    """
    Chuyển chuỗi sudoku thành ma trận NumPy 9x9.
    """
    numbers = [int(char) for char in puzzle]
    
    board = np.array(numbers)
    
    board = board.reshape(9, 9)
    
    return board

#===============================
# Count Empty Cells
#===============================
def count_empty_cells(board):
    """
    Đếm số ô trống (ô có giá trị 0) trong bảng sudoku.
    """
    return np.sum(board == 0) # true = 1, false = 0, nên sẽ đếm được số ô trống.

def count_empty_cells_in_string(puzzle):
    """
    Đếm số ô trống trực tiếp từ chuỗi sudoku.
    """
    return puzzle.count('0') # Đếm số lần '0' xuất hiện trong chuỗi, tương đương với số ô trống.

#===============================
# Classify Difficulty
#===============================

def classify_difficulty_from_string(puzzle):
    
    empty = puzzle.count('0')
    
    if empty <= 46:
        return "Easy"
    
    elif empty == 47:
        return "Medium"
    
    elif empty == 48:
        return "Hard"
    
    else:
        return "Extreme"

#===============================
# Test 1 Puzzle
#===============================

sample_puzzle = df.iloc[0]["quizzes"] # Lấy câu đố đầu tiên trong dataset

board = string_to_board(sample_puzzle)

print("\nSample Sudoku:\n")

for row in board:
    print(row)
    
print(f"\nEmpty Cells: {count_empty_cells(board)}")

print(f"\nDifficulty: {classify_difficulty_from_string(sample_puzzle)}")

#===============================
# Classify Entire Dataset
#===============================

print("\nClassifying dataset...")

df['empty_cells'] = df['quizzes'].apply(count_empty_cells_in_string)

df['difficulty'] = df['quizzes'].apply(classify_difficulty_from_string)

print("\nDifficulty Statistics:\n")

print(df["difficulty"].value_counts()) # Đếm số lượng câu đố ở mỗi độ khó.

#===============================
# Save Results 
#===============================



print("\nĐang trích xuất mỗi độ khó 100 bài...")

df_easy = df[df['difficulty'] == 'Easy'].sample(100, random_state=42) # Lấy 100 bài đầu tiên có độ khó Easy
df_medium = df[df['difficulty'] == 'Medium'].sample(100, random_state=42) # Lấy 100 bài đầu tiên có độ khó Medium
df_hard = df[df['difficulty'] == 'Hard'].sample(100, random_state=42) # Lấy 100 bài đầu tiên có độ khó Hard
df_extreme = df[df['difficulty'] == 'Extreme'].sample(100, random_state=42) # Lấy 100 bài đầu tiên có độ khó Extreme

# Gộp 4 tập nhỏ lại thành tập 400 bài
final_df = pd.concat([df_easy, df_medium, df_hard, df_extreme])

# Reset lại số thứ tự dòng 
final_df = final_df.reset_index(drop=True)

# Lưu thành file mới 
final_df.to_csv("data/processed_sudoku.csv", index=False)


print("\nSaved successfully!")

print(f"\nĐã tạo file processed_sudoku.csv chứa {final_df.shape[0]} ván cờ.")

