import os
import pandas as pd
import matplotlib.pyplot as plt

#======================
# LOAD DỮ LIỆU TỪ 3 NGUỒN
#======================
bt = pd.read_csv("results/backtracking_results.csv")
csp = pd.read_csv("results/csp_results.csv")
csp_fc = pd.read_csv("results/csp_fc_results.csv")  

difficulty_order = ["Easy", "Medium", "Hard", "Extreme"]

#=====================
# TỔNG HỢP DỮ LIỆU TRUNG BÌNH
#=====================
bt_summary = bt.groupby("difficulty", observed=True).agg({"time_ms": "mean", "steps": "mean"}).reindex(difficulty_order)
csp_summary = csp.groupby("difficulty", observed=True).agg({"time_ms": "mean", "steps": "mean"}).reindex(difficulty_order)
fc_summary = csp_fc.groupby("difficulty", observed=True).agg({"time_ms": "mean", "steps": "mean"}).reindex(difficulty_order)

os.makedirs("charts", exist_ok=True)

# Cấu hình tọa độ cho bộ 3 cột nằm cạnh nhau không bị đè dính
x = range(len(difficulty_order))
width = 0.25  

# Định nghĩa hệ màu 3 sắc chuyên nghiệp cho báo cáo khoa học
color_bt = "#4c72b0"   # Xanh dương - Bản duyệt mù
color_csp = "#dd8452"  # Cam - Bản MRV cũ
color_fc = "#55a868"   # Xanh lá - Bản Active FC tối ưu

#=======================================================
# Biểu đồ 1: TIME COMPARISON (BAR CHART) - Đối sành 3 bên
#=======================================================
plt.figure(figsize=(9, 5))

plt.bar([i - width for i in x], bt_summary["time_ms"], width=width, label="Backtracking", color=color_bt)
plt.bar([i for i in x], csp_summary["time_ms"], width=width, label="CSP (MRV)", color=color_csp)
plt.bar([i + width for i in x], fc_summary["time_ms"], width=width, label="CSP + MRV + FC", color=color_fc)

plt.xticks(x, difficulty_order)
plt.ylabel("Time (ms)")
plt.title("Average Solving Time Comparison (3 Algorithms)")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("charts/time_comparison.png", dpi=300)
plt.close()

#=======================================================
# Biểu đồ 2: STEPS COMPARISON (BAR CHART) - Thang Log
#=======================================================
plt.figure(figsize=(9, 5))

plt.bar([i - width for i in x], bt_summary["steps"], width=width, label="Backtracking", color=color_bt)
plt.bar([i for i in x], csp_summary["steps"], width=width, label="CSP (MRV)", color=color_csp)
plt.bar([i + width for i in x], fc_summary["steps"], width=width, label="CSP + MRV + FC", color=color_fc)

plt.yscale("log")
plt.xticks(x, difficulty_order)
plt.ylabel("Steps (Log Scale)")
plt.title("Average Search Steps Comparison (3 Algorithms)")
plt.grid(axis='y', linestyle='--', alpha=0.5, which="both")
plt.legend()
plt.tight_layout()
plt.savefig("charts/steps_comparison.png", dpi=300)
plt.close()

#=======================================================
# Biểu đồ 3: TIME TREND (LINE CHART) - Đường xu hướng thời gian
#=======================================================
plt.figure(figsize=(9, 5))

plt.plot(difficulty_order, bt_summary["time_ms"], marker="o", linewidth=2, label="Backtracking", color=color_bt)
plt.plot(difficulty_order, csp_summary["time_ms"], marker="s", linewidth=2, label="CSP (MRV)", color=color_csp)
plt.plot(difficulty_order, fc_summary["time_ms"], marker="^", linewidth=2, label="CSP + MRV + FC", color=color_fc)

plt.ylabel("Time (ms)")
plt.title("Time Trend by Difficulty (3 Algorithms)")
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("charts/time_trend.png", dpi=300)
plt.close()

#=======================================================
# Biểu đồ 4: STEPS TREND (LINE CHART) - Đường xu hướng bước duyệt
#=======================================================
plt.figure(figsize=(9, 5))

plt.plot(difficulty_order, bt_summary["steps"], marker="o", linewidth=2, label="Backtracking", color=color_bt)
plt.plot(difficulty_order, csp_summary["steps"], marker="s", linewidth=2, label="CSP (MRV)", color=color_csp)
plt.plot(difficulty_order, fc_summary["steps"], marker="^", linewidth=2, label="CSP + MRV + FC", color=color_fc)

plt.yscale("log")
plt.ylabel("Steps (Log Scale)")
plt.title("Search Steps Trend by Difficulty (3 Algorithms)")
plt.grid(True, linestyle='--', alpha=0.5, which="both")
plt.legend()
plt.tight_layout()
plt.savefig("charts/steps_trend.png", dpi=300)
plt.close()

print("=" * 60)
print("All 3-way charts saved successfully in high resolution!")
print("=" * 60)
print("charts/time_comparison.png")
print("charts/steps_comparison.png")
print("charts/time_trend.png")
print("charts/steps_trend.png")