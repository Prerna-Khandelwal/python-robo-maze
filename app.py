import streamlit as st
import urllib.parse
import random

# 1. Page Configuration
st.set_page_config(page_title="Robo-Escape", layout="centered")

# 2. Compact Maze Layout (8x8 for better mobile fit)
MAZE = [
    "XXXXXXXX",
    "XP     X", 
    "X  XXX  X",
    "X    X  X",
    "X  X    X",
    "X  XXXX X",
    "X       X",
    "XXXXXXXX"
]

# 3. Game State
if 'r' not in st.session_state:
    st.session_state.r, st.session_state.c = 1, 1
if 'moves' not in st.session_state:
    st.session_state.moves = 0

if 'target_r' not in st.session_state:
    possible = [(r, c) for r, row in enumerate(MAZE) for c, char in enumerate(row) if char == " " and (r,c) != (1,1)]
    st.session_state.target_r, st.session_state.target_c = random.choice(possible)

def move_player(dr, dc):
    nr, nc = st.session_state.r + dr, st.session_state.c + dc
    if MAZE[nr][nc] == "X":
        st.session_state.r, st.session_state.c = 1, 1 
        st.toast("🚫 Reset!", icon="⚠️")
    else:
        st.session_state.r, st.session_state.c = nr, nc
        st.session_state.moves += 1
        if (nr, nc) == (st.session_state.target_r, st.session_state.target_c):
            st.balloons()

# 4. Ultra-Compact Styling
st.markdown("""
    <style>
    .main .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    .maze-container {
        font-size: 24px !important;
        font-family: monospace;
        line-height: 1.0;
        text-align: center;
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        white-space: pre;
    }
    div[data-testid="stHorizontalBlock"] { gap: 0.5rem; }
    button { padding: 0px !important; height: 45px !important; }
    </style>
    """, unsafe_allow_html=True)

# 5. Buttons in ONE LINE
st.write(f"**Moves: {st.session_state.moves}**")
cols = st.columns(4) # 4 columns for 4 buttons
with cols[0]: st.button("◀", on_click=move_player, args=(0, -1), use_container_width=True)
with cols[1]: st.button("▲", on_click=move_player, args=(-1, 0), use_container_width=True)
with cols[2]: st.button("▼", on_click=move_player, args=(1, 0), use_container_width=True)
with cols[3]: st.button("▶", on_click=move_player, args=(0, 1), use_container_width=True)

# 6. Render Maze
grid_html = ""
for r, row in enumerate(MAZE):
    for c, char in enumerate(row):
        if (r, c) == (st.session_state.r, st.session_state.c): grid_html += "🤖"
        elif (r, c) == (st.session_state.target_r, st.session_state.target_c): grid_html += "🟡"
        elif char == "X": grid_html += "🟦"
        else: grid_html += "⬜"
    grid_html += "\n"

st.markdown(f'<div class="maze-container">{grid_html}</div>', unsafe_allow_html=True)

# 7. Win Section
if (st.session_state.r, st.session_state.c) == (st.session_state.target_r, st.session_state.target_c):
    st.markdown(f"""
        <div style="background-color:#00ffcc; padding:15px; border-radius:10px; text-align:center; border: 2px solid #1a1a40; margin-top: 10px;">
            <h3 style="color:#1a1a40; margin:0;">🏆 MISSION COMPLETE! 🏆</h3>
            <p style="color:#1a1a40; font-size:14px; margin:5px 0;">Want to learn to code games like this?</p>
            <h4 style="color:#ff0066; margin:0;">Join Prerna Khandelwal's Classes</h4>
            <p style="color:#333; font-weight:bold; font-size:12px;">Python • Scratch • JavaScript</p>
        </div>
    """, unsafe_allow_html=True)
    
    msg = urllib.parse.quote(f"I beat the Robo-Maze in {st.session_state.moves} moves! I'd like to join your coding class.")
    st.link_button("🟢 Click to Connect on WhatsApp", f"https://wa.me/918949803950?text={msg}", use_container_width=True)
    
    if st.button("🔄 Play Again", use_container_width=True):
        for key in ['target_r', 'target_c']: del st.session_state[key]
        st.session_state.r, st.session_state.c, st.session_state.moves = 1, 1, 0
        st.rerun()
