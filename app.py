import streamlit as st
import urllib.parse
import random

# 1. Page Configuration
st.set_page_config(page_title="Robo-Escape", layout="centered")

# 2. Stable Maze Layout (8x8)
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

# 3. Game State Initialization
if 'r' not in st.session_state:
    st.session_state.r, st.session_state.c = 1, 1
if 'moves' not in st.session_state:
    st.session_state.moves = 0

# SMART TARGET GENERATOR: Ensures the target is never trapped
if 'target_r' not in st.session_state:
    # Only pick from the open "bottom" and "right" areas where the path is clear
    open_path_spots = [
        (1, 4), (1, 5), (1, 6),
        (3, 1), (3, 2), (3, 3), (3, 6),
        (4, 3), (4, 4), (4, 5), (4, 6),
        (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)
    ]
    st.session_state.target_r, st.session_state.target_c = random.choice(open_path_spots)

# 4. Movement Logic (Fixed to prevent "random" jumps)
def move_player(dr, dc):
    new_r = st.session_state.r + dr
    new_c = st.session_state.c + dc
    
    # Check if the next move is within the grid and not a wall
    if 0 <= new_r < len(MAZE) and 0 <= new_c < len(MAZE[0]):
        if MAZE[new_r][new_c] != "X":
            st.session_state.r = new_r
            st.session_state.c = new_c
            st.session_state.moves += 1
            # Check for win immediately
            if (new_r, new_c) == (st.session_state.target_r, st.session_state.target_c):
                st.balloons()
        else:
            st.toast("🚫 Wall!", icon="🧱")

# 5. CSS for Perfect Alignment
st.markdown("""
    <style>
    .main .block-container { padding-top: 1rem; }
    .maze-wrapper {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        width: 100%;
        max-width: 350px;
        margin: 0 auto;
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 12px;
    }
    .cell {
        aspect-ratio: 1 / 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
    }
    div[data-testid="stHorizontalBlock"] { gap: 0.2rem; }
    button { height: 50px !important; }
    </style>
    """, unsafe_allow_html=True)

# 6. UI Header & Controls
st.title("⚡ ROBO-ESCAPE ⚡")
st.write(f"**Moves: {st.session_state.moves}**")

cols = st.columns(4) 
with cols[0]: st.button("◀", on_click=move_player, args=(0, -1), use_container_width=True)
with cols[1]: st.button("▲", on_click=move_player, args=(-1, 0), use_container_width=True)
with cols[2]: st.button("▼", on_click=move_player, args=(1, 0), use_container_width=True)
with cols[3]: st.button("▶", on_click=move_player, args=(0, 1), use_container_width=True)

# 7. Render Organized Grid
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

# 8. Success Message
if (st.session_state.r, st.session_state.c) == (st.session_state.target_r, st.session_state.target_c):
    st.markdown(f"""
        <div style="background-color:#00ffcc; padding:15px; border-radius:10px; text-align:center; border: 2px solid #1a1a40; margin-top: 15px;">
            <h3 style="color:#1a1a40; margin:0;">🏆 MISSION COMPLETE! 🏆</h3>
            <p style="color:#1a1a40; font-size:14px; margin:5px 0;">Build games with Prerna Khandelwal</p>
            <h4 style="color:#ff0066; margin:0;">Python • Scratch • JavaScript</h4>
        </div>
    """, unsafe_allow_html=True)
    
    msg = urllib.parse.quote(f"I beat the Robo-Maze in {st.session_state.moves} moves! I want to join your class.")
    st.link_button("🟢 Connect on WhatsApp", f"https://wa.me/918949803950?text={msg}", use_container_width=True)
    
    if st.button("🔄 Play Again", use_container_width=True):
        for key in ['target_r', 'target_c']: del st.session_state[key]
        st.session_state.r, st.session_state.c, st.session_state.moves = 1, 1, 0
        st.rerun()
