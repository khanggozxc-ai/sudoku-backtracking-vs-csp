import pandas as pd

# Đọc kết quả

bt_summary = pd.read_csv("results/backtracking_results.csv")

csp_summary = pd.read_csv("results/csp_results.csv")


#

difficulty_order = [
    "Easy",
    "Medium",
    "Hard",
    "Extreme"
]

#================================
# So sánh thời gian trung bình
#================================

bt_summary = bt_summary.groupby("difficulty").agg({
    "time_ms": "mean",
    "steps": "mean",
    "empty_cells": "mean"
})

csp_summary = csp_summary.groupby("difficulty").agg({
    "time_ms": "mean",
    "steps": "mean"
})

print("BT difficulties:")
print(bt_summary.index)

print("\nCSP difficulties:")
print(csp_summary.index)

# Tạo bảng so sánh

comparison = pd.DataFrame({
    "BT_Time(ms)": bt_summary["time_ms"],
    "CSP_Time(ms)": csp_summary["time_ms"],
    "BT_Steps": bt_summary["steps"],
    "CSP_Steps": csp_summary["steps"]
})

comparison["Speedup"] = (
    comparison["BT_Time(ms)"]
    / comparison["CSP_Time(ms)"]
)

comparison["Steps_Reduction"] = (
    comparison["BT_Steps"]
    / comparison["CSP_Steps"]
)

comparison = comparison.reindex(difficulty_order)

print("\nCOMPARISON")
print("="*60)

print(comparison.round(2))

print("\nAVERAGE EMPTY CELLS")
print("="*60)
print(bt_summary["empty_cells"].round(2))