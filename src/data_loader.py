# Đọc CSV → chuyển thành ma trận NumPy 9x9
import pandas as pd
# đọc file CSV chứa dữ liệu sudoku
df = pd.read_csv("data/sudoku.csv")

print("="*50)
print('DATASET INFOMATION')
print("="*50)

# Xem bản này có những cột gì.
print("Columns:")
print(df.columns)

# Xem dataset có bao nhiêu dòng, bao nhiêu cột.
print("\nShape:")
print(df.shape)

# Lấy một dòng đầu tiên để xem nó trông như thế nào.
print("\nFirst row:")
print(df.iloc[0])

puzzle = df.iloc[0]["quizzes"]

print("\nLength:")
print(len(puzzle))

print("="*50)
