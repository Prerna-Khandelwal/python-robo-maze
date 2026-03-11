import streamlit as st
import urllib.parse
import random

# 1. Page Configuration
st.set_page_config(page_title="Robo-Escape", layout="centered")

# 2. Stable Maze Layout
MAZE = [
    "XXXXXXXXXX",
    "XP       X", 
    "X  XXXX  X",
    "X    X   X",
    "X  X   X X",
    "X  XXXXX X",
    "X        X",
    "XXXXXXXXXX"
]

# 3. Game State Initialization
if 'r' not in st.session_state:
    st.session_state.r, st.session_state.c = 1, 1
if 'moves' not in st.session_state:
    st.session_state.moves = 0

# FIXED: Find target only ONCE and store it
if 'target_r' not in st.session_state:
    possible_targets = []
    for r, row in enumerate(MAZE):
        for c, char in enumerate(row):
            if char == " " and (r != 1 or c != 1):
                possible_targets.append((r, c))
    t_r, t_c = random.choice(possible_targets)
    st.session_state.target_r = t_r
    st.session_state.target_c = t_c

# 4. Movement Logic
def move_player(dr, dc):
    new_r = st.session_state.r + dr
    new_c = st.session_state.c + dc
    
    if MAZE[new_r][new_c] == "X":
        st.session_state.r, st.session_state.c = 1, 1 
        st.toast("🚫 Hit a wall! Resetting...", icon="⚠️")
    else:
        st.session_state.r, st.session_state.c = new_r, new_c
        st.session_state.moves += 1
        if new_r == st.session_state.target_r and new_c == st.session_state.target_c:
            st.balloons()

# 5. Professional Styling
st.markdown("""
    <style>
    .maze-container {
        font-size: 28px !important;
        font-family: monospace;
        line-height: 1.1;
        letter-spacing: 2px;
        text-align: center;
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        white-space: pre;
    }
    .stButton button { width: 100%; height: 55px; font-size: 22px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ ROBO-ESCAPE ⚡")
st.write(f"**Moves: {st.session_state.moves}**")

# 6. Controls
col1, col2, col3 = st.columns([1,1,1])
with col2: st.button("▲", on_click=move_player, args=(-1, 0))
c1, c2, c3 = st.columns([1,1,1])
with c1: st.button("◀", on_click=move_player, args=(0, -1))
with c2: st.button("▼", on_click=move_player, args=(1, 0))
with c3: st.button("▶", on_click=move_player, args=(0, 1))

# 7. Render Maze (FIXED GRID LOGIC)
grid_html = ""
for r_idx, row in enumerate(MAZE):
    for c_idx, char in enumerate(row):
        if r_idx == st.session_state.r and c_idx == st.session_state.c:
            grid_html += "🤖"
        elif r_idx == st.session_state.target_r and c_idx == st.session_state.target_c:
            grid_html += "🟡"
        elif char == "X":
            grid_html += "🟦"
        else:
            grid_html += "⬜"
    grid_html += "\n"

st.markdown(f'<div class="maze-container">{grid_html}</div>', unsafe_allow_html=True)

# 8. Win Message & Reset
if st.session_state.r == st.session_state.target_r and st.session_state.c == st.session_state.target_c:
    st.success("🏆 TARGET REACHED!")
    
    msg = f"I beat the random maze in {st.session_state.moves} moves!"
    url = f"https://wa.me/918949803950?text={urllib.parse.quote(msg)}"
    st.link_button("🟢 Learn Python with Prerna Khandelwal. Click to connect on WhatsApp", url, use_container_width=True)
    
    if st.button("🔄 Play Again (New Target)"):
        # Clear specific session keys to force re-generation
        del st.session_state.target_r
        del st.session_state.target_c
        st.session_state.r, st.session_state.c = 1, 1
        st.session_state.moves = 0
        st.rerun()
