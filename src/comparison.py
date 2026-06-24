import os
import numpy as np
import pandas as pd
# Đọc kết quả
try:
    bt_summary = pd.read_csv("results/backtracking_results.csv")

    csp_summary = pd.read_csv("results/csp_results.csv")

    fc_summary = pd.read_csv("results/csp_fc_results.csv")
    
except FileNotFoundError as e:
    print(f"⚠️ LỖI: Thiếu file kết quả thực nghiệm thô trong thư mục 'results/'.")
    print(f"Chi tiết lỗi: {e}")
    exit(1)

difficulty_order = [
    "Easy",
    "Medium",
    "Hard",
    "Extreme"
]
for df_temp in [bt_summary, csp_summary, fc_summary]:
    
    df_temp["difficulty"] = pd.Categorical(
        df_temp['difficulty'],
        categories=difficulty_order,
        ordered=True
    )
    
#================================
# So sánh thời gian trung bình
#================================

bt_summary = bt_summary.groupby("difficulty", observed=True).agg({
    "time_ms": "mean",
    "steps": "mean",
    "backtracks": "mean",
    "empty_cells": "mean",
    "correct": "mean"
})

csp_summary = csp_summary.groupby("difficulty", observed=True).agg({
    "time_ms": "mean",
    "steps": "mean",
    "backtracks": "mean",
    "correct": "mean"
})

fc_summary = fc_summary.groupby("difficulty", observed=True).agg({
    "time_ms": "mean",
    "steps": "mean",
    "backtracks": "mean",
    "correct": "mean"
})

# CHUYỂN ACCURACY THÀNH %
bt_accuracy = bt_summary["correct"] * 100
csp_accuracy = csp_summary["correct"] * 100
fc_accuracy = fc_summary["correct"] * 100


print("BT difficulties:")
print(list(bt_summary.index))

print("\nCSP difficulties:")
print(list(csp_summary.index))

print("\nCSP + FC difficulties:")
print(list(fc_summary.index))

# =======================================================
# TẠO BẢNG ĐỐI SÁNH TỔNG HỢP 3 BÊN (3-WAY COMPARISON)
# =======================================================

comparison = pd.DataFrame({
    "Avg_Empty_Cells": bt_summary["empty_cells"],
    
    # Cột thời gian thực thi (ms)
    "BT_Time(ms)": bt_summary["time_ms"],
    "CSP_Time(ms)": csp_summary["time_ms"],
    "FC_Time(ms)": fc_summary["time_ms"],
    
    # Cột tổng số bước duyệt cây quyết định
    "BT_Steps": bt_summary["steps"],
    "CSP_Steps": csp_summary["steps"],
    "FC_Steps": fc_summary["steps"],
    
    # Cột quay lùi
    "BT_Backtracks": bt_summary["backtracks"],
    "CSP_Backtracks": csp_summary["backtracks"],
    "FC_Backtracks": fc_summary["backtracks"],
    
    "BT_Accuracy(%)": bt_accuracy,
    "CSP_Accuracy(%)": csp_accuracy,
    "FC_Accuracy(%)": fc_accuracy
})

# Tính toán chỉ số hiệu quả cho phiên bản CSP + MRV cũ
comparison["Speedup_CSP"] = comparison["BT_Time(ms)"] / comparison["CSP_Time(ms)"].replace(0, np.nan)
comparison["Steps_Red_CSP"] = comparison["BT_Steps"] / comparison["CSP_Steps"].replace(0, np.nan)

# Tính toán chỉ số hiệu quả cho phiên bản Active Forward Checking mới
comparison["Speedup_FC"] = comparison["BT_Time(ms)"] / comparison["FC_Time(ms)"].replace(0, np.nan)
comparison["Steps_Red_FC"] = comparison["BT_Steps"] / comparison["FC_Steps"].replace(0, np.nan)

comparison["Backtrack_Red_CSP"] = comparison["BT_Backtracks"] / comparison["CSP_Backtracks"].replace(0, np.nan)
comparison["Backtrack_Red_FC"] = comparison["BT_Backtracks"] / comparison["FC_Backtracks"].replace(0, np.nan)

# ======================================================
# # ĐỊNH VỊ THUẬT TOÁN NHANH NHẤT
# ======================================================

comparison["Fastest"] = comparison[["BT_Time(ms)", "CSP_Time(ms)", "FC_Time(ms)"]].idxmin(axis=1)

# Thay thế hậu tố tên cột 
comparison["Fastest"] = comparison["Fastest"].str.replace("_Time(ms)", "", regex=False)

# Sắp xếp lại lề dòng và thực hiện làm tròn số an toàn
comparison = comparison.reindex(difficulty_order)
comparison = comparison.round(2)

# ======================================================
# # XUẤT BÁO CÁO RA MÀN HÌNH TERMINAL
# ======================================================

print("\n" + "=" * 100)
print("BẢNG ĐỐI SÁNH HIỆU NĂNG TỔNG HỢP ĐỒ ÁN (3-WAY BENCHMARK MASTER REPORT)")
print("=" * 100)
print(comparison.to_string())
print("=" * 100)

print("\nAVERAGE EMPTY CELLS DISTRIBUTION")
print("=" * 100)
print(bt_summary["empty_cells"].round(2).to_string())
print("=" * 100)

# ======================================================
# # LƯU TRỮ FILE CSV KẾT QUẢ CUỐI CÙNG
# ======================================================
os.makedirs("results", exist_ok=True)
comparison.to_csv("results/comparison_summary.csv")

print("\n💾 Xuất báo cáo đối sánh tổng hợp thành công!")
print("👉 Đường dẫn file: results/comparison_summary.csv\n")