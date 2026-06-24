import os
import time
import pandas as pd
from data_loader import(string_to_board, count_empty_cells)
from tracker import benchmark_backtracking 

# đọc file dữ liệu chứa các đề tài sudoku đầu vào

df = pd.read_csv(
    "data/processed_sudoku.csv", 
    dtype={"quizzes": str,
           "solutions": str
           }
)

# Khởi tạo danh sách rỗng để lưu trữ kết quả đo dạc của từng bài

results = []

pipeline_start = time.perf_counter()
#==========================================
# Benchmark toàn bộ dataset
#==========================================

for index, row in df.iterrows():
    puzzle = row["quizzes"] # Trích xuất chuỗi mã hóa của bài Sudoku
    
    difficulty = row["difficulty"] # Trích xuất độ khó tương ứng
    
    board = string_to_board(puzzle) # Chuyển đổi ma trận text thành ma trận 9x9
    
    empty_cells = count_empty_cells(board)
    
    benchmark = benchmark_backtracking(board) # Kích hoạt bộ bấm giờ để đo đạc thời gian(ms) và số bước giải
    
    # Ghi nhận kết quả vào kho lưu trữ
    
    results.append({
        "puzzle_id": index + 1,
        "difficulty": difficulty,
        "empty_cells": empty_cells,
        "time_ms": benchmark["time_ms"],
        "solved": benchmark["solved"],
        "correct": benchmark["correct"],
        "steps": benchmark["steps"],
        "backtracks": benchmark["backtracks"]
    })
    
    # Sau 50 bài thì in tiến độ ra màn hình 1 lần
    
    if (index + 1) % 50 == 0:
        
        print(
            f"[{index+1:03d}/{len(df)}]"
            f"{difficulty:<8} | "
            f"{benchmark['time_ms']:.3f} ms | "
            f"Steps: {benchmark['steps']:,} | "
            f"Backtracks: {benchmark['backtracks']}"
        )

# ==========================================
# Kết thúc benchmark
# ==========================================

pipeline_end = time.perf_counter()

total_runtime = pipeline_end - pipeline_start

#=======================================
# TỔNG HỢP VÀ XUẤT BÁO CÁO
#=======================================

# CHuyển đổi mảng kết quả thành DataFrame để dễ thao tác

results_df = pd.DataFrame(results)

# THứ tự độ khó
difficulty_order = [
    "Easy",
    "Medium",
    "Hard",
    "Extreme"
]

results_df["difficulty"] = pd.Categorical(
    results_df["difficulty"],
    categories = difficulty_order,
    ordered = True
)

print("\n Sample Results")
print("="*60)

print(results_df.head(10).to_string(index=False))

#===============================
# Kiểm tra độ chính xác
#===============================
print("\nSolutions Verification")
print("="*60)

print(results_df[["solved", "correct"]].value_counts())

total = len(results_df)

solved_count = results_df["solved"].sum()

correct_count = results_df["correct"].sum()

print(f"\n👉 Tỷ lệ giải xong : {solved_count}/{total} ({solved_count / total * 100:.2f}%)")

print(f"👉 Tỷ lệ nghiệm đúng: {correct_count}/{total} ({correct_count / total * 100:.2f}%)")

# ==========================================
# Thống kê số ô trống
# ==========================================

print("\nEMPTY CELLS DISTRIBUTION STATISTICS")
print("="*60)

empty_summary = (
    results_df
    .groupby("difficulty", observed=True)["empty_cells"]
    .agg(["mean", "min", "max"])
)

print(empty_summary.round(2))

#======================
# THỐNG KÊ HIỆU NĂNG
#======================
print("\nPERFORMANCE SUMMARY")
print("="*60)

summary = results_df.groupby("difficulty", observed=True).agg({
    "time_ms": ["mean", "min", "max"],
    "steps": ["mean", "min", "max"],
    "backtracks": ["mean", "min", "max"]
})

print(summary.round(2))

# ==========================================
# Thống kê Backtrack riêng
# ==========================================

print("\nBACKTRACK STATISTICS")
print("=" * 60)

backtrack_summary = (
    results_df
    .groupby("difficulty", observed=True)["backtracks"]
    .agg(["mean", "min", "max"])
)

print(backtrack_summary.round(2))

# ==========================================
# Tổng thời gian benchmark
# ==========================================

print("\nBENCHMARK RUNTIME")
print("=" * 60)

print(
    f"Total Runtime: "
    f"{total_runtime:.2f} seconds"
)

# Xuất toàn bộ kết quả ra file CSV results
results_df = results_df.sort_values(
    by=["difficulty", "puzzle_id"]
)

os.makedirs("results", exist_ok=True)

results_df.to_csv(
    "results/backtracking_results.csv",
    index=False
)

# ==========================================
# Tổng kết
# ==========================================

print("\n" + "=" * 60)

print("BACKTRACKING BENCHMARK PIPELINE COMPLETE")

print("=" * 60)

print(f"Total puzzles: {total}\n")

print(
    results_df["difficulty"]
    .value_counts()
    .sort_index()
)

print("\nKết quả thực nghiệm đã được lưu tại:")

print("results/backtracking_results.csv")

print("=" * 60)