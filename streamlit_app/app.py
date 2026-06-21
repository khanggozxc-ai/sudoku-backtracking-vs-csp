import streamlit as st
import numpy as np
import pandas as pd
import time
import os

# ==========================================
# 1. CẤU HÌNH TRANG WEB
# ==========================================
st.set_page_config(page_title="Sudoku AI Solver", page_icon="🦄", layout="wide")

# ==========================================
# 2. BƠM CSS NỀN & HIỆU ỨNG KÍNH
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;900&display=swap');
    
    /* Nền Gradient cực mượt */
    .stApp, [data-testid="stAppViewContainer"], #root {
        background: linear-gradient(-45deg, #ffb3ba, #ffdfba, #ffffba, #baffc9, #bae1ff) !important;
        background-size: 400% 400% !important;
        animation: gradientBG 10s ease infinite !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(8px) !important;
    }
    [data-testid="stHeader"] { background: transparent !important; }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Bàn cờ Sudoku */
    .sudoku-container { display: flex; justify-content: center; margin-top: 10px; margin-bottom: 20px; }
    .sudoku-table { 
        border-collapse: collapse; border: 4px solid #475569; 
        font-family: 'Nunito', sans-serif; box-shadow: 0 15px 35px rgba(0,0,0,0.15); 
        background: rgba(255, 255, 255, 0.6); 
        backdrop-filter: blur(10px); border-radius: 12px; overflow: hidden; 
    }
    .sudoku-cell { width: 60px; height: 60px; text-align: center; vertical-align: middle; font-size: 28px; border: 1px solid #94a3b8; transition: all 0.1s ease-in-out; }
    .sudoku-cell.bold-right { border-right: 3px solid #475569; }
    .sudoku-cell.bold-bottom { border-bottom: 3px solid #475569; }
    
    .sudoku-cell.original { color: #1e293b; background-color: rgba(255, 255, 255, 0.9); font-weight: 900; }
    .sudoku-cell.ai-filled { color: white; background-color: #fb7185; font-weight: 900; transform: scale(1.1); border-radius: 8px; box-shadow: 0 4px 10px rgba(251, 113, 133, 0.5); position: relative; z-index: 10; }
    .sudoku-cell.empty { color: transparent; }
    </style>
    """, 
    unsafe_allow_html=True
)

# ==========================================
# 3. HÀM TẠO HTML BÀN CỜ
# ==========================================
def get_board_html(current_board, original_board):
    html = '<div class="sudoku-container"><table class="sudoku-table">'
    for i in range(9):
        html += "<tr>"
        for j in range(9):
            val = current_board[i][j]
            orig_val = original_board[i][j]
            classes = ["sudoku-cell"]
            if j in [2, 5]: classes.append("bold-right")
            if i in [2, 5]: classes.append("bold-bottom")
            
            if orig_val != 0:
                classes.append("original")
                cell_str = str(orig_val)
            elif val != 0:
                classes.append("ai-filled")
                cell_str = str(val)
            else:
                classes.append("empty")
                cell_str = ""
            html += f'<td class="{" ".join(classes)}">{cell_str}</td>'
        html += "</tr>"
    html += '</table></div>'
    return html

# ==========================================
# 4. DATA & SESSION STATE
# ==========================================
@st.cache_data
def load_data():
    if os.path.exists("data/processed_sudoku.csv"):
        return pd.read_csv("data/processed_sudoku.csv")
    return None

df_sudoku = load_data()

fallback_board = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]
])

def pick_random(df):
    if df is not None and not df.empty:
        row = df.sample(1).iloc[0]
        return np.array([int(x) for x in row['quizzes']]).reshape(9, 9), row['difficulty']
    return fallback_board, "Default"

if 'original_board' not in st.session_state:
    b_arr, diff = pick_random(df_sudoku)
    st.session_state.original_board = b_arr.copy()
    st.session_state.current_board = b_arr.copy()
    st.session_state.current_diff = diff

# ==========================================
# 5. LOGIC AI CORE
# ==========================================
def is_valid(b, r, c, n):
    if n in b[r, :]: return False
    if n in b[:, c]: return False
    br, bc = (r//3)*3, (c//3)*3
    if n in b[br:br+3, bc:bc+3]: return False
    return True

def get_empty(b):
    for r in range(9):
        for c in range(9):
            if b[r, c] == 0: return r, c
    return None

def solve_bt(b, orig_b, cnt, b_ph, m_ph, slp):
    empty = get_empty(b)
    if not empty: return True
    r, c = empty
    for n in range(1, 10):
        if is_valid(b, r, c, n):
            b[r, c] = n
            cnt[0] += 1
            b_ph.markdown(get_board_html(b, orig_b), unsafe_allow_html=True)
            m_ph.info(f"🔄 **Backtracking** | Steps: **{cnt[0]:,}**")
            time.sleep(slp)
            if solve_bt(b, orig_b, cnt, b_ph, m_ph, slp): return True
            b[r, c] = 0
            b_ph.markdown(get_board_html(b, orig_b), unsafe_allow_html=True)
            time.sleep(slp)
    return False

class Stats:
    def __init__(self): self.steps = 0; self.bkt = 0

def init_domains(b):
    doms = {}
    r_u, c_u, bx_u = [set() for _ in range(9)], [set() for _ in range(9)], [set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            v = b[r][c]
            if v != 0:
                r_u[r].add(v); c_u[c].add(v); bx_u[(r//3)*3+(c//3)].add(v)
    for r in range(9):
        for c in range(9):
            if b[r][c] == 0:
                doms[(r, c)] = set(range(1,10)) - (r_u[r] | c_u[c] | bx_u[(r//3)*3+(c//3)])
    return doms

def solve_csp(b, orig_b, stats, b_ph, m_ph, slp):
    doms = init_domains(b)
    def backtrack(curr_doms):
        if not curr_doms: return True
        cell = min(curr_doms, key=lambda k: len(curr_doms[k]))
        r, c = cell
        for n in curr_doms[cell]:
            stats.steps += 1
            b[r][c] = n
            b_ph.markdown(get_board_html(b, orig_b), unsafe_allow_html=True)
            m_ph.info(f"🚀 **CSP + MRV + FC** | Steps: **{stats.steps:,}** | Quay lui: **{stats.bkt:,}**")
            time.sleep(slp)
            
            nxt_doms = {}
            fc_fail = False
            br, bc = (r//3)*3, (c//3)*3
            for nb, n_dom in curr_doms.items():
                if nb == cell: continue
                nr, nc = nb
                if nr == r or nc == c or (br <= nr < br+3 and bc <= nc < bc+3):
                    if n in n_dom:
                        new_dom = n_dom.copy()
                        new_dom.remove(n)
                        if not new_dom: fc_fail = True; break
                        nxt_doms[nb] = new_dom
                    else: nxt_doms[nb] = n_dom
                else: nxt_doms[nb] = n_dom
            
            if not fc_fail:
                if backtrack(nxt_doms): return True
            b[r][c] = 0
            stats.bkt += 1
            b_ph.markdown(get_board_html(b, orig_b), unsafe_allow_html=True)
            time.sleep(slp)
        return False
    return backtrack(doms)

# ==========================================
# 6. GIAO DIỆN HIỂN THỊ CHÍNH
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1055/1055661.png", width=60)
    st.markdown("## 🎯 Bảng Điều Khiển")
    
    st.markdown("### 🎲 Bốc Đề Random")
    if st.button("🎲 Chọn Ngẫu Nhiên", type="primary", use_container_width=True):
        b_arr, diff = pick_random(df_sudoku)
        st.session_state.original_board = b_arr.copy()
        st.session_state.current_board = b_arr.copy()
        st.session_state.current_diff = diff
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 🔍 Chọn Đề Cụ Thể")
    if df_sudoku is not None:
        sel_diff = st.selectbox("Lọc độ khó:", ["Easy", "Medium", "Hard", "Extreme"])
        f_df = df_sudoku[df_sudoku['difficulty'] == sel_diff]
        opts = {f"Đề số {idx + 1} ({r['empty_cells']} ô trống)": idx for idx, r in f_df.iterrows()}
        sel_opt = st.selectbox("Danh sách đề:", list(opts.keys()))
        if st.button("Tải Đề Này", use_container_width=True):
            idx = opts[sel_opt]
            b_arr = np.array([int(x) for x in df_sudoku.loc[idx, 'quizzes']]).reshape(9, 9)
            st.session_state.original_board = b_arr.copy()
            st.session_state.current_board = b_arr.copy()
            st.session_state.current_diff = sel_diff
            st.rerun()
            
    st.markdown("---")
    st.markdown("### 🤖 Cấu Hình AI")
    algo = st.selectbox("Thuật toán:", ("CSP + Heuristic MRV + FC", "Quay lui (Backtracking)"))
    spd = st.slider("Tốc độ giải bài", 0.0, 0.2, 0.05, 0.01)
    btn_solve = st.button("▶️ AI GIẢI NGAY", use_container_width=True, type="primary")

# Khu vực hiển thị bảng
st.markdown(f"<h1 style='text-align: center; color: #1e293b;'>🦄 SUDOKU AI SOLVER</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; color: #475569;'>Mức độ hiện tại: {st.session_state.current_diff}</h3>", unsafe_allow_html=True)

b_place = st.empty()
m_place = st.empty()

b_place.markdown(get_board_html(st.session_state.current_board, st.session_state.original_board), unsafe_allow_html=True)

if btn_solve:
    wb = st.session_state.original_board.copy()
    ob = st.session_state.original_board.copy()
    t_start = time.time()
    solved = False
    
    if "Backtracking" in algo:
        cnt = [0]
        solved = solve_bt(wb, ob, cnt, b_place, m_place, spd)
    else:
        stt = Stats()
        solved = solve_csp(wb.tolist(), ob.tolist(), stt, b_place, m_place, spd)
        
    t_end = time.time()
    
    if solved:
        m_place.success(f"🎉 **Hoàn thành xuất sắc!** AI đã giải xong trong {(t_end-t_start)*1000:.2f} mili-giây.")
        st.balloons()
