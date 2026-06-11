import pandas as pd

# Đọc kết quả

bt_summary = pd.read_csv("results/backtracking_results.csv")

csp_summary = pd.read_csv("results/csp_results.csv")

fc_summary = pd.read_csv("results/csp_fc_results.csv")


#

difficulty_order = [
    "Easy",
    "Medium",
    "Hard",
    "Extreme"
]

for df_temp in [bt_summary, csp_summary]:
    
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
    "empty_cells": "mean"
})

csp_summary = csp_summary.groupby("difficulty", observed=True).agg({
    "time_ms": "mean",
    "steps": "mean"
})

fc_summary = fc_summary.groupby("difficulty", observed=True).agg({
    "time_ms": "mean",
    "steps": "mean"
})

print("BT difficulties:")
print(list(bt_summary.index))

print("\nCSP difficulties:")
print(list(csp_summary.index))

print("\nCSP + FC difficulties:")
print(list(csp_summary.index))

# =======================================================
# TẠO BẢNG ĐỐI SÁNH TỔNG HỢP 3 BÊN (3-WAY COMPARISON)
# =======================================================

comparison = pd.DataFrame({
    # Cột thời gian thực thi (ms)
    "BT_Time(ms)": bt_summary["time_ms"],
    "CSP_Time(ms)": csp_summary["time_ms"],
    "FC_Time(ms)": fc_summary["time_ms"],
    
    # Cột tổng số bước duyệt cây quyết định
    "BT_Steps": bt_summary["steps"],
    "CSP_Steps": csp_summary["steps"],
    "FC_Steps": fc_summary["steps"]
})

# Tính toán chỉ số hiệu quả cho phiên bản CSP + MRV cũ
comparison["Speedup_CSP"] = comparison["BT_Time(ms)"] / comparison["CSP_Time(ms)"]
comparison["Steps_Red_CSP"] = comparison["BT_Steps"] / comparison["CSP_Steps"]

# Tính toán chỉ số hiệu quả cho phiên bản Active Forward Checking mới
comparison["Speedup_FC"] = comparison["BT_Time(ms)"] / comparison["FC_Time(ms)"]
comparison["Steps_Red_FC"] = comparison["BT_Steps"] / comparison["FC_Steps"]

comparison = comparison.reindex(difficulty_order)

print("\n" + "="*80)
print("BẢNG ĐỐI SÁNH HIỆU NĂNG TOÀN DIỆN GIỮA 3 PHIÊN BẢN THUẬT TOÁN")
print("="*80)
print(comparison.round(2))

print("\nAVERAGE EMPTY CELLS BY DIFFICULTY")
print("="*80)
print(bt_summary["empty_cells"].round(2))