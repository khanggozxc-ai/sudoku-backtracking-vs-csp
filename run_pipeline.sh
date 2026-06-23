    #!/bin/bash

    # Ép matplotlib chạy ở chế độ không giao diện (chống lỗi crash trên Docker)
    export MPLBACKEND=Agg

    echo "========================================================="
    echo "🚀 KHỞI ĐỘNG CHUỖI THỰC NGHIỆM SUDOKU AUTOMATION..."
    echo "========================================================="

    echo "[1/5] Chạy thực nghiệm Backtracking thuần túy (400 bài)..."
    python src/automation.py

    echo -e "\n[2/5] Chạy thực nghiệm CSP + MRV (400 bài)..."
    python src/automation_csp.py

    echo -e "\n[3/5] Chạy thực nghiệm Active CSP + FC (400 bài)..."
    python src/automation_csp_fc.py

    echo -e "\n[4/5] Đang xử lý gộp dữ liệu và in bảng đối sánh..."
    python src/comparison.py

    echo -e "\n[5/5] Đang xuất bộ biểu đồ phân tích hiệu năng..."
    python src/visualize.py

    echo "========================================================="
    echo "🎉 CHUỖI THỰC NGHIỆM ĐÃ HOÀN THÀNH XUẤT SẮC!"
    echo "📁 Hãy kiểm tra thư mục 'results/' và 'charts/' trên máy máy tính."
    echo "========================================================="