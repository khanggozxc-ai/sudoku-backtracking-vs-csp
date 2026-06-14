import streamlit as st
import numpy as np
import pandas as pd
import time
import sys

# Thêm đường dẫn src vào system path để import được module
sys.path.append("./src")

try:
    # Nếu file Backtracking cũ của bạn tên là solver.py
    from solver import find_empty_cell, is_valid
    # File mới bạn vừa tối ưu
    from csp_solver import initialize_domains, CSPStats
except ImportError as e:
    st.error(f"⚠️ Lỗi import: {e}. Vui lòng kiểm tra lại tên file và cấu trúc thư mục.")

# ==========================================
# CẤU HÌNH TRANG WEB VÀ CSS TÙY CHỈNH
# ==========================================
st.set_page_config(page_title="Sudoku AI Solver", page_icon="🧠", layout="wide")

# Hàm render CSS tùy chỉnh để làm đẹp bảng Sudoku
def render_css():
    st.markdown(
        """
        <style>
        .stDataFrame div[data-testid="stTable"] {
            border: 2px solid black !important;
        }
        /* Customizing table header to hide it */
        .stDataFrame th { display: none; }
        .stDataFrame tr th { display: none; }
        </style>
        """,
        unsafe_allow_html=True
    )

render_css()

st.title("🧠 Đồ án: Hệ thống giải Sudoku bằng Trí tuệ Nhân tạo")
st.markdown("---")

# ==========================================
# CÁC HÀM GIẢI TÍCH HỢP ANIMATION RENDER UI
# ==========================================
def solve_backtracking_animated(board, counter, board_placeholder, metrics_placeholder, sleep_time):
    """Hàm Backtracking có vẽ lại bảng sau mỗi bước đi"""
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True
        
    row, col = empty_cell

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row, col] = num
            counter[0] += 1
            
            # --- RENDER GIAO DIỆN ---
            board_placeholder.dataframe(pd.DataFrame(board).replace(0, ""), use_container_width=True)
            metrics_placeholder.markdown(f"**⚡ Đang giải (Backtracking)... | Số bước thử (Steps): {counter[0]}**")
            time.sleep(sleep_time)

            if solve_backtracking_animated(board, counter, board_placeholder, metrics_placeholder, sleep_time):
                return True

            # Quay lui
            board[row, col] = 0
            # --- RENDER QUAY LUI ---
            board_placeholder.dataframe(pd.DataFrame(board).replace(0, ""), use_container_width=True)
            time.sleep(sleep_time)

    return False


def solve_csp_animated(board, stats, board_placeholder, metrics_placeholder, sleep_time):
    """Hàm CSP có vẽ lại bảng sau mỗi bước đi"""
    domains = initialize_domains(board)
    
    def backtrack(current_domains):
        if not current_domains:
            return True
            
        # Chọn ô MRV
        min_cell = min(current_domains, key=lambda k: len(current_domains[k]))
        row, col = min_cell
        domain = current_domains[min_cell]
        
        for num in domain:
            stats.steps += 1
            board[row][col] = num
            
            # --- RENDER GIAO DIỆN ---
            board_placeholder.dataframe(pd.DataFrame(board).replace(0, ""), use_container_width=True)
            metrics_placeholder.markdown(f"**⚡ Đang giải (CSP)... | Số bước (Steps): {stats.steps} | Quay lui: {stats.backtracks}**")
            time.sleep(sleep_time)
            
            next_domains = {}
            fc_failed = False
            box_r, box_c = (row // 3) * 3, (col // 3) * 3
            
            for neighbor, n_domain in current_domains.items():
                if neighbor == min_cell: continue
                nr, nc = neighbor
                if (nr == row or nc == col or (box_r <= nr < box_r + 3 and box_c <= nc < box_c + 3)):
                    if num in n_domain:
                        new_domain = n_domain.copy()
                        new_domain.remove(num)
                        if len(new_domain) == 0:
                            fc_failed = True
                            break 
                        next_domains[neighbor] = new_domain
                    else:
                         next_domains[neighbor] = n_domain
                else:
                    next_domains[neighbor] = n_domain
            
            if not fc_failed:
                if backtrack(next_domains):
                    return True
                    
            # Quay lui
            board[row][col] = 0
            stats.backtracks += 1
            # --- RENDER QUAY LUI ---
            board_placeholder.dataframe(pd.DataFrame(board).replace(0, ""), use_container_width=True)
            time.sleep(sleep_time)
            
        return False

    return backtrack(domains)

# ==========================================
# GIAO DIỆN CỘT TRÁI (ĐIỀU KHIỂN & ĐẦU VÀO)
# ==========================================
col_left, col_right = st.columns([1, 2])

with col_left:
    st.header("⚙️ Bảng điều khiển")
    
    # 1. Tốc độ mô phỏng
    speed = st.slider("Tốc độ mô phỏng (Animation Speed)", min_value=0.0, max_value=0.5, value=0.05, step=0.01)
    
    # 2. Chọn thuật toán giải
    algorithm = st.selectbox(
        "Chọn thuật toán giải:",
        ("Quay lui (Backtracking)", "CSP + Heuristic MRV + Forward Checking")
    )
    
    st.info("💡 Tính năng tải bàn cờ từ file CSV (Dataset của Thành viên B) sẽ được cập nhật tại đây.")
    sample_board_data = np.array([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ])
    
    # Hai lựa chọn giải
    solve_instantly = st.button("🚀 GIẢI NGAY LẬP TỨC", use_container_width=True)
    solve_animated = st.button("▶️ GIẢI TỪNG BƯỚC (ANIMATION)", use_container_width=True, type="primary")

# ==========================================
# GIAO DIỆN CỘT PHẢI (HIỂN THỊ KẾT QUẢ)
# ==========================================
with col_right:
    st.subheader("Bàn cờ Sudoku")
    
    # Placeholder để render lại bảng liên tục
    board_placeholder = st.empty()
    # Placeholder cho bộ đếm steps real-time
    metrics_placeholder = st.empty()
    
    # Hiển thị bàn cờ ban đầu
    board_placeholder.dataframe(pd.DataFrame(sample_board_data).replace(0, ""), use_container_width=True)
    metrics_placeholder.markdown("**Sẵn sàng giải...**")
    
    if solve_animated:
        working_board = sample_board_data.copy()
        
        start_time = time.time()
        is_solved = False
        
        if algorithm == "Quay lui (Backtracking)":
            counter = [0]
            # Gọi hàm có animation
            is_solved = solve_backtracking_animated(working_board, counter, board_placeholder, metrics_placeholder, speed)
        
        elif algorithm == "CSP + Heuristic MRV + Forward Checking":
            stats = CSPStats()
            # Gọi hàm có animation, chuyển sang dạng list
            is_solved = solve_csp_animated(working_board.tolist(), stats, board_placeholder, metrics_placeholder, speed)
            
        end_time = time.time()
        time_ms = (end_time - start_time) * 1000
        
        if is_solved:
            st.success("✅ Đã tìm thấy lời giải thành công!")
            st.balloons()
