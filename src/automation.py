import pandas as pd
from data_loader import string_to_board
from tracker import benchmark_backtracking

# đọc file dữ liệu chứa các đề tài sudoku đầu vào

df = pd.read_csv(
    "data/processed_sudoku.csv"
)

# Khởi tạo danh sách rỗng để lưu trữ kết quả đo dạc của từng bài

results = []

#==========================================
# Vòng lặp quét dữ liệu + đo dạc hiệu ứng
#==========================================

for index, row in df.iterrows():
    puzzle = row["quizzes"] # Trích xuất chuỗi mã hóa của bài Sudoku
    
    difficulty = row["difficulty"] # Trích xuất độ khó tương ứng
    
    board = string_to_board(puzzle) # Chuyển đổi ma trận text thành ma trận 9x9
    
    benchmark = benchmark_backtracking(board) # Kích hoạt bộ bấm giờ để đo đạc thời gian(ms) và số bước giải
    
    # Ghi nhận kết quả vào kho lưu trữ
    
    results.append({
        "puzzle_id": index + 1,
        "difficulty": difficulty,
        "time_ms": benchmark["time_ms"],
        "steps": benchmark["steps"]
    })
    
    # Sau 50 bài thì in tiến độ ra màn hình 1 lần
    
    if (index + 1) % 50 == 0:
        
        print(
            f"[{index+1:03d}/{len(df)}]"
            f"{difficulty:<8} | "
            f"{benchmark['time_ms']:.3f} ms | "
            f"Steps: {benchmark['steps']}"
            )


#=======================================
# TỔNG HỢP VÀ XUẤT BÁO CÁO
#=======================================

# CHuyển đổi mảng kết quả thành DataFrame để dễ thao tác

results_df = pd.DataFrame(results)
results_df["time_ms"] = results_df["time_ms"].round(3)

print("\n Sample Resulft")
print("="*60)

print(results_df.head(10).to_string(index=False))

# Thống kê hiệu năng trung bình theo từng độ khó

print("\nHiệu năng trung bình theo độ khó")

summary = results_df.groupby("difficulty").agg({
    "time_ms": "mean",
    "steps": "mean"
})

print(summary.round(2))

# Xuất toàn bộ kết quả ra file CSV results
import os

os.makedirs("results", exist_ok=True)

results_df.to_csv(
    "results/backtracking_results.csv",
    index=False
)

print("\n" + "="*60)
print("BACKTRACKING BENCHMARK SUMMARY")
print("="*60)

print(f"Total puzzles: {len(results_df)}")

print(
    results_df["difficulty"]
    .value_counts()
)

print("\nAverage Performance")

summary = results_df.groupby("difficulty").agg({
    "time_ms": "mean",
    "steps": "mean"
})

print(summary.round(2))

print("\nResults saved:")
print("results/backtracking_results.csv")

print("="*60)