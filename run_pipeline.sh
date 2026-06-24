#!/bin/bash

# Thao tác Fail-Fast: Dừng script ngay lập tức nếu bất kỳ lệnh nào gặp lỗi
set -e

# Ép Matplotlib sử dụng backend Agg để chạy được trên Docker / Server không có giao diện đồ họa
export MPLBACKEND=Agg

# Thời gian bắt đầu toàn bộ pipeline
START_TIME=$(date +%s)

# Tạo sẵn các thư mục cần thiết
mkdir -p data
mkdir -p results
mkdir -p charts

echo "========================================================="
echo "KHỞI ĐỘNG CHUỖI THỰC NGHIỆM SUDOKU AUTOMATION PIPELINE"
echo "========================================================="

# # =========================================================
# # KIỂM TRA DỮ LIỆU ĐẦU VÀO (VÁ LỖI COMMENT)
# # =========================================================
if [ ! -f "data/processed_sudoku.csv" ]; then
    echo "Không tìm thấy data/processed_sudoku.csv"
    echo "Đang tự động tiền xử lý dữ liệu..."

    if [ ! -f "data/sudoku.csv" ]; then
        echo "LỖI: Không tìm thấy file gốc data/sudoku.csv"
        exit 1
    fi

    python src/data_loader.py
    echo "Tiền xử lý dữ liệu hoàn tất"
fi

# # =========================================================
# # 1. BACKTRACKING
# # =========================================================
echo
echo "[1/5] RUNNING: BACKTRACKING BENCHMARK"
STEP_START=$(date +%s)
python src/automation.py

if [ ! -f "results/backtracking_results.csv" ]; then
    echo "Không tạo được results/backtracking_results.csv"
    exit 1
fi
STEP_END=$(date +%s)
echo "Backtracking hoàn tất sau $((STEP_END - STEP_START)) giây"

# # =========================================================
# # 2. CSP + MRV
# # =========================================================
echo
echo "[2/5] RUNNING: CSP + MRV BENCHMARK"
STEP_START=$(date +%s)
python src/automation_csp.py

if [ ! -f "results/csp_results.csv" ]; then
    echo "❌ Không tạo được results/csp_results.csv"
    exit 1
fi
STEP_END=$(date +%s)
echo "CSP + MRV hoàn tất sau $((STEP_END - STEP_START)) giây"

# # =========================================================
# # 3. CSP + FC
# # =========================================================
echo
echo "[3/5] RUNNING: CSP + MRV + FORWARD CHECKING"
STEP_START=$(date +%s)
python src/automation_csp_fc.py

if [ ! -f "results/csp_fc_results.csv" ]; then
    echo "Không tạo được results/csp_fc_results.csv"
    exit 1
fi
STEP_END=$(date +%s)
echo "CSP + FC hoàn tất sau $((STEP_END - STEP_START)) giây"

# # =========================================================
# # 4. COMPARISON REPORT
# # =========================================================
echo
echo "[4/5] GENERATING COMPARISON REPORT"
STEP_START=$(date +%s)
python src/comparison.py

if [ ! -f "results/comparison_summary.csv" ]; then
    echo "Không tạo được results/comparison_summary.csv"
    exit 1
fi
STEP_END=$(date +%s)
echo "Comparison Report hoàn tất sau $((STEP_END - STEP_START)) giây"

# # =========================================================
# # 5. VISUALIZATION (VÁ LỖI ĐỒNG BỘ TÊN FILE CHỈ SỐ 01_)
# # =========================================================
echo
echo "[5/5] GENERATING VISUALIZATION CHARTS"
STEP_START=$(date +%s)
python src/visualize.py

if [ ! -f "charts/01_time_comparison.png" ]; then
    echo "Không tìm thấy biểu đồ đầu ra tại charts/01_time_comparison.png"
    exit 1
fi
STEP_END=$(date +%s)
echo "Visualization hoàn tất sau $((STEP_END - STEP_START)) giây"

# # =========================================================
# # TỔNG KẾT TOÀN DIỆN PIPELINE
# # =========================================================
END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))

echo
echo "========================================================="
echo "PIPELINE COMPLETED SUCCESSFULLY"
echo "========================================================="
echo "Dữ liệu thực nghiệm : results/"
echo "Biểu đồ phân tích   : charts/"
echo "Báo cáo tổng hợp    : results/comparison_summary.csv"
echo "Tổng thời gian chạy : ${TOTAL_TIME} giây"
echo "========================================================="