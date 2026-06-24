import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#======================
# LOAD DỮ LIỆU TỪ 3 NGUỒN
#======================
try:
    bt = pd.read_csv("results/backtracking_results.csv")
    csp = pd.read_csv("results/csp_results.csv")
    csp_fc = pd.read_csv("results/csp_fc_results.csv")  
    
except FileNotFoundError as e:
    print("Missing benchmark result file.")
    print(e)
    exit(1)

difficulty_order = ["Easy", "Medium", "Hard", "Extreme"]

#=====================
# TỔNG HỢP DỮ LIỆU TRUNG BÌNH
#=====================
bt_summary = (
    bt.groupby("difficulty", observed=True)
    .agg({
        "time_ms": "mean", 
        "steps": "mean",
        "backtracks": "mean",
        "correct": "mean"        
    })
    .reindex(difficulty_order)
)
csp_summary = (
    csp.groupby("difficulty", observed=True)
    .agg({
        "time_ms": "mean",
        "steps": "mean",
        "backtracks": "mean",
        "correct": "mean"
        })
    .reindex(difficulty_order)
)
fc_summary =(
    csp_fc.groupby("difficulty", observed=True)
    .agg({
        "time_ms": "mean",
        "steps": "mean",
        "backtracks": "mean",
        "correct": "mean"
        })
    .reindex(difficulty_order)
)
chart_summary = pd.DataFrame({
    "BT_Time": bt_summary["time_ms"],
    "CSP_Time": csp_summary["time_ms"],
    "FC_Time": fc_summary["time_ms"],
    
    "BT_Steps": bt_summary["steps"],
    "CSP_Steps": csp_summary["steps"],
    "FC_Steps": fc_summary["steps"],

    "BT_Backtracks": bt_summary["backtracks"],
    "CSP_Backtracks": csp_summary["backtracks"],
    "FC_Backtracks": fc_summary["backtracks"],

    "BT_Accuracy": bt_summary["correct"] * 100,
    "CSP_Accuracy": csp_summary["correct"] * 100,
    "FC_Accuracy": fc_summary["correct"] * 100
})
os.makedirs("results", exist_ok=True)
chart_summary.round(2).to_csv("results/chart_summary.csv")

# =====================================================
# # OUTPUT FOLDER CONFIGURATION
# =====================================================
os.makedirs("charts", exist_ok=True)
x = range(len(difficulty_order))
width = 0.25

# Hệ màu chuẩn chỉnh cho báo cáo khoa học
color_bt = "#4c72b0"
color_csp = "#dd8452"
color_fc = "#55a868"

# =====================================================
# # 01 TIME COMPARISON
# =====================================================
plt.figure(figsize=(9, 5))
plt.bar([i - width for i in x], bt_summary["time_ms"], width=width, label="Backtracking", color=color_bt)
plt.bar(x, csp_summary["time_ms"], width=width, label="CSP (MRV)", color=color_csp)
plt.bar([i + width for i in x], fc_summary["time_ms"], width=width, label="CSP + FC", color=color_fc)

plt.xticks(x, difficulty_order)
plt.ylabel("Time (ms)")
plt.title("Average Solving Time Comparison")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("charts/01_time_comparison.png", dpi=300)
plt.close()

# =====================================================
# # 02 STEPS COMPARISON
# =====================================================
plt.figure(figsize=(9, 5))
plt.bar([i - width for i in x], bt_summary["steps"], width=width, label="Backtracking", color=color_bt)
plt.bar(x, csp_summary["steps"], width=width, label="CSP (MRV)", color=color_csp)
plt.bar([i + width for i in x], fc_summary["steps"], width=width, label="CSP + FC", color=color_fc)

plt.yscale("log")
plt.xticks(x, difficulty_order)
plt.ylabel("Steps (Log Scale)")
plt.title("Average Search Steps Comparison")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5, which="both")
plt.tight_layout()
plt.savefig("charts/02_steps_comparison.png", dpi=300)
plt.close()

# =====================================================
# # 03 BACKTRACK COMPARISON
# =====================================================
plt.figure(figsize=(9, 5))
plt.bar([i - width for i in x], bt_summary["backtracks"], width=width, label="Backtracking", color=color_bt)
plt.bar(x, csp_summary["backtracks"], width=width, label="CSP (MRV)", color=color_csp)
plt.bar([i + width for i in x], fc_summary["backtracks"], width=width, label="CSP + FC", color=color_fc)

plt.yscale("log")
plt.xticks(x, difficulty_order)
plt.ylabel("Backtracks (Log Scale)")
plt.title("Average Backtracks Comparison")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5, which="both")
plt.tight_layout()
plt.savefig("charts/03_backtracks_comparison.png", dpi=300)
plt.close()

# =====================================================
# # 04 ACCURACY COMPARISON
# =====================================================
plt.figure(figsize=(9, 5))
plt.bar([i - width for i in x], bt_summary["correct"] * 100, width=width, label="Backtracking", color=color_bt)
plt.bar(x, csp_summary["correct"] * 100, width=width, label="CSP (MRV)", color=color_csp)
plt.bar([i + width for i in x], fc_summary["correct"] * 100, width=width, label="CSP + FC", color=color_fc)

plt.xticks(x, difficulty_order)
plt.ylabel("Accuracy (%)")
plt.title("Solution Accuracy Comparison")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("charts/04_accuracy_comparison.png", dpi=300)
plt.close()

# =====================================================
# # 05 TIME TREND
# =====================================================
plt.figure(figsize=(9, 5))
plt.plot(difficulty_order, bt_summary["time_ms"], marker="o", linewidth=2, label="Backtracking", color=color_bt)
plt.plot(difficulty_order, csp_summary["time_ms"], marker="s", linewidth=2, label="CSP (MRV)", color=color_csp)
plt.plot(difficulty_order, fc_summary["time_ms"], marker="^", linewidth=2, label="CSP + FC", color=color_fc)

plt.ylabel("Time (ms)")
plt.title("Time Trend by Difficulty")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("charts/05_time_trend.png", dpi=300)
plt.close()

# =====================================================
# # 06 STEPS TREND
# =====================================================
plt.figure(figsize=(9, 5))
plt.plot(difficulty_order, bt_summary["steps"], marker="o", linewidth=2, label="Backtracking", color=color_bt)
plt.plot(difficulty_order, csp_summary["steps"], marker="s", linewidth=2, label="CSP (MRV)", color=color_csp)
plt.plot(difficulty_order, fc_summary["steps"], marker="^", linewidth=2, label="Search Steps Trend by Difficulty", color=color_fc)

plt.yscale("log")
plt.ylabel("Steps (Log Scale)")
plt.title("Search Steps Trend by Difficulty")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5, which="both")
plt.tight_layout()
plt.savefig("charts/06_steps_trend.png", dpi=300)
plt.close()

# In báo cáo kết quả hoàn tất ra Console
print("=" * 60)
print("ALL 6 CHARTS GENERATED SUCCESSFULLY IN HIGH RESOLUTION")
print("=" * 60)
print("charts/01_time_comparison.png")
print("charts/02_steps_comparison.png")
print("charts/03_backtracks_comparison.png")
print("charts/04_accuracy_comparison.png")
print("charts/05_time_trend.png")
print("charts/06_steps_trend.png")
print("\nSummary CSV saved successfully:")
print("results/chart_summary.csv")
print("=" * 60)