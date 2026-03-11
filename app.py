import streamlit as st
import urllib.parse
import random

# 1. Page Configuration
st.set_page_config(page_title="Robo-Escape", layout="centered")

# 2. Stable Maze Layout
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

# 4. FIXED CSS: Using a Grid Layout for Perfect Alignment
st.markdown("""
    <style>
    .main .block-container { padding-top: 1rem; }
    .maze-wrapper {
        display: grid;
        grid-template-columns: repeat(8, 1fr); /* 8 columns to match MAZE */
        width: 100%;
        max-width: 350px; /* Limits width on desktop */
        margin: 0 auto;
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
    .cell {
        aspect-ratio: 1 / 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
    }
    div[data-testid="stHorizontalBlock"] { gap: 0.2rem; }
    button { height: 45px !important; padding: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# 5. UI Layout
st.title("⚡ ROBO-ESCAPE ⚡")
st.write(f"**Moves: {st.session_state.moves}**")

# Top Buttons
cols = st.columns(4) 
with cols[0]: st.button("◀", on_click=move_player, args=(0, -1), use_container_width=True)
with cols[1]: st.button("▲", on_click=move_player, args=(-1, 0), use_container_width=True)
with cols[2]: st.button("▼", on_click=move_player, args=(1, 0), use_container_width=True)
with cols[3]: st.button("▶", on_click=move_player, args=(0, 1), use_container_width=True)

# 6. Render Grid (Using Divs instead of Text for Alignment)
grid_html = '<div class="maze-wrapper">'
for r, row in enumerate(MAZE):
    for c, char in enumerate(row):
        content = ""
        if (r, c) == (st.session_state.r, st.session_state.c): content = "🤖"
        elif (r, c) == (st.session_state.target_r, st.session_state.target_c): content = "🟡"
        elif char == "X": content = "🟦"
        else: content = "⬜"
        grid_html += f'<div class="cell">{content}</div>'
grid_html += '</div>'

st.markdown(grid_html, unsafe_allow_html=True)

# 7. Winning Message
if (st.session_state.r, st.session_state.c) == (st.session_state.target_r, st.session_state.target_c):
    st.markdown(f"""
        <div style="background-color:#00ffcc; padding:15px; border-radius:10px; text-align:center; border: 2px solid #1a1a40; margin-top: 15px;">
            <h3 style="color:#1a1a40; margin:0;">🏆 MISSION COMPLETE! 🏆</h3>
            <p style="color:#1a1a40; font-size:14px; margin:5px 0;">Learn Python, Scratch & JavaScript with</p>
            <h4 style="color:#ff0066; margin:0;">Prerna Khandelwal</h4>
        </div>
    """, unsafe_allow_html=True)
    
    msg = urllib.parse.quote(f"I beat Prerna Khandelwal's Robo-Maze in {st.session_state.moves} moves!")
    st.link_button("🟢 Connect on WhatsApp", f"https://wa.me/918949803950?text={msg}", use_container_width=True)
    
    if st.button("🔄 Play Again", use_container_width=True):
        for key in ['target_r', 'target_c']: del st.session_state[key]
        st.session_state.r, st.session_state.c, st.session_state.moves = 1, 1, 0
        st.rerun()
